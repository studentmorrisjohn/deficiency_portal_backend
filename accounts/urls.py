from django.urls import path
from accounts import views

urlpatterns = [
    path('isAuthenticated', views.CheckAuthenticatedView.as_view()),
    path('user-name', views.UserName.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('change-pass', views.ChangePasword.as_view()),
    path('insert-users', views.InsertUsers.as_view())
]
