from django.db import connections
import cx_Oracle

from ..models import Liquidacion, Trabajador

class LiquidacionServicePeoplesoft:
    def get_liquidaciones(self, rut, anio, mes_desde, mes_hasta) -> Trabajador:
        try:
            with connections['peoplesoft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()

                cursor.callproc("SP_GET_LIQUIDACIONES", [out_cur, rut, anio, mes_desde, mes_hasta])
                if out_cur:
                    items = [res for res in out_cur]
                    if len(items) > 0:
                        format_items = self.format_liquidaciones(items)
                        return format_items
                    else:
                        raise ValueError("No se encontraron liquidaciones")
        except cx_Oracle.DatabaseError as e:
            raise ValueError("Error de base de datos: " + str(e))
        except Exception as e:
            raise e

    def format_liquidaciones(self, liquidaciones):
        list_liquidaciones = []
        for liquidacion in liquidaciones:
            list_liquidaciones.append(
                Liquidacion(
                    anio=int(liquidacion[2]),
                    mes=int(liquidacion[3]),
                    nombre_documento=liquidacion[0],
                    archivo_blob=liquidacion[5]
                )
            )

        trabajador = Trabajador(
            rut=liquidaciones[0][1],
            nombre=liquidaciones[0][4],
            liquidaciones=list_liquidaciones
        )

        return trabajador