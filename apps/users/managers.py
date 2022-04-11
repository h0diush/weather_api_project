from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    '''Создание пользователя'''

    def email_valid(self, email):
        try:
            validate_email(email)
        except ValidationError:
            return ValidationError('Введите корректно электронную почту')

    def create_user(self, email, username, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_valid(email)
        else:
            return ValidationError('Электронная почта уже используется')
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """Создание суперпользователя комбинацией email-password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError(
                "Суперпользователь должен иметь is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValidationError(
                "Суперпользователь должен иметь is_superuser=True")

        if email:
            email = self.normalize_email(email)
            self.email_valid(email)
        else:
            raise ValidationError("Данный email уже используется")

        user = self.create_user(email, username, password, **extra_fields)
        return user
