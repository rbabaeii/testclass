from django.db import models
from utils.models import BaseModel , Image
from django.contrib.auth import get_user_model
from accounts.models import Location
from ckeditor.fields import RichTextField 
# from payment.models import Payments

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

class Category(BaseModel , MPTTModel):
    name = models.CharField(verbose_name='نام دسته ', max_length=100)
    parent = TreeForeignKey('self' , null=True , blank = True, on_delete=models.CASCADE , related_name='childern')
    depth = models.IntegerField(verbose_name='عمق')
    image = models.ForeignKey(Image , null=True , blank= True , on_delete=models.SET_NULL)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return f'{self.name} - {self.depth}'


User = get_user_model()
class Store(BaseModel):
    owner = models.ForeignKey(User , on_delete= models.CASCADE , related_name='owner')
    location = models.OneToOneField(Location , null=True     , on_delete=models.SET_NULL )
    category = models.ForeignKey(Category ,  null=True     , on_delete= models.SET_NULL )
    city = models.CharField(verbose_name='شهر' , max_length=100)
    store_name = models.CharField(verbose_name='نام رستوران' , max_length=250)
    store_phone = models.CharField(verbose_name='شماره رستوران' ,help_text='به همراه پیش  شماره شهر' , max_length=11)
    is_verified = models.BooleanField(verbose_name='احراز هویت' , default= False)
    delivery_price = models.IntegerField(verbose_name='هزینه پیک' , default = 0)

    class Meta:
        verbose_name = 'store'
        verbose_name_plural = 'stores'

    def __str__(self) -> str:
        return f'{self.store_name} - {self.city}'


class StoreDocument(BaseModel):
    store = models.ForeignKey(Store , on_delete=models.CASCADE , related_name='Store')
    national_card_img = models.OneToOneField(Image , null=True ,on_delete=models.SET_NULL , related_name='card')
    business_lisence_img = models.OneToOneField(Image ,null=True ,on_delete=models.SET_NULL , related_name='lisence')
    menu_img = models.ForeignKey(Image ,null=True , on_delete=models.SET_NULL , related_name='menu')
    working_hours = models.JSONField()


    class Meta:
        verbose_name = 'StoreDocument'
        verbose_name_plural = 'StoreDocuments'

    def __str__(self) -> str:
        return f'{self.store.store_name} '

class Food(BaseModel):
    name = models.CharField(verbose_name='نام غذا' , max_length=100)
    contents = RichTextField(verbose_name='جزییات')
    price = models.IntegerField(verbose_name='قیمت')
    store = models.ForeignKey(Store , on_delete=models.CASCADE , related_name= 'store')
    # category = models.ForeignKey(Category , on_delete=models.CASCADE , null = True , blank=True)
    img = models.ForeignKey(Image , null=True     , on_delete= models.SET_NULL , related_name='img')
    is_verified = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'food'
        verbose_name_plural = 'foods'

    def __str__(self) -> str:
        return f'{self.name} - {self.price}'
        
class Hall(BaseModel):
    owner = models.ForeignKey(User , on_delete= models.CASCADE , related_name='Hall')
    location = models.ForeignKey(Location , null=True     ,on_delete= models.SET_NULL , related_name='locations')
    city = models.CharField(max_length=100 , verbose_name='شهر')
    capacity = models.IntegerField(verbose_name='ظرفیت')
    hall_phone = models.CharField(verbose_name='شماره سالن' ,help_text='به همراه پیش  شماره شهر' , max_length=11)


    class Meta:
        verbose_name = 'Hall'
        verbose_name_plural = 'Halls'

    def __str__(self) -> str:
        return f'{self.store_name} - {self.city}'

class Table(BaseModel):
    store = models.ForeignKey(Store , on_delete=models.CASCADE , related_name='Tables')
    table_number = models.IntegerField(verbose_name='شماره میز ')
    capacity = models.IntegerField(verbose_name='ظرفیت')
    hour_price = models.IntegerField(verbose_name='هزینه هر ساعت')


    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

    def __str__(self) -> str:
        return f'{self.store.store_name} - {self.capacity}'

# class RentTable(BaseModel):
#     user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='RentTable')
#     table = models.ForeignKey(Table , on_delete=models.SET_NULL , related_name='RentTable')
#     payment = models.ForeignKey(Payments , on_delete=models.SET_NULL , related_name='RentTable')
#     rent_date = models.DateField(verbose_name='روز رزرو')
#     start_time = models.TimeField(verbose_name='زمان شروع')
#     end_time = models.TimeField(verbose_name='زمان پایان')
#     total_price = models.IntegerField(verbose_name='هزینه کلی')


#     class Meta:
#         verbose_name = 'Hall'
#         verbose_name_plural = 'Halls'

#     def __str__(self) -> str:
#         return f'{self.user.get_username} - {self.table.store.store_name} - {self.table.table_number}'