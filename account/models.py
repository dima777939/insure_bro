from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, name, description, email, password, **extra_fields):
        values = [name, description, email]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError("The {} value must be set".format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            name=name, description=description, email=email, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, name, description, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, description, email, password, **extra_fields)

    def create_superuser(self, name, description, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(name, description, email, password, **extra_fields)


class InsuranceCompany(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "description"]

    name = models.CharField(
        max_length=20, verbose_name="Название компании", unique=True
    )
    description = models.CharField(max_length=500, verbose_name="Описание")
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True)

    object = AccountManager()

    class Meta:
        ordering = ("name",)
        verbose_name = "Страховая компания"
        verbose_name_plural = "Страховые компании"

    def __str__(self):
        return self.name
