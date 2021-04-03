from django.shortcuts import render, reverse, HttpResponse, get_object_or_404

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

    return render(request, 'checkout/checkout-template.html', {
        'session_id': session.id,
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })
