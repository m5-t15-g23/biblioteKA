from django.urls import path
from . import views

urlpatterns = [
    path("loans/", views.LoanView.as_view()),
    path("loans/<int:pk>/", views.LoanCopyDetailView.as_view()),
]
