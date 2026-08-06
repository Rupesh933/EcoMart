from django.contrib.auth.models import BaseUserManager

class MyAccountManager(BaseUserManager):
    """
    This is the manager for the account model.
    It is used to create users and superusers.
    """

    # This is for Creating normal user
    def create_user(self, first_name, last_name, username, email, phone_number, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have an username")
        
        if not phone_number:
            raise ValueError("User must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # This is for Creating superuser
    def create_superuser(self, first_name, last_name, email, username, password, phone_number="", **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
