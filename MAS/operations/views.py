from django.shortcuts import render
from .models import *
from .filters import ShowGanttChart
from .forms import AddJobDetails, AddProjectDetails
import plotly.figure_factory as ff
import pandas as pd
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def show_gantt_chart(request):
    query_result = Job.objects.all().values()
    query_filter = ShowGanttChart(request.GET, queryset=query_result)
    query_results = query_filter.qs
    if request.GET.get('Search') == 'Search' and request.GET.get('Project_id') != "":
        df = pd.DataFrame(list(query_results))
        colors = {'Not Started': 'rgb(220, 0, 0)',
                  'Incomplete': 'rgb(1, 0.9, 0.16)',
                  'Complete': 'rgb(0, 255, 100)',
                  'Delayed': 'rgb(0,0,255)',
                  'not started': 'rgb(220, 0, 0)',
                  'incomplete': 'rgb(1, 0.9, 0.16)',
                  'complete': 'rgb(0, 255, 100)',
                  'delayed': 'rgb(0,0,255)',
                  }
        fig = ff.create_gantt(df, colors=colors, index_col='status', show_colorbar=True,
                              group_tasks=True)
        graph = fig.to_html(full_html=False, default_height=500, default_width=700)
        return render(request, "operations/gantt_chart.html", context={'query_filter': query_filter, 'graph': graph})
    else:
        return render(request, "operations/gantt_chart.html", context={'query_filter': query_filter})


class AddProjectDetailsView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = AddProjectDetails
    success_url = reverse_lazy('add_job')
    template_name = "operations/add_project.html"


class AddJobDetailsView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = AddJobDetails
    success_url = reverse_lazy('add_job')
    template_name = "operations/add_job.html"