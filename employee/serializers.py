from rest_framework import serializers
from deficiency.serializers import DeficiencySummarySerializer
from student.serializers import StudentSummarySerializer
from deficiency.models import Deficiency
from school.models import Membership, StudentProfile
from school.serializers import AffiliationSerializer

# To get the Total No. of Students, Total No. of Deficiencies, 
# Total No. of Completed Deficiencies, and Total No. of Pending Deficiencies
class GeneralSummary():
    def __init__(self):
        self.student_count = StudentProfile.objects.all().count()
        self.deficiency_count = Deficiency.objects.values("name").distinct().count()
        self.complete_count = Deficiency.objects.all().filter(is_complete=True).count()
        self.pending_count = Deficiency.objects.all().filter(is_complete=False).count()

# To get the Total No. Per Deficiency, Total No. of Completed Status Per Deficiency,
# and Total No. of Pending Status Per Deficiency
class PerDeficiencySummary():
    def __init__(self, deficiency_name):
        self.deficiency_name = deficiency_name

        self.deficiency_count = Deficiency.objects.filter(name=self.deficiency_name).count()
        self.complete_count = Deficiency.objects.filter(name=self.deficiency_name).filter(is_complete=True).count()
        self.pending_count = Deficiency.objects.filter(name=self.deficiency_name).filter(is_complete=False).count()

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

class GeneralSummarySerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        output = {}

        output['total_student'] = instance.student_count
        output['total_deficiency'] = instance.deficiency_count
        output['complete_count'] = instance.complete_count
        output['pending_count'] = instance.pending_count
    
        return output

class PerDeficiencySummarySerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        output = {}
    
        output['total_count'] = instance.deficiency_count
        output['complete_count'] = instance.complete_count
        output['pending_count'] = instance.pending_count
    
        return output
    
class DashboardDeficiencyNameTableSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        output = {}

        output['name'] = instance['name']
        output['category'] = instance['category']
        output['student_count'] = Deficiency.objects.filter(name=instance['name']).count()

        return output
    
class BarChartData():
    def __init__(self, college_abbreviation, deficiency_name=None):
        self.name = college_abbreviation
        self.pending = Deficiency.objects.filter(student__department__college__college_abbreviation=college_abbreviation).filter(is_complete=False)
        self.complete = Deficiency.objects.filter(student__department__college__college_abbreviation=college_abbreviation).filter(is_complete=True)


        if deficiency_name:
            self.pending_count = self.pending.filter(name=deficiency_name).count()
            self.complete_count = self.complete.filter(name=deficiency_name).count()
        else:
            self.pending_count = self.pending.count()
            self.complete_count = self.complete.count()
          
class BarChartSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        output = {}

        output['name'] = instance.name
        output['pending'] = instance.pending_count
        output['completed'] = instance.complete_count

        return output