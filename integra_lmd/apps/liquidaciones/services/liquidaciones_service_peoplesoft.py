from typing import List
import oracledb
from ...services.global_service import oracle_connection
from ..models import Liquidacion, Trabajador

from ..custom_exceptions import LiquidacionException, SinDatosLiquidacionException, SinLiquidacionesException, TrabajadorNoExisteException

class LiquidacionServicePeoplesoft:
    def get_liquidaciones(self, rut: str, anio: int, mes: int, cantidad_meses: int) -> Trabajador:
        """
        Obtiene las liquidaciones de un trabajador en el sistema Peoplesoft.
        
        Args:
            rut: Identificador del trabajador
            anio: Año desde el cual serán consultadas las liquidaciones
            mes: Mes desde el cual serán consultadas las liquidaciones
            cantidad_meses: Cantidad de meses para atrás que serán consultadas
            
        Returns:
            Objeto Trabajador con sus datos y liquidaciones
            
        Raises:
            TrabajadorNotFoundException: Si no se encuentra al trabajador
            LiquidacionesNotFoundException: Si el trabajador existe pero no tiene liquidaciones
            DatabaseConnectionError: Si hay un error de conexión a la base de datos
            Exception: Para otros errores no controlados
        """
        try:
            with oracle_connection() as connection:
                with connection.cursor() as cursor:
                    out_cur = cursor.var(oracledb.CURSOR)
                    out_status = cursor.var(int)
                    out_message = cursor.var(str)

                    cursor.callproc("LMD_SP_GET_LIQUIDACIONES", [out_cur, rut, out_status, out_message])

                    res_cur = out_cur.getvalue()
                    res_status = out_status.getvalue()
                    res_message = out_message.getvalue()

                    if res_status == 1:
                        print(f"Error: {res_message}")
                        raise TrabajadorNoExisteException(rut)
                    elif res_status == 2:
                        print(f"Error: {res_message}")
                        raise SinLiquidacionesException(rut)
                    elif res_status < 0:
                        print(f"Error: {res_message}")
                        raise

                    items = list(res_cur)  # Convierte el cursor a una lista

                    list_liquidaciones = self.format_liquidaciones(items)

                    list_liquidaciones_sorted = sorted(list_liquidaciones, key=lambda l: (l.anio, l.mes))
                    
                    # Obtener la liquidación más reciente
                    last_liq = list_liquidaciones_sorted[-1]
                    
                    # Filtrar liquidaciones por periodo solicitado
                    list_liquidaciones_filtered = self.filtrar_liquidaciones(list_liquidaciones_sorted, int(anio), int(mes), int(cantidad_meses))
                    
                    # Obtener datos completos del trabajador
                    worker_data = self.get_liquidaciones_data(rut, last_liq.compania, anio, mes, last_liq.nombre_trabajador, list_liquidaciones_filtered)
                    
                    return worker_data
                    
        except TrabajadorNoExisteException:
            raise TrabajadorNoExisteException(f"No se encontró al trabajador con RUT: {rut}")
        except SinLiquidacionesException:
            raise SinLiquidacionesException(f"El trabajador con RUT: {rut} existe pero no tiene liquidaciones registradas")
        except oracledb.DatabaseError as e:
            error_code = e.args[0].code if hasattr(e.args[0], 'code') else 'desconocido'
            error_msg = e.args[0].message if hasattr(e.args[0], 'message') else str(e)
            raise oracledb.DatabaseError(f"Error de conexión a la base de datos (código {error_code}): {error_msg}")
        except Exception as e:
            raise Exception(f"Error no controlado: {str(e)}")

    def filtrar_liquidaciones(self, lista_liquidaciones: List[Liquidacion], anio: int, 
                             mes: int, cantidad_meses: int) -> List[Liquidacion]:
        """
        Filtra las liquidaciones según periodo solicitado.
        
        Args:
            lista_liquidaciones: Lista completa de liquidaciones
            anio: Año de referencia 
            mes: Mes de referencia
            cantidad_meses: Cantidad de meses anteriores a incluir
            
        Returns:
            Lista filtrada de liquidaciones
        """
        # Crear una lista de los periodos requeridos
        periodos = []
        for i in range(cantidad_meses):
            nuevo_mes = mes - i
            nuevo_anio = anio

            # Ajustar el año y el mes si el mes es menor o igual a 0
            while nuevo_mes <= 0:
                nuevo_mes += 12
                nuevo_anio -= 1
            
            periodos.append((nuevo_anio, nuevo_mes))
        
        # Filtrar las liquidaciones según los periodos generados
        liquidaciones_filtradas = [
            l for l in lista_liquidaciones if (l.anio, l.mes) in periodos
        ]
        
        # Ordenar por año y mes descendente
        liquidaciones_filtradas.sort(key=lambda l: (l.anio, l.mes), reverse=True)
        
        return liquidaciones_filtradas

    def format_liquidaciones(self, liquidaciones: List[tuple]) -> List[Liquidacion]:
        """
        Formatea la lista de liquidaciones a objetos Liquidacion.
        
        Args:
            liquidaciones: Lista de tuplas con datos de liquidaciones
            
        Returns:
            Lista de objetos Liquidacion
        """
        return [
            Liquidacion(
                anio=int(liquidacion[0]),
                mes=int(liquidacion[1]),
                nombre_trabajador=liquidacion[2],
                compania=liquidacion[3],
                nombre_documento=liquidacion[4],
                archivo_blob=liquidacion[5],
                monto_remuneracion=int(liquidacion[6]) if liquidacion[6] is not None else 0,
                imponible_cesantia=int(liquidacion[7]) if liquidacion[7] is not None else 0,
            ) for liquidacion in liquidaciones
        ]

    def get_liquidaciones_data(self, emplid: str, company: str, year: str, month: str, name: str, liquidaciones: List[Trabajador]):
        """Obtiene los datos de liquidación específicos de un trabajador."""
        try:
            with oracle_connection() as connection:
                with connection.cursor() as cursor:
                    out_cur = cursor.var(oracledb.CURSOR)
                    out_status = cursor.var(int)
                    out_message = cursor.var(str)

                    cursor.callproc("LMD_SP_GET_LIQUIDACIONES_DATA", [out_cur, emplid, company, year, month, out_status, out_message])
                    
                    res_cur = out_cur.getvalue()
                    res_status = out_status.getvalue()
                    res_message = out_message.getvalue()

                    if res_status == 1:
                        print(f"Error: {res_message}")
                        raise TrabajadorNoExisteException(emplid)
                    elif res_status == 2:
                        print(f"Error: {res_message}")
                        raise SinLiquidacionesException(emplid)
                    elif res_status < 0:
                        print(f"Error: {res_message}")
                        raise                    

                    items = list(res_cur)
                    if not items:
                        raise ValueError("No se encontraron datos de liquidación")

                    return self.format_liquidaciones_data(items, emplid, name, company, liquidaciones)

        except oracledb.DatabaseError as e:
            raise ValueError(f"Error de base de datos: {e}")
        except Exception as e:
            raise e

    def format_liquidaciones_data(self, data: List[tuple], emplid: str, name: str, company: str, liquidaciones: List[Liquidacion]) -> Trabajador:
        """
        Formatea los datos de liquidación en un objeto Trabajador.
        
        Args:
            data: Datos del trabajador
            emplid: RUT del trabajador
            name: Nombre del trabajador
            company: Código de la compañía
            liquidaciones: Lista de liquidaciones del trabajador
            
        Returns:
            Objeto Trabajador con todos sus datos
        """
        try:
            row = data[0]
            fecha_contrato = row[2].strftime("%Y-%m-%d") if row[2] else None
            fecha_afiliacion = row[3].strftime("%Y-%m-%d") if row[3] else None
            
            return Trabajador(
                rut=emplid,
                nombre=name,
                empresa=company,
                tipo_contrato=row[0] or "",
                afc=row[1] or "",
                fecha_contrato_trabajo=fecha_contrato or "",
                fecha_afiliacion=fecha_afiliacion or "",
                actividad_laboral=row[4] or "",
                caja_compensacion=row[5] or "",
                direccion_trabajo=row[6] or "",
                ocupacion=row[7] or "",
                calidad_trabajador=row[8] or "",
                regimen_previsional=row[9] or "",
                institucion_previsional=row[10] or "",
                institucion_salud=row[11] or "",
                renta_imponible=int(row[12]) if row[12] is not None else 0,
                jubilado=row[13] or "",
                liquidaciones=liquidaciones
            )
        except (IndexError, TypeError) as e:
            raise ValueError(f"Error al formatear datos del trabajador: {str(e)}")