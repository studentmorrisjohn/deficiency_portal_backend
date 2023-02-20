from rest_framework import serializers
from deficiency.models import Deficiency
from student.serializers import StudentSummarySerializer

class DeficiencySummarySerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField('get_balance')
    status = serializers.SerializerMethodField('get_status')

    def get_balance(self, obj):
        if obj.category == "Finance":
            return obj.financedeficiency.amount
        
        return "NA"

    def get_status(self, obj):
        if obj.is_complete:
            return "Completed"

        return "Pending"

    class Meta:
        model = Deficiency
        fields = ['id', 'category', 'name', 'status', 'balance']

class DeficiencyDetailSerializer(DeficiencySummarySerializer):
    student_summary = serializers.SerializerMethodField('get_student')
    added_by = serializers.SerializerMethodField('get_encoded_by')
    processed_by = serializers.SerializerMethodField('get_processed_by')

    def get_student(self, obj):
        return StudentSummarySerializer(obj.student).data

    def get_encoded_by(self, obj):
        return f"{obj.added_by.user.first_name} {obj.added_by.user.last_name}"

    def get_processed_by(self, obj):
        if obj.processed_by:
            return obj.processed_by.user.first_name
        return "------"

    class Meta:
        model = Deficiency
        fields = ['id', 'category', 'name', 'status', 'balance', 'student_summary', 'added_by', 'processed_by', 'date_added', 'date_fulfilled']

class NewDeficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deficiency
        fields = '__all__'


class DeficiencyNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deficiency
        fields = ['name', 'category']