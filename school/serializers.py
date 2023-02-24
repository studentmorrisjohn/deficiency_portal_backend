from rest_framework import serializers
from school.models import Organization, Membership

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