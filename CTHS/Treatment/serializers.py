from rest_framework import serializers

from User_app.models import Congenital_disease, Patient
from Medicine.models import Drug

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
        fields = ['med_sup_id', 'name', 'amount']
        read_only_fields = ['med_sup_id', 'name', 'amount']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['p_id']