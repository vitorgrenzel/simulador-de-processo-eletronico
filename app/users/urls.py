"""Users urls."""
from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required

# from users.views import ApiGetProfiles, UserCreateView, CreatePasswordView, RecoverPasswordView, UserProfileView, UserChangePasswordView


app_name = 'users'
urlpatterns = [
    # url(r'^api/get/$', login_required(ApiGetProfiles.as_view()), name='verify-profiles-api'),
    # path(
    #     'add/',
    #     login_required(UserCreateView.as_view()),
    #     name='add_user'
    # ),
    # path(
    #     'create_password/<slug:pk>/<str:datetime>/<str:token>',
    #     CreatePasswordView.as_view(),
    #     name='create_password'
    # ),
    # path(
    #     'profile/', 
    #     login_required(UserProfileView.as_view()), 
    #     name='profile'
    # ),
    # path(
    #     'profile/change-password/', 
    #     login_required(UserChangePasswordView.as_view()), 
    #     name='change_password'
    # ),
    # path('recover_password/', RecoverPasswordView.as_view(), name='recover-password'),
]
