from django.urls import path
from .views import (
    SendVerifyCode, CheckVerifyCode,
    UpdateUserView, ForgetPasswordSendCodeView,
    ForgetPasswordVerifyCodeView, ChangePasswordView,
    ChangePasswordDirectlyView, VerifyChangePasswordDirectlyView, LocationView,
    UserDetailsView 
)
urlpatterns = [
    path('send-code/', SendVerifyCode.as_view(), name='send-code'),
    path('verify-code/', CheckVerifyCode.as_view(), name='verify-code'),
    path('complete-user-signup/', UpdateUserView.as_view(), name='complete-user-signup'),
    path('forget-password-send-code/', ForgetPasswordSendCodeView.as_view(),
         name='forget-password-send-code'),
    path('forget-passowrd-verify-code/', ForgetPasswordVerifyCodeView.as_view(),
         name='forget-password-verify-code'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-password-directly/', ChangePasswordDirectlyView.as_view(),
         name='change-password-directly'),
    path('verify-change-password/', VerifyChangePasswordDirectlyView.as_view(),
         name='verify-change-password'),
    path('location/', LocationView.as_view(), name='location'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
]