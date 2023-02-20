from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/student/', include('student.urls')),
    path('api/employee/', include('employee.urls')),
    path('admin/', admin.site.urls),
]
