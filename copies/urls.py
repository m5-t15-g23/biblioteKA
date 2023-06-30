from django.urls import path

from . import views

urlpatterns = [
    path("copies/", views.CopyView.as_view())
]
