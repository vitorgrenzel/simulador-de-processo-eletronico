"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from django.views.generic.base import TemplateView

from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from processo.views import (
    ProcessoLista,
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('processo/', include("processo.urls")), 
    url('^searchableselect/', include('searchableselect.urls')),
    url(r'^accounts/login/$',
        LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'site_header': 'Simulador eproc - IMED',
            }
        )
    ),
    url(r'^accounts/logout/$',
        LogoutView.as_view(
            template_name='admin/logout.html',
        )
    ),
    path('painel-advogado/', login_required(ProcessoLista.as_view()), name='painel-advogado'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# This is only needed when using runserver.
# if settings.DEBUG:
#     urlpatterns = [
#         url(r'^media/(?P<path>.*)$', serve,
#             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#         ] + staticfiles_urlpatterns() + urlpatterns
