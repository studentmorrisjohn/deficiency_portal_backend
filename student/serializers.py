from rest_framework import serializers
from school.models import StudentProfile, Membership
from school.serializers import AffiliationSerializer
from accounts.models import User

class StudentSummarySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    affiliations = serializers.SerializerMethodField('get_affiliations')
    mobile_number = serializers.SerializerMethodField('get_number')
    
    def get_name(self, obj):
        return f"{obj.user.last_name}, {obj.user.first_name} {obj.user.middle_name}"

    def get_affiliations(self, obj):
        affiliation_query = Membership.objects.filter(student__student_id=obj.student_id)
        return AffiliationSerializer(affiliation_query, many=True).data
    
    def get_number(self, obj):
        return obj.user.mobile_number

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'name', 'affiliations', 'mobile_number']
