from dataclasses import dataclass, field
from typing import Any, Dict, List
import uuid
import asyncio
import random
from .base import ComandoSaga, ManejadorComandoSaga


@dataclass
class ComandoInicializarTracking(ComandoSaga):
    id_marca: uuid.UUID = None
    nombre_campana: str = None
    tipo_campana: str = None
    presupuesto: float = 0.0
    influencers: List[Dict[str, Any]] = field(default_factory=list)
    metricas_objetivo: Dict[str, Any] = field(default_factory=dict)
    
    async def ejecutar(self) -> Dict[str, Any]:
        if random.random() < 0.15:
            raise Exception(f"Error en base de datos de tracking para campaña {self.nombre_campana}")
        
        metricas_iniciales = {
            "impresiones": 0,
            "clicks": 0,
            "conversiones": 0,
            "engagement_rate": 0.0,
            "ctr": 0.0,
            "roi": 0.0,
            "influencers_activos": len(self.influencers),
            "presupuesto_utilizado": 0.0,
            "presupuesto_total": self.presupuesto
        }
        
        return {
            "id_campana": str(self.id_campana),
            "nombre": self.nombre_campana,
            "tracking_id": str(uuid.uuid4()),
            "metricas_iniciales": metricas_iniciales,
            "dashboard_url": f"https://tracking.alpespartners.com/campaigns/{self.id_campana}",
            "estado": "tracking_inicializado"
        }
    
    async def compensar(self) -> Dict[str, Any]:
        return {
            "id_campana": str(self.id_campana),
            "nombre": self.nombre_campana,
            "mensaje": f"Tracking eliminado para campaña {self.nombre_campana}",
            "estado": "tracking_compensado"
        }


class ManejadorTracking(ManejadorComandoSaga):
    
    async def inicializar_tracking(self, comando: ComandoInicializarTracking) -> Dict[str, Any]:
        self.logger.info(f"Iniciando tracking para campaña: {comando.nombre_campana}")
        resultado = await self.manejar_comando(comando)
        
        if resultado["exitoso"]:
            self.logger.info(f"Tracking inicializado exitosamente para campaña {comando.nombre_campana}")
        else:
            self.logger.error(f"Fallo al inicializar tracking para campaña {comando.nombre_campana}: {resultado['error']}")
        
        return resultado
    
    async def compensar_tracking(self, comando: ComandoInicializarTracking) -> Dict[str, Any]:
        self.logger.info(f"Iniciando compensación de tracking para campaña: {comando.nombre_campana}")
        resultado = await self.manejar_compensacion(comando)
        
        if resultado["exitoso"]:
            self.logger.info(f"Compensación de tracking para campaña {comando.nombre_campana} completada")
        else:
            self.logger.error(f"Fallo en compensación de tracking para campaña {comando.nombre_campana}: {resultado['error']}")
        
        return resultado