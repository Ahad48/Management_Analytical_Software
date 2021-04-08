import django_filters
from .models import *


class ShowGanttChart(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['Project_id', ]

    def __int__(self, *args, **kwargs):
        super(ShowGanttChart, self).__init__(*args, **kwargs)
        if self.data == {[]}:
            self.queryset = self.queryset.none()