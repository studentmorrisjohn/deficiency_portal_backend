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
        fields = ['organization', 'role']