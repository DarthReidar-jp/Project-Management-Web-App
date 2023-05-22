from django.contrib import admin
from .models import Project,ProjectMember,Phase,Unit,Task,TaskAssignment

admin.site.register(Project) #追記
admin.site.register(ProjectMember) 
admin.site.register(Phase) 
admin.site.register(Unit) 
admin.site.register(Task) 
admin.site.register(TaskAssignment) 
# Register your models here.
