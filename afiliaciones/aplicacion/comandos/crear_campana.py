from dataclasses import dataclass
import uuid
from typing import List, Optional
from datetime import datetime
from .base import Comando


@dataclass
class CrearCampana(Comando):
    id_marca: uuid.UUID
    nombre: str
    descripcion: str
    tipo: str
    presupuesto: float
    nombre_marca: str
    influencers: List
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
