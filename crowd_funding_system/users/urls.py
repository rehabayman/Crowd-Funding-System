from django.urls import path
from .views import show, show_projects

urlpatterns = [
    path('<str:id>/projects', show_projects, name="user_projects"),
    path('<str:id>', show, name="user_details"),
]
