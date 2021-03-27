from django.contrib import admin
from operations.models import Job, Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'number_of_days', 'number_of_employees', 'number_of_units', 'budget',
                    'productivity')

    def get_queryset(self, request):
        queryset = super(ProjectAdmin, self).get_queryset(request)
        return queryset


admin.site.register(Project, ProjectAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('Project_id', 'Task', 'job_desc', 'Start', 'Finish', 'status')


admin.site.register(Job, JobAdmin)