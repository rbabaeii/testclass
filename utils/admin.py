from django.contrib import admin
from .models import Image, Configure


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']


@admin.register(Configure)
class PDFAdmin(admin.ModelAdmin):
    list_display = ['id', 'web_title', 'nav_icon', 'arp_price', 'site_description', 'fav_icon']
