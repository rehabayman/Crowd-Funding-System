from django.urls import path
from .views import ProfileUpdate, UserDelete, test_home
app_name="users"
urlpatterns=[
    path('<id>/edit',ProfileUpdate.as_view() , name="edit_profile_url"),
    path('<id>/delete',UserDelete.as_view() , name="delete_user_url"),
    # this url for testing
    path('/', test_home,name="home")
]