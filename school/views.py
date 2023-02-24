from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from school.serializers import OrganizationOptionsSerializer
from school.models import Organization
# Create your views here.
class OrganizationOptions(APIView):
    def get(self, request, format=None):
        name = request.GET.get('name')
        
        if name:
            organizations = Organization.objects.filter(name__icontains=name).order_by('name')
        else:
            organizations = Organization.objects.all().order_by('name')

        serializer = OrganizationOptionsSerializer(organizations, many=True)

        return Response(serializer.data)