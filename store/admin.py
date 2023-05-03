from django.contrib import admin
from .models import Store , StoreDocument , Category ,Food
# Register your models here.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id' , 'owner' , 'category' , 'city' , 'store_name' , 'store_phone' , 'is_verified']
    ordering = ['-created_at']


@admin.register(StoreDocument)
class StoreDocument(admin.ModelAdmin):
    list_display = ['id' , 'store' , 'working_hours']
    ordering = ['-created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' , 'parent' , 'depth']
    ordering = ['-created_at']

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [ 'id' , 'name' , 'price' , 'store']