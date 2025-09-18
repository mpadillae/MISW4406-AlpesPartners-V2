from typing import List, Dict, Any, Optional
import uuid
import asyncio
from datetime import datetime
from dataclasses import dataclass, field

from ..comandos.influencer import ComandoNotificarInfluencer, ManejadorInfluencer
from ..comandos.marca import ComandoNotificarMarca, ManejadorMarca
from ..comandos.tracking import ComandoInicializarTracking, ManejadorTracking
from ...dominio.eventos.eventos_saga import (
    SagaCampanaCompletada, 
    SagaCampanaFallida, 
    SagaCampanaCompensada
)
from .saga_logger import SagaLogger


@dataclass
class EstadoSaga:
    id_saga: uuid.UUID
    id_campana: uuid.UUID
    id_marca: uuid.UUID
    fecha_inicio: datetime
    estado: str
    pasos_completados: List[str] = field(default_factory=list)
    pasos_fallidos: List[str] = field(default_factory=list)
    pasos_compensados: List[str] = field(default_factory=list)
    detalles_error: Optional[str] = None
    resultados: Dict[str, Any] = field(default_factory=dict)
    timestamps_pasos: Dict[str, datetime] = field(default_factory=dict)
    
    def agregar_resultado_paso(self, paso: str, resultado: Dict[str, Any]):
        self.resultados[paso] = resultado
        if paso not in self.pasos_completados:
            self.pasos_completados.append(paso)
    
    def obtener_timestamp_paso(self, paso: str) -> datetime:
        return self.timestamps_pasos.get(paso, self.fecha_inicio)
    
    def registrar_inicio_paso(self, paso: str):
        self.timestamps_pasos[paso] = datetime.now()


class CoordinadorSagaCampana:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CoordinadorSagaCampana, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.saga_logger = SagaLogger()
            self.manejador_influencer = ManejadorInfluencer()
            self.manejador_marca = ManejadorMarca()
            self.manejador_tracking = ManejadorTracking()
            self.sagas_activas: Dict[str, EstadoSaga] = {}
            self.historial_sagas: Dict[str, EstadoSaga] = {}
            self.__class__._initialized = True
    
    async def iniciar_saga_campana(
        self, 
        id_campana: uuid.UUID, 
        id_marca: uuid.UUID,
        detalles_campana: Dict[str, Any]
    ) -> EstadoSaga:
        id_saga = uuid.uuid4()
        
        estado_saga = EstadoSaga(
            id_saga=id_saga,
            id_campana=id_campana,
            id_marca=id_marca,
            fecha_inicio=datetime.now(),
            estado='iniciada'
        )
        
        self.sagas_activas[str(id_saga)] = estado_saga
        self.saga_logger.iniciar_saga(id_saga, id_campana, id_marca, detalles_campana)
        
        try:
            await self._ejecutar_saga(estado_saga, detalles_campana)
        except Exception as e:
            self.saga_logger.fallar_paso(estado_saga.id_saga, "saga_general", str(e))
            estado_saga.estado = 'fallida'
            estado_saga.detalles_error = str(e)
            await self._compensar_saga(estado_saga, detalles_campana)
        
        return estado_saga
    
    async def _ejecutar_saga(self, estado_saga: EstadoSaga, detalles_campana: Dict[str, Any]):
        await self._notificar_influencers(estado_saga, detalles_campana)
        await self._notificar_marca(estado_saga, detalles_campana)
        await self._inicializar_tracking(estado_saga, detalles_campana)
        
        estado_saga.estado = 'completada'
        self.historial_sagas[str(estado_saga.id_saga)] = estado_saga
        
        self.saga_logger.completar_saga(
            estado_saga.id_saga, 
            'completada', 
            estado_saga.pasos_completados
        )
        
        evento_completada = SagaCampanaCompletada(
            id_saga=estado_saga.id_saga,
            id_campana=estado_saga.id_campana,
            id_marca=estado_saga.id_marca,
            servicios_completados=estado_saga.pasos_completados.copy()
        )
        
        estado_saga.resultados['evento_final'] = evento_completada
    
    async def _notificar_influencers(self, estado_saga: EstadoSaga, detalles_campana: Dict[str, Any]):
        paso = "notificar_influencers"
        estado_saga.registrar_inicio_paso(paso)
        
        influencers = detalles_campana.get('influencers', [])
        self.saga_logger.ejecutar_paso(estado_saga.id_saga, paso, f"Notificando {len(influencers)} influencers")
        
        resultados_influencers = []
        
        for influencer in influencers:
            comando = ComandoNotificarInfluencer(
                id_saga=estado_saga.id_saga,
                id_campana=estado_saga.id_campana,
                id_influencer=influencer.get('nombre', ''),
                nombre_influencer=influencer.get('nombre', ''),
                plataforma=influencer.get('plataforma', ''),
                seguidores=influencer.get('seguidores', 0),
                categoria=influencer.get('categoria', ''),
                detalles_campana=detalles_campana
            )
            
            resultado = await self.manejador_influencer.notificar_influencer(comando)
            if not resultado["exitoso"]:
                estado_saga.pasos_fallidos.append(f"{paso}_{influencer.get('nombre', '')}")
                error_msg = f"Fallo notificando influencer {influencer.get('nombre', '')}: {resultado['error']}"
                self.saga_logger.fallar_paso(estado_saga.id_saga, paso, error_msg)
                raise Exception(error_msg)
            
            resultados_influencers.append(resultado["resultado"])
        
        estado_saga.pasos_completados.append(paso)
        estado_saga.resultados[paso] = resultados_influencers
        self.saga_logger.completar_paso(estado_saga.id_saga, paso, resultados_influencers)
    
    async def _notificar_marca(self, estado_saga: EstadoSaga, detalles_campana: Dict[str, Any]):
        paso = "notificar_marca"
        estado_saga.registrar_inicio_paso(paso)
        
        marca_nombre = detalles_campana.get('nombre_marca', '')
        self.saga_logger.ejecutar_paso(estado_saga.id_saga, paso, f"Notificando marca: {marca_nombre}")
        
        comando = ComandoNotificarMarca(
            id_saga=estado_saga.id_saga,
            id_campana=estado_saga.id_campana,
            id_marca=estado_saga.id_marca,
            nombre_marca=detalles_campana.get('nombre_marca', ''),
            detalles_campana=detalles_campana,
            influencers_asignados=detalles_campana.get('influencers', [])
        )
        
        resultado = await self.manejador_marca.notificar_marca(comando)
        if not resultado["exitoso"]:
            estado_saga.pasos_fallidos.append(paso)
            error_msg = f"Fallo notificando marca: {resultado['error']}"
            self.saga_logger.fallar_paso(estado_saga.id_saga, paso, error_msg)
            raise Exception(error_msg)
        
        estado_saga.pasos_completados.append(paso)
        estado_saga.resultados[paso] = resultado["resultado"]
        self.saga_logger.completar_paso(estado_saga.id_saga, paso, resultado["resultado"])
    
    async def _inicializar_tracking(self, estado_saga: EstadoSaga, detalles_campana: Dict[str, Any]):
        paso = "inicializar_tracking"
        estado_saga.registrar_inicio_paso(paso)
        
        campana_nombre = detalles_campana.get('nombre', '')
        self.saga_logger.ejecutar_paso(estado_saga.id_saga, paso, f"Inicializando tracking para: {campana_nombre}")
        
        comando = ComandoInicializarTracking(
            id_saga=estado_saga.id_saga,
            id_campana=estado_saga.id_campana,
            id_marca=estado_saga.id_marca,
            nombre_campana=detalles_campana.get('nombre', ''),
            tipo_campana=detalles_campana.get('tipo', ''),
            presupuesto=detalles_campana.get('presupuesto', 0.0),
            influencers=detalles_campana.get('influencers', []),
            metricas_objetivo=detalles_campana.get('metricas_objetivo', {})
        )
        
        resultado = await self.manejador_tracking.inicializar_tracking(comando)
        if not resultado["exitoso"]:
            estado_saga.pasos_fallidos.append(paso)
            raise Exception(f"Fallo inicializando tracking: {resultado['error']}")
        
        tracking_id = resultado["resultado"].get("tracking_id", "")
        estado_saga.agregar_resultado_paso(paso, {"tracking_id": tracking_id})
        
        self.saga_logger.completar_paso(
            estado_saga.id_saga,
            paso,
            {
                "tracking_id": tracking_id,
                "campana_nombre": campana_nombre,
                "resultado": resultado["resultado"]
            }
        )
    
    async def _compensar_saga(self, estado_saga: EstadoSaga, detalles_campana: Dict[str, Any]):
        self.saga_logger.iniciar_compensacion(
            estado_saga.id_saga,
            f"Iniciando compensaciones para {len(estado_saga.pasos_completados)} pasos completados"
        )
        estado_saga.estado = 'compensando'
        
        pasos_a_compensar = list(reversed(estado_saga.pasos_completados))
        
        for paso in pasos_a_compensar:
            try:
                await self._compensar_paso(paso, estado_saga, detalles_campana)
                estado_saga.pasos_compensados.append(paso)
                self.saga_logger.completar_compensacion(
                    estado_saga.id_saga,
                    paso,
                    "Compensación ejecutada exitosamente"
                )
            except Exception as e:
                self.saga_logger.fallar_compensacion(
                    estado_saga.id_saga,
                    paso,
                    f"Error en compensación: {str(e)}",
                    e
                )
        
        estado_saga.estado = 'compensada'
        self.saga_logger.finalizar_saga(
            estado_saga.id_saga,
            'compensada',
            f"Saga compensada con {len(estado_saga.pasos_compensados)} pasos compensados"
        )
        
        self.historial_sagas[str(estado_saga.id_saga)] = estado_saga
        
        evento_compensada = SagaCampanaCompensada(
            id_saga=estado_saga.id_saga,
            id_campana=estado_saga.id_campana,
            id_marca=estado_saga.id_marca,
            servicios_compensados=estado_saga.pasos_compensados.copy()
        )
        
        estado_saga.resultados['evento_compensacion'] = evento_compensada
    
    async def _compensar_paso(self, paso: str, estado_saga: EstadoSaga, detalles_campana: Dict[str, Any]):
        if paso == "inicializar_tracking":
            comando = ComandoInicializarTracking(
                id_saga=estado_saga.id_saga,
                id_campana=estado_saga.id_campana,
                nombre_campana=detalles_campana.get('nombre', '')
            )
            await self.manejador_tracking.compensar_tracking(comando)
            
        elif paso == "notificar_marca":
            comando = ComandoNotificarMarca(
                id_saga=estado_saga.id_saga,
                id_campana=estado_saga.id_campana,
                id_marca=estado_saga.id_marca,
                nombre_marca=detalles_campana.get('nombre_marca', '')
            )
            await self.manejador_marca.compensar_marca(comando)
            
        elif paso == "notificar_influencers":
            influencers = detalles_campana.get('influencers', [])
            for influencer in influencers:
                comando = ComandoNotificarInfluencer(
                    id_saga=estado_saga.id_saga,
                    id_campana=estado_saga.id_campana,
                    id_influencer=influencer.get('nombre', ''),
                    nombre_influencer=influencer.get('nombre', '')
                )
                await self.manejador_influencer.compensar_influencer(comando)
    
    def _mover_saga_a_historial(self, estado_saga: EstadoSaga):
        id_saga_str = str(estado_saga.id_saga)
        if id_saga_str in self.sagas_activas:
            self.historial_sagas[id_saga_str] = estado_saga
            del self.sagas_activas[id_saga_str]
            self.saga_logger.log_mensaje(
                estado_saga.id_saga,
                "INFO",
                f"Saga movida al historial con estado: {estado_saga.estado}"
            )
    
    def obtener_estado_saga(self, id_saga: uuid.UUID) -> Optional[EstadoSaga]:
        id_saga_str = str(id_saga)
        if id_saga_str in self.sagas_activas:
            return self.sagas_activas[id_saga_str]
        return self.historial_sagas.get(id_saga_str)
    
    def obtener_todas_sagas(self) -> Dict[str, EstadoSaga]:
        todas_sagas = {}
        todas_sagas.update(self.sagas_activas)
        todas_sagas.update(self.historial_sagas)
        return todas_sagas
    
    def obtener_historial_sagas(self) -> Dict[str, EstadoSaga]:
        return {k: v for k, v in self.historial_sagas.items() 
                if v.estado in ['completada', 'compensada']}
    
    def obtener_estadisticas_sagas(self) -> Dict[str, Any]:
        todas_sagas = self.obtener_todas_sagas()
        
        estadisticas = {
            'total_sagas': len(todas_sagas),
            'sagas_activas': len(self.sagas_activas),
            'sagas_completadas': len([s for s in todas_sagas.values() if s.estado == 'completada']),
            'sagas_compensadas': len([s for s in todas_sagas.values() if s.estado == 'compensada']),
            'sagas_en_proceso': len([s for s in todas_sagas.values() if s.estado in ['iniciada', 'compensando']]),
            'tasa_exito': 0.0
        }
        
        if estadisticas['total_sagas'] > 0:
            estadisticas['tasa_exito'] = (estadisticas['sagas_completadas'] / estadisticas['total_sagas']) * 100
        
        return estadisticas