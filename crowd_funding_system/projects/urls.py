from django.urls import path
from . import views
from .views import new_project


urlpatterns = [
    path('<uuid:project_id>', views.project_details, name='project_details'),
    path('', views.index, name='index'),
    path('new',new_project),
]
