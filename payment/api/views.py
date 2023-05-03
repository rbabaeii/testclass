from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView , Response , status
from django.views import View
from payment.models import Order , OrderItem , Payments , Comment
from .serializers import *
from .permissions import *
from store.api.permissins import UserVerified
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404 , render
from payment.api.utils import *
# class CreateOrderView(generics.CreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = CreateOrderSerializer
#     permission_classes = (UserVerified , )

class DetailOrderView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = DetialOrderSerializer
    permission_classes = (OwnerOrAdmin , )



class UpdateOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    permission_classes = (OwnerOrAdmin , )


# class CreateAddOrderItemView(generics.CreateAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
#     permission_classes = (OrderOwnerOrAdmin ,)

class AddOrderItemView(APIView):

    permission_classes = (UserVerified , )

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request , self):
                self.permission_denied(
                    request,
                    message= getattr(permission , 'message' , None) ,
                    code= getattr(permission , 'code' , None)
                )
    
    def post(self , request , *args , **kwargs):
        self.check_permissions(request=request)
        data = request.data.get('food')
        food = Food.objects.get(id = data)
        store__food = food.store
        obj , created = Order.objects.get_or_create(user = request.user , payment__isnull = True)
        if created:
            obj.store = store__food
            obj.delivery_price = food.store.delivery_price
            obj.location = food.store.location
            obj.save()
        serializer = OrderItemSerializer(data = request.data , context = {'user': request.user , 'order':obj})
        if serializer.is_valid():
            serializer.save(order = obj)
            return Response(serializer.data , status = status.HTTP_200_OK)
        else :
            return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
        
class UpdateOrderItemView(generics.UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (OrderOwnerOrAdmin , )

class DeleteOrderItem(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = DeleteOrderItemSerializer
    permission_classes = (OrderOwnerOrAdmin ,)

class AddCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    permission_classes = (IsAuthenticated , )

class ListOrderCommentsView(APIView):
    def get(self , request , *args , **kwargs):
        pk = kwargs.get('pk')
        queryset = Comment.objects.filter(order = pk)
        serializer = ListOrderCommentSerialier(queryset , many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)






class SendRequestPaymentView(APIView):


    #? sandbox merchant 
    if settings.SANDBOX:
        sandbox = 'sandbox'
    else:
        sandbox = 'www'

    ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

    amount = 1000  # Rial / Required
    description = "توضیحات مربوط به تراکنش"  # Required
    phone = 'YOUR_PHONE_NUMBER'  # Optional
    # Important: need to edit for realy server.
    CallbackURL = 'http://127.0.0.1:8080/api/v1/payment/verify/'

    # def post(self, request , *args , **kwargs):
    #     pk = kwargs.get('pk')
    #     order = get_object_or_404(Order , id = pk , user = request.user)
    #     request.session['order_id'] = order.id
    #     serializer = SendRequestPaymentSerializer(order)
    #     if serializer.is_valid():
    #         data = {
    #             "MerchantID": settings.MERCHANT,
    #             "Amount": order.items_price,
    #             "Description": self.description,
    #             "Phone": order.user.phone_number,
    #             "CallbackURL": self.CallbackURL,
    #         }
    #         data = json.dumps(data)
    #         # set content length by data
    #         headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    #         try:
    #             response = requests.post(self.ZP_API_REQUEST, data=data,headers=headers, timeout=10)

    #             if response.status_code == 200:
    #                 response = response.json()
    #                 if response['Status'] == 100:
    #                     obj = Payments.objects.create(amount = order.items_price , authority = response['Authority'] ,description = response['Description'])
    #                     obj.save()
    #                     return Response({'status': True, 'url': self.ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']} , status= status.HTTP_200_OK)
    #                 else:
    #                     return {'status': False, 'code': str(response['Status'])}
    #             return response
            
    #         except requests.exceptions.Timeout:
    #             return Response({'message':'timeout'} , status= status.HTTP_408_REQUEST_TIMEOUT)
    #         except requests.exceptions.ConnectionError:
    #             return Response({'status': False, 'code': 'connection error'})



class PaymentCreateAPIView(APIView):
    permission_classes = (IsAuthenticated ,)

    if settings.SANDBOX:
        sandbox = 'sandbox'
    else:
        sandbox = 'www'

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order , id = pk , user = request.user)
        serializer = SendRequestPaymentSerializer(order)
        if order.payment == None or order.is_payed == False:
            response = get_payment_gateway(
                amount=order.items_price,
                description= order.description,
                user_phone= request.user.phone_number
                )
            if response.get('Authority') is not None:
                obj = Payments.objects.create(amount = order.items_price , authority = response['Authority'] ,description = order.description)
                obj.save()         
                order.payment = obj
                order.save()
                link = f'https://{self.sandbox}.zarinpal.com/pg/StartPay/{response["Authority"]}'
                return Response({'link': link}, status=status.HTTP_200_OK)
            else:
                return Response({"خطا":"خطای غیرمنتظره ای رخداد لطفا بعدا دوباره امتحان کنید"} , status= status.HTTP_400_BAD_REQUEST)
        return Response({"خطا" : "این سفارش قبلا پرداخت شده است "}, status=status.HTTP_400_BAD_REQUEST)



class PaymentVerifyView(APIView):
    # permission_classes = (IsAuthenticated ,)
    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority', '')
        Status = request.GET.get('Status', '')
        payment = get_object_or_404(Payments,authority=authority)
        serializer = PaymentSerializer(payment)
        order = get_object_or_404(Order , payment__id = payment.id)
        if Status == 'OK' and payment:
            response = verify_payment(authority=authority, amount=payment.amount)
            if response['Status'] == 100 or response['Status'] == 101:
                order.is_payed = True
                order.save()
                return Response(serializer.data)
            else:
                order.is_payed = False
                payment.delete()
                order.save()
                return Response({"message" : "پرداخت ناموفق بود  لطفا بعدا تلاش کنید"} , status = status.HTTP_400_BAD_REQUEST)
        payment.delete()
        return Response({"پیام" : "پرداخت ناموفق بود  لطفا بعدا تلاش کنید"} , status= status.HTTP_400_BAD_REQUEST)

