from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe

@require_POST
@csrf_exempt
def webhook(request):
    """ Listen for webhooks and handle them """

    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify the signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, wh_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)  # Invalid signature
    except Exception as e:
        return HttpResponse(content=e, status=400)  # Any other exception

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevent handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe    
    event_type = event['type']

    # If there's a handler for it, get it from the event map.
    # Otherwise use the generic one
    try:
        event_handler = event_map[event_type]
    except KeyError:
        event_handler = handler.handle_event

    # Call the event handler with the event, e.g.
    # handler.handle_payment_intent_succeeded(event)
    response = event_handler(event)
    return response
