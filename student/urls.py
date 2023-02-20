from django.urls import path
from student import views

urlpatterns = [
    path('affiliations/<str:student_id>', views.AffilitationList.as_view()),
    path('deficiencies/<str:stud_id>', views.DeficiencyList.as_view()),
    path('deficiency-details/<str:def_id>',views.DeficiencyDetail.as_view())
]
