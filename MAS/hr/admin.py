from django.contrib import admin
from hr.models import Department, Employee, Attendance, EmployeeSkillChart


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['Department_id', 'Department_name']

    def get_queryset(self, request):
        queryset = super(DepartmentAdmin, self).get_queryset(request)
        return queryset


admin.site.register(Department, DepartmentAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name', 'department_name', 'performance_score', 'error', 'comments']

    def get_queryset(self, request):
        queryset = super(EmployeeAdmin, self).get_queryset(request)
        return queryset


admin.site.register(Employee, EmployeeAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['Employee_id', 'attendance', 'date']


admin.site.register(Attendance, AttendanceAdmin)


class EmployeeSkillChartAdmin(admin.ModelAdmin):
    list_display = ['Employee_id', 'technology', 'growth', 'ideas', 'skill', 'vision', 'problem_solving']


admin.site.register(EmployeeSkillChart, EmployeeSkillChartAdmin)
