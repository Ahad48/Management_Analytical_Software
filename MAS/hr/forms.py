from django.forms import ModelForm
from .models import EmployeeSkillChart, Employee


class AddEmployeeSkillScore(ModelForm):
    class Meta:
        model = EmployeeSkillChart
        fields = ['Employee_id', 'technology', 'growth', 'ideas', 'skill', 'vision', 'problem_solving']


class AddEmployee(ModelForm):
    class Meta:
        model = Employee
        fields = ['department_name', 'employee_id', 'employee_name', 'performance_score', 'error', 'comments']
