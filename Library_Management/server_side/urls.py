from django.urls import path
from .views import BookListView, BookAddView, BookEditView, BookDeleteView, BorrowBookView, BorrowedBookTransactionListView, SignupView, LoginView

url_prefix = "api/"

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('api/books/', BookListView.as_view(), name='book-list'),  # List books
    path('api/books/add/', BookAddView.as_view(), name='book-add'),  # Add a book
    path('api/books/<int:pk>/', BookEditView.as_view(), name='book-edit'),  # Edit a specific book by its pk
    path('api/books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete-book'), # deleting a specific book by its pk
    
    # Borrow Management
    path('api/borrow/', BorrowBookView.as_view(), name="borrow-book"),  # Borrow a book
    path('api/transactions/', BorrowedBookTransactionListView.as_view(), name="borrow-book-transactions"),  # List transactions
]