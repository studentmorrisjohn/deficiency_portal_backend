from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        STUDENT = "STUDENT", "Student"
        EMPLOYEE = "EMPLOYEE", "Employee"

    base_role = Role.ADMIN
    base_is_staff = True

    role = models.CharField(max_length=55, choices=Role.choices)
    is_staff = models.BooleanField(default=False)
    
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=55, null=True, blank=True)
    birth_date = models.DateField(default=None, null=True, blank=True)
    mobile_number = models.CharField(max_length=55, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            self.is_staff = self.base_is_staff
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)
    
    @property
    def name(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}"

class Student(User):
    base_role = User.Role.STUDENT
    base_is_staff = False

    class Meta:
        proxy = True

class Employee(User):
    base_role = User.Role.EMPLOYEE
    base_is_staff = True

    class Meta:
        proxy = True

class UploadTask(models.Model):
    file_name = models.CharField(max_length=100)
    done_uploading = models.BooleanField(default=False)
    job_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    csv_generated = models.BooleanField(default=False)
    csv_filename = models.CharField(max_length=100, default=None, null=True, blank=True)
    failed = models.BooleanField(default=False)

    def __str__(self):
        status_message = f"is being uploaded with a job id {self.job_id}" if not self.done_uploading else "is done uploading. Download the email list"
        if self.failed:
            status_message = "has failed uploading"
        return f"The file {self.file_name}  {status_message}"