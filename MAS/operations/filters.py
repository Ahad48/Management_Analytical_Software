import django_filters
from .models import *


class ShowGanttChart(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['Project_id', ]