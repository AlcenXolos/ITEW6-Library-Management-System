from django.utils import timezone
from django.conf import settings
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    copies_available = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    
class BorrowTransactions(models.Model):
    STATUS_CHOICES = [
        ("borrowed", "Borrowed"),
        ("returned", "Returned")
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="borrowed")
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        return self.status == 'borrowed' and self.due_date < timezone.now().date()
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"