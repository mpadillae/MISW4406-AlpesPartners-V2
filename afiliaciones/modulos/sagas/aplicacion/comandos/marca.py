from dataclasses import dataclass
from typing import Any, Dict, List
import uuid
import asyncio
import random
from .base import ComandoSaga, ManejadorComandoSaga


@dataclass
class ComandoNotificarMarca(ComandoSaga):
    id_marca: uuid.UUID = None
    nombre_marca: str = None
    detalles_campana: Dict[str, Any] = None
    influencers_asignados: List[Dict[str, Any]] = None
    
    async def ejecutar(self) -> Dict[str, Any]:
        if random.random() < 0.10:
            raise Exception(f"Error en sistema de notificaciones de marca {self.nombre_marca}")
        
        return {
            "id_marca": str(self.id_marca),
            "nombre": self.nombre_marca,
            "mensaje": f"Marca {self.nombre_marca} notificada sobre campaña {self.detalles_campana.get('nombre', 'N/A')}",
            "influencers_count": len(self.influencers_asignados) if self.influencers_asignados else 0,
            "estado": "notificada"
        }
    
    async def compensar(self) -> Dict[str, Any]:
        return {
            "id_marca": str(self.id_marca),
            "nombre": self.nombre_marca,
            "mensaje": f"Notificación de campaña cancelada para marca {self.nombre_marca}",
            "estado": "compensado"
        }


class ManejadorMarca(ManejadorComandoSaga):
    
    async def notificar_marca(self, comando: ComandoNotificarMarca) -> Dict[str, Any]:
        self.logger.info(f"Iniciando notificación a marca: {comando.nombre_marca}")
        resultado = await self.manejar_comando(comando)
        
        if resultado["exitoso"]:
            self.logger.info(f"Marca {comando.nombre_marca} notificada exitosamente")
        else:
            self.logger.error(f"Fallo al notificar marca {comando.nombre_marca}: {resultado['error']}")
        
        return resultado
    
    async def compensar_marca(self, comando: ComandoNotificarMarca) -> Dict[str, Any]:
        self.logger.info(f"Iniciando compensación para marca: {comando.nombre_marca}")
        resultado = await self.manejar_compensacion(comando)
        
        if resultado["exitoso"]:
            self.logger.info(f"Compensación para marca {comando.nombre_marca} completada")
        else:
            self.logger.error(f"Fallo en compensación de marca {comando.nombre_marca}: {resultado['error']}")
        
        return resultado