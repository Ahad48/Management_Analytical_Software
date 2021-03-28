from django.forms import ModelForm, DateInput
from .models import Project, Job


class AddProjectDetails(ModelForm):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'number_of_days', 'number_of_employees', 'number_of_units', 'budget',
                  'productivity']


class DateInput(DateInput):
    input_type = 'date'


class AddJobDetails(ModelForm):
    class Meta:
        model = Job
        fields = ['Project_id', 'Task', 'job_desc', 'Start', 'Finish', 'status']
        widgets = {
            'Start': DateInput(),
            'Finish': DateInput(),
        }
