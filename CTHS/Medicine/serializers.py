from rest_framework import serializers

from Medicine.models import Drug, Dispense, Med_supply

from Treatment.models import Prescription, Diagnosis
from Treatment.serializers import TreatmentSerializer
from User_app.models import Doctor, User, Nurse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
        read_only_fields = ['id']

class DoctorSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = Doctor
        fields = '__all__'

class NurseSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = Nurse
        fields = '__all__'

class Med_supplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Med_supply
        fields = ['med_sup_id', 'sup_id', 'name', 'sup_id']
        read_only_fields = ['med_sup_id', 'sup_id', 'name', 'sup_id']

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['med_sup_id', 'drug_id', 'name', 'drug_id']
        read_only_fields = ['med_sup_id', 'drug_id', 'name', 'drug_id']

class DispenseSerializer(serializers.ModelSerializer):
    prescription_id = serializers.IntegerField(required=False)
    drug = DrugSerializer(source="dis_drug_id", required=False)
    med_sup = Med_supplySerializer(source="dis_med_id", required=False)
    dispense_type = serializers.CharField(source="get_type_display", required=False)
    class Meta:
        model = Dispense
        fields = ['id', 'amount', 'dispense_type' ,'type', 'prescription_id', 'drug', 'med_sup' ]
        read_only_fields = ['id']

    def create(self, validate_data):
        return Dispense.objects.create(**validate_data)

class PrescriptionSerializer(serializers.ModelSerializer):
    detail = serializers.CharField(required=False)
    dispense = DispenseSerializer(source="dispense_set", many=True, required=False)
    treatment_cn = TreatmentSerializer(required=False)
    doctor_id = DoctorSerializer(required=False)
    status = serializers.CharField(source="get_status_display", required=False)
    class Meta:
        model = Prescription
        fields = ['id', 'detail', 'status', 'treatment_cn', 'dispense', 'doctor_id']
        read_only_fields = ['id']