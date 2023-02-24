from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from deficiency.models import Deficiency
from deficiency.serializers import DeficiencySummarySerializer, DeficiencyDetailSerializer
from school.models import Membership
from school.serializers import AffiliationSerializer
from student.serializers import StudentNameSerializer, StudentProfileSerializer

# Create your views here.
class DeficiencyList(APIView):
    def get(self, request, format=None):
        user = self.request.user
        student_id = user.username

        deficiency_list_query = Deficiency.objects.filter(student__student_id=student_id)

        if not deficiency_list_query:
            return Response({"warning": "the student does not have any deficiencies"})

        serializer = DeficiencySummarySerializer(deficiency_list_query, many=True)
        return Response(serializer.data)

class StudentName(APIView):
    def get(self, reuquest, format=None):
        user = self.request.user

        serializer = StudentNameSerializer(user)

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

class AffiliationDetail(APIView):
    def delete(self, request, id, format=None):
        affiliation = Membership.objects.get(id=id)
        affiliation.delete()

        serializer = AffiliationSerializer(affiliation)
        return Response(serializer.data)

class StudentProfile(APIView):
    def get(self, request,format=None):
        user = self.request.user

        serializer = StudentProfileSerializer(user)

        return Response(serializer.data)