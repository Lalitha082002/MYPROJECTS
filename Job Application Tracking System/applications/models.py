from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    company_name = models.CharField(max_length=100)

    job_role = models.CharField(max_length=100)

    location = models.CharField(max_length=100)

    job_type = models.CharField(max_length=50)

    salary = models.CharField(max_length=50, blank=True)

    application_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    description = models.TextField(blank=True)

    interview_date = models.DateField(null=True, blank=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.company_name + " - " + self.job_role