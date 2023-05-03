from rest_framework import serializers
from store.models import Store , StoreDocument , Category , Food
from utils.models import Image
from payment.models import *

class CreateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ('owner' , )
        extra_kwargs = {'is_verified':{'read_only':True}}

    # def validate(self, owner):  
    #     user = self.context['request'].user
    #     if Store.objects.filter(owner = user).exists():
    #         raise serializers.ValidationError("Error ! Store with this user already exist") 
    #     else:
    #         return owner

    def save(self, **kwargs):
        request = self.context['request']
        return super(CreateStoreSerializer , self).save(owner = request.user)


class ListStoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(method_name='get_owner')
    location = serializers.SerializerMethodField(method_name='get_location')
    
    def get_owner(self , obj):
        return obj.owner.username

    def get_location(self , obj):
        if obj.location is not None:
            return obj.location.address
        else :
            return None
        
    class Meta:
        model = Store
        fields = '__all__'

class UpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        extra_kwargs = {'owner':{'read_only':True} , 'is_verified':{'read_only':True}}

class VerifyStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('owner' , 'store_name' , 'store_phone' , 'city' )

class ListCategorySerializer(serializers.ModelSerializer):
    def get_parent(self , obj):
        if obj.parent is not None:
            return obj.parent.name
        return None
    
    parent = serializers.SerializerMethodField(method_name='get_parent')
    class Meta:
        model = Category
        fields = ('name' , 'parent' , 'depth' , 'image')

class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name' , 'parent' , 'depth' , 'image')

class CreateStoreDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDocument
        fields = '__all__'
            
class ListStoreDocumentSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField(method_name='get_store')
    def get_store(self , obj):
        return obj.store.store_name
    class Meta:
        model = StoreDocument
        fields = '__all__'

class UpdateStoreDocumentSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField(method_name='get_store')
    def get_store(self , obj):
        return obj.store.store_name

    class Meta:
        model = StoreDocument
        fields = '__all__'
        extra_kwargs = {'store':{'read_only':True}}


class MakeFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        extra_kwargs = {'is_verified':{'read_only':True}}


class ListFoodByStoreSerializer(serializers.ModelSerializer):

    img = serializers.SerializerMethodField(method_name='get_img')
    store = serializers.SerializerMethodField(method_name='get_store')

    def get_store(self , obj):
        return (
            {
            "name": obj.store.store_name ,
            "phone" : obj.store.store_phone ,
            "category" :obj.store.category.name
            }
            )


    def get_img(self, obj):
        if obj.img:
            return Image.get_url(obj.img.image.url)
        return None

    class Meta:
        model = Food
        fields = '__all__'


class ListFoodByCategorySerializer(serializers.ModelSerializer):

    img = serializers.SerializerMethodField(method_name='get_img')
    category = serializers.SerializerMethodField(method_name='get_category')

    def get_category(self , obj):
        return obj.store.category.name
            
            


    def get_img(self, obj):
        if obj.img:
            return Image.get_url(obj.img.image.url)
        return None

    class Meta:
        model = Food
        fields = '__all__'

class UpdateFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        read_only_fields = ('store' , )

class ListOrderForStoreSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    def get_user(self , obj):
        return obj.user.username , obj.user.phone_number
        
    class Meta:
        model = Order
        fields = "__all__"

class ChangeOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ='__all__'
        read_only_fields = ('user' , 'location' , 'store' , 'items_price' , 'delivery_price' , 'payment')