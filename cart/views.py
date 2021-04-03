from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages

# Create your views here.
from books.models import Book


def add_to_cart(request, book_id):

    # retrieve the shopping cart from session
    cart = request.session.get('shopping_cart', {})

    # first argument means we are retriving an instance of the Book model
    # second argument is the criteria
    book = get_object_or_404(Book, pk=book_id)

    cart[book_id] = {
        'id': book_id,
        'title': book.title,
        'cost': 99,
        'qty': 1
    }

    # save the shopping cart
    request.session['shopping_cart'] = cart

    messages.success(request, "Book has been added to your shopping cart")
    return redirect(reverse('view_books'))


def view_cart(request):

    cart = request.session.get('shopping_cart', {})

    return render(request, 'cart/view_cart-template.html', {
        'cart': cart
    })
