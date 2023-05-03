
from . import views
from django.urls import path

urlpatterns = [
    path('store/create/' , views.CreateStoreView.as_view() , name= 'create-new-store'),
    path('store/list/city/' , views.ListStoreView.as_view() , name= 'list-store-by-city'),
    path('store/list/category/<str:category>/' , views.ListStoreByCategory.as_view() , name= 'list-store-by-category'),
    path('store/detail/<str:pk>/' , views.DetailStoreView.as_view() , name='detail-store'),
    path('store/update/<str:pk>/' , views.UpdateStoreView.as_view() , name='Update-store'),
    path('store/verify/<str:pk>/' , views.VerifyStoreView.as_view() , name='verify-store'),
    path('store/add/documents/' , views.CreateStoreDocuments.as_view() , name='add-store-document'),
    path('list/documents/<str:store>/' , views.ListStoreDocument.as_view() , name='list-store-documents'),
    path('update/documents/<str:store>/' , views.UpdateStoreDocument.as_view() , name = 'update-store-documents'),
    path('category/list/' , views.ListCategoryView.as_view() , name='list-category'),
    path('category/detail/<str:pk>/' , views.DetialCategoryView.as_view() , name='detail-categories'),
    path('food/add/' , views.MakeFoodView.as_view() , name='make-food') ,
    path('food/list/stores/<str:store>/' , views.ListFoodByStoreView.as_view() , name='list-foods-by-store'),
    path('food/list/category/<str:category>/' , views.ListFoodByCategoryView.as_view() , name='list-foods-by-category'),
    path('food/detail/<str:pk>/' , views.DetialUpdateFood.as_view() , name="food-detail-update"),
    path('store/<str:pk>/orders/list/' , views.ListOrderForStoreView.as_view() , name='list-orders-for-store'),
    path('store/order/change-status/<str:pk>/' , views.ChangeOrderStatus.as_view() , name='change-order-status')
]