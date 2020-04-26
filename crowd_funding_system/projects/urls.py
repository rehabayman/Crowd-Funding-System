from django.urls import path
from .views import *
from . import views

app_name="projects"

urlpatterns=[   
    path('new',new_project, name='new_project'),
    path('report/<uuid:project_id>',views.report_project, name='report_project'),
    path('<id>',ProjectDetails.as_view() , name="project_details"),
    path('<id>/delete',ProjectDelete.as_view() , name="project_delete"),
    path('<str:id>/edit', edit_project_rating, name="edit_project_rating"),
    path('<str:project_id>/comment', add_comment, name="add_comment"),
    path('<str:project_id>/<comment_id>/reply', add_reply_on_comment, name="add_reply_on_comment"),
    # path('<uuid:project_id>', views.project_details, name='project_details'),
    path('', views.index, name='index'),
]


