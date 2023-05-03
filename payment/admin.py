from django.contrib import admin
from .models import Payments , Comment , Order , OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'store' , 'items_price' , 'is_payed' , 'payment' ]
    ordering = ['-created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id' , 'order' , 'food' , 'number']
    ordering = ['-created_at']

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id' ,'amount' , 'authority' , 'description' ]
    ordering = ['-created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id' , 'text' , 'order')
    ordering = ['-created_at']
