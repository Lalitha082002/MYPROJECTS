
from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            'company_name',
            'job_role',
            'location',
            'job_type',
            'salary',
            'application_date',
            'status',
            'description',
            'interview_date',
        ]
