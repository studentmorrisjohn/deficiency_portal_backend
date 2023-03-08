from rest_framework import serializers
from school.models import Organization, Membership
from accounts.models import User

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name']

class AffiliationSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Membership
        fields = ['id', 'organization', 'role']

class OrganizationOptionsSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_option_value')
    label = serializers.SerializerMethodField('get_label')

    def get_option_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name

    class Meta:
        model = Organization
        fields = ['value', 'label']

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    department = serializers.SerializerMethodField('get_department')

    def get_name(self, obj):
        return f"{obj.last_name}, {obj.first_name} {obj.middle_name}"

    def get_department(self, obj):
        if obj.role == "STUDENT":
            return obj.studentprofile.department.department_name
        else:
            return "Registrar"

    class Meta:
        model = User
        fields = ['username', 'name', 'gender', 'birth_date', 'department', 'mobile_number', 'email']