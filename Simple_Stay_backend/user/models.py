from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('user_type') != 'admin':
            raise ValueError('Superuser field role must be "admin"')
        
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser field is_active must be true')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser field is_staff must be true')

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser field is_admin must be True')

        return self.create_user(email=email, password=password, **extra_fields)
        
        


class CustomUser(AbstractBaseUser):

    USER_TYPES = (
        ('user', 'user'),

        ('owner', 'Owner'),

        ('admin', 'Admin'),
    )

    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.PositiveBigIntegerField(null=True,blank=True)
    user_type = models.CharField(max_length=100,default='user',choices=USER_TYPES)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  # Add this line

    

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
