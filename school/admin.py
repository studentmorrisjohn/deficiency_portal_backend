from django.contrib import admin
from school.models import EmployeeProfile, StudentProfile, College, Department, Organization, Membership
# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(StudentProfile)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Organization)
admin.site.register(Membership)