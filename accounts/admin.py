from django.contrib import admin
from .models import  Location, User


# class LegalSellerInline(admin.TabularInline):
#     model = LegalSeller


# class NaturalSellerInline(admin.TabularInline):
#     model = NaturalSeller


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_staff', 'is_verified', 'created_at', 'updated_at']
    ordering = ['-created_at']


# @admin.register(Seller)
# class SellerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user',  'mobile_number','is_verified']
#     ordering = ['-created_at']


@admin.register(Location)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'postal_code']
    ordering = ['-created_at']


# @admin.register(LegalSeller)
# class LegalSellerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'seller']
#     ordering = ['-created_at']


# @admin.register(NaturalSeller)
# class NaturalSellerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'seller']
#     ordering = ['-created_at']
