"""Users admin."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.admin import GroupAdmin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from import_export.admin import ImportExportModelAdmin
# from filer.models import File

from users.models import User, Turma, Simulacao, Papel
# from users.forms import UserCreateForm

class UserAdmin(ImportExportModelAdmin):
    pass

admin.site.register(User, UserAdmin)
# admin.site.register(User)
# admin.site.register(Profile, GroupAdmin)
admin.site.register(Turma)
admin.site.register(Simulacao)
admin.site.register(Papel)


# class UserAdmin(OriginalUserAdmin):
#     add_form = UserCreateForm
#     list_display = ('email', 'first_name', 'last_name', 'get_profile', 'is_active')
#     search_fields = ('email', 'groups',)
#     list_filter = ('groups', 'is_active', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('email', 'password' )}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'turma', )}),
#         ('Permissions', {'fields': ('groups', )}),
#     )
#     add_fieldsets = (
#         (None, {'fields': ('email', )}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'turma', )}),
#         ('Permissions', {'fields': ('group', )}),
#     )
#     actions = ('disable_selected_users', 'enable_selected_users', )

#     def get_list_display_links(self, request, list_display):
#         if request.user.is_superuser:
#             if self.list_display_links or self.list_display_links is None or not list_display:
#                 return self.list_display_links
#             else:
#                 # Use only the first item in list_display as link
#                 return list(list_display)[:1]
#         return None

#     def disable_selected_users(self, request, queryset):
#         queryset.update(is_active=False)
#     disable_selected_users.short_description = _('Disable selected users')
    
#     def enable_selected_users(self, request, queryset):
#         queryset.update(is_active=True)
#     enable_selected_users.short_description = _('Enable selected users')

#     def get_profile(self, obj):
#         # obj here is the object in this row of the list.
#         # Lets say you want to show the difference between the amount of
#         # the current transaction and the maximum amount is known then:
#         groups = obj.groups.all()
#         # If user has two profiles or mory, removes profiles with fewer permissions
#         if len(list(groups)) > 1:
#             user_group = None
#             count = 0
#             for group in groups:
#                 count_permissions = len(list(group.permissions.all()))
#                 if count <= count_permissions:
#                     user_group = group
#                     count = count_permissions
#             obj.groups.clear()
#             obj.groups.add(user_group)
#         return obj.groups.all().first()
#     get_profile.short_description = _('Profile')
#     get_profile.admin_order_field = 'groups__name'

#     def get_fieldsets(self, request, obj=None):
#         if not obj:
#             return self.add_fieldsets
#         return super().get_fieldsets(request, obj)

#     def get_form(self, request, obj=None, **kwargs):
#         """
#         Use special form during user creation
#         """
#         defaults = {}
#         if obj is None:
#             defaults['form'] = self.add_form
#         defaults.update(kwargs)
#         return super().get_form(request, obj, **defaults)

#     # def response_add(self, request, obj, post_url_continue=None):
#     #     return redirect('admin:users_user_changelist')

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if not request.user.is_superuser:
#             return qs.exclude(is_superuser=True)
#         return qs

#     def get_readonly_fields(self, request, obj=None):
#         fields = super().get_readonly_fields(request, obj)

#         if not request.user.is_superuser:
#             # Non superusers can't set superuser status on
#             # their subordinates.
#             fields = list(fields) + ['is_superuser']
#         return fields

    # def delete_queryset(self, request, queryset):
    #     for user in queryset:
    #         # All files from this user are moved to current user
    #         files = File.objects.filter(owner=user)
    #         files.update(owner=request.user)
    #     return super().delete_queryset(request, queryset)
