from django.urls import path
from .views import ProjectDetails, ProjectDelete,new_project, new_project, edit_project_rating
from . import views

app_name="projects"

urlpatterns=[   
    path('new',new_project),
    path('<id>',ProjectDetails.as_view() , name="project_details"),
    path('<id>/delete',ProjectDelete.as_view() , name="project_delete"),
    path('<str:id>/edit', edit_project_rating, name="edit_project_rating"),
    # path('<uuid:project_id>', views.project_details, name='project_details'),
    path('', views.index, name='index'),
]


