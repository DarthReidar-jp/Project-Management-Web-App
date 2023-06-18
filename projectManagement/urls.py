from django.urls import path
from . import views


urlpatterns = [
    # プロジェクト系
    path('project_list/', views.project_list, name='project_list'),  # プロジェクト一覧画面
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),  # プロジェクト削除
    path('projects/create/', views.project_create, name='project_create'),  # プロジェクト作成画面
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),  # プロジェクト編集画面

    # フェーズ系<int:project_id>
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),  # フェーズ一覧画面
    path('projects/<int:project_id>/phases/create/', views.phase_create, name='phase_create'),  # フェーズ作成画面
    path('projects/<int:project_id>/phases/<int:phase_id>/edit/', views.phase_edit, name='phase_edit'),  # フェーズ編集画面

    # ユニット系
    path('projects/<int:project_id>/phases/<int:phase_id>/', views.phase_detail, name='phase_detail'),  # ユニット一覧画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/create/', views.unit_create, name='unit_create'),  # ユニット作成画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/edit/', views.unit_edit, name='unit_edit'),  # ユニット編集画面

    # タスク系
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),  # タスク詳細画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/create/', views.task_create, name='task_create'),  # タスク作成画面
    path('projects/<int:project_id>/phases/<int:phase_id>/units/<int:unit_id>/tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),  # タスク詳細編集画面
]
