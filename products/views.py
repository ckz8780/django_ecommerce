from django.shortcuts import render
from .models import Product

def all_products(request):
	products = Product.objects.all()
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

	return render(request, 'products/products.html', {'products': products})