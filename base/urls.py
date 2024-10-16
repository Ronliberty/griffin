from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import profile_view, edit_profile_view


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('available-projects/', views.available_projects, name='available_projects'),
    path('projects/accept/<int:project_id>/', views.accept_project, name='accept_project'),
    path('ongoing-projects/', views.ongoing_projects, name='ongoing_projects'),
    path('complete-project/<int:project_id>/', views.complete_project, name='complete_project'),
    path('work-history/', views.work_history, name='work_history'),
    path('profile/', views.profile_view, name='profile'),  # For viewing profile
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),

]
