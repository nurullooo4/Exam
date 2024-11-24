from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError


class UserModelManager(UserManager):
    def create_user(self,
                    email: str,
                    first_name: str = '',
                    last_name: str = '',
                    username: str = None,
                    password: str = None):
        if not email:
            raise ValidationError('Users must have an email address')

        email = self.normalize_email(email)

        if not username:
            username = email.split('@')[0]

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,
                         email: str,
                         first_name: str,
                         last_name: str,
                         password: str):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_customer = False
        user.is_admin = True
        user.save()

        if not user.is_superuser or not user.is_staff:
            raise ValidationError('Superuser must have is_superuser=True and is_staff=True')

        return user


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_customer=True)


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)
