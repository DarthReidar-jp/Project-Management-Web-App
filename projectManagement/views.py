from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Phase, ProjectMember, Unit, Task, TaskAssignment
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F, Sum
import json,string
from django.core import serializers
from django.utils import timezone
import string,random
from .forms import ProjectCreateForm,PhaseCreateForm,UnitCreateForm,TaskCreateForm
from django.forms import formset_factory

#開発用初期画面
def welcome_view(request):
    return render(request, 'welcome.html')

# プロジェクト一覧表示機能
def project_list(request):
    if request.method == 'GET':
        search_option = request.GET.get('search')
        sort_option = request.GET.get('sort')

        projects = Project.objects.all()

        # 検索オプションが指定された場合は、プロジェクト名でフィルタリング
        if search_option:
            projects = projects.filter(project_name__icontains=search_option)

        # ソートオプションに基づいてプロジェクトを並び替え
        if sort_option == 'created':
            projects = projects.order_by('created_at')
        elif sort_option == 'updated':
            projects = projects.order_by('-updated_at')
        elif sort_option == 'name':
            projects = projects.order_by('project_name')

        project_data = []
        for project in projects:
            # 進捗の計算
            total_tasks = 0
            completed_tasks = 0
            for phase in project.phases.all():
                for unit in phase.units.all():
                    tasks = unit.tasks.all()
                    total_tasks += tasks.count()
                    completed_tasks += tasks.filter(is_completed_task=True).count()

            progress = 0
            if total_tasks > 0:
                progress = completed_tasks / total_tasks * 100

            project_info = {
                'project': project,
                'progress': progress,
                'deadline': project.dead_line,
                'priority': project.priority,
                'total_work_hours': total_tasks * 10,  # 1タスクあたり10時間と仮定
                'responsible': project.responsible,
                'project_kind': project.project_kind,
            }
            project_data.append(project_info)

        context = {
            'projects': project_data,
            'search_option': search_option,
            'sort_option': sort_option,
        }

        return render(request, 'project_list.html', context)

    return JsonResponse({'success': False, 'message': '無効なリクエストメソッドです。'})

# プロジェクト削除機能
@csrf_exempt
def project_delete(request, project_id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'プロジェクトが存在しません。'})

    return JsonResponse({'success': False, 'message': '無効なリクエストメソッドです。'})

@login_required
def project_join(request):
    invitation_id = request.GET.get('invitation_id')  # これでinvitation_idを取得
    if request.method == 'POST' and invitation_id is not None:
        project = Project.objects.filter(invitation_id=invitation_id).first()
        if project is not None:
            ProjectMember.objects.create(user=request.user, project=project, role='member')
        return redirect('project_list')
        
    elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if invitation_id is not None:
            project = Project.objects.filter(invitation_id=invitation_id).first()
            if project is not None:
                return JsonResponse({'project': {
                    'name': project.project_name,
                    'responsible': project.responsible.username
                }})
            else:
                return JsonResponse({'project': None})
        else:
            return JsonResponse({'error': 'No invitation ID provided'}, status=400)
    else:
        return render(request, 'project_join.html')

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            print("Project deadline:", form.cleaned_data['dead_line'])
            project = form.save(commit=False)
            project.responsible = request.user

            # ランダムな招待IDを生成
            invitation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            project.invitation_id = invitation_id

            project.save()
            print("Saved project deadline:", Project.objects.last().dead_line)

            # プロジェクト作成者をメンバーとして追加
            ProjectMember.objects.create(
                user=request.user,
                project=project,
                role='manager'
            )

            return redirect('project_list')  # 作成後にプロジェクト一覧ページにリダイレクト

    else:
        form = ProjectCreateForm()

    return render(request, 'project_create.html', {'form': form})

#プロジェクト編集機能
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = ProjectCreateForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectCreateForm(instance=project)
        
    context = {
        'form': form,
    }
    return render(request, 'project_edit.html', context)

#フェーズ一覧表示機能
def phase_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    phases = project.phases.order_by('start_day')

    context = {
        'project': project,
        'phases': phases,
    }
    return render(request, 'phase_list.html', context)

#フェーズ作成機能（未完成）
def phase_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = PhaseCreateForm(request.POST or None)
    if form.is_valid():
        phase = form.save(commit=False)
        phase.project = project
        phase.save()

        # プロジェクト詳細画面にリダイレクト
        return redirect('phase_list', project_id=project_id)

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'phase_create.html', context)

#フェーズ編集機能
def phase_edit(request, project_id, phase_id):
    phase = get_object_or_404(Phase, id=phase_id)

    if request.method == 'POST':
        form = PhaseCreateForm(request.POST, instance=phase)
        if form.is_valid():
            form.save()
            return redirect('unit_list', project_id=project_id, phase_id=phase_id)
    else:
        form = PhaseCreateForm(instance=phase)
        
    context = {
        'form': form,
    }
    return render(request, 'phase_edit.html', context)


#ユニット一覧表示機能
def unit_list(request, project_id, phase_id):
    phase = get_object_or_404(Phase, id=phase_id)
    project = phase.project
    return render(request, 'unit_list.html', {'phase': phase, 'project': project})

#ユニット作成機能
def unit_create(request, project_id, phase_id):
    phase = get_object_or_404(Phase, pk=phase_id)
    project = get_object_or_404(Project, pk=project_id)

    TaskFormSet = formset_factory(TaskCreateForm, extra=1)
    if request.method == 'POST':
        form = UnitCreateForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.phase = phase
            unit.start_day = date.today()
            unit.save()

            i = 1
            while True:
                task_name = request.POST.get(f'task_name_{i}')
                task_description = request.POST.get(f'task_description_{i}')
                task_deadline = request.POST.get(f'task_deadline_{i}')
                start_day = date.today()

                if not task_name and not task_description and not task_deadline:
                    break

                if task_name:  # Only create task if name is present
                    Task.objects.create(
                        unit=unit,
                        task_name=task_name,
                        task_description=task_description,
                        dead_line=task_deadline,
                        start_day=start_day
                    )
                i += 1

            return redirect('unit_list', project_id=project_id, phase_id=phase_id)


    else:
        form = UnitCreateForm()

    context = {
        'form': form,
        'phase': phase,
        'project_id': project_id,
        'phase_id': phase_id,
    }

    return render(request, 'unit_create.html', context)

#
def unit_edit(request, project_id, phase_id, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    if request.method == 'POST':
        form = UnitCreateForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list', project_id=project_id, phase_id=phase_id)
    else:
        form = UnitCreateForm(instance=unit)

    context = {
        'form': form,
    }

    return render(request, 'unit_edit.html', context)

#タスク詳細表示機能
def task_detail(request, project_id, phase_id, unit_id, task_id):
    task = get_object_or_404(Task, id=task_id)

    context = {
        'project_id': project_id,
        'phase_id': phase_id,
        'unit_id': unit_id,
        'task': task
    }

    return render(request, 'task_detail.html', context)

#タスク作成機能
def task_create(request, project_id, phase_id, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    if request.method == 'POST':
        form = TaskCreateForm(request.POST, project_id=project_id)
        if form.is_valid():
            task = form.save(commit=False)
            task.unit = unit
            task.start_day = date.today()
            task.save()
            
            task_assignment = TaskAssignment.objects.create(
                task=task,
                project_member=form.cleaned_data.get('task_member') or request.user
            )
            
            return redirect('unit_list', project_id=project_id, phase_id=phase_id)
    else:
        form = TaskCreateForm(project_id=project_id)

    return render(request, 'task_create.html', {'form': form, 'project_id': project_id, 'phase_id': phase_id, 'unit_id': unit_id})

#タスク編集機能(未完成)
def task_edit(request):
    return render(request, 'task_edit.html')
