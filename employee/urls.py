from django.urls import path
from employee import views
urlpatterns = [
    path('deficiency-details/<str:def_id>', views.DeficiencyDetail.as_view()),
    path('deficiency-name-list', views.DeficiencyNameList.as_view()),
    path('student-list/<str:name>', views.StudentList.as_view()),
    path('deficiency-names', views.DeficiencyNameOptions.as_view()),
    path('all-students/<str:name>', views.AllStudents.as_view()),
    path('profile', views.EmployeeProfileView.as_view()),
    path('report/<str:deficiency_name>', views.GenerateReportView.as_view()),
    path('dashboard-table', views.DashboardDeficiencyNameTable.as_view()),
    path('summary', views.GeneralSummaryView.as_view()),
    path('deficiency-summary/<str:deficiency_name>', views.PerDeficiencySummaryView.as_view()),
    path('bar-chart', views.BarChartSummary.as_view())
]
