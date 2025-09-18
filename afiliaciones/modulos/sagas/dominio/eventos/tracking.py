from dataclasses import dataclass, field
import uuid
from .eventos_saga import EventoSaga


@dataclass
class ComandoInicializarTracking(EventoSaga):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    nombre_campana: str = None
    tipo_campana: str = None
    presupuesto: float = 0.0
    influencers: list = field(default_factory=list)
    metricas_objetivo: dict = field(default_factory=dict)


@dataclass
class ComandoCompensarTracking(EventoSaga):
    id_campana: uuid.UUID = None
    motivo_compensacion: str = None