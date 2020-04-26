from rest_framework import serializers

from Medicine.models import Drug, Dispense, Med_supply

from Treatment.models import Prescription

class Med_supplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Med_supply

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug

class DispenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispense

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        field = ['detail', 'treatment_cn']