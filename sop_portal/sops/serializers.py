from rest_framework import serializers
from .models import SOP

class SOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOP
        fields = '__all__'
