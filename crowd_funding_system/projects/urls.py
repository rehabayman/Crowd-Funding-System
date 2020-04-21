from django.urls import path
from .views import new_project

urlpatterns = [
    path('new',new_project),
]