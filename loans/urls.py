from django.urls import path
from . import views

urlpatterns = [
    path("loans/", views.LoanView.as_view()),
    path("loans/<int:copy_id>/", views.LoanCopyDetailView.as_view()),
]
