from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
from apps.base.models import BaseModel
from .constants import USER_ROLE
 
class UserManager(BaseUserManager):
    def create_user(self,email,password=None, **kwargs):
        if not email:
            raise ValueError("Email not valid!")
        
        email = self.normalize_email(email)
        kwargs.setdefault('is_active',True)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self,email,password=None, **kwargs): 
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **kwargs)

class User(BaseModel,AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # optional
    email = models.EmailField(unique=True)   
    role = models.CharField(choices=USER_ROLE,default='customer')
    email_verified = models.BooleanField(default=False)
    email_otp = models.IntegerField(blank=True,null=True)
    email_otp_created_at = models.DateTimeField(blank=True,null=True)

    USERNAME_FIELD = 'email'                
    REQUIRED_FIELDS = [] 
    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    
    def save(self,*args,**kwargs):
        if self.email and not self.username:
            email_name, domain_part = self.email.strip().rsplit("@", 1)
            self.username = email_name
        super().save(*args, **kwargs) 
     