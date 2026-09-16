from django.contrib.auth.backends import ModelBackend
from apps.accounts.models import Account


class EmailAuthBackend(ModelBackend):
    """
    Authenticate using email address instead of username.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
