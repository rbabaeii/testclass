from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model
from utils.models import BaseModel
from accounts.models import Location
from store.models import Store , Food

class Payments(BaseModel):
    amount = models.IntegerField()
    authority = models.CharField(max_length=100)
    description = models.TextField(verbose_name='توضیحات')
    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
    def __str__(self) -> str:
        return f'{self.authority}'
User = get_user_model()
class Order(BaseModel):
    ORDER_STATUS =(
        ('AC' , 'Awaiting confirmation'),
        ('SC' , 'Store confirmation'),
        ('WD' , 'waiting for delivery'),
        ('HD', 'has been delivered')
    )
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user')
    location = models.ForeignKey(Location , null=True   , on_delete= models.SET_NULL , related_name='location')
    store = models.ForeignKey(Store , null=True   , on_delete=models.SET_NULL ,  related_name='order')
    items_price = models.IntegerField(default=0)
    delivery_price = models.IntegerField(default= 0)
    description = models.TextField(default='' , verbose_name='توضیحات')
    payment = models.OneToOneField(Payments ,  null=True  , blank=True , on_delete=models.SET_NULL , related_name='payment')
    is_payed = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20 , choices=ORDER_STATUS , default='AC')


    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
    def __str__(self) -> str:
        return f'{self.user} - {self.payment}'

class OrderItem(BaseModel):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name= 'orderitem')
    food = models.ForeignKey(Food , on_delete=models.CASCADE , related_name='orderitem')
    number = models.IntegerField()


    class Meta:
        verbose_name = 'orderitem'
        verbose_name_plural = 'orderitems'


    def __str__(self) -> str:
        return f'{self.order} - {self.food}'

class Comment(BaseModel):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name= 'Comment')
    text = models.TextField(verbose_name='متن')

    def __str__(self) -> str:
        return f'{self.order.user}-{self.text}'