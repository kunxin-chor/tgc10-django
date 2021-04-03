from django.urls import path
import books.views

urlpatterns = [
    path('', books.views.index, name="view_books"),
    path('create', books.views.create_book),
    path('book_details/<book_id>', books.views.view_book_details,
         name='view_book_details'),
    path('update/<book_id>', books.views.update_book,
         name="update_book"),
    path('publishers/create', books.views.create_publisher),
    path('publishers', books.views.show_publishers,
         name='show_publishers'),
    path('publishers/update/<publisher_id>',
         books.views.update_publisher, name="update_publisher"),
    path('publishers/delete/<publisher_id>',
         books.views.delete_publisher, name="delete_publisher")
]
