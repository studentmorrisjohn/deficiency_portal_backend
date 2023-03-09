from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import User
# Create your models here.

class College(models.Model):
    college_abbreviation = models.CharField(max_length=10, primary_key=True)
    college_name = models.CharField(max_length=100)

    def __str__(self):
        return self.college_name

class Department(models.Model):
    department_abbreviation = models.CharField(max_length=50, primary_key=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=100, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.student_id

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.employee_id

class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Membership(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="affiliated_student")
    role = models.CharField(max_length=100, default=None)

    def __str__(self):
        return f"{self.student} is a member of {self.organization}"