def cart_contents(request):
    # retrieve the shopping cart from the session:
    cart = request.session.get('shopping_cart', {})
    return {
        'shopping_cart': cart,
        'number_of_items': len(cart)
    }