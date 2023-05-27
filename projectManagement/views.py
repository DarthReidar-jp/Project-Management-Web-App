from django.shortcuts import render, redirect
from .models import Project

# プロジェクト一覧
from django.shortcuts import render
from .models import Project

def home(request):
    projects = Project.objects.all()
    project_data = []
    for project in projects:
        total_tasks = 0
        completed_tasks = 0
        for phase in project.phases.all():
            for unit in phase.units.all():
                tasks = unit.tasks.all()
                total_tasks += tasks.count()
                completed_tasks += tasks.filter(is_completed_task=True).count()

        # Calculate progress percentage
        progress = 0
        if total_tasks > 0:
            progress = completed_tasks / total_tasks * 100

        # Calculate total work hours
        total_work_hours = '未定'
        if total_tasks > 0:
            total_work_hours = total_tasks * 10  # Assuming each task takes 10 hours

        project_info = {
            'project': project,
            'progress': progress,
            'deadline': project.dead_line,
            'priority': project.priority,
            'total_work_hours': total_work_hours,
            'responsible': project.responsible,
            'project_kind': project.project_kind,
        }
        project_data.append(project_info)

    context = {
        'projects': project_data,
    }
    return render(request, 'home.html', context)





def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        invite_email = request.POST.get('invite_email')
        invite_role = request.POST.get('invite_role')
        project_deadline = request.POST.get('project_deadline')
        project_priority = request.POST.get('project_priority')
        project_leader_email = request.POST.get('project_leader_email')
        project_leader_role = request.POST.get('project_leader_role')
        project_status = request.POST.get('project_status')

        # プロジェクトをデータベースに保存
        project = Project.objects.create(
            project_name=project_name,
            project_description=project_description,
            project_kind=project_status,
            responsible=request.user,
            priority=project_priority,
            dead_line=project_deadline
        )

        # プロジェクトメンバーの招待情報を保存
        # invite_emailとinvite_roleを使って招待情報を保存する処理を実装してください

        # プロジェクト責任者情報を保存
        # project_leader_emailとproject_leader_roleを使ってプロジェクト責任者情報を保存する処理を実装してください

        return redirect('home')  # 作成後にプロジェクト一覧ページにリダイレクト

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
