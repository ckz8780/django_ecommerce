import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile

import json

class Order(models.Model):

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False, default='')
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True, default='')
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True, default='')
    county = models.CharField(max_length=80, null=True, blank=True, default='')
    date = models.DateTimeField(auto_now_add=True)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')


    def generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()


    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for shipping costs
        """
        
        # Aggregate all lineitems to get their total cost
        lineitem_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']

        # Set the new order_total
        self.order_total = lineitem_total or 0

        # Determine shipping cost
        if self.order_total <= settings.FREE_SHIPPING_THRESHOLD:
            self.shipping_cost = self.order_total * settings.STANDARD_SHIPPING_PERCENTAGE/100
        else:
            self.shipping_cost = 0

        # Calculate and set grand total
        self.grand_total = self.order_total + self.shipping_cost
        self.save()


    def build_cart_from_order(self):
        """
        Construct the original cart given an order and all its items
        """
        cart = {}
        for item in self.lineitems.all():
            item_id = item.product.id
            size = item.product_size
            quantity = item.quantity
            if size:
                if item_id in list(cart.keys()):
                    if size in cart[item_id]['items_by_size'].keys():
                        cart[item_id]['items_by_size'][size] += quantity
                    else:
                        cart[item_id]['items_by_size'][size] = quantity
                else:
                    cart[item_id] = {'items_by_size': {size: quantity}}
            else:
                if item_id in list(cart.keys()):
                    cart[item_id] += item.quantity
                else:
                    cart[item_id] = item.quantity
        return json.dumps(cart)


    def save(self, *args, **kwargs):
        """
        Override the default save method to set the order number
        if it hasn't been set already
        """
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.order_number

        
class OrderLineItem(models.Model):

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0, editable=False)


    def save(self, *args, **kwargs):
        """
        Override the default save method to set the lineitem total
        and update the order total
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
    