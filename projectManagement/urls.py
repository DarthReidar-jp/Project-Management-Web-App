from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('account/create/', views.account_create, name='account_create'),
    path('projects/', views.project_list, name='project_list'),
    path('account/password_reset/', views.password_reset, name='password_reset'),
    path('projects/<int:project_id>/manager', views.project_detail_manager, name='project_detail_manager'),
    path('projects/<int:project_id>/phases/<int:phase_id>/worker/', views.phase_detail_worker, name='phase_detail_worker'),
    path('projects/create/', views.create_project, name='create_project'),
    path('account/create/complete/', views.account_create_complete, name='account_create_complete'),
    path('account/password_reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/phases/create/', views.create_phase, name='create_phase'),
    path('account/settings/e-mail-edit-link/', views.email_edit, name='email_edit'),
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/edit/', views.edit_unit, name='edit_unit'),
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/create/', views.create_task, name='create_task'),
    path('projects/<int:project_id>/phases/<int:phase_id>/units/create/', views.create_unit, name='create_unit'),
    path('account/settings/e-mail-edit/complete/', views.email_edit_complete, name='email_edit_complete'),
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('projects/<int:project_id>/phases/<int:phase_id>/edit/', views.edit_phase, name='edit_phase'),
]
