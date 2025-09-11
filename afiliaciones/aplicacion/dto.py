from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class MarcaRequest(BaseModel):
    id_marca: uuid.UUID
    nombre_marca: str = Field(..., min_length=1, max_length=100)


class InfluencerRequest(BaseModel):
    nombre: str
    plataforma: str
    seguidores: int = 0
    categoria: str


class CrearCampanaRequest(BaseModel):
    marca: MarcaRequest
    nombre: str = Field(...)
    descripcion: str = Field(..., min_length=1, max_length=500)
    tipo: str = Field(...)
    presupuesto: float = Field(...)
    influencers: List[InfluencerRequest] = Field(default_factory=list)
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None


class MarcaResponse(BaseModel):
    id_marca: uuid.UUID
    nombre_marca: Optional[str] = None


class InfluencerResponse(BaseModel):
    nombre: str
    plataforma: str
    seguidores: int
    categoria: str


class CampanaResponse(BaseModel):
    id: uuid.UUID
    marca: MarcaResponse
    nombre: str
    descripcion: str
    tipo: str
    estado: str
    fecha_creacion: datetime
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: float
    influencers: List[InfluencerResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class IniciarCampanaRequest(BaseModel):
    id_campana: uuid.UUID


class CampanaListResponse(BaseModel):
    campanas: list[CampanaResponse]
    total: int
