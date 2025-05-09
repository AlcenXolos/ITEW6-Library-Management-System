from django.urls import path
from .views import BookListView, BookAddView, BookEditView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('add/', BookAddView.as_view(), name='book-add'),
    path('<int:pk>/', BookEditView.as_view(), name='book-edit'),
]