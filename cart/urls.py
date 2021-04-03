from django.urls import path

import cart.views

urlpatterns = [
    path('add/<book_id>', cart.views.add_to_cart,
         name="add_to_cart")
]
