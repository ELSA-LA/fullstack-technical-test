from rest_framework import serializers
from .models import Usuario, Animal, Adopcion
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print(attrs)
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Añadir el rol al token
        refresh["rol"] = self.user.rol

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nombre", "apellido", "email", "rol", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Usuario(
            email=validated_data["email"],
            nombre=validated_data["nombre"],
            apellido=validated_data["apellido"],
            rol=validated_data["rol"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.apellido = validated_data.get("apellido", instance.apellido)
        instance.rol = validated_data.get("rol", instance.rol)

        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()
        return instance


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ["id", "nombre", "edad", "raza", "tipo", "estado"]


class AdopcionSerializer(serializers.ModelSerializer):
    adoptador = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(rol=Usuario.ADOPTANTE), required=False
    )
    voluntario = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(rol=Usuario.VOLUNTARIO), required=False
    )

    class Meta:
        model = Adopcion
        fields = [
            "id",
            "animal",
            "adoptador",
            "voluntario",
            "fecha",
            "estado",
            "fecha_devolucion",
        ]
