from django.urls import path
from . import views

urlpatterns = [
    #プロジェクト系
    #プロジェクト一覧画面
    path('home/', views.home, name='home'),
    #プロジェクト作成画面
    path('projects/create/', views.project_create, name='project_create'), 
    #プロジェクト編集画面
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    
    #フェーズ系<int:project_id>
    #プロジェクト詳細画面
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    #フェーズ作成画面
    path('projects/<int:project_id>/phases/create/', views.phase_create, name='phase_create'),
    #フェーズ編集画面
    path('projects/<int:project_id>/phases/<int:phase_id>/edit/', views.phase_edit, name='phase_edit'),

    #ユニット系
    #フェーズ詳細画面
    path('projects/<int:project_id>/phases/<int:phase_id>/', views.phase_detail, name='phase_detail'),
    #ユニット作成画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/create/', views.unit_create, name='unit_create'),
    #ユニット編集画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/edit/', views.unit_edit, name='unit_edit'),

    #タスク系
    #タスク詳細画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    #タスク作成画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/create/', views.task_create, name='task_create'),
    #タスク詳細編集画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    ]

