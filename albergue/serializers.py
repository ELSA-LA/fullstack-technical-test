from rest_framework import serializers
from .models import Voluntario, Adoptador, Animal, Adopcion

class VoluntarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntario
        fields = '__all__'


class AdoptadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoptador
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'


class AdopcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopcion
        fields = '__all__'