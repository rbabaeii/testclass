from rest_framework import serializers
from payment.models import *
from rest_framework.fields import CurrentUserDefault

# class CreateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
#         read_only_fields = ('user' , 'items_price')
#     def save(self, **kwargs):
#         request = self.context['request']
#         return super(CreateOrderSerializer , self).save(user = request.user)
#     def validate(self, attrs):
#         user = self.context['request'].user
#         order= Order.objects.filter(user = user).order_by('-created_at')[0]
#         print(order.payment)
#         if order.payment == None :
#             raise serializers.ValidationError('Error Please pay for your previous order first')
#         else:
#             return attrs

class DetialOrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    location = serializers.SerializerMethodField(method_name='get_location')
    store = serializers.SerializerMethodField(method_name='get_store')
    def get_user(self , obj):
        return obj.user.username

    def get_location(self , obj):
        if obj.location is not None:
            return obj.location.address
        else :
            return None

    def get_store(self , obj):
        return (
            {
            "name": obj.store.store_name ,
            "phone" : obj.store.store_phone ,
            "category" :obj.store.category.name
            })
            
    class Meta:
        model = Order 
        fields = '__all__'


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = '__all__'
        read_only_fields = ('user' , 'items_price' , 'delivery_price')
    @property
    def get_items_price(self):
        id = self.context.get('view').kwargs.get('pk')
        order_items = OrderItem.objects.filter(order__id = id)
        sum = 0
        for item in order_items:
            item_price = item.food.price * item.number
            sum += item_price
        return sum

    def update(self, instance, validated_data):

        instance.items_price = self.get_items_price
        return super(UpdateOrderSerializer , self).update(instance , validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id' , 'order' , 'food' , 'number')
        read_only_fields = ('order' , )
    def validate(self, attrs):
        food = attrs['food']
        order = self.context['order']
        # user = self.context['request'].user
        # order = Order.objects.filter(user = user).order_by('-created_at')[0]
        if food.store != order.store:
            raise serializers.ValidationError("please select your foods from a one store")
        if order.payment != None:
            raise serializers.ValidationError("this order is expired please make new order")
        else:
            return attrs

class DeleteOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    #     read_only_fields = ('order' , )

    # def save(self, **kwargs):
    #     user = self.context['request'].user
    #     order = Order.objects.filter(user = user).order_by('-created_at')
    #     return super(AddCommentSerializer  , self).save(order = order)
    def validate_order(self , order):
        user = self.context['request'].user
        if order.user == user:
            return  order
        else:
            raise serializers.ValidationError('This order is not yours')

class ListOrderCommentSerialier(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    def get_user(self , obj):
        return obj.order.user.username

    class Meta:
        model = Comment
        fields = ('id' , 'order' , 'text' , 'user')
        
class SendRequestPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    def validate(self, attrs):
        payment = attrs.get('payment')
        is_payed = attrs.get('is_payed')
        print(payment , is_payed)
        if payment == None and is_payed == False:
            return attrs
        else:
            return serializers.ValidationError('This order payed before')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'