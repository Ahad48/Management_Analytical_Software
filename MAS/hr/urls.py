from django.urls import path
from . import views


urlpatterns = [
    path("Add_Employee_Skill/", views.AddEmployeeSkillScoreView.as_view(), name="add_employee_skill"),
    path("view_skill_chart/", views.generate_skill_chart, name='view_skill_chart'),
    path("add_emp_form/", views.AddEmployeesView.as_view(), name="add_emp_form"),
]