"""MAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from login import views as user_views
from django.conf import settings
from django.contrib.auth import views as auth_views
from hr import views as hr_views
from operations import views as op_views
from marketing import views as mk_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path("sign_in/", auth_views.LoginView.as_view(template_name="login/sign_in.html"), name='sign_in'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path("Add_Employee_Skill/", hr_views.AddEmployeeSkillScoreView.as_view(), name="add_employee_skill"),
    path("view_skill_chart/", hr_views.generate_skill_chart, name='view_skill_chart'),
    path("show_gantt_chart/", op_views.show_gantt_chart, name='show_gantt_chart'),
    path("add_emp_form/", hr_views.AddEmployeesView.as_view(), name="add_emp_form"),
    path("sentiment/", mk_views.get_company, name="sentiment"),
    path("add_project/", op_views.AddProjectDetailsView.as_view(), name="add_project"),
    path("add_job/", op_views.AddJobDetailsView.as_view(), name="add_job"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
