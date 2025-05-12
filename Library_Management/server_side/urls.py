from django.urls import path
from .views import ReturnBookView, BookListCreateView, BookEditView, BookDeleteView, BorrowBookView, BorrowedBookTransactionListView, SignupView, LoginView, list_borrowers, UsersWithPendingBorrowsView

url_prefix = "api/"

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/borrowers/', list_borrowers, name='list_borrowers'),
    path('api/borrowed-users/', UsersWithPendingBorrowsView.as_view(), name='borrowed-users'),
    
    path('api/books/', BookListCreateView.as_view(), name='book-list-create'),  # List books
    # path('api/books/add/', BookAddView.as_view(), name='book-add'),  # Add a book
    path('api/books/<int:pk>/', BookEditView.as_view(), name='book-edit'),  # Edit a specific book by its pk
    path('api/books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete-book'), # deleting a specific book by its pk
    
    # Borrow Management
    path('api/borrow/', BorrowBookView.as_view(), name="borrow-book"),  # Borrow a book
    path('api/transactions/', BorrowedBookTransactionListView.as_view(), name="borrow-book-transactions"),  # List transactions

    #Return Management
    path('api/return/<int:borrow_id>/', ReturnBookView.as_view(), name='return-book'),
]