from django.urls import path
from . import views

urlpatterns = [
    path("follow/<int:book_id>/", views.FollowerView.as_view()),
]
