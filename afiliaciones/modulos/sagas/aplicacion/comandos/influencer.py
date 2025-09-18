from dataclasses import dataclass
from typing import Any, Dict
import uuid
import asyncio
import random
from .base import ComandoSaga, ManejadorComandoSaga


@dataclass
class ComandoNotificarInfluencer(ComandoSaga):
    id_influencer: str = None
    nombre_influencer: str = None
    plataforma: str = None
    seguidores: int = 0
    categoria: str = None
    detalles_campana: Dict[str, Any] = None
    
    async def ejecutar(self) -> Dict[str, Any]:
        if random.random() < 0.05:
            raise Exception(f"Error de red al notificar influencer {self.nombre_influencer}")
        
        return {
            "id_influencer": self.id_influencer,
            "nombre": self.nombre_influencer,
            "mensaje": f"Influencer {self.nombre_influencer} notificado sobre campaña {self.detalles_campana.get('nombre', 'N/A')}",
            "estado": "notificado"
        }
    
    async def compensar(self) -> Dict[str, Any]:
        return {
            "id_influencer": self.id_influencer,
            "nombre": self.nombre_influencer,
            "mensaje": f"Notificación cancelada para influencer {self.nombre_influencer}",
            "estado": "compensado"
        }


class ManejadorInfluencer(ManejadorComandoSaga):
    
    async def notificar_influencer(self, comando: ComandoNotificarInfluencer) -> Dict[str, Any]:
        self.logger.info(f"Iniciando notificación a influencer: {comando.nombre_influencer}")
        resultado = await self.manejar_comando(comando)
        
        if resultado["exitoso"]:
            self.logger.info(f"Influencer {comando.nombre_influencer} notificado exitosamente")
        else:
            self.logger.error(f"Fallo al notificar influencer {comando.nombre_influencer}: {resultado['error']}")
        
        return resultado
    
    async def compensar_influencer(self, comando: ComandoNotificarInfluencer) -> Dict[str, Any]:
        self.logger.info(f"Iniciando compensación para influencer: {comando.nombre_influencer}")
        resultado = await self.manejar_compensacion(comando)
        
        if resultado["exitoso"]:
            self.logger.info(f"Compensación para influencer {comando.nombre_influencer} completada")
        else:
            self.logger.error(f"Fallo en compensación de influencer {comando.nombre_influencer}: {resultado['error']}")
        
        return resultado