from django.urls import path, include
from .views import all_products, product_management, delete_product, edit_product

urlpatterns = [
    path('', all_products, name='products'),
    path('manage/', product_management, name='product_management'),
    path('manage/edit/<product_id>', edit_product, name='edit_product'),
    path('manage/delete/<product_id>/', delete_product, name='delete_product'),
]
