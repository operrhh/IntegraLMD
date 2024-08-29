from rest_framework import serializers


# Serializers for the API
class LiquidacionParamsSerializer(serializers.Serializer):
    rut = serializers.CharField(required=True)
    anio = serializers.CharField(required=True)
    mesDesde = serializers.CharField(required=True)
    mesHasta = serializers.CharField(required=True)


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