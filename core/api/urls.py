from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.api.urls')),
    # path('products/', include('products.api.urls')),
    path('payments/', include('payment.api.urls')),
    path('utils/', include('utils.api.urls')),
    path('' , include('store.api.urls')),
]