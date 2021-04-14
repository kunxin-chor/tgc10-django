from django.shortcuts import render, reverse, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# import django settings (meaning the settings.py file)
from django.conf import settings
import stripe
import json

from books.models import Book


def checkout(request):
    # need to set the API key for stripe to work
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # need the shopping cart
    cart = request.session.get('shopping_cart', {})

    # create line items
    line_items = []

    # to store how many quantity of each book has been purchased
    all_book_ids = []

    for book_id, book in cart.items():
        book_model = get_object_or_404(Book, pk=book_id)

        line_item = {
            "name": book_model.title,
            # because Stripe deals only with cents
            "amount": int(book_model.cost * 100),
            "quantity": book['qty'],
            "currency": "SGD"
        }

        line_items.append(line_item)

        # store a record to remember that for a given book id,
        # what is the quantity ordered
        all_book_ids.append({
            'book_id': book_id,
            'qty': book['qty']
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        client_reference_id=request.user.id,
        metadata={
            "all_book_ids": json.dumps(all_book_ids)
        },
        mode="payment",
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL
    )

    # remove all items from the shopping cart
    request.session['shopping_cart'] = {}

    return render(request, 'checkout/checkout-template.html', {
        'session_id': session.id,
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


# we want to exempt the payment_completed function from CSRF
@csrf_exempt
def payment_completed(request):
    # 1. verify that it is actually from Stripes
    payload = request.body

    # extract out the signature from the data that Stripes sent us
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    # prepare a variable to store the data that stripe is sending us
    event = None

    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    # actually do the verification to make the data from the stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SigntuareVerificationError as e:
        # means the data is not from Stripe
        return HttpResponse(status=400)

    # 2. once we have verified from Stripe, we have
    # extract out data that Stripe sent us
    if event['type'] == 'checkout.session.completed':

        # the event represents the payment being completed
        session = event['data']['object']
        all_book_ids_str = session['metadata']['all_book_ids']
        all_book_ids = json.loads(all_book_ids_str)
        print(all_book_ids)

        print(session)
        # todo: put in the code to handle successful transaction
    return HttpResponse(status=200)
