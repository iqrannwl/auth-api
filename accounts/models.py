from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
import random
from django.utils.deconstruct import deconstructible
from .managers import CustomUserManager

@deconstructible
class RandomAvatar:
    def __init__(self):
        self.avatar = [
            'avatars/1.png',
            'avatars/2.png',
            'avatars/3.png',
            'avatars/4.png',
        ]
    
    def __call__(self):
        return random.choice(self.avatar)


class CustomUser(AbstractBaseUser, TimeStampedModel):
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone  = PhoneNumberField()
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="media", default=RandomAvatar())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name", "phone"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_lable):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    @property
    def is_superuser(self):
        return self.is_admin