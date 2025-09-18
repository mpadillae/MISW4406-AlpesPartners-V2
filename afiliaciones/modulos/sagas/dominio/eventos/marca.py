from dataclasses import dataclass
import uuid
from .eventos_saga import EventoSaga


@dataclass
class ComandoNotificarMarca(EventoSaga):
    id_marca: uuid.UUID = None
    nombre_marca: str = None
    detalles_campana: dict = None
    influencers_asignados: list = None


@dataclass
class ComandoCompensarMarca(EventoSaga):
    id_marca: uuid.UUID = None
    nombre_marca: str = None
    motivo_compensacion: str = None