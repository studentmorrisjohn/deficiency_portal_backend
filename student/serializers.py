from rest_framework import serializers
from school.models import StudentProfile, Membership
from school.serializers import AffiliationSerializer

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