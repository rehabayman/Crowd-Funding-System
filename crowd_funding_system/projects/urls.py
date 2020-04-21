from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:project_id>', views.project_details, name='project_details'),
    path('', views.index, name='index'),
]