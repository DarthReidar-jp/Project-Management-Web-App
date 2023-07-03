from django.contrib import admin
from .models import Project, ProjectMember, Phase, Unit, Task, TaskAssignment,Notification

class NotificationInline(admin.TabularInline):
    model = Notification

class TaskAssignmentInline(admin.TabularInline):
    model = TaskAssignment

class TaskInline(admin.TabularInline):
    model = Task

class UnitInline(admin.TabularInline):
    model = Unit
    inlines = [TaskInline]

class PhaseInline(admin.TabularInline):
    model = Phase
    inlines = [UnitInline]

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'responsible', 'priority', 'is_completed_project']
    list_filter = ['is_completed_project']
    inlines = [ProjectMemberInline, PhaseInline]
    list_per_page = 10
    list_select_related = ['responsible']

class PhaseAdmin(admin.ModelAdmin):
    list_display = ['phase_name', 'project', 'start_day', 'dead_line', 'is_completed_phase']
    list_filter = ['project']
    inlines = [UnitInline]
    list_per_page = 10
    list_select_related = ['project']

class UnitAdmin(admin.ModelAdmin):
    list_display = ['unit_name', 'phase', 'start_day', 'dead_line', 'is_completed_unit']
    list_filter = ['phase']
    inlines = [TaskInline]
    list_per_page = 10
    list_select_related = ['phase__project']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'unit', 'start_day', 'dead_line', 'is_completed_task']
    list_filter = ['unit']
    list_per_page = 10
    list_select_related = ['unit__phase__project']

class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ['task', 'project_member', 'is_completed_member']
    list_filter = ['task']
    list_per_page = 10
    list_select_related = ['task__unit__phase__project']

class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role']
    list_filter = ['project']
    list_per_page = 10
    list_select_related = ['user', 'project']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title','notification_type', 'project','user']
    list_filter = ['project']
    list_per_page = 10

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskAssignment, TaskAssignmentAdmin)
admin.site.register(Notification,NotificationAdmin)
