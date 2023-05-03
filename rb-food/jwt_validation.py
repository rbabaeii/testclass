import re

from django.urls import resolve
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None or self.get_request_view_attr(request, 'ignore_authentication'):
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    @staticmethod
    def replace_uuid_with_star(url):
        regex = re.compile('[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}', re.I)
        match = regex.search(url)
        if match:
            url = url.replace(match.group(), '*')
        return url

    @staticmethod
    def get_request_view_attr(request, attr):
        return resolve(request.path).func.view_class.__dict__.get(attr)
