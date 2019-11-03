from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages

from .forms import OrderForm
from products.models import Product
from .models import Order, OrderLineItem


def checkout(request):

	if request.method == 'POST':
		cart = request.session.get('cart', {})

		form_data = {
			'full_name': request.POST['full_name'],
			'phone_number': request.POST['phone_number'],
			'country': request.POST['country'],
			'postcode': request.POST['postcode'],
			'town_or_city': request.POST['town_or_city'],
			'street_address1': request.POST['street_address1'],
			'street_address2': request.POST['street_address2'],
			'county': request.POST['county'],
		}

		order_form = OrderForm(form_data)
		if order_form.is_valid():
			order = order_form.save()

			for item_id, quantity in cart.items():
				try:
					product = Product.objects.get(id=item_id)
					order_line_item = OrderLineItem(
						order = order, 
						product = product, 
						quantity = quantity
						)
					order_line_item.save()
				except Product.DoesNotExist:
					messages.error(request, (
						"One of the products in your cart wasn't found in our database. "
						"Please call us for assistance! Your card was not charged.")
					)
					order.delete()
					return redirect(reverse('view_cart'))

			###################################
			# TODO: Actual Stripe charge here #
			###################################

			return(redirect(reverse('checkout_success', args=[order.order_number])))
		else:
			messages.error(request, 'There was an error with your form. Please double check your information.')
	else:
		order_form = OrderForm()

	stripe_public_key = settings.STRIPE_PUBLIC_KEY

	if not stripe_public_key:
		messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')
		
	template = 'checkout/checkout.html'
	context = {
		'stripe_public_key': stripe_public_key,
		'order_form': order_form,
	}

	return render(request, template, context)


def checkout_success(request, order_number):

	messages.success(request, f'Order successfully processed! Your order number is {order_number}')
	order = Order.objects.get(order_number=order_number)

	template = 'checkout/checkout_success.html'
	context = {
		'order': order
	}

	return render(request, template, context)