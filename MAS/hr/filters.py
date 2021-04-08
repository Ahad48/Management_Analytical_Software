import django_filters
from .models import *


class ShowSkillChart(django_filters.FilterSet):
    class Meta:
        model = EmployeeSkillChart
        fields = ['Employee_id', ]
        