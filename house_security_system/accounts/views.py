from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.response import Response
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.google.views import OAuth2Error
import jwt
import requests

import sys

sys.path.append("..")
from JWT.JWT import create_jwt_pair_for_user

class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, response, **kwargs):
        try:
            identity_data = jwt.decode(
                response["id_token"]["id_token"], #another nested id_token was returned
                options={
                    "verify_signature": False,
                    "verify_iss": True,
                    "verify_aud": True,
                    "verify_exp": True,
                },
                issuer=self.id_token_issuer,
                audience=app.client_id,
            )
        except jwt.PyJWTError as e:
            raise OAuth2Error("Invalid id_token") from e
        login = self.get_provider().sociallogin_from_response(request, identity_data)
        return login

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = "http://localhost:8000/accounts/dj-rest-auth/google/"
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.GET)
        self.serializer.is_valid(raise_exception=True)
        self.login()

        # print(self.get_response().__dict__)
        if self.get_response().status_code == 200:
            provider_url = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,birthdays'

            # print(create_jwt_pair_for_user(request.user)["access"])
            # headers = {'Authorization': f'Bearer {create_jwt_pair_for_user(request.user)["access"]}'}
            # response = requests.get(provider_url, headers=headers)
            # print(response)
            # if response.status_code == 200:
            return Response(create_jwt_pair_for_user(request.user))
            # else:
            #     return Response({"detail": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)
        return self.get_response()



    # def get(self, request, *args, **kwargs):
    #     def get(self, request, *args, **kwargs):
    #
    #         token_data = {
    #             'client_id': '82263305240-uv4nh847703q3n1978aqjcrka1o73k63.apps.googleusercontent.com',
    #             'client_secret': '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',
    #             'code': request.GET.get('code'),
    #             'grant_type': 'authorization_code',
    #             'redirect_uri': self.callback_url,
    #             'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/user.birthday.read',
    #         }
    #
    #         token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
    #         if token_response.status_code != 200:
    #             return Response({'error': 'Failed to obtain Google access token'}, status=400)
    #
    #         google_token_data = token_response.json()
    #         access_token = google_token_data.get('access_token')
    #
    #         if token_response.status_code == 200:
    #             print("logged")


