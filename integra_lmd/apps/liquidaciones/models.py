from typing import List

class Liquidacion:
    def __init__(self, anio: int, mes: int, nombre_documento: str, archivo_blob: bytes, nombre_trabajador:str, compania:str, monto_remuneracion:int, imponible_cesantia:int):
        if not 1 <= mes <= 12:
            raise ValueError("El mes debe estar entre 1 y 12.")
        self.anio = anio
        self.mes = mes
        self.nombre_documento = nombre_documento
        self.archivo = archivo_blob.read()
        self.nombre_trabajador = nombre_trabajador
        self.compania = compania
        self.monto_remuneracion = monto_remuneracion
        self.imponible_cesantia = imponible_cesantia
    
    def save_file(self, path: str):
        with open(path, 'wb') as archivo:
            archivo.write(self.archivo)

class Trabajador:
    def __init__(self, 
                rut: str,
                nombre: str,
                empresa: str,
                tipo_contrato:str, 
                afc:bool, 
                fecha_contrato_trabajo:str,
                fecha_afiliacion:str,
                actividad_laboral:str,
                caja_compensacion:str,
                direccion_trabajo:str,
                ocupacion:str,
                calidad_trabajador:str,
                regimen_previsional:str,
                institucion_previsional:str,
                institucion_salud:str,
                renta_imponible:str,
                liquidaciones: List[Liquidacion]):
        if not liquidaciones:
            raise ValueError("El trabajador debe tener al menos una liquidación.")
        self.rut = rut
        self.nombre = nombre
        self.empresa = empresa
        self.tipo_contrato = tipo_contrato
        self.afc = afc
        self.fecha_contrato_trabajo = fecha_contrato_trabajo
        self.fecha_afiliacion = fecha_afiliacion
        self.actividad_laboral = actividad_laboral
        self.caja_compensacion = caja_compensacion
        self.direccion_trabajo = direccion_trabajo
        self.ocupacion = ocupacion
        self.calidad_trabajador = calidad_trabajador
        self.regimen_previsional = regimen_previsional
        self.institucion_previsional = institucion_previsional
        self.institucion_salud = institucion_salud
        self.renta_imponible = renta_imponible
        self.liquidaciones = liquidaciones

    def format_json(self) -> dict:
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "empresa": self.empresa,
            "tipoContrato": self.tipo_contrato,
            "afc": self.afc,
            "fechaContratoTrabajo": self.fecha_contrato_trabajo,
            "fechaAfiliacion": self.fecha_afiliacion,
            "actividadLaboral": self.actividad_laboral,
            "cajaCompensacion": self.caja_compensacion,
            "direccionTrabajo": self.direccion_trabajo,
            "ocupacion": self.ocupacion,
            "calidadTrabajador": self.calidad_trabajador,
            "regimenPrevisional": self.regimen_previsional,
            "institucionPrevisional": self.institucion_previsional,
            "institucionSalud": self.institucion_salud,
            "rentaImponible": self.renta_imponible,
            "liquidaciones": [
                {
                    "anio": liquidacion.anio,
                    "mes": liquidacion.mes,
                    "nombreDocumento": liquidacion.nombre_documento,
                    "montoRemuneracion": liquidacion.monto_remuneracion,
                    "imponibleCesantia": liquidacion.imponible_cesantia
                }
                for liquidacion in self.liquidaciones
            ]
        }