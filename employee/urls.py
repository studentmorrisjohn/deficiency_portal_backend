from django.urls import path
from employee import views
urlpatterns = [
    path('deficiency-details/<str:def_id>', views.DeficiencyDetail.as_view()),
    path('deficiency-name-list', views.DeficiencyNameList.as_view()),
    path('student-list/<str:name>', views.StudentList.as_view()),
    path('deficiency-names', views.DeficiencyNameOptions.as_view()),
    path('all-students/<str:name>', views.AllStudents.as_view()),
    path('profile', views.EmployeeProfileView.as_view())
]
