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
    project_deadline = forms.DateField(label='プロジェクト期限', widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}), required=True, input_formats=['%Y-%m-%d'])
    project_priority = forms.ChoiceField(label='プロジェクトの優先度設定', choices=PRIORITY_CHOICES, required=True)

    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'project_kind', 'project_deadline', 'project_priority']

    def clean_project_priority(self):
        priority = self.cleaned_data.get('project_priority')
        if not priority:
            raise forms.ValidationError('プロジェクト期限は必須です。')
        return int(priority)

    def clean_project_deadline(self):
        dead_line = self.cleaned_data['project_deadline']
        if not dead_line:
            raise forms.ValidationError('プロジェクト期限は必須です。')
        return dead_line