from django.urls import path
from . import views
from .views import user_list


urlpatterns = [
    path('', views.landing_page, name='griffin-landing'),
    path('staff/login/', views.staff_login, name='staff_login'),  # Staff login
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('create-project/', views.create_project, name='create_project'),
    path('projects/', views.project_list, name='project_list'),
    path('ongoing-projects/', views.ongoing_projects_view, name='ongoing_projects_view'),
    path('all-completed-projects/', views.all_completed_projects, name='all_completed_projects'),
    path('tasks/', views.tasks, name='tasks'),
    path('users/', user_list, name='user_list'),
]
