from django.urls import path
from .views import edit_project_rating #, update_project_rating

urlpatterns=[
    path('<str:id>/edit', edit_project_rating, name="edit_project_rating"),
    # path('<str:id>/update', update_project_rating, name="update_project_rating"),
]

