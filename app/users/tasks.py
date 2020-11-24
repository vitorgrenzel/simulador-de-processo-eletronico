"""Products tasks."""
import logging

# from django.contrib.sites.models import Site
from django.contrib.staticfiles.finders import find

from celery import task


LOGGER = logging.getLogger(__name__)

@task(ignore_result=False)
def send_email_base(subject, body, to):
    from django.core.mail import EmailMultiAlternatives
    from email.mime.image import MIMEImage

    if isinstance(to, str):
        to = [to]
    message = EmailMultiAlternatives(subject=subject, body=body, to=to)
    message.content_subtype = 'html'
    message.mixed_subtype = 'related'
 
    # Getting the SSYS logo
    email_file = open(find('admin/img/Logo-SSYS.jpg'), 'rb')
    logo = MIMEImage(email_file.read())
    logo.add_header('Content-ID', '<logo>')
    message.attach(logo)

    # Getting the Pernambucanas logo 
    email_file = open(find('admin/img/logo_pernambucanas_sm.jpg'), 'rb')
    pernambucanas = MIMEImage(email_file.read())
    pernambucanas.add_header('Content-ID', '<pernambucanas>')
    message.attach(pernambucanas)
    
    try:
        message.send(fail_silently=True)
    except OSError as error:
        LOGGER.warning('Error in task (send_email_base): (%s)', error)
        return False
    except Exception as error:
        LOGGER.warning('Error in task (send_email_base): (%s)', error)
        return False
    LOGGER.info("Email send to (%s) with succes!", to)
    return True


@task(ignore_result=True)
def send_email_account_created(user, request=None, language='pt-br'):
    """Send email to new user"""
    from django.template.loader import render_to_string
    from django.utils import translation
    from django.utils.translation import ugettext_lazy as _
    from django.urls import reverse
    from users.utils import convert_datatime_to_base64
    from django.conf import settings

    LOGGER.info("Start - send_email_account_created task")
    # site = Site.objects.get_current()
    template_name = 'passwords/emails/create_account.html'

    base_64 = convert_datatime_to_base64(user.date_joined)

    url = settings.BASE_SITE + reverse(
        'users:create_password',
        kwargs={'pk': user.id, 'datetime': base_64, 'token': user.key_confirmation}
    )

    context = {
        'user': user,
        'url': url,
        'base_site': settings.BASE_SITE
    }

    txt_body = render_to_string(template_name, context)
    subject = _('BookDigital - your user account was created.')
    send_email_base(subject, txt_body, user.email)
  
    LOGGER.info("Finish task (send_email_account_created)!")


@task(ignore_result=False)
def send_email_recovery(user):
    """Send email to recover password"""
    from django.template.loader import render_to_string
    from django.utils import translation
    from django.utils.translation import ugettext_lazy as _
    from django.urls import reverse
    from users.utils import convert_datatime_to_base64
    from django.conf import settings

    LOGGER.info("Start - send_email_recovery task")
    result = True

    template_name = 'passwords/emails/recover_password.html'

    base_64 = convert_datatime_to_base64(user.last_login)

    user_language = 'pt-br'

    try:
        translation.activate(user_language)
        url = settings.BASE_SITE + reverse(
            'users:create_password',
            kwargs={'pk': user.id, 'datetime': base_64, 'token': user.key_confirmation}
        )
    finally:
        translation.activate(current_language)

    context = {
        'user': user,
        'url': url,
        'base_site': settings.BASE_SITE
    }

    # translate email to user language
    try:
        translation.activate(user_language)
        txt_body = render_to_string(template_name, context)
        subject = _('BookDigital - password recovery.')
        send_email_base(subject, txt_body, user.email)
    except Exception as error:
        LOGGER.warning("Error in task (send_email_recovery): (%s)", error)
        result = False
    finally:
        translation.activate(current_language)
    LOGGER.info("Finish task (send_email_recovery)! Result: (%s)", result)
    return result
