from django.urls import path
from .views import BookListView, BookAddView, BookEditView, BorrowBookView, BorrowedBookTransactionListView

url_prefix = "api/"

urlpatterns = [
    path('api/books/', BookListView.as_view(), name='book-list'),  # List books
    path('api/books/add/', BookAddView.as_view(), name='book-add'),  # Add a book
    path('api/books/<int:pk>/', BookEditView.as_view(), name='book-edit'),  # Edit a specific book by its pk
    
    # Borrow Management
    path('api/borrow/', BorrowBookView.as_view(), name="borrow-book"),  # Borrow a book
    path('api/transactions/', BorrowedBookTransactionListView.as_view(), name="borrow-book-transactions"),  # List transactions
]