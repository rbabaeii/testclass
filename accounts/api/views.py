from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView , CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.serializers import (SignUpUserVerifySerializer,
                                      VerifyUserOTPCodeSerializer,
                                      UserSerializer, ForgetPasswordUserVerifySerializer,
                                      ForgetPasswordVerifyUserOTPCodeSerializer, ChangePasswordSerializer,
                                      CustomTokenObtainPairSerializer, BaseChangePasswordSerializer,
                                      ChangePasswordDirectlySerializer, LocationSerializer,
                                       UserDetailsSerializer
                                      )
from accounts.models import User, Location 


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super(LoginView, self).post(request, *args, **kwargs)


class SendVerifyCode(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpUserVerifySerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                {"user_validator": data.get("user_validator"),
                 "message": _("Code sent successfully")},
                status=status.HTTP_200_OK)


class CheckVerifyCode(GenericAPIView):
    serializer_class = VerifyUserOTPCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.verify_code()
            refresh = RefreshToken.for_user(user)
            response = {
                "user": user.id,
                "message": _("User created successfully"),
                'refresh': str(refresh),
                'access': str(refresh.access_token),

            }
            return Response(response, status=status.HTTP_201_CREATED)


class UpdateUserView(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        serializer = self.get_serializer(instance=user, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": _("User profile completed successfully")
            }, status=status.HTTP_200_OK)


class ForgetPasswordSendCodeView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgetPasswordUserVerifySerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.check_user()
            return Response({"message": _("OTP code send to your email/phone")})


class ForgetPasswordVerifyCodeView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgetPasswordVerifyUserOTPCodeSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user_token = serializer.verify_code()
            return Response({
                "token": user_token,
                "user_validator": serializer.validated_data.get("user_validator"),
                "message": _("You are validate to change your password.")
            })


class ChangePasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.change_password()
            return Response({
                "message": _("Password changed successfully."),
            })


class ChangePasswordDirectlyView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = BaseChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response({
                'message': _('OTP CODE Sent To Your Email/Phone, Please Verify The Code'),
                'status': status.HTTP_200_OK
            })


class VerifyChangePasswordDirectlyView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordDirectlySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.change_password()
            return Response({
                'message': _('Your Password Changed Successfully'),
                'status': status.HTTP_200_OK
            })


class LocationView(ListAPIView, GenericAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(user_id=self.request.user.id)
        return super(LocationView, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        location_id = self.request.GET.get('location_id', None)
        location = Location.get_object_or_404(id=location_id, user_id=self.request.user.id)
        serializer = self.serializer_class(location, self.request.data)
        if serializer.is_valid():
            serializer.update(location, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
