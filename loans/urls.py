from django.urls import path
from . import views

urlpatterns = [
    path('loans/<int:pk>/', views.LoanView.as_view()),
]