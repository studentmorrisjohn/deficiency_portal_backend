from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from school.models import EmployeeProfile, StudentProfile
from deficiency.models import Deficiency, FinanceDeficiency
from deficiency.serializers import DeficiencyDetailSerializer, DeficiencyNameListSerializer, DeficiencyNameOptionSerializer
from employee.serializers import StudentListSerializer
from accounts.permissions import HasEmployeePermission

# Create your views here.
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
    
    def put(self, request, def_id, format=None):
        deficiency = self.get_object(def_id)

        deficiency.is_complete = request.data["is_complete"]
        employee = EmployeeProfile.objects.get(employee_id=request.data["processed_by"])
        deficiency.processed_by = employee
        
        deficiency.save()

        serializer = DeficiencyDetailSerializer(deficiency)
        return Response(serializer.data)
    
    def delete(self, request, def_id, format=None):
        deficiency = self.get_object(def_id)
        
        deficiency.delete()

        serializer = DeficiencyDetailSerializer(deficiency)
        return Response(serializer.data)

class DeficiencyNameList(APIView):
    # permission_classes = [HasEmployeePermission]
    def get(self, request, format=None):
        deficiency_name_list = Deficiency.objects.values("name", "category").distinct()
        serializer = DeficiencyNameListSerializer(deficiency_name_list, many=True)
        return Response(serializer.data)

class StudentList(APIView):
    # permission_classes = [HasEmployeePermission]
    def get(self, request, name, format=None):
        deficiency_name = name
        student_list_query = Deficiency.objects.filter(name=deficiency_name).order_by("is_complete")

        if not  student_list_query:
            return Response({"warning": "the deficiency does not exist!"})

        serializer = StudentListSerializer(student_list_query, many=True)
        return Response(serializer.data)
    
    def post(self, request, name, *args, **kwargs):
        student = StudentProfile.objects.get(student_id=request.data["student_id"])
        employee = EmployeeProfile.objects.get(employee_id=request.data["added_by"])

        new_deficiency = Deficiency(student=student, added_by=employee, name=name, category=request.data["category"])
        new_deficiency.save()

        if request.data["category"] == "Finance":
            try:
                amount = request.data["amount"]
                new_finance_deficiency = FinanceDeficiency(deficiency_id=new_deficiency.id, amount=amount)
                
                new_finance_deficiency.save()
            except KeyError:
                return Response({"warning": "no amount given"})

        serializer = DeficiencyDetailSerializer(new_deficiency)
        return Response(serializer.data)

class DeficiencyNameOptions(APIView):
    def get(self, request, format=None):
        name = request.GET.get('name')
        
        if name:
            deficiency_names = Deficiency.objects.filter(name__icontains=name).order_by('name')
        else:
            deficiency_names = Deficiency.objects.all().order_by('name')

        serializer = DeficiencyNameListSerializer(deficiency_names, many=True)

        return Response(serializer.data)