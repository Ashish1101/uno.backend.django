from datetime import datetime, timedelta
import uuid
from random import randint, random
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField

import pytz
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from generics.utils.models import GenericModel

class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None):
        if not mobile:
            raise ValueError('Users must have an mobile number')

        user = self.model(
            mobile=mobile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None):

        user = self.create_user(
            mobile, password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

def random_otp():
    return random.randint(1111, 9999)

class Otp(GenericModel):
    phone_no = models.BigIntegerField(null=True, blank=True)
    otp = models.PositiveIntegerField(default=random_otp)
    expiry_datetime = models.DateTimeField()

    class Meta:
        verbose_name = ('user otp')
        verbose_name_plural = ('users otp')

    def __str__(self):
        return "{} : {}".format(self.otp, self.phone_no)

    def __unicode__(self):
        return "{} : {}".format(self.otp, self.phone_no)


class User(AbstractBaseUser, GenericModel):
    """
    User Model:
        It contains basic user information required for authentication,
        In case of api request, user can use authentication token for login
    """

    first_name = models.CharField(max_length=32, null=True, blank=True)
    middle_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)

    username = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    pan = models.CharField(max_length=10, null=True, blank=True)
    aadhar = models.CharField(max_length=16, null=True, blank=True)

    father_name = models.CharField(max_length=128, null=True, blank=True)
    mother_name = models.CharField(max_length=128, null=True, blank=True)
    spouse_name = models.CharField(max_length=128, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    mpin = models.CharField(max_length=4, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True, unique=True)
    is_mobile_verified = models.BooleanField(default=False)
    is_aadhaar_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def __str__(self):
        return "{} - {} - {} ".format(self.mobile, self.first_name, self.password)

    def __unicode__(self):
        return "{} - {}".format(self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def send_otp(self):
        from apps.users.models import Otp
        Otp.objects.filter(phone_no=self.mobile, is_active=True).update(is_active=False)
        otp = randint(100000, 999999)
        expiry_minutes = datetime.now() + timedelta(minutes=5)
        otp_obj = Otp.objects.create(phone_no=self.mobile, otp=otp, expiry_datetime=expiry_minutes)
        otp_obj.save()
        return otp
        # send_otp = send_sms_otp(self.mobile, otp_template.format(otp=otp))

    def verify_otp_or_mpin(self, supplied_otp,):
        is_verified = False
        if supplied_otp is not None:
            from apps.users.models import Otp
            print("this is user", self.mobile)
            otp_obj = Otp.objects.filter(phone_no=self.mobile, is_active=True).order_by('-created_on').first()
            print("this is opt", otp_obj.otp, supplied_otp)
            current_time = datetime.now(pytz.utc)
            if otp_obj and otp_obj.expiry_datetime > current_time and str(otp_obj.otp) == str(supplied_otp):
                if not self.is_mobile_verified:
                    self.is_mobile_verified = True
                self.save()
                otp_obj.is_active = False
                otp_obj.save()
                is_verified = True
        return is_verified

    def pan(self, pan):
        self.pan(pan)

AADHAAR = "AADHAAR"
PAN = "PAN"

TRANSACTION_TYPE_CHOICES = [
    (AADHAAR, _('Aadhaar')),
    (PAN, _('Pan'))
]


class KYC(GenericModel):
    data = JSONField(default=dict, blank=True)
    type = models.CharField(
        max_length=100, choices=TRANSACTION_TYPE_CHOICES, default=AADHAAR)
    type_id = models.CharField(max_length=12, null=True, blank=True)
    reference_id = models.CharField(max_length=75, null=True)

    class Meta:
        db_table = 'users_kyc'
        verbose_name = "kyc"
        verbose_name_plural = "kyc's"
