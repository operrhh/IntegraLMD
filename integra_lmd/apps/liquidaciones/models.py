from typing import List

class Liquidacion:
    def __init__(self, anio: int, mes: int, nombre_documento: str, archivo_blob: bytes):
        if not 1 <= mes <= 12:
            raise ValueError("El mes debe estar entre 1 y 12.")
        self.anio = anio
        self.mes = mes
        self.nombre_documento = nombre_documento
        self.archivo = archivo_blob.read()
    
    def save_file(self, path: str):
        with open(path, 'wb') as archivo:
            archivo.write(self.archivo)

class Trabajador:
    def __init__(self, 
                rut: str,
                nombre: str, 
                tipo_contrato:str, 
                afc:bool, 
                fecha_contrato_trabajo:str,
                fecha_afiliacion:str,
                monto_remuneracion:int,
                imponible_cesantia:int,
                actividad_laboral:str,
                caja_compensacion:str,
                direccion_trabajo:str,
                ocupacion:str,
                calidad_trabajador:str,
                regimen_previsional:str,
                institucion_previsional:str,
                institucion_salud:str,
                liquidaciones: List[Liquidacion]):
        if not liquidaciones:
            raise ValueError("El trabajador debe tener al menos una liquidación.")
        self.rut = rut
        self.nombre = nombre
        self.tipo_contrato = tipo_contrato
        self.afc = afc
        self.liquidaciones = liquidaciones

    def format_json(self) -> dict:
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "liquidaciones": [
                {
                    "anio": liquidacion.anio,
                    "mes": liquidacion.mes,
                    "nombreDocumento": liquidacion.nombre_documento,
                }
                for liquidacion in self.liquidaciones
            ]
        }