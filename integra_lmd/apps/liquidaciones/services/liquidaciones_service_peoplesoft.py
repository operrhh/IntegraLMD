from django.db import connections
import cx_Oracle
from ..models import Liquidacion, Trabajador

class LiquidacionServicePeoplesoft:
    def get_liquidaciones(self, rut, anio, mes_desde, mes_hasta) -> Trabajador:
        """Obtiene las liquidaciones de un trabajador en el sistema Peoplesoft."""
        try:
            with connections['peoplesoft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()
                cursor.callproc("SP_GET_LIQUIDACIONES", [out_cur, rut, anio, mes_desde, mes_hasta])
                
                items = list(out_cur)  # Convierte el cursor a una lista
                if not items:
                    raise ValueError("No se encontraron liquidaciones")

                list_liquidaciones = self.format_liquidaciones(items)
                liq = list_liquidaciones[0]
                
                worker_data = self.get_liquidaciones_data(rut, liq.compania, anio, mes_hasta, liq.nombre_trabajador, list_liquidaciones)
                return worker_data

        except cx_Oracle.DatabaseError as e:
            raise ValueError(f"Error de base de datos: {e}")
        except Exception as e:
            raise e

    def get_liquidaciones_data(self, emplid, company, year, month, name, liquidaciones):
        """Obtiene los datos de liquidación específicos de un trabajador."""
        try:
            with connections['peoplesoft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()
                cursor.callproc("SP_GET_LIQUIDACIONES_DATA", [out_cur, emplid, company, year, month])
                
                items = list(out_cur)
                if not items:
                    raise ValueError("No se encontraron datos de liquidación")

                return self.format_liquidaciones_data(items, emplid, name, liquidaciones)

        except cx_Oracle.DatabaseError as e:
            raise ValueError(f"Error de base de datos: {e}")
        except Exception as e:
            raise e

    def format_liquidaciones(self, liquidaciones):
        """Formatea la lista de liquidaciones a objetos Liquidacion."""
        return [
            Liquidacion(
                anio=int(liquidacion[0]),
                mes=int(liquidacion[1]),
                nombre_trabajador=liquidacion[2],
                compania=liquidacion[3],
                nombre_documento=liquidacion[4],
                archivo_blob=liquidacion[5]
            ) for liquidacion in liquidaciones
        ]

    def format_liquidaciones_data(self, data, emplid, name, liquidaciones):
        """Formatea los datos de liquidación en un objeto Trabajador."""
        return Trabajador(
            rut=emplid,
            nombre=name,
            tipo_contrato=data[0][0],
            afc=data[0][1],
            fecha_contrato_trabajo=data[0][2].strftime("%Y-%m-%d"),
            fecha_afiliacion=data[0][3].strftime("%Y-%m-%d"),
            monto_remuneracion=data[0][4],
            imponible_cesantia=data[0][5],
            actividad_laboral=data[0][6],
            caja_compensacion=data[0][7],
            direccion_trabajo=data[0][8],
            ocupacion=data[0][9],
            calidad_trabajador=data[0][10],
            regimen_previsional=data[0][11],
            institucion_previsional=data[0][12],
            institucion_salud=data[0][13],
            liquidaciones=liquidaciones
        )
