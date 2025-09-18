from dataclasses import dataclass
from .eventos_saga import EventoSaga


@dataclass
class ComandoNotificarInfluencer(EventoSaga):
    id_influencer: str = None
    nombre_influencer: str = None
    plataforma: str = None
    seguidores: int = 0
    categoria: str = None
    detalles_campana: dict = None


@dataclass
class ComandoCompensarInfluencer(EventoSaga):
    id_influencer: str = None
    nombre_influencer: str = None
    motivo_compensacion: str = None