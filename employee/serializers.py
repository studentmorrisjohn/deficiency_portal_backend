from rest_framework import serializers
from deficiency.serializers import DeficiencySummarySerializer
from student.serializers import StudentSummarySerializer
from deficiency.models import Deficiency
from school.models import Membership
from school.serializers import AffiliationSerializer

class Summary():
    def __init__(self, deficiency_name):
        self.deficiency_name = deficiency_name

    def query(self):
        self.deficiency_count = Deficiency.objects.filter(name=self.deficiency_name).count()
        self.complete_count = Deficiency.objects.filter(name=self.deficiency_name).filter(is_complete=True).count()
        self.pending_count = Deficiency.objects.filter(name=self.deficiency_name).filter(is_complete=False).count()

    def to_representation(self):
        output = {}

        output['total_count'] = self.deficiency_count
        output['complete_count'] = self.complete_count
        output['pending_count'] = self.pending_count



class StudentListSerializer(DeficiencySummarySerializer):
    student = serializers.SerializerMethodField('get_student')

    def get_student(self, obj):
        return StudentSummarySerializer(obj.student).data

    class Meta:
        model = Deficiency
        fields = ['id', 'student', 'status', 'balance']

class ReportSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        output = {}

        user = instance.student.user

        affiliation_query = Membership.objects.filter(student__student_id=user.username)
        affiliations = ", ".join([f"{x['role']} of {x['organization']['name']}" for x in AffiliationSerializer(affiliation_query, many=True).data])
        status = "Complete" if instance.is_complete else "Pending"
        

        output['Deficiecy ID'] = instance.deficiency_id
        output['Deficiency Name'] = instance.name
        output['Category'] = instance.category
        output['Status'] = status
        
        output['Student Number'] = user.username
        output['Student Name'] = user.name
        output['Program'] = instance.student.department.department_name
        output['Email'] = user.email
        output['Contact Number'] = user.mobile_number
        output['Affiliation'] = affiliations

        output['Encoded By'] = instance.added_by.user.name
        output['Added On'] = instance.date_added
        output['Processed By'] = instance.processed_by.user.name if instance.processed_by else "----"
        output['Processed On'] = instance.date_fulfilled

        if instance.category == "Finance":
            output['Balance To Be Settled'] = instance.financedeficiency.amount
        else:
            output['Documents to be Submitted'] = instance.name
        
        return output