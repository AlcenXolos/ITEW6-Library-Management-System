# Default User Auth
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Book, BorrowTransactions
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'copies_available']

class BorrowTransactionsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=User.objects.all(), write_only=True
    )
    user = serializers.SerializerMethodField(read_only=True)  # Read-only user object
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = BorrowTransactions
        fields = [
            'id',
            'user_id',
            'user',
            'book',
            'book_id',
            'borrow_date',
            'due_date',
            'return_date',
            'status',
        ]
        
    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "email": obj.user.email,
        }

    def validate(self, data):
        user = data['user']
        book = data['book']
        borrowed_at = data.get('borrowed_at', timezone.now())
        due_date = data.get('due_date')
        status = data.get('status')
        
        if not User.objects.filter(id=user.id).exists():
            raise serializers.ValidationError("The user with the given ID does not exist.")
        
        # 1. Check if the book exists
        if not Book.objects.filter(id=book.id).exists():
            raise serializers.ValidationError("The book with the given ID does not exist.")
        
        # 2. Check if book has available copies
        if book.copies_available < 1:
            raise serializers.ValidationError("No available copies of this book.")

        # 3. Prevent duplicate unreturned borrow
        if BorrowTransactions.objects.filter(user=user, book=book, status='borrowed').exists():
            raise serializers.ValidationError("The user already borrowed this book and haven't returned it yet.")

        # 4. Validate due_date after borrowed_at
        if due_date and borrowed_at and due_date < borrowed_at.date():
            raise serializers.ValidationError("Due date must be after borrowed date.")

        # 5. Validate status
        if status not in ['borrowed', 'returned']:
            raise serializers.ValidationError("Status must be 'borrowed' or 'returned'.")

        return data

    # Actual borrowing method
    def create(self, validated_data):
        book = validated_data['book']
        # Decrement available copies when borrowed
        if validated_data['status'] == 'borrowed':
            book.copies_available -= 1
            book.save()
        return super().create(validated_data)
