from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, BorrowTransactions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .serializers import BookSerializer, BorrowTransactionsSerializer
from .serializers import SignupSerializer, LoginSerializer

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Signup successful.",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful.",
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Response helper function
def build_response(status, message, data):
    return Response(
        {
            "status": status, 
            "message": message, 
            "data": data
        }, 
        status=status
    )

class BookListView(APIView):
    """
    View to list all books.
    """
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookAddView(APIView):
    """
    View to add a new book (ADMIN only).
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookEditView(APIView):
    """
    View to edit book information (ADMIN only).
    """
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteBookView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        active_borrows = BorrowTransactions.objects.filter(book=book, status="borrowed")

        if active_borrows.exists():
            return Response(
                {"detail": "Cannot delete book. It is currently borrowed by one or more users."},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.delete()
        return Response(
            {"detail": "Book deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


# POST: Borrow a book
class BorrowBookView(APIView):
    """
    API View for borrowing books
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        
        try:
            book = Book.objects.get(id=data.get("book_id"))
        except Book.DoesNotExist:
            return build_response(
                status.HTTP_404_NOT_FOUND,
                "The book with the given ID does not exist.",
                {},
            )
            
        data['user_id'] = request.user.id
        
        data['borrowed_date'] = timezone.now()
        
        # Ensure the 'status' is set to 'borrowed' by default
        if 'status' not in data:
            data['status'] = 'borrowed'  # Set the default status to 'borrowed'

        # Serialize the data
        serializer = BorrowTransactionsSerializer(data=data)
        if serializer.is_valid():
            # Save the new borrowed book transaction
            serializer.save()

            return build_response(
                status.HTTP_201_CREATED,
                "Book borrowed successfully.",
                serializer.data,
            )
        
        # If data is invalid, return error response
        return build_response(
            status.HTTP_400_BAD_REQUEST,
            "Failed to borrow the book.",
            serializer.errors,
        )


# GET: List all borrowed books (transactions)
class BorrowedBookTransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if the user is an admin
        if request.user.is_staff:
            # Admins can see all borrowed book transactions
            queryset = BorrowTransactions.objects.all().select_related('book', 'user')
        else:
            # Regular users can only see their own borrowed transactions
            queryset = BorrowTransactions.objects.filter(user=request.user).select_related('book', 'user')

        serializer = BorrowTransactionsSerializer(queryset, many=True)
        
        return build_response(
            status.HTTP_200_OK,
            "Successfully retrieved the list of borrow transactions.",
            serializer.data,
        )