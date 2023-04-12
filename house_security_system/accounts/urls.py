from django.urls import path, re_path
from .views import GoogleLogin

urlpatterns = [
    # path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    re_path(r"^dj-rest-auth/google/$", GoogleLogin.as_view(), name="google_login"),
    # path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
]

