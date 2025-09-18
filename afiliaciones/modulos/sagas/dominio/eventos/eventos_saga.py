from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import List, Optional


@dataclass
class EventoSaga:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default_factory=datetime.now)
    id_saga: uuid.UUID = None
    id_campana: uuid.UUID = None


@dataclass
class InfluencerNotificado(EventoSaga):
    id_influencer: str = None
    nombre_influencer: str = None
    mensaje: str = None


@dataclass
class InfluencerNotificacionFallida(EventoSaga):
    id_influencer: str = None
    nombre_influencer: str = None
    razon_falla: str = None


@dataclass
class InfluencerNotificacionCompensada(EventoSaga):
    id_influencer: str = None
    nombre_influencer: str = None


@dataclass
class MarcaNotificada(EventoSaga):
    id_marca: uuid.UUID = None
    nombre_marca: str = None
    mensaje: str = None


@dataclass
class MarcaNotificacionFallida(EventoSaga):
    id_marca: uuid.UUID = None
    nombre_marca: str = None
    razon_falla: str = None


@dataclass
class MarcaNotificacionCompensada(EventoSaga):
    id_marca: uuid.UUID = None
    nombre_marca: str = None


@dataclass
class TrackingInicializado(EventoSaga):
    id_campana: uuid.UUID = None
    metricas_iniciales: dict = field(default_factory=dict)


@dataclass
class TrackingInicializacionFallida(EventoSaga):
    id_campana: uuid.UUID = None
    razon_falla: str = None


@dataclass
class TrackingCompensado(EventoSaga):
    id_campana: uuid.UUID = None


@dataclass
class SagaCampanaCompletada(EventoSaga):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    servicios_completados: List[str] = field(default_factory=list)


@dataclass
class SagaCampanaFallida(EventoSaga):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    razon_falla: str = None
    servicios_compensados: List[str] = field(default_factory=list)


@dataclass
class SagaCampanaCompensada(EventoSaga):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    servicios_compensados: List[str] = field(default_factory=list)