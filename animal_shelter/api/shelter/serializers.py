from rest_framework import serializers
from apps.shelter.models import ShelterUser, Animal, Adoption


#-----Voluntarios
class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterUser
        fields = ('id', 'first_name', 'last_name', 'email', 'is_volunteer', 'is_active')

class VolunteerCreationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = ShelterUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_volunteer')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return data

    def create(self, validated_data):
        user = ShelterUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_volunteer=True
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

#-----Adoptant
class AdoptantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterUser
        fields = ('id', 'first_name', 'last_name', 'email', 'is_adoptant', 'is_active')

class AdoptantCreationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = ShelterUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_adoptant')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return data

    def create(self, validated_data):
        user = ShelterUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_adoptant=True
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
    
    
# -------Animals 
class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'name', 'age', 'breed', 'type', 'status']

#--------Adoption 
class AdoptionSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer(read_only=True)
    volunteer = VolunteerSerializer(read_only=True)
    adopter = AdoptantSerializer(read_only=True)
    
    class Meta:
        model = Adoption
        fields = ['id', 'animal', 'volunteer', 'adopter', 'adoption_date', 'status']
