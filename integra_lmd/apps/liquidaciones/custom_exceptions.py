class LiquidacionException(Exception):
    """Excepción base para errores en el servicio de liquidaciones."""
    pass

class TrabajadorNoExisteException(LiquidacionException):
    """Excepción para el caso en que no existe el trabajador."""
    def __init__(self, rut=None):
        self.rut = rut
        message = f"No se encontró ningún trabajador con RUT {rut}" if rut else "No se encontró al trabajador"
        super().__init__(message)

class SinLiquidacionesException(LiquidacionException):
    """Excepción para el caso en que el trabajador existe pero no tiene liquidaciones."""
    def __init__(self, rut=None):
        self.rut = rut
        message = f"El trabajador con RUT {rut} no tiene liquidaciones disponibles" if rut else "El trabajador no tiene liquidaciones disponibles"
        super().__init__(message)

class SinDatosLiquidacionException(LiquidacionException):
    """Excepción para el caso en que no se pueden obtener los datos detallados de liquidación."""
    def __init__(self, rut=None, anio=None, mes=None):
        self.rut = rut
        self.anio = anio
        self.mes = mes
        message = f"No se encontraron datos para la liquidación del periodo {mes}/{anio}" if anio and mes else "No se encontraron datos de liquidación"
        if rut:
            message += f" para el trabajador con RUT {rut}"
        super().__init__(message)