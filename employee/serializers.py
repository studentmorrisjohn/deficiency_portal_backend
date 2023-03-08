from rest_framework import serializers
from deficiency.serializers import DeficiencySummarySerializer
from student.serializers import StudentSummarySerializer
from deficiency.models import Deficiency

class StudentListSerializer(DeficiencySummarySerializer):
    student = serializers.SerializerMethodField('get_student')

    def get_student(self, obj):
        return StudentSummarySerializer(obj.student).data

    class Meta:
        model = Deficiency
        fields = ['id', 'student', 'status', 'balance']

