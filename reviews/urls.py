from django.urls import path
import reviews.views

urlpatterns = [
    path('', reviews.views.show_reviews),
    path('create', reviews.views.create_review)
]
