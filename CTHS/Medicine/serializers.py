

from rest_framework import serializers
from Medicine.models import Dispense, Drug, Med_supply
from Treatment.models import Diagnosis, Prescription
from Treatment.serializers import TreatmentSerializer
from User_app.models import Doctor, Nurse, User


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
    drug = DrugSerializer(source="dis_drug_id", required=False)
    med_sup = Med_supplySerializer(source="dis_med_id", required=False)
    type = serializers.CharField(source="get_type_display")
    class Meta:
        model = Dispense
        fields = ['id', 'amount' ,'type', 'drug', 'med_sup' ]
        read_only_fields = ['id']
    

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

class CreatePrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'detail', 'status', 'treatment_cn', 'doctor_id']
        read_only_fields = ['id']
