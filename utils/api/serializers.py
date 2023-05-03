from rest_framework import serializers

from utils.models import Image


class ImageSerializer(serializers.ModelSerializer):
    """  serializer for Image """
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return Image.get_url(obj.image.url)
        return None

    class Meta:
        model = Image
        fields = "__all__"

