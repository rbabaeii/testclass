from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rpfood.error_manager import ErrorHandler
from utils.api.serializers import ImageSerializer
from utils.models import Image
from utils.utils import get_image_instance


class UploadImageView(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    def post(self, request, *args, **kwargs):
        image = self.request.FILES.get("image") or self.request.data.get("image")
        image_instance = get_image_instance(image)
        if image:
            new_image = Image.objects.create(image=image_instance , alt = self.request.data.get('alt') , description = self.request.data.get('description'))
            return Response(
                ImageSerializer(instance=new_image, context={"request": request}).data,
                status=status.HTTP_201_CREATED
            )
        raise ErrorHandler.get_error_exception(400, "invalid_image")
