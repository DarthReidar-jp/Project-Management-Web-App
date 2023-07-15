プロジェクト詳細画面
url
path('projects/<int:project_id>/', views.project_detail, name='detail_project'),

機能一覧
・ページタイトルはプロジェクト名
    ページのタイトルはプロジェクト名
    画面上にも
    左上に大きな文字で表示
・プロジェクトの編集
    画面上のページタイトルの横に編集ボタンを配置
    クリックされたらプロジェクト編集画面への移動
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
・フェーズ一覧表示
    大き目な長方形のタイルでフェーズごとに表示
    フェーズには順序がある。
    期限の早いごとに上から並ぶ。
    縦並びのみ、中央ぞろえ
・フェーズの概要表⽰
    フェーズ名
    進捗 そのフェーズ内完了タスク/そのフェーズ内の総タスク
    工数 そのフェーズ内のタスク数
    期限 
    責任者 
・フェーズの新規作成
    右のほうに正方形のタイルで
    新規作成を促すタイトルとアイコン表示
    クリックされたらプロジェクト作成画面へ移動
    path('projects/<int:project_id>/phases/create/', views.create_phase, name='create_phase'),
・フェーズ詳細画⾯へ移動
    フェーズタイトルをクリック
    フェーズ詳細画面へ移動
    クリックしたくなるようなデザイン



