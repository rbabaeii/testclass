from django.urls import path

from utils.api.views import UploadImageView

urlpatterns = [
    path('images/upload/', UploadImageView.as_view(), name='upload-image'),
]
