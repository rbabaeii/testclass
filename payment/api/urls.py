from django.urls import path
from .views import *

urlpatterns = [
    path('order/update/<str:pk>/' , UpdateOrderView.as_view() , name= 'update-order'),
    path('order/detail/<str:pk>/' , DetailOrderView.as_view() , name= 'detail-order'),
    path('order-item/add/' , AddOrderItemView.as_view() , name= 'add-orderItem'),
    path('order-item/update/<str:pk>/' , UpdateOrderItemView.as_view() , name='update-orderItem'),
    path('order-item/delete/<str:pk>/' , DeleteOrderItem.as_view() , name='delete-orderItem'),
    path('order/comment/add/' , AddCommentView.as_view() , name= 'add-comment'),
    path('order/comment/list/<str:pk>/' , ListOrderCommentsView.as_view()),
    path('pay/create/<str:pk>/' , PaymentCreateAPIView.as_view()),
    path('pay/verify/' , PaymentVerifyView.as_view())
]
