from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.registration.views import SocialAccountListView




urlpatterns = [

    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('accounts/', include('accounts.urls')),

    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.providers.google.urls')),
]