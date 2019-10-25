from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from products.models import Product

def search(request):
	query = request.GET.get('q')
	if query:
		products = Product.objects.filter(name__icontains=query)
		return render(request, 'products/products.html', {'products': products, 'search_term': query})
	
	messages.error(request, "You didn't enter any search criteria!")
	return redirect(reverse('products'))
