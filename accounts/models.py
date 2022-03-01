from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import uuid
from django.utils.safestring import mark_safe

GENDER = (
    ('male','Male'),
    ('female','Female'),
)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name=models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    gender = models.CharField(choices=GENDER,blank=True,null=True,max_length=50)
    dob = models.DateField(verbose_name='Date of Birth',default=timezone.now)
    email = models.EmailField(_('email address'), unique=True)
    mobile=models.BigIntegerField(blank=True,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    profile = models.ImageField(upload_to='profile\\',blank=True)
    auth_token = models.CharField(max_length=150,editable = False)
    is_varified = models.BooleanField(default=False)

    @property
    def full_name(self):
        
        return self.first_name+' '+self.last_name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def image_tag(self):
        if self.profile:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.profile.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
    def __str__(self):
        return self.email
