from django import forms
from django.core.exceptions import ValidationError
from .models import Project,ProjectMember,Phase,Unit,Task,TaskAssignment 

class ProjectCreateForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        (1, 'high'),
        (2, 'middle'),
        (3, 'low'),
    ]
    project_name = forms.CharField(label='プロジェクト名', required=True)
    project_description = forms.CharField(label='プロジェクトの説明', widget=forms.Textarea, required=False)
    project_kind = forms.CharField(label='プロジェクト種類', required=False)
    dead_line = forms.DateField(
        label='プロジェクト期限',
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True)
    priority = forms.ChoiceField(
        label='プロジェクトの優先度設定', 
        choices=PRIORITY_CHOICES, 
        initial=2,
        required=True,
        widget=forms.Select(attrs={'id': 'one',}))

    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'project_kind', 'dead_line','priority']

    def clean_project_priority(self):
        priority = self.cleaned_data.get('priority')
        if not priority:
            raise forms.ValidationError('プロジェクト優先度は必須です。')
        return int(priority)

    def clean_project_deadline(self):
        dead_line = self.cleaned_data.get('dead_line')
        if not dead_line:
            raise forms.ValidationError('プロジェクト期限は必須です。')
        return dead_line
 
class PhaseCreateForm(forms.ModelForm):
    phase_name = forms.CharField(label='フェーズ名', required=True)
    phase_description = forms.CharField(label='プロジェクトの説明', widget=forms.Textarea, required=False)
    start_day = forms.DateField(
        label='フェーズ開始日',
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True)
    dead_line = forms.DateField(
        label='フェーズ期限',
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True)
 
    class Meta:
        model = Phase
        fields = ['phase_name', 'phase_description','start_day' ,'dead_line']

class UnitCreateForm(forms.ModelForm):
    unit_name = forms.CharField(label='ユニット名', required=True)
    unit_description = forms.CharField(label='ユニットの説明', widget=forms.Textarea, required=False)
    start_day = forms.DateField(
        label='ユニット開始日',
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True)
    dead_line = forms.DateField(
        label='ユニット期限',
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True)
    class Meta:
        model = Unit
        fields = ['unit_name', 'unit_description', 'start_day','dead_line']

class TaskCreateForm(forms.ModelForm):
    task_name = forms.CharField(label='タスク名', required=True)
    task_description = forms.CharField(label='タスクの説明', widget=forms.Textarea, required=False)
    start_day = forms.DateField(
        label='タスク開始日',
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True)
    dead_line = forms.DateField(
        label='タスク期限',
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True)
    class Meta:
        model = Task
        fields = ['task_name', 'task_description','start_day', 'dead_line']
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        if project_id:
            self.fields['task_member'] = forms.ModelChoiceField(
                queryset=ProjectMember.objects.filter(project_id=project_id),
                required=False,
                empty_label="選択してください"
            )

class InviteUserForm(forms.Form):
    email = forms.EmailField(label='Eメールアドレス', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))


