from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid
from typing import Any, Dict
import logging


@dataclass
class ComandoSaga(ABC):
    id_saga: uuid.UUID = None
    id_campana: uuid.UUID = None
    
    @abstractmethod
    async def ejecutar(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def compensar(self) -> Dict[str, Any]:
        pass


class ManejadorComandoSaga:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def manejar_comando(self, comando: ComandoSaga) -> Dict[str, Any]:
        try:
            resultado = await comando.ejecutar()
            self.logger.info(f"Comando {comando.__class__.__name__} ejecutado exitosamente")
            return {"exitoso": True, "resultado": resultado}
        except Exception as e:
            self.logger.error(f"Error ejecutando comando {comando.__class__.__name__}: {str(e)}")
            return {"exitoso": False, "error": str(e)}
    
    async def manejar_compensacion(self, comando: ComandoSaga) -> Dict[str, Any]:
        try:
            resultado = await comando.compensar()
            self.logger.info(f"Compensación de {comando.__class__.__name__} ejecutada exitosamente")
            return {"exitoso": True, "resultado": resultado}
        except Exception as e:
            self.logger.error(f"Error en compensación de {comando.__class__.__name__}: {str(e)}")
            return {"exitoso": False, "error": str(e)}