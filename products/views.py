from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q

from .models import Product

def all_products(request):
	products = Product.objects.all()
	query = None
	if request.GET:
		if 'sort' in request.GET:
			sortkey = request.GET['sort']
			if 'direction' in request.GET:
				direction = request.GET['direction']
				if direction == 'desc':
					sortkey = f'-{sortkey}'
			
			products = products.order_by(sortkey)

		if 'category' in request.GET:
			categories = request.GET['category'].split(',')
			products = products.filter(category__name__in=categories)

		if 'q' in request.GET:
			query = request.GET['q']
			if not query:
				messages.error(request, "You didn't enter any search criteria!")
				return redirect(reverse('products'))

			queries = Q(name__icontains=query) | Q(description__icontains=query)
			products = products.filter(queries)


	return render(request, 'products/products.html', {'products': products, 'search_term': query})