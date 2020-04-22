from django.urls import path
from . import views
from .views import new_project, edit_project_rating #, update_project_rating

urlpatterns=[
    path('<str:id>/edit', edit_project_rating, name="edit_project_rating"),
    path('<uuid:project_id>', views.project_details, name='project_details'),
    path('', views.index, name='index'),
    path('new',new_project),
    # path('<str:id>/update', update_project_rating, name="update_project_rating"),
]
