from django.urls import path

from .views import register_user, login_user, logout_user
from .views import ProfileUpdate, UserDelete, test_home, show, show_projects, show_donations


app_name="users"
urlpatterns=[
    
    path("register/", register_user, name="users_register"),
    path("login/", login_user, name="users_login"),
    path("logout/", logout_user, name="users_logout"),

    path('<id>/edit',ProfileUpdate.as_view() , name="edit_profile_url"),
    path('<id>/delete',UserDelete.as_view() , name="delete_user_url"),
    # this url for testing
    path('/', test_home,name="home"),
    path('<str:id>/projects', show_projects, name="user_projects"),
    path('<str:id>/donations', show_donations, name="user_donations"),
    path('<str:id>', show, name="user_details"),
]

