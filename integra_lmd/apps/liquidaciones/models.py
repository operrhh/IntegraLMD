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
    def __init__(self, rut: str, nombre: str, liquidaciones: List[Liquidacion]):
        if not liquidaciones:
            raise ValueError("El trabajador debe tener al menos una liquidación.")
        self.rut = rut
        self.nombre = nombre
        self.liquidaciones = liquidaciones

    def format_json(self) -> dict:
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "liquidaciones": [
                {
                    "anio": liquidacion.anio,
                    "mes": liquidacion.mes,
                    "nombreDocumento": liquidacion.nombre_documento
                }
                for liquidacion in self.liquidaciones
            ]
        }