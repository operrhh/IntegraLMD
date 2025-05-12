from datetime import datetime
import os
import json

from ..services.liquidaciones_service_peoplesoft import LiquidacionServicePeoplesoft
from ..services.liquidaciones_service_aws import BucketService


from ..models import Trabajador

class LiquidacionService:
    def __init__(self):
        self.liquidacion_service_peoplesoft = LiquidacionServicePeoplesoft()
        self.bucket_service = BucketService()
    
    def get_liquidaciones(self, rut, anio, mes, cantidad_meses):
        try:
            trabajador = self.liquidacion_service_peoplesoft.get_liquidaciones(rut, anio, mes, cantidad_meses)

            json_response = {
                "fechaReporte": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "totalLiquidaciones": len(trabajador.liquidaciones),
                "detalle": trabajador.format_json()
            }

            self.save_file_pdf(trabajador)
            self.save_json_file(json_response, trabajador)

            # self.bucket_service.list_objects_bucket()
            
            self.bucket_service.upload_file(key=trabajador.rut)

            return json_response
        except Exception as e:
            raise e

    def save_file_pdf(self, trabajador: Trabajador):

        ruta_actual = os.path.abspath(__file__)
        directorio = os.path.dirname(ruta_actual)

        try:
            for liquidacion in trabajador.liquidaciones:
                if not os.path.exists(f"{directorio}/tmp/{trabajador.rut}"):
                    os.makedirs(f"{directorio}/tmp/{trabajador.rut}")

                liquidacion.save_file(f"{directorio}/tmp/{trabajador.rut}/{liquidacion.nombre_documento}")
        except FileNotFoundError as e:
            raise ValueError("Error al guardar archivo de liquidación: " + str(e))
        except Exception as e:
            raise ValueError("Error al guardar archivo de liquidación: " + str(e) + " - " + str(type(e)))
        
    def save_json_file(self, json_response, trabajador: Trabajador):
        ruta_actual = os.path.abspath(__file__)
        directorio = os.path.dirname(ruta_actual)

        try:
            if not os.path.exists(f"{directorio}/tmp/{trabajador.rut}"):
                os.makedirs(f"{directorio}/tmp/{trabajador.rut}")

            # Convertir el dict a una cadena JSON
            json_str = json.dumps(json_response, ensure_ascii=False, indent=4)

            with open(f"{directorio}/tmp/{trabajador.rut}/response.json", "w") as file:
                file.write(json_str)
        except FileNotFoundError as e:
            raise ValueError("Error al guardar archivo json: " + str(e))
        except Exception as e:
            raise ValueError("Error al guardar archivo json: " + str(e) + " - " + str(type(e)))