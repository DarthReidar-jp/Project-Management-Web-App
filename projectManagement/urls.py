from django.urls import path
from . import views

urlpatterns = [
    #アカウント画面系URL
    #ログイン画面
    #path('login/', views.login, name='login'),
    ]
'''#アカウント作成画面
    path('account/create/', views.account_create, name='account_create'),
    #アカウント作成完了画面
    path('account/create/complete/', views.account_create_complete, name='account_create_complete'),
    #アカウント再設定リンク画面
    path('account/settings/e-mail-edit-link/', views.email_edit, name='email_edit'),
    #アカウント再設定完了画面
    path('account/settings/e-mail-edit/complete/', views.email_edit_complete, name='email_edit_complete'),
    #パスワードリセット画面
    path('account/password_reset/', views.password_reset, name='password_reset'),
    #パスワード再設定完了画面
    path('account/password_reset/complete/', views.password_reset_complete, name='password_reset_complete'),
   
    
    #プロジェクト系
    #プロジェクト一覧画面
    path('projects/', views.project_list, name='project_list'),
    #プロジェクト作成画面
    path('projects/create/', views.create_project, name='create_project'), 
    #プロジェクト編集画面
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    
    #フェーズ系
    #フェーズ一覧画面
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
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
    '''
