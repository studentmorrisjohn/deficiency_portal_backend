from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from deficiency.models import Deficiency
from deficiency.serializers import DeficiencySummarySerializer, DeficiencyDetailSerializer
from school.models import Membership
from school.serializers import AffiliationSerializer

# Create your views here.
class DeficiencyList(APIView):
    def get(self, request, stud_id, format=None):
        student_id = stud_id
        deficiency_list_query = Deficiency.objects.filter(student__student_id=student_id)

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
    def get(self, request, student_id, format=None):
        affiliations = Membership.objects.filter(student__student_id=student_id)

        if affiliations:
            serializer = AffiliationSerializer(affiliations, many=True)
            return Response(serializer.data)
        
        return Response({"affiliations":"none"})
    