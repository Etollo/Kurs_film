from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from reviewer import settings


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, user_language, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not user_language:
            raise ValueError("Users must have a language")

        user = self.model(
            email=self.normalize_email(email),
            user_language=user_language,
        )

    # def create_extended_user(self, email, first_name, last_name, birthday, user_language, password=None):
    #     if not email:
    #         raise ValueError("Users must have an email address")
    #     # if not username:
    #     #     raise ValueError("Users must have an username")
    #     if not first_name:
    #         raise ValueError("Users must have a first name")
    #     if not last_name:
    #         raise ValueError("Users must have a last name")
    #     if not birthday:
    #         raise ValueError("Users must have a birthday")
    #     if not user_language:
    #         raise ValueError("Users must have a language")

        # extended_user = self.model(
        #     email=self.normalize_email(email),
        #     # username=username,
        #     first_name=first_name,
        #     last_name=last_name,
        #     birthday=birthday,
        #     user_language=user_language,
        # )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_language, password):
        user = self.create_user(
            email=self.normalize_email(email),
            user_language=user_language,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(verbose_name="email", max_length=200, unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    gender = models.IntegerField(choices=settings.GENDER_CHOICES, default=1)
    birthday = models.DateField(null=True)
    user_language = models.CharField(max_length=20, db_index=True, default='en', choices=settings.LANGUAGES)
    photo = models.ImageField(upload_to='photos/users', null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday', 'user_language']

    objects = CustomUserManager()

    class Meta:
        permissions = [
            ("edit_user", "Can edit an user data"),
            ("delete_user", "Can remove an user"),
            ("view_company_user", "Can view all company users"),
        ]

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_date_joined(self):
        return self.date_joined

    def __str__(self):
        return self.email
