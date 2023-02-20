from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import LoginSerializer

# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
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


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    def get(self, request, format=None):
        return Response()