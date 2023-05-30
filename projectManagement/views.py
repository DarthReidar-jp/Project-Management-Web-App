from django.shortcuts import render, redirect, get_object_or_404
from .models import Project,Phase,ProjectMember
from datetime import date

def welcome_view(request):
    return render(request, 'welcome.html')

# プロジェクト一覧
def home(request):
    projects = Project.objects.all()
    project_data = []
    #プロジェクト内の総タスクのカウント
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

#プロジェクトの作成
def project_create(request):
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

    return render(request, 'project_create.html')

#プロジェクト詳細画面
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    phases = project.phases.order_by('dead_line')

    context = {
        'project': project,
        'phases': phases,
    }
    return render(request, 'project_detail.html', context)

#プロジェクト編集
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Handle project editing logic here

    context = {
        'project': project,
    }
    return render(request, 'project_edit.html', context)

#フェーズ作成
def phase_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        phase_name = request.POST['phase_name']
        phase_description = request.POST['phase_description']
        phase_deadline = request.POST['phase_deadline']
        start_day = date.today()  # 今日の日付を使用する例

        phase = Phase.objects.create(
            project=project,
            phase_name=phase_name,  # フィールド名を修正
            phase_description=phase_description,  # フィールド名を修正
            start_day=start_day,  # start_dayの値を設定
            dead_line=phase_deadline  # フィールド名を修正
        )

    # プロジェクト詳細画面にリダイレクト
        return redirect('project_detail', project_id=project_id)
        # Handle further actions or redirects

    context = {
        'project': project
    }

    return render(request, 'phase_create.html', context)

# フェーズ編集
def phase_edit(request, project_id, phase_id):
    phase = get_object_or_404(Phase, id=phase_id)
    project = phase.project
    return render(request, 'phase_edit.html', {'phase': phase, 'project': project})

# フェーズ詳細
def phase_detail(request, project_id, phase_id):
    phase = get_object_or_404(Phase, id=phase_id)
    project = phase.project
    return render(request, 'phase_detail.html', {'phase': phase, 'project': project})

# ユニット作成
def unit_create(request):
    return render(request, 'unit_create.html')

# ユニット編集
def unit_edit(request):
    return render(request, 'unit_edit.html')

# タスク詳細
def task_detail(request):
    return render(request, 'task_detail.html')

# タスク作成
def task_create(request):
    return render(request, 'task_create.html')

# タスク編集
def task_edit(request):
    return render(request, 'task_edit.html')
