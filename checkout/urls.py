from django.urls import path, include
from .views import checkout, cache_checkout_data, checkout_success

urlpatterns = [
    path('', checkout, name='checkout'),
    path('cache_checkout_data/', cache_checkout_data, name='cache_checkout_data'),
    path('checkout_successs/<order_number>/', checkout_success, name='checkout_success'),
]