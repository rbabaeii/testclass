from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from .managers import CustomUserManager
from utils.models import BaseModel
from django.utils.translation import gettext_lazy as _


class User(AbstractUser, BaseModel):
    phone_regex = RegexValidator(regex=r'^(09)+?\d{9}',
                                 message=_(
                                     "Phone number must be entered in the format: '09xxxxxxxxx'. Up to 11 digits "
                                     "allowed. "))
    username = models.CharField(max_length=256, unique=True)
    mobile_number = models.CharField(max_length=11, validators=[phone_regex], null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    city = models.CharField(max_length=20 , default= None , null=True , blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    national_code = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.mobile_number} - {self.first_name} - {self.last_name}'

    @classmethod
    def get_user(cls, user_validator):
        try:
            user = User.objects.get(Q(mobile_number=user_validator) | Q(email=user_validator))
        except cls.DoesNotExist:
            raise ValidationError({"message": _("User does not exist.")})

        return user

    def get_user_location(self):
        return Location.objects.filter(user_id=self.id)

    


class Location(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.TextField()
    postal_code = models.IntegerField()
    mobile = models.CharField(verbose_name='شماره تلفن' , max_length=11)
    exact_addr = models.TextField(default='')
    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'


    def __str__(self):
        return f'{self.user.username} - {self.address}'
