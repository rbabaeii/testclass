from rest_framework import generics
from rest_framework.views import Response , APIView , status
from store.models import Store , StoreDocument , Category , Food
from .serializers import  *
from rest_framework.permissions import IsAuthenticated , IsAdminUser  , AllowAny
from .permissins import *
from payment.models import *

class CreateStoreView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = CreateStoreSerializer
    permission_classes = (UserVerified , )

class ListStoreView(APIView):
    permission_classes = (IsAuthenticated , )
    def get(self , request , *args , **kwargs):
        queryset = Store.objects.filter(city = request.user.city , is_verified = True)
        serializer = ListStoreSerializer(queryset , many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class ListStoreByCategory(APIView):
    permission_classes = (IsAuthenticated , ) 
    def get(self , request , *args , **kwargs):
        category = kwargs.get('category')
        queryset = Store.objects.filter(category = category , city = request.user.city ,is_verified = True)
        serializer = ListStoreSerializer(queryset , many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)


class DetailStoreView(generics.RetrieveDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = ListStoreSerializer
    permission_classes = ( IsAdminOrStoreOwner , )

class UpdateStoreView(generics.UpdateAPIView):
    queryset = Store.objects.all()
    serializer_class = UpdateStoreSerializer
    permission_classes = (IsAdminOrStoreOwner , )

class VerifyStoreView(generics.UpdateAPIView):
    queryset = Store.objects.all()
    serializer_class = VerifyStoreSerializer
    permission_classes = (IsAdminUser ,)


class CreateStoreDocuments(generics.CreateAPIView):
    queryset = StoreDocument.objects.all()
    serializer_class = CreateStoreDocumentSerializer
    permission_classes = (Has_Store , )

class ListStoreDocument(generics.RetrieveAPIView):
    queryset = StoreDocument.objects.all()
    serializer_class = ListStoreDocumentSerializer
    permission_classes = (IsAuthenticated , IsAdminOrOwnerOrRedonly )
    lookup_field = 'store'

class UpdateStoreDocument(generics.RetrieveUpdateAPIView):
    queryset = StoreDocument.objects.all()
    serializer_class = UpdateStoreDocumentSerializer
    permission_classes = (IsAuthenticated , IsAdminOrOwnerOrRedonly )
    lookup_field = 'store'
    
class ListCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ListCategorySerializer
    permission_classes = (IsAuthenticated ,)


class DetialCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = DetailCategorySerializer
    permission_classes = (IsAdminUser , )


class MakeFoodView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = MakeFoodSerializer
    permission_classes = (IsAdminOrOwnerOrRedonly , )


class ListFoodByStoreView(APIView):
    permission_classes = (IsAuthenticated , )
    def get(self ,request , *args , **kwargs):
        store = kwargs.get('store')
        queryset = Food.objects.filter(store = store)
        serializer_class = ListFoodByStoreSerializer(queryset, many = True)
        return Response(data = serializer_class.data , status=status.HTTP_200_OK)
    
class ListFoodByCategoryView(APIView):
    permission_classes = (IsAuthenticated ,)
    def get(self , requset ,*args , **kwargs):
        category = kwargs.get('category')
        queryset = Food.objects.filter(store__category = category , store__city = requset.user.city)
        serializer = ListFoodByCategorySerializer(queryset , many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)


class DetialUpdateFood(APIView):
    permission_classes = (IsAdminOrOwnerOrRedonly ,)
    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request , self):
                self.permission_denied(
                    request,
                    message= getattr(permission , 'message' , None) ,
                    code= getattr(permission , 'code' , None)
                )


    def get(self , request , *args , **kwargs):
        self.check_permissions(request= request)
        pk = kwargs.get('pk')
        queryset = Food.objects.get(id = pk)
        serializer = ListFoodByStoreSerializer(queryset)
        return Response(data = serializer.data , status= status.HTTP_200_OK)

    def put(self , request , *args  , **kwargs):
        pk = kwargs.get('pk')
        self.check_permissions(request=request)
        queryset = Food.objects.get(id = pk)
        serializer =UpdateFoodSerializer( queryset,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status = status.HTTP_200_OK)
        else :
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , *args , **kwargs):
        pk = kwargs.get('pk')

        self.check_permissions(request=request)
        queryset = Food.objects.get(id = pk)
        queryset.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class ListOrderForStoreView(APIView):
    permission_classes = (IsAdminOrStoreOwnerForListOrder,)
    def get(self,request , *args , **kwargs):
        pk = kwargs.get('pk')
        queryset = Order.objects.filter(store__id = pk , payment__isnull = False , is_payed = True)
        store = Store.objects.get(id = pk)
        self.check_object_permissions(request=request , obj=store)
        serializers = ListOrderForStoreSerializer(queryset , many = True)
        return Response(serializers.data , status = status.HTTP_200_OK)

class ChangeOrderStatus(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = ChangeOrderStatusSerializer
    permission_classes = (IsOrderStoreOwnerOrAdmin , )