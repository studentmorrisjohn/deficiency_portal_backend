from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.serializers import LoginSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from accounts.serializers import UserNameSerializer

# Create your views here.
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            print(user)

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success', "role": user.role})
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })

class LoginView(APIView):
    permission_classes =[AllowAny]
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        auth.login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Logged Out' })
        except:
            return Response({ 'error': 'Something went wrong when logging out' })

class ChangePasword(APIView):
    def post(self, request, format=None):
        user = request.user
        current_pass = request.user.password
        current_pass_entered = request.data["old_pass"]
        new_pass = request.data["new_pass"]
        re_new_pass = request.data["re_new_pass"]
        
        if not check_password(current_pass_entered, current_pass):
            return Response({"error": "You entered the wrong current password"})
        
        if new_pass != re_new_pass:
            return Response({"error": "Passwords do not match"})
        
        user.set_password(new_pass)
        user.save()
        update_session_auth_hash(request, request.user)
        return Response({"success": "You changed your password successfully"})


class UserName(APIView):
    def get(self, reuquest, format=None):
        user = self.request.user

        serializer = UserNameSerializer(user)

        return Response(serializer.data)