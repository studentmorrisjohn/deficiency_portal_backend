from rest_framework import serializers
from school.models import StudentProfile, Membership
from school.serializers import AffiliationSerializer
from accounts.models import User

class StudentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username']

class StudentSummarySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    affiliations = serializers.SerializerMethodField('get_affiliations')
    
    def get_name(self, obj):
        return f"{obj.user.last_name}, {obj.user.first_name} {obj.user.middle_name}"

    def get_affiliations(self, obj):
        affiliation_query = Membership.objects.filter(student__student_id=obj.student_id)
        return AffiliationSerializer(affiliation_query, many=True).data

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'name', 'affiliations']

class StudentProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    department = serializers.SerializerMethodField('get_department')

    def get_name(self, obj):
        return f"{obj.last_name}, {obj.first_name} {obj.middle_name}"

    def get_department(self, obj):
        return obj.studentprofile.department.department_name

    class Meta:
        model = User
        fields = ['username', 'name', 'gender', 'birth_date', 'department', 'mobile_number', 'email']
        