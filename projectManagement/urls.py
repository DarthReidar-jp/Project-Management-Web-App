from django.urls import path
from . import views

urlpatterns = [
    #プロジェクト系
    #プロジェクト一覧画面
    path('home/', views.home, name='home'),
    #プロジェクト作成画面
    path('projects/create/', views.create_project, name='create_project'), 
    #プロジェクト編集画面
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    
    #フェーズ系<int:project_id>
    #フェーズ一覧画面
    path('projects/1/', views.project_detail, name='detail_project'),
    #フェーズ作成画面
    path('projects/<int:project_id>/phases/create/', views.create_phase, name='create_phase'),
    #フェーズ編集画面
    path('projects/<int:project_id>/phases/<int:phase_id>/edit/', views.edit_phase, name='edit_phase'),

    #ユニット系
    #ユニット一覧画面
    path('projects/<int:project_id>/phases/<int:phase_id>/', views.phase_detail, name='phase_detail'),
    #ユニット作成画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/create/', views.create_unit, name='create_unit'),
    #ユニット編集画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/edit/', views.edit_unit, name='edit_unit'),

    #タスク系
    #タスク詳細画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    #タスク作成画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/create/', views.create_task, name='create_task'),
    #タスク詳細編集画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    ]

