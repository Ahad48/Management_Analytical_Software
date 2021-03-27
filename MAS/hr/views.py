from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import AddEmployeeSkillScore, AddEmployee
from .models import *
import plotly.graph_objects as go


class AddEmployeeSkillScoreView(CreateView):
    model = EmployeeSkillChart
    form_class = AddEmployeeSkillScore
    success_url = reverse_lazy('view_skill_chart')
    template_name = "hr/add_skill_form.html"


def generate_skill_chart(request):
    categories = ['Technology Know How', 'Growth', 'Ideas', 'Skills', 'Vision', 'Problem Solving']
    emp = EmployeeSkillChart.objects.all()
    fig = go.Figure()

    for i in emp:
        employee_id = i.Employee_id
        employee = Employee.objects.get(employee_id=employee_id)

        fig.add_trace(go.Scatterpolar(
            r=[i.technology, i.growth, i.ideas, i.skill, i.vision, i.problem_solving],
            theta=categories,
            fill='toself',
            name=employee.employee_name
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],

            )),
        showlegend=True
    )
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, "hr/trial.html", context={'graph': graph})


class AddEmployeesView(CreateView):
    model = Employee
    form_class = AddEmployee
    success_url = reverse_lazy('add_emp_form')
    template_name = "hr/add_emp_form.html"
