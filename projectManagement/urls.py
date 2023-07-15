from . import views
from django.urls import path
from .views import ProjectMembersView

urlpatterns = [

    #notifications
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),

    #invite projects
    path('invite-user/<int:project_id>/', views.invite_user, name='invite_user'),#未完成
    path('invitation/<str:invitation_code>/', views.project_invitation, name='project_invitation'),#未完成
    path('invitation_login/<str:invitation_code>/', views.invitation_login, name='invitation_login'),#未完成
    path('invitation_signup/<str:invitation_code>/', views.invitation_signup, name='invitation_signup'),#未完成

    #join projects
    path('projects/search/', views.project_search, name='project_search'),
    path('projects/join/<int:project_id>/', views.project_join, name='project_join'),
    
    #project type
    path('projects/list/', views.project_list, name='project_list'), 
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'), 
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('toggle_favorite/<int:project_id>/', views.toggle_favorite, name='toggle_favorite'),

    #phase type <int:project_id>
    path('<int:project_id>/', views.phase_list, name='phase_list'),
    path('<int:project_id>/phases/create/', views.phase_create, name='phase_create'), 
    path('<int:project_id>/phases/<int:phase_id>/edit/', views.phase_edit, name='phase_edit'),
    path('<int:project_id>/phase/<int:phase_id>/delete/', views.phase_delete, name='phase_delete'),

    #unit type <project_id><phase_id>
    path('<int:project_id>/phases/<int:phase_id>/', views.unit_list, name='unit_list'),
    path('<int:project_id>/phases/<int:phase_id>/units/create/', views.unit_create, name='unit_create'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/edit/', views.unit_edit, name='unit_edit'),
    path('<int:project_id>/phases/<int:phase_id>/unit/<int:unit_id>/delete/', views.unit_delete, name='unit_delete'),

    #task type <project_id><phase_id><unit_id>
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/create/', views.task_create, name='task_create'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/task_toggle/', views.task_toggle, name='task_toggle'),

    path('api/project-members/<int:project_id>/', ProjectMembersView.as_view(), name='project-members'),
]
