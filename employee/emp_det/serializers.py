from rest_framework import serializers
from .models import Employee, Project, Address
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def validate_pincode(self, value):
        if not re.match(r'^\d{6}$', value):
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value


class EmployeeSerializer(serializers.ModelSerializer):
    
    address = AddressSerializer(required=True)
    
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_name(self, value):
        logger.info("NAME: %s", value)
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("Name should only contain letters and spaces.")
        
        name_lower = value.lower()
        if Employee.objects.filter(name__iexact=name_lower).exists():
            raise serializers.ValidationError("A user with this name already exists.")
        return value
    
    def validate_phone(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Phone numbers must be a list.")
        
        errors = []
        for phone in value:
            if not re.match(r'^\d{10}$', phone):
                errors.append(f"Invalid phone number: {phone}. Each phone number must be exactly 10 digits.")
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return value

    def validate(self, value):
        expected_fields = [field.name for field in self.Meta.model._meta.fields]
        expected_fields = set(expected_fields) - {'id'}

        provided_fields = set(self.initial_data.keys())
        
        logger.info("Validating data: %s", value)
        logger.info(f"Expected ->  {expected_fields}")
        logger.info(f"Provided ->  {provided_fields}")

        if expected_fields != provided_fields or len(expected_fields) != len(provided_fields):
            raise serializers.ValidationError(
                {"error": "The fields in the request do not match the expected fields"}
            )
        return value

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        employee = Employee.objects.create(address=address, **validated_data)
        return employee

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            Address.objects.update_or_create(
                defaults=address_data,
                pk=instance.address.pk
            )
        return super().update(instance, validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def validate_title(self, value):
        if not re.match(r'^[a-zA-Z\s\d]+$', value):
            raise serializers.ValidationError("Title should only contain letters, digits and spaces.")
        
        title_lower = value.lower()
        if Project.objects.filter(title__iexact=title_lower).exists():
            raise serializers.ValidationError("A project with this title already exists.")
        return value

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            start_date = data['start_date']
            end_date = data['end_date']
            
            duration = (end_date - start_date).days
            if duration < 0:
                raise serializers.ValidationError("End date must be after the start date.")
            
            data['duration'] = duration
        return data
