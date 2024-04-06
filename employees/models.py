from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.
from .manager import EmployeeManager

class Employee(AbstractBaseUser, PermissionsMixin):
    employee_id = models.CharField(max_length=100, unique=True)

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_no = models.IntegerField(default=0)
    date_of_birth = models.DateTimeField(auto_now_add=True)
    employee_created = models.DateTimeField(auto_now_add=True)

    # address
    city = models.CharField(max_length=155)
    sub_city = models.CharField(max_length=155)
    woreda = models.CharField(max_length=155)
    house_no = models.IntegerField(null=True)

    # Job Status
    is_manager = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)
    is_credit_class = models.BooleanField(default=False)
    is_saving_super = models.BooleanField(default=False)

    # Perminssion Statuss
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'employee_id'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name
        
    objects = EmployeeManager()

