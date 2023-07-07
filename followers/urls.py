from django.urls import path

from . import views

urlpatterns = [
    path("follow/", views.FollowerView.as_view()),
    path("follow/<int:book_id>/", views.FollowerView.as_view()),
    path("follow/colaborator/", views.FollowerListView.as_view()),
    path("unfollow/<int:book_id>/", views.FollowerDestroyView.as_view())
]
