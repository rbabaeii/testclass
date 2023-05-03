import os
import re
from accounts.models import User
from rpfood.error_manager import ErrorHandler
from django.db.models import Q
import img2pdf
from utils.models import Image
from PIL import Image as PilImage
import requests
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile


def check_user_validator(value):
    email_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)
    phone_regex = re.compile(r'^(09)+?\d{9}', re.IGNORECASE)

    if phone_regex.fullmatch(value):
        return {"mobile_number": value}

    if email_regex.fullmatch(value):
        return {"email": value}

    return {}


def validate_otp_code(value):
    if len(str(value)) != 4:
        raise ErrorHandler.get_error_exception(400, "invalid_otp_code")


def validate_phone_or_email(value):
    email_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)
    phone_regex = re.compile(r'^(09)+?\d{9}', re.IGNORECASE)

    validate = [phone_regex.fullmatch(value), email_regex.fullmatch(value)]
    if not any(validate):
        raise ErrorHandler.get_error_exception(400, "invalid_user_validator")


def check_if_user_exists(value):
    if User.objects.filter(Q(mobile_number=value) | Q(email__iexact=value)).exists():
        raise ErrorHandler.get_error_exception(400, "already_exist_user")


def convert_img_to_pdf(images_list):
    filename = 'mypdf.pdf'
    images = []
    for item in images_list:
        img = Image.objects.get(id=item)
        img_link = img.get_image()
        image = requests.get(img_link, verify=False).content
        memory_image = BytesIO(image)
        pil_image = PilImage.open(memory_image)
        img_format = os.path.splitext(img_link)[1][1:].upper()
        img_format = 'JPEG' if img_format == 'JPG' else img_format
        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)
        new_image = ContentFile(new_image.getvalue())
        file_name = InMemoryUploadedFile(new_image, None, item, 'image/png', None, None)
        images.append(file_name)
    with open(filename, 'wb') as f:
        f.write(img2pdf.convert(images))
    return filename



