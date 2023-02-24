from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/student/', include('student.urls')),
    path('api/employee/', include('employee.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]