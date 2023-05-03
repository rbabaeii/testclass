from django.db import models
import uuid
from django.http import Http404
from django.conf import settings
from storages.backends.ftp import FTPStorage
FTP_FILE_STORAGE = FTPStorage()


def ftp_upload_to(instance, filename):
    return f'public_html/images/image_{instance.id}.{filename.split(".")[-1]}'


def ftp_file_upload_to(instance, filename):
    return f'public_html/files/files_{instance.id}.{filename.split(".")[-1]}'


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def update(self, **kwargs):
        for field in kwargs:
            self.__setattr__(field, kwargs[field])
        self.save()

    @classmethod
    def get_object_or_404(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            raise Http404

    @classmethod
    def is_exist(cls, *args, **kwargs):
        obj = cls.objects.filter(*args, **kwargs)
        return obj.exists(), obj.first()


class Image(BaseModel):
    image = models.ImageField(upload_to=ftp_upload_to, storage=FTP_FILE_STORAGE)
    alt = models.CharField(max_length=100)
    description = models.CharField(max_length=100 , verbose_name='توضیحات')
    
    def get_image(self):
        image_url = self.get_url(self.image.url) if self.image else None
        return image_url

    @classmethod
    def get_url(cls, path):
        return f"{settings.FTP_STORAGE_ADDRESS}/images{path.split('images')[-1]}"



class Configure(BaseModel):
    web_title = models.CharField(max_length=256)
    nav_icon = models.ForeignKey(Image, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='nav_icon')
    arp_price = models.PositiveIntegerField(default=1000)
    site_description = models.TextField(null=True, blank=True)
    fav_icon = models.ForeignKey(Image, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='fav_icon')
