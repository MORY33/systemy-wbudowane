from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import uuid
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.conf import settings


User = get_user_model()


def create_jwt_pair_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

    return tokens


def delete_token(user: User):
    if user.is_authenticated:
        token = user.auth_token
        BlacklistedToken.objects.create(token=token)
        settings.SIMPLE_JWT['SIGNING_KEY'] = settings.SECRET_KEY