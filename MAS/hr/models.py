from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Department(models.Model):
    Department_name = models.CharField(max_length=30, unique=True)
    Department_id = models.CharField(max_length=10, unique=True, default="")

    def __str__(self):
        return self.Department_name


class Employee(models.Model):
    employee_id = models.CharField(max_length=10, unique=True, default="")
    employee_name = models.CharField(max_length=50)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, default="")
    performance_score = models.FloatField()
    error = models.FloatField()
    certification = models.TextField(blank=True)

    def __str__(self):
        return self.employee_id


attend = [('present', 'Present'), ('absent', 'Absent')]


class Attendance(models.Model):
    Employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, default="")
    attendance = models.CharField(max_length=8, default="", choices=attend)
    date = models.DateField(auto_now_add=True)


class EmployeeSkillChart(models.Model):
    Employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, default="")
    technology = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    growth = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    ideas = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    skill = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    vision = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    problem_solving = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])