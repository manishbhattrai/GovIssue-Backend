from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=300)
    middle_name = models.CharField(max_length=300,blank=True)
    last_name = models.CharField(max_length=300)
    bio = models.TextField(blank=True)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    Document_image = models.ImageField(upload_to='documents/', null=True, blank=False)
    phone_number = PhoneNumberField(region="NP" ,unique=True)
    trust_points = models.IntegerField(default=0)


    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"

        return f"{self.first_name} {self.last_name}"

    @property
    def role(self):
        if self.is_admin or self.is_staff:
            return "admin"

        return "user"

    def __str__(self):
        return self.email