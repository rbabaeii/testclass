import datetime
import random
import uuid
from django.core.cache import cache
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rpfood.error_manager import ErrorHandler
from accounts.models import User, Location
from utils.email_handler import send_email_thread
from utils.sms_handler import send_sms_thread
from accounts.utils import (check_user_validator,
                            validate_phone_or_email,
                            validate_otp_code,
                            check_if_user_exists)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        attrs['username'] = attrs['username'].lower()
        return super(CustomTokenObtainPairSerializer, self).validate(attrs)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('mobile_number', 'email')

    def save(self, **kwargs):
        instance = super(UserSerializer, self).save(**kwargs)
        password = self.validated_data.get("password")
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class VerifyUserBaseSerializer(serializers.Serializer):
    user_validator = serializers.CharField(validators=[validate_phone_or_email])

    def send_code(self):
        otp_code = random.randint(1000, 9999)
        send_time = timezone.now()
        user_validator = self.validated_data.get("user_validator")
        cache.set(f"user-{user_validator}", {"otp_code": otp_code, "send_time": send_time})
        print({"otp_code": otp_code, "send_time": send_time})
        # send code via email or phone function
        text = f'Rp Food \n OTP Code {otp_code}'
        if '@' in user_validator:
            send_email_thread("Verify your email", '', [user_validator], text)
        else:
            send_sms_thread(user_validator, text)

    def check_user(self):
        user_validator = self.validated_data.get("user_validator")
        try:
            User.objects.get(Q(mobile_number=user_validator) | Q(email__iexact=user_validator))
        except User.DoesNotExist:
            raise ErrorHandler.get_error_exception(404, "user_not_found")
        self.send_code()


class SignUpUserVerifySerializer(VerifyUserBaseSerializer):
    user_validator = serializers.CharField(validators=[validate_phone_or_email, check_if_user_exists])


class ForgetPasswordUserVerifySerializer(VerifyUserBaseSerializer):
    user_validator = serializers.CharField(validators=[validate_phone_or_email])


class VerifyUserOTPCodeBaseSerializer(serializers.Serializer):
    user_validator = serializers.CharField(validators=[validate_phone_or_email])
    otp_code = serializers.IntegerField(validators=[validate_otp_code])


class VerifyUserOTPCodeSerializer(VerifyUserOTPCodeBaseSerializer):

    def verify_code(self):
        otp_code = self.validated_data.get("otp_code")
        user_validator = self.validated_data.get("user_validator")
        time = timezone.now()

        user_cache = cache.get(f"user-{user_validator}")
        if user_cache and (time - user_cache.get("send_time")).total_seconds() <= 120:
            check_if_user_exists(user_validator)
            if user_cache.get("otp_code") == otp_code:
                new_user = User.objects.create(
                    username=f"user_{uuid.uuid4().hex[:10]}",
                    is_verified=True,
                    is_active=True,
                    **check_user_validator(user_validator)
                )
                return new_user
            cache.delete(f"user-{user_validator}")
            raise ErrorHandler.get_error_exception(400, "incorrect_otp_code")

        raise ErrorHandler.get_error_exception(400, "expired_otp_code")


class ForgetPasswordVerifyUserOTPCodeSerializer(VerifyUserOTPCodeBaseSerializer):
    def verify_code(self):
        otp_code = self.validated_data.get("otp_code")
        user_validator = self.validated_data.get("user_validator")
        time = timezone.now()

        user_cache = cache.get(f"user-{user_validator}")
        if user_cache and (time - user_cache.get("send_time")).total_seconds() <= 120:
            if user_cache.get("otp_code") == otp_code:
                # cache.set(f"user-{user_validator}", {**user_cache, "verified": True})
                user_random_token = get_random_string(length=100)
                cache.set(f"user-{user_validator}", {"token": user_random_token})
                return user_random_token
            raise ErrorHandler.get_error_exception(400, "incorrect_otp_code")
        raise ErrorHandler.get_error_exception(400, "expired_otp_code")


class ChangePasswordSerializer(serializers.Serializer):
    user_validator = serializers.CharField(validators=[validate_phone_or_email])
    password = serializers.CharField()
    re_password = serializers.CharField()
    token = serializers.CharField()

    def change_password(self):
        password = self.validated_data.get("password")
        re_password = self.validated_data.get("re_password")
        user_validator = self.validated_data.get("user_validator")
        token = self.validated_data.get("token")

        user_cache = cache.get(f"user-{user_validator}")
        if not user_cache:
            raise ErrorHandler.get_error_exception(401, "change_password_not_allowed")

        if password != re_password:
            raise ErrorHandler.get_error_exception(400, "incorrect_passwords")

        if token != user_cache.get("token"):
            raise ErrorHandler.get_error_exception(400, "invalid_token")

        user = User.get_user(user_validator)
        user.set_password(password)
        user.save()
        cache.delete(f"user-{user_validator}")


class BaseChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    re_password = serializers.CharField()

    def send_code(self):
        current_password = self.validated_data.get('current_password')
        new_password = self.validated_data.get('new_password')
        re_password = self.validated_data.get('re_password')
        request = self.context['request']
        user = request.user
        send_time = timezone.now()
        otp_code = random.randint(1000, 9999)
        if user.check_password(current_password):
            if new_password and re_password and new_password == re_password:
                cache.set(f'user-{user.username}', {'otp_code': otp_code, 'send_time': send_time,
                                                    'password': new_password})
                print({'otp_code': otp_code})

                # send otp code via email or phone
                if user.phone:
                    send_sms_thread(user.phone, f'RpKala \n Change Password OTP Code : {otp_code}')
                elif user.email:
                    send_email_thread("Password Recovery", '', [user.email],
                                      f'Rpkala \n Change Password OTP Code : {otp_code}')

            else:
                raise ErrorHandler.get_error_exception(400, "incorrect_passwords")
        else:
            raise ErrorHandler.get_error_exception(400, "incorrect_current_password")


class ChangePasswordDirectlySerializer(serializers.Serializer):
    otp_code = serializers.IntegerField(validators=[validate_otp_code])

    def change_password(self):
        otp_code = self.validated_data.get('otp_code')
        time = timezone.now()
        request = self.context['request']
        user = request.user

        user_cache = cache.get(f'user-{user.username}')
        if user_cache and (time - user_cache.get("send_time")).total_seconds() <= 120:
            if user_cache.get('otp_code') != otp_code:
                raise ErrorHandler.get_error_exception(400, "invalid_otp_code")

            password = user_cache.get('password')
            user.set_password(password)
            user.save()
            cache.delete(f'user-{user.username}')

        else:
            raise ErrorHandler.get_error_exception(400, "expired_otp_code")


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        exclude = ('user',)




class UserDetailsSerializer(serializers.ModelSerializer):
    is_seller = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'mobile_number', 'phone_number',
                  'email', 'national_code',
                  ]
