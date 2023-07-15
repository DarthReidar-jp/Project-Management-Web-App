import json
import string
import random
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F, Sum
from django.core import serializers
from django.utils import timezone
from django.forms import formset_factory
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from .models import Project, Phase, ProjectMember, Unit, Task, TaskAssignment, Notification,FavoriteProject
from .forms import ProjectCreateForm,PhaseCreateForm,UnitCreateForm,TaskCreateForm,InviteUserForm

#開発用初期画面（削除予定）
def welcome_view(request):
    return render(request, 'welcome.html')

#通知リスト機能(未完成)
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notification_list.html', {'notifications': notifications})

#通知詳細表示機能（未完成）
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    return render(request, 'notification_detail.html', {'notification': notification})

#招待機能（未完成）
def invite_user(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = InviteUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # send email with invitation link
            send_mail(
                'プロジェクトへのご招待',
                '私たちのプロジェクトに参加してください!Please click the link below:\nhttp://localhost:8000/app/invitation_login/{}/'.format(project.invitation_code),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return render(request, 'phase_list.html')
    else:
        form = InviteUserForm()
    return render(request, 'invite_user.html', {'form': form})

#招待ユーザーのログイン(未完成)
def invitation_login(request, invitation_code):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('project_invitation', invitation_code=invitation_code)  # 招待URLにリダイレクト
        else:
            # 認証失敗時の処理
            pass
    return render(request, 'invitation_login.html')

#招待ユーザーの登録(未完成)
def invitation_signup(request, invitation_code):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        user = User.objects.create_user(email, password)
        login(request, user)
        return redirect('project_invitation', invitation_code=invitation_code)  # 招待URLにリダイレクト
    return render(request, 'invitation_signup.html')

#招待ユーザーのプロジェクト参加（未完成）
def project_invitation(request):
    return render(request,'invitation_signup.html')

#プロジェクト一覧表示機能
@login_required
def project_list(request):
    if request.method == 'GET':
        search_option = request.GET.get('search')
        sort_option = request.GET.get('sort')

        #ログインユーザーが参加しているプロジェクトのみを表示
        user_projects = ProjectMember.objects.filter(user=request.user, status='joined').values_list('project', flat=True)
        projects = Project.objects.filter(id__in=user_projects)

        user_favorites = FavoriteProject.objects.filter(user=request.user)
        favorite_projects = [fav.project for fav in user_favorites]

        #検索オプションが指定された場合は、プロジェクト名でフィルタリング
        if search_option:
            projects = projects.filter(project_name__icontains=search_option)

        # ソートオプションに基づいてプロジェクトを並び替え
        if sort_option == 'created':
            projects = projects.order_by('created_at')
        elif sort_option == 'updated':
            projects = projects.order_by('-updated_at')
        elif sort_option == 'name':
            projects = projects.order_by('project_name')
        elif sort_option == 'favorite':
            favorite_project_ids = FavoriteProject.objects.filter(user=request.user).values_list('project', flat=True)
            projects = projects.filter(id__in=favorite_project_ids).order_by('created_at')

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
                 progress = round(completed_tasks / total_tasks * 100)

            project_info = {
                'project': project,
                'progress': progress,
                'deadline': project.dead_line,
                'responsible': project.responsible,
                'project_kind': project.project_kind,
                'is_favorite': project in favorite_projects,
            }
            project_data.append(project_info)

        context = {
            'projects': project_data,
            'search_option': search_option,
            'sort_option': sort_option,
        }

        return render(request, 'project_list.html', context)
    return JsonResponse({'success': False, 'message': '無効なリクエストメソッドです。'})

#お気に入り登録機能
@csrf_exempt
def toggle_favorite(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        favorite, created = FavoriteProject.objects.get_or_create(user=request.user, project=project)
        if not created:
            favorite.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

#プロジェクト削除機能
@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return redirect('project_list')
    
#参加プロジェクト検索機能
@login_required
def project_search(request):
    if request.method == 'GET':
        joined_id = request.GET.get('joined_id')
        try:
            project = Project.objects.get(joined_id=joined_id)
            return render(request, 'project_search.html', {'project': project})
        except Project.DoesNotExist:
            return render(request, 'project_search.html', {'message': '見つかりませんでした'})
    return JsonResponse({'success': False, 'message': '無効なリクエストメソッドです。'})

#プロジェクト参加機能
@login_required
def project_join(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        ProjectMember.objects.create(user=request.user, project=project, status='joined')
        return redirect('phase_list', project_id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'プロジェクトが存在しません。'})

#プロジェクト作成機能
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.responsible = request.user
            #ランダムな招待IDを生成
            joined_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            project.joined_id= joined_id
            project.save()

            #プロジェクト作成者をメンバーとして追加
            ProjectMember.objects.create(
                user=request.user,
                project=project,
                role='manager',
                status='joined'
            )
            return redirect('project_list')  # 作成後にプロジェクト一覧ページにリダイレクト
            #メンバーの招待機能やら責任者の設定を追加したい
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
            #招待IDの変更や確認をしたい、責任者やプロジェクトメンバーの編集もしたい
    else:
        form = ProjectCreateForm(instance=project)
        
    context = {
        'form': form,
        'project_id':project_id
    }
    return render(request, 'project_edit.html', context)

#フェーズ一覧表示
def phase_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    phases = project.phases.order_by('start_day')
    is_manager = ProjectMember.objects.filter(user=request.user, project=project, role='manager').exists()

    context = {
        'project': project,
        'phases': phases,
        'is_manager': is_manager,
    }
    return render(request, 'phase_list.html', context)

#フェーズ作成機能
def phase_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = PhaseCreateForm(request.POST)
        if form.is_valid():
            phase = form.save(commit=False)
            phase.project = project
            phase.save()
            return redirect('phase_list', project_id=project_id)
    else:
        form = PhaseCreateForm()

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'phase_create.html', context)
    
# フェーズ編集機能 
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
        'project_id': project_id,
        'phase_id': phase_id
    }
    return render(request, 'phase_edit.html', context)

#フェーズ削除
def phase_delete(request, project_id, phase_id):
    phase = get_object_or_404(Phase, id=phase_id)
    if request.method == 'POST':
        phase.delete()
        return redirect('phase_list', project_id=project_id)
    return redirect('phase_edit', project_id=project_id, phase_id=phase_id)

#ユニット一覧表示機能
def unit_list(request, project_id, phase_id):
    phase = get_object_or_404(Phase, id=phase_id)
    project = phase.project
    return render(request, 'unit_list.html', {'phase': phase, 'project': project})

#タスクの完了・未完了を切り替える新しいビュー
def task_toggle(request, project_id, phase_id, unit_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    assignment = get_object_or_404(TaskAssignment, task=task, project_member__user=request.user)
    assignment.is_completed_member = not assignment.is_completed_member
    assignment.save()
    task.save()
    return redirect('unit_list', project_id=project_id, phase_id=phase_id)

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
                task_member = request.POST.get(f'task_member_{i}')  # Get the assigned member ID
                start_day = date.today()

                if not task_name and not task_description and not task_deadline and not task_member:
                    break

                if task_name:  # Only create task if name is present
                    task = Task.objects.create(
                        unit=unit,
                        task_name=task_name,
                        task_description=task_description,
                        dead_line=task_deadline,
                        start_day=start_day
                    )
                    # Assign the member to the task
                    member = get_object_or_404(ProjectMember, pk=task_member)
                    TaskAssignment.objects.create(task=task, project_member=member)
                i += 1

            return redirect('unit_list', project_id=project_id, phase_id=phase_id)


    else:
        form = UnitCreateForm()

    context = {
        'form': form,
        'project':project,
        'phase': phase,
        'project_id': project_id,
        'phase_id': phase_id,
    }

    return render(request, 'unit_create.html', context)

#ユニット編集機能
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
        'project_id': project_id,
        'phase_id': phase_id,
        'unit_id': unit_id
    }

    return render(request, 'unit_edit.html', context)

#ユニット削除
def unit_delete(request, project_id, phase_id, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.method == 'POST':
        unit.delete()
        return redirect('unit_list', project_id=project_id , phase_id=phase_id)
    return redirect('unit_edit', project_id=project_id, phase_id=phase_id, unit_id=unit_id)

#タスク詳細表示機能
def task_detail(request, project_id, phase_id, unit_id, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = TaskCreateForm(instance=task)

    context = {
        'form': form,
        'project_id': project_id,
        'phase_id': phase_id,
        'unit_id': unit_id,
        'task_id':task_id,
    }

    return render(request, 'task_detail.html', context)

#タスク削除
def task_delete(request, project_id, phase_id, unit_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('unit_list', project_id=project_id, phase_id=phase_id)
    return redirect('task_detail', project_id=project_id, phase_id=phase_id, unit_id=unit_id, task_id=task_id)

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

class ProjectMembersView(View):
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project_members = ProjectMember.objects.filter(project_id=project_id)
        members = [{"id": pm.user.id, "name": pm.user.username} for pm in project_members]
        return JsonResponse(members, safe=False, status=200)