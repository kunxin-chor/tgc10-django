from django.urls import path
import reviews.views

urlpatterns = [
    path('', reviews.views.show_reviews),
    path('create/<book_id>', reviews.views.create_review,
         name="create_review")
]
