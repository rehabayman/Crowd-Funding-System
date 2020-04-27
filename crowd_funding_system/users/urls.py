from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_user, login_user, logout_user, activate_user
from .views import ProfileUpdate, UserDelete, test_home, show, show_projects, show_donations
from django.urls import path, reverse_lazy

app_name="users"
urlpatterns=[
    
    path("register/", register_user, name="users_register"),
    path("login/", login_user, name="users_login"),
    path("logout/", logout_user, name="users_logout"),
    path("activate/<active>/<user_id>", activate_user, name="user_activation"),

    path('edit',ProfileUpdate.as_view() , name="edit_profile_url"),
    path('delete',UserDelete.as_view() , name="delete_user_url"),
    # this url for testing
    path('/', test_home,name="home"),
    path('<str:id>/projects', show_projects, name="user_projects"),
    path('<str:id>/donations', show_donations, name="user_donations"),
    path('<str:id>', show, name="user_details"),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name= './users/password_reset_form.html', 
        success_url=reverse_lazy('users:password_reset_done'), 
        subject_template_name='./users/password_reset_subject.txt', 
        email_template_name="./users/password_reset_email.html"),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name= './users/password_reset_done.html'), 
        name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name= './users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name= './users/password_reset_complete.html'), 
        name='password_reset_complete'),
    
]

