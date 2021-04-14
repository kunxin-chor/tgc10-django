from django.urls import path

from .views import checkout, payment_completed

urlpatterns = [
    path('', checkout, name='checkout'),
    path('payment_completed', payment_completed)
]