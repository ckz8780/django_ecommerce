from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from products.models import Product

def search(request):
	query = request.GET.get('q')
	if query:
		products = Product.objects.filter(name__icontains=query)
		return render(request, 'products/products.html', {'products': products})
	
	messages.error(request, 'Please enter some search criteria')
	return redirect(reverse('products'))
