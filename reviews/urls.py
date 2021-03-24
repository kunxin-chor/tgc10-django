from django.urls import path
import reviews.views

urlpatterns = [
    path('create', reviews.views.create_review)
]
