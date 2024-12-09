from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Services
from ..services.liquidaciones_service import LiquidacionService

# Serializers
from .serializers import LiquidacionParamsSerializer, FormattedLiquidacionSerializer


@api_view(['GET'])
def liquidaciones(request):
    serializer = LiquidacionParamsSerializer(data=request.GET)
    if serializer.is_valid():
        params = serializer.validated_data
        liquidacion_service = LiquidacionService()
        try:
            res = liquidacion_service.get_liquidaciones(
                params['rut'],
                params['anio'],
                params['mes'],
                params['cantidad_meses']
            )
            res_serializer = FormattedLiquidacionSerializer(data=res)
            if res_serializer.is_valid():
                return Response(status=status.HTTP_200_OK, data=res)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=res_serializer.errors)
        except Exception as e:    
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"error": str(e)})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)