from django import forms
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from .models import Project, ProjectMember, Phase, Unit, Task, TaskAssignment

class ProjectCreateForm(forms.ModelForm):
    KIND_CHOICES = [
        ('Web', 'Web'),
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
    ]
    project_name = forms.CharField(label='Project Name', required=True)
    project_description = forms.CharField(label='Project Description', widget=forms.Textarea, required=False)
    project_kind = forms.ChoiceField(
        label='Kind of Project',
        choices=KIND_CHOICES,
        initial=2,
        required=True,
        widget=forms.Select(attrs={'id': 'one',}))
    start_day = forms.DateField(
        label='Project Start Day',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True)
    dead_line = forms.DateField(
        label='Project Deadline',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True)

    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'project_kind', 'start_day', 'dead_line',]

    def clean_project_deadline(self):
        dead_line = self.cleaned_data.get('dead_line')
        if not dead_line:
            raise forms.ValidationError('Project deadline is required.')
        return dead_line

class PhaseCreateForm(forms.ModelForm):
    phase_name = forms.CharField(label='Phase Name', required=True)
    phase_description = forms.CharField(label='Project Description', widget=forms.Textarea, required=False)
    start_day = forms.DateField(
        label='Phase Start Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True)
    dead_line = forms.DateField(
        label='Phase Deadline',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True)

    class Meta:
        model = Phase
        fields = ['phase_name', 'phase_description','start_day' ,'dead_line']

class UnitCreateForm(forms.ModelForm):
    unit_name = forms.CharField(label='Unit Name', required=True)
    unit_description = forms.CharField(label='Unit Description', widget=forms.Textarea, required=False)
    start_day = forms.DateField(
        label='Unit Start Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True)
    dead_line = forms.DateField(
        label='Unit Deadline',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True)

    class Meta:
        model = Unit
        fields = ['unit_name', 'unit_description', 'start_day','dead_line']

class TaskCreateForm(forms.ModelForm):
    task_name = forms.CharField(label='Task Name', required=True)
    task_description = forms.CharField(label='Task Description', widget=forms.Textarea, required=False)
    start_day = forms.DateField(
        label='Task Start Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False)
    dead_line = forms.DateField(
        label='Task Deadline',
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
                empty_label="Select"
            )

class InviteUserForm(forms.Form):
    email = forms.EmailField(label='Email Address', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
