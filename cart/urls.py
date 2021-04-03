from django.urls import path

import cart.views

urlpatterns = [
    path('add/<book_id>', cart.views.add_to_cart,
         name="add_to_cart"),
    path('', cart.views.view_cart, name='view_cart'),
    path('remove/<book_id>', cart.views.remove_from_cart,
         name="remove_from_cart"),
    path('update_quantity/<book_id>', cart.views.update_quantity,
         name="update_cart_quantity")
]
