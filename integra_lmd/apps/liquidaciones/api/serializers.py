from datetime import datetime
from rest_framework import serializers


# Serializers for the API
class LiquidacionParamsSerializer(serializers.Serializer):
    rut = serializers.CharField(required=True)
    anio = serializers.CharField(required=True)
    mes = serializers.CharField(required=True)
    cantidad_meses = serializers.CharField(required=True)

    def validate_mes(self, value):
            # Validar que el mes tenga exactamente dos caracteres
            if len(value) != 2:
                raise serializers.ValidationError("El mes debe tener exactamente 2 caracteres.")
            
            # Validar que el valor sea un número entre "01" y "12"
            if not value.isdigit() or not (1 <= int(value) <= 12):
                raise serializers.ValidationError("El mes debe ser un valor numérico entre 01 y 12.")

            return value
    
    def validate_anio(self, value):
            # Obtener el año actual
            anio_actual = datetime.now().year
            
            # Validar que el año no sea mayor al actual
            if not value.isdigit():
                raise serializers.ValidationError("El año debe ser un valor numérico.")
            
            if int(value) > anio_actual:
                raise serializers.ValidationError(f"El año no puede ser mayor al actual ({anio_actual}).")
            
            return value        


# Serializers for the services
class LiquidacionDetalleSerializer(serializers.Serializer):
    nombreDocumento = serializers.CharField()
    anio = serializers.IntegerField()
    mes = serializers.IntegerField()

class LiquidacionSerializer(serializers.Serializer):
    rut = serializers.CharField()
    nombre = serializers.CharField()
    liquidaciones = LiquidacionDetalleSerializer(many=True)

class FormattedLiquidacionSerializer(serializers.Serializer):
    fechaReporte = serializers.CharField()
    totalLiquidaciones = serializers.IntegerField()
    detalle = LiquidacionSerializer()