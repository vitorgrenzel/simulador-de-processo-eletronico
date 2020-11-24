"""User views."""
import logging
import json

from django.http import JsonResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.admin.forms import AdminAuthenticationForm
from django.views.generic import View, CreateView, UpdateView, FormView
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _

from users.models import Profile, User
from users.forms import UserCreateForm, UserCreatePassword, UserRecoverPassword, UserProfile, PasswordChangeForm
from users.utils import convert_datatime_to_base64


LOGGER = logging.getLogger(__name__)


class LoginView(DjangoLoginView):
    authentication_form = AdminAuthenticationForm
    template_name = 'admin/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_to = reverse("pages-root")
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)


class UserCreateView(CreateView):
    """Add User view."""
    model = User
    template_name = 'users/add_form.html'
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create User')
        return context


class CreatePasswordView(UpdateView):
    """Create user password view."""
    model = User
    template_name = 'passwords/change_password.html'
    form_class = UserCreatePassword
    title = _('Create Password')

    def get_success_url(self):
        return reverse_lazy('login') + "?password_created=1"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get(self, request, *args, **kwargs):
        # get all parameters from url
        user_id = self.kwargs.get('pk', None)
        base64 = self.kwargs.get('datetime', None)
        user_key = self.kwargs.get('token', None)
        error_response = Http404(_('This URL does not work or has expired.'))
        # check if all parameters are valid and not are user logged
        if user_id and base64 and user_key:
            if not request.user.is_anonymous:
                logout(request)
            user = User.objects.filter(id=user_id, key_confirmation=user_key).first()
            if not user:
                raise error_response
            # check if user need create your password
            if user.need_change_password:
                # check if base64 is correct
                check_base64 = convert_datatime_to_base64(user.date_joined)
                if str(base64) == str(check_base64):
                    # send to create password page
                    return super().get(request, *args, **kwargs)
                else:
                    raise error_response
            else:
                # check if base64 is correct
                check_base64 = convert_datatime_to_base64(user.last_login)
                if str(base64) == str(check_base64):
                    # send to recover password page
                    self.title = _('New Password')
                    return super().get(request, *args, **kwargs)
                else:
                    raise error_response
        else:
            raise error_response


class RecoverPasswordView(FormView):
    form_class = UserRecoverPassword
    template_name = 'passwords/recover_password.html'

    def get_success_url(self):
        return reverse_lazy('login') + "?password_recovery=1"


class UserProfileView(UpdateView):
    """Edit User view."""
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfile

    @never_cache
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('pages-root') + "?profile_edited=1"

    def get_object(self):
        return self.request.user
        

class UserChangePasswordView(UpdateView):
    """User Change Password View."""
    model = User
    template_name = 'users/profile-change-password.html'
    form_class = PasswordChangeForm
    
    def get_success_url(self, *args, **kwargs):
        return reverse('pages-root') + "?password_edited=1"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['instance'] = self.request.user
        kwargs['request'] = self.request
        return kwargs

    def get_object(self):
        return self.request.user
    

class ApiGetProfiles(View):
    """Endpoint to get profiles."""
    def post(self, request, *args, **kwargs):
        # tag_id = request.GET.get('tag', '')
        if not request.user.is_staff and not request.user.is_superuser:
            return JsonResponse({'status': False})
        body = json.loads(request.body.decode("utf-8"))
        sku_list = body.get('sku_list', None)
        if sku_list:
            sku_list = sku_list.split(',')
        page_id = body.get('page_id', None)
        if sku_list:
            try:
                # Get all profiles enabled to select
                profiles = Profile.objects.annotate(num_perm=Count('permissions')).filter(num_perm=0)
                # Verify if skus has pages and profiles associated and remove this profiles
                sku_profile = []
                for sku in skus:
                    sku_pages = sku.pages.all() if not page_id else sku.pages.exclude(id=page_id)
                    # Create SKU -> Page -> Profile relation
                    if sku_pages:
                        objs = []
                        for page in sku_pages:
                            profiles = profiles.exclude(id__in=page.groups.all().values_list('id', flat=True))
                            obj = {}
                            obj['page'] = {
                                'title': page.title_set.all().first().title,
                                'profiles': list(page.groups.all().values_list('name', flat=True))
                            }
                            objs.append(obj)
                        sku_profile.append({'sku': sku.__str__(), 'pages': objs})
                # Create list from enabled profiles
                list_profiles = []
                for profile in profiles:
                    info_profile = {'id': str(profile.id), 'name': profile.name, 'selected': False}
                    if page_id:
                        if profile.pages.all().filter(id__in=list([page_id])):
                            info_profile.update({'selected': True})
                    list_profiles.append(info_profile)

                # Send to template
                if list_profiles:
                    return JsonResponse({
                        'status': True,
                        'groups': list(list_profiles),
                        'sku_profile': str(sku_profile)
                    }, safe=True)

            except Exception as error:
                LOGGER.warning(f'Error in Api ApiGetProfiles: (%s).', error)
        return JsonResponse({'status': False, 'sku_profile': str(sku_profile)}, safe=True)
