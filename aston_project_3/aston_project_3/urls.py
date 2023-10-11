"""
URL configuration for aston_project_3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.account.urls")),
    # path("api/", include("apps.account.urls")),
    # path("accounts/login/", include("django.contrib.auth.urls")),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LoginView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path(
        "accounts/password_change/",
        auth_views.LoginView.as_view(template_name="registration/password_change.html"),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        auth_views.LoginView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password_reset/",
        auth_views.LoginView.as_view(template_name="registration/password_reset.html"),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.LoginView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.LoginView.as_view(template_name="registration/reset.html"),
        name="reset",
    ),
    path(
        "accounts/reset/done/",
        auth_views.LoginView.as_view(template_name="registration/reset_done.html"),
        name="reset_done",
    ),
]
# print(include("django.contrib.auth.urls"))
