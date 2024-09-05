from rest_framework import serializers
from .models import Usuario, Animal, Adopcion

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'email', 'rol', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            password=validated_data['password'],
            rol=validated_data['rol']
        )
        return user

class AnimalSerializer(serializers.ModelSerializer):
    voluntario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(rol=Usuario.VOLUNTARIO))

    class Meta:
        model = Animal
        fields = ['id', 'nombre', 'edad', 'raza', 'tipo', 'estado', 'voluntario']

class AdopcionSerializer(serializers.ModelSerializer):
    adoptador = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(rol=Usuario.ADOPTANTE))
    voluntario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(rol=Usuario.VOLUNTARIO))

    class Meta:
        model = Adopcion
        fields = ['id', 'animal', 'adoptador', 'voluntario', 'fecha', 'estado', 'fecha_devolucion']
