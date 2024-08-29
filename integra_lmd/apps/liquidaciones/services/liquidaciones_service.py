from datetime import datetime
import os
from ..services.liquidaciones_service_peoplesoft import LiquidacionServicePeoplesoft

from ..models import Trabajador, Liquidacion

class LiquidacionService:
    def __init__(self):
        self.liquidacion_service_peoplesoft = LiquidacionServicePeoplesoft()
    
    def get_liquidaciones(self, rut, anio, mes_desde, mes_hasta):
        try:
            trabajador = self.liquidacion_service_peoplesoft.get_liquidaciones(rut, anio, mes_desde, mes_hasta)

            self.save_file_pdf(trabajador)
            
            res = {
                "fechaReporte": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "totalLiquidaciones": len(trabajador.liquidaciones),
                "detalle": trabajador.format_json()
            }

            return res
        except Exception as e:
            raise e 

    def save_file_pdf(self, trabajador: Trabajador):

        ruta_actual = os.path.abspath(__file__)
        directorio = os.path.dirname(ruta_actual)

        try:
            for liquidacion in trabajador.liquidaciones:
                if not os.path.exists(f"{directorio}/src/{trabajador.rut}"):
                    os.makedirs(f"{directorio}/src/{trabajador.rut}")

                liquidacion.save_file(f"{directorio}/src/{trabajador.rut}/{liquidacion.nombre_documento}")
        except FileNotFoundError as e:
            raise ValueError("Error al guardar archivo: " + str(e))
        except Exception as e:
            raise ValueError("Error al guardar archivo: " + str(e) + " - " + str(type(e)))