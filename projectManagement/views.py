from django.shortcuts import render

# アカウント作成
def account_create(request):
    return render(request, 'account_create.html')

# プロジェクト一覧
def project_list(request):
    return render(request, 'project_list.html')

# プロジェクト作成
def create_project(request):
    return render(request, 'create_project.html')

# プロジェクト編集
def edit_project(request):
    return render(request, 'edit_project.html')

# プロジェクト詳細
def project_detail(request):
    return render(request, 'project_detail.html')

# フェーズ詳細
def phase_detail(request):
    return render(request, 'phase_detail.html')

# フェーズ作成
def create_phase(request):
    return render(request, 'create_phase.html')

# フェーズ編集
def edit_phase(request):
    return render(request, 'edit_phase.html')

# ユニット作成
def create_unit(request):
    return render(request, 'create_unit.html')

# ユニット編集
def edit_unit(request):
    return render(request, 'edit_unit.html')

# タスク詳細
def task_detail(request):
    return render(request, 'task_detail.html')

# タスク作成
def create_task(request):
    return render(request, 'create_task.html')

# タスク編集
def edit_task(request):
    return render(request, 'edit_task.html')
