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

    if book_id in cart:
        cart[book_id]['qty'] += 1
        cart[book_id]['total_cost'] = int(
            cart[book_id]['qty']) * float(cart[book_id]['cost'])
    else:

        cart[book_id] = {
            'id': book_id,
            'title': book.title,
            # because decimal cannot be convereted to JSON
            'cost': float(book.cost),
            'total_cost': float(book.cost),
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


def remove_from_cart(request, book_id):
    # retrieve the shopping cart from the session
    cart = request.session.get('shopping_cart', {})

    if book_id in cart:
        # remove the key represented by id of the book
        # from the cart dictionary
        del cart[book_id]
        # save the cart back to the session
        request.session['shopping_cart'] = cart
        messages.success(
            request, "The item has been removed from the shopping cart")

    return redirect(reverse('view_books'))


def update_quantity(request, book_id):

    # retrive the shopping cart from session
    cart = request.session.get('shopping_cart', {})
    if book_id in cart:
        cart[book_id]['qty'] = int(request.POST['qty'])
        cart[book_id]['total_cost'] = float(
            cart[book_id]['cost']) * int(request.POST['qty'])
        request.session['shopping_cart'] = cart
        messages.success(request, 'The quantity for the item has changed')

    return redirect(reverse('view_cart'))
