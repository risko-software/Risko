"""Risk_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve as serve_static

import os

def _static_butler(request, path, **kwargs):
    """
    Serve static files using the django static files configuration
    WITHOUT collectstatic. This is slower, but very useful for API 
    only servers where the static files are really just for /admin

    Passing insecure=True allows serve_static to process, and ignores
    the DEBUG=False setting
    """
    return serve_static(request, path, insecure=True, **kwargs)

context_risko_app = os.environ['CONTEXT_RISKO_APP'] 
#context_risko_app = 'risko/'

my_url_admin = '{}admin/'.format(context_risko_app) 
my_url_risko = context_risko_app
my_url_reset = '{}reset/password_reset'.format(context_risko_app) 
my_url_reset_done = '{}reset/password_reset_done'.format(context_risko_app) 
my_url_reset_confirm = r'^{}reset/(?P<uidb64>[0-9A-za-z_\-]+)/(?P<token>.+)/$'.format(context_risko_app)
my_url_reset_complete = '{}reset/done'.format(context_risko_app) 
my_url_static = r'{}static/(.+)'.format(context_risko_app)  

urlpatterns = [
    path(my_url_admin, admin.site.urls),
    path(my_url_risko, include("Risk_project_ufps.urls")),
    path(my_url_reset, 
        PasswordResetView.as_view(
            template_name='registration/password_reset_formf.html',
            email_template_name='registration/password_reset_emailf.html'
        ), 
    	name="password_reset"
    ),
    path(my_url_reset_done, PasswordResetDoneView.as_view(
        template_name='registration/password_reset_donef.html'), 
    	name = 'password_reset_done'
    ),
    re_path(my_url_reset_confirm, PasswordResetConfirmView.as_view(
    	template_name='registration/password_reset_confirmf.html'), 
    	name = 'password_reset_confirm'
    ),
    path(my_url_reset_complete, PasswordResetCompleteView.as_view(
    	template_name='registration/password_reset_completef.html'), 
    	name = 'password_reset_complete'
    ),
    re_path(my_url_static, _static_butler),
]







