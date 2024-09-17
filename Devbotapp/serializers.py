from rest_framework import serializers
from .models import UIRequirement, TechnicalRequirement

class UIRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UIRequirement
        fields = '__all__'

class TechnicalRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalRequirement
        fields = '__all__'
