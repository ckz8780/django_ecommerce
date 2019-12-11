from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import OrderForm
from products.models import Product
from .models import Order, OrderLineItem


def checkout(request):

	if request.method == 'POST':
		cart = request.session.get('cart', {})

		form_data = {
			'full_name': request.POST['full_name'],
			'email': request.POST['email'],
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
			for item_id, item_data in cart.items():
				try:
					product = Product.objects.get(id=item_id)
					# If we're working w/ an item with no sizes, item_data will be the quantity
					if isinstance(item_data, int):
						order_line_item = OrderLineItem(
							order = order, 
							product = product, 
							quantity = item_data
						)
						order_line_item.save()
					# Otherwise we need to add order lineitems for each size
					else:
						for size, quantity in item_data['items_by_size'].items():
							order_line_item = OrderLineItem(
								order = order, 
								product = product, 
								quantity = quantity,
								product_size = size
							)
							order_line_item.save()

				# for item_id, quantity in cart.items():
				# 	try:
				# 		product = Product.objects.get(id=item_id)
				# 		order_line_item = OrderLineItem(
				# 			order = order, 
				# 			product = product, 
				# 			quantity = quantity
				# 			)
				# 		order_line_item.save()
				except Product.DoesNotExist:
					messages.error(request, (
						"One of the products in your bag wasn't found in our database. "
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

	order = Order.objects.get(order_number=order_number)
	messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email has been sent to {order.email}.')

	# Send a confirmation email
	cust_email = order.email
	subject = render_to_string('checkout/confirmation_emails/confirmation_email_subject.txt', {'order': order})
	body = render_to_string('checkout/confirmation_emails/confirmation_email_body.txt', {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

	send_mail(
		subject,
		body,
		settings.DEFAULT_FROM_EMAIL,
		[cust_email]
	)

	# Empty the customer's cart
	del request.session['cart']

	template = 'checkout/checkout_success.html'
	context = {
		'order': order
	}

	return render(request, template, context)