from rest_framework import serializers

from User_app.models import Congenital_disease, Patient
from .models import Treatment, Diagnosis
from Medicine.models import Drug, Med_supply

class Congenital_diseaseSerializerWithoutPatient(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=255)

    def create(self, validate_data):
        return Congenital_disease.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class Congenital_diseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congenital_disease
        fields = ['id', 'name']
        read_only_fields = ['id']

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['med_sup_id', 'name', 'amount', 'drug_id']
        read_only_fields = ['med_sup_id', 'name', 'amount', 'drug_id']

class Med_supplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Med_supply
        fields = ['med_sup_id', 'name', 'amount', 'sup_id']
        read_only_fields = ['med_sup_id', 'name', 'amount', 'sup_id']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['p_id']

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class TreatmentSerializer(serializers.ModelSerializer):
    patient_condition = serializers.CharField(source="get_patient_condition_display")
    diagnosis = DiagnosisSerializer()
    class Meta:
        model = Treatment
        fields = ['cn', 'patient_condition', 'diagnosis', 'patient_p_id']
        read_only_fields = ['cn']

class DrugMedSupplySerializer(serializers.Serializer):
    drug = DrugSerializer(many=True)
    med_sup = Med_supplySerializer(many=True)