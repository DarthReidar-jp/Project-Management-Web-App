from django.urls import path
from . import views


urlpatterns = [

    path('notifications/', views.notification_list, name='notification_list'),
     path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    # project type
    path('projects/list/', views.project_list, name='project_list'), 
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'), 
    path('projects/join/', views.project_join, name='project_join_without_id'),
    path('projects/join/<str:invitation_id>/', views.project_join, name='project_join'),#chesck Project join screen 
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),

    # phase type <int:project_id>
    path('<int:project_id>/', views.phase_list, name='phase_list'),
    path('<int:project_id>/phases/create/', views.phase_create, name='phase_create'), 
    path('<int:project_id>/phases/<int:phase_id>/edit/', views.phase_edit, name='phase_edit'),

    # unit type <project_id><phase_id>
    path('<int:project_id>/phases/<int:phase_id>/', views.unit_list, name='unit_list'),
    path('<int:project_id>/phases/<int:phase_id>/units/create/', views.unit_create, name='unit_create'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/edit/', views.unit_edit, name='unit_edit'),

    # task type <project_id><phase_id><unit_id>
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/create/', views.task_create, name='task_create'),
    path('<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    # タスクの完了・未完了を切り替える新しいパス
    path('task_toggle/<int:project_id>/<int:phase_id>/<int:unit_id>/<int:task_id>/', views.task_toggle, name='task_toggle'),
]
