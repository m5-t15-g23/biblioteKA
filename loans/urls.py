from django.urls import path
from . import views

urlpatterns = [
    path("loans/", views.LoanCopyDetailView.as_view()),
    path("loans/<int:book_id>/", views.LoanView.as_view()),
    path("loans/copy/<int:copy_id>/", views.LoanCopyDetailView.as_view()),
    path("loans/student/<int:student_id>/",
         views.LoanColaboratorDetailView.as_view()),
    path("loans/<int:loan_id>/checkout/", views.LoanCheckoutView.as_view()),
]
