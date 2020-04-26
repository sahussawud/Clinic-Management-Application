from rest_framework import serializers

from Medicine.models import Drug, Dispense, Med_supply

from Treatment.models import Prescription

class Med_supplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Med_supply
        fields = '__all__'

class DispenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispense
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    dispense = DispenseSerializer(source="dispense_set", many=True)
    class Meta:
        model = Prescription
        fields = ['id', 'detail', 'treatment_cn', 'dispense']
        read_only_fields = ['id']