from django.urls import path
from .views import ProjectDonate, ProjectDelete


app_name="projects"
urlpatterns=[   
    path('/<id>/donate',ProjectDonate.as_view() , name="project_donate"),
    path('/<id>/delete',ProjectDelete.as_view() , name="project_delete")
]

