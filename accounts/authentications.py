from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from accounts.models import User


class CustomAuthenticationBackend(ModelBackend):
    """
    Customize authenticate step for user login
    """
    def authenticate(self, request, username='', password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username.lower()) | Q(mobile_number=username) | Q(email=username))
        except User.DoesNotExist:
            return

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
