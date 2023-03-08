from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from deficiency.models import Deficiency
from deficiency.serializers import DeficiencySummarySerializer, DeficiencyDetailSerializer
from school.models import Membership
from school.serializers import AffiliationSerializer, ProfileSerializer

# Create your views here.
class DeficiencyList(APIView):
    def get(self, request, format=None):
        user = self.request.user
        student_id = user.username

        deficiency_list_query = Deficiency.objects.filter(student__student_id=student_id).order_by("is_complete", "date_added")

        if not deficiency_list_query:
            return Response({"warning": "the student does not have any deficiencies"})

        serializer = DeficiencySummarySerializer(deficiency_list_query, many=True)
        return Response(serializer.data)

class DeficiencyDetail(APIView):
    def get_object(self, def_id):
        try:
            return Deficiency.objects.get(id=def_id)
        except Deficiency.DoesNotExist:
            raise Http404

    def get(self, request, def_id, format=None):
        deficiency_query = self.get_object(def_id)
        
        serializer = DeficiencyDetailSerializer(deficiency_query)
        return Response(serializer.data)

class AffilitationList(APIView):
    def get(self, request, format=None):
        user = self.request.user
        student_id = user.username

        affiliations = Membership.objects.filter(student__student_id=student_id)

        if affiliations:
            serializer = AffiliationSerializer(affiliations, many=True)
            return Response(serializer.data)
        
        return Response({"affiliations":"none"})

    def post(self, request, format=None):
        student_id = request.user.username
        organization_id = request.data["organization"]
        position = request.data["role"]
        affiliation = Membership.objects.create(organization_id=organization_id, student_id=student_id, role=position)

        serializer = AffiliationSerializer(affiliation)
        return Response(serializer.data)
    
class AffiliationDetail(APIView):
    def delete(self, request, id, format=None):
        affiliation = Membership.objects.get(id=id)
        affiliation.delete()

        serializer = AffiliationSerializer(affiliation)
        return Response(serializer.data)

class StudentProfile(APIView):
    def get(self, request,format=None):
        user = self.request.user
        print(user.role)

        serializer = ProfileSerializer(user)

        return Response(serializer.data)
    
    def put(self, request, format=None):
        user = request.user
        new_number = request.data["mobile_number"]
        new_email = request.data["email"]

        user.mobile_number = new_number
        user.email = new_email

        user.save()

        return Response({"success": "Profile was successfully updated"})
    