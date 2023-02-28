from django.urls import path, re_path
from student import views
from school.views import OrganizationOptions

urlpatterns = [
    path('affiliations', views.AffilitationList.as_view()),
    path('deficiencies', views.DeficiencyList.as_view()),
    path('deficiency-details/<str:def_id>',views.DeficiencyDetail.as_view()),
    path('profile', views.StudentProfile.as_view()),
    path('affiliation/<str:id>', views.AffiliationDetail.as_view()),
    path('organizations', OrganizationOptions.as_view())
]
