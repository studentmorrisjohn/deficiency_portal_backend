from django.urls import path
from accounts import views

urlpatterns = [
    path('isAuthenticated', views.CheckAuthenticatedView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
]
