from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from servicios import servicio_afiliaciones

router = APIRouter()

# DTOs


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

# Endpoints


@router.post("/campana")
async def crear_campana(request: CrearCampanaRequest):
    """Crear una nueva campaña"""
    try:
        # Convertir UUIDs y datetime a strings para la serialización JSON
        data = request.dict()
        if 'marca' in data and 'id_marca' in data['marca']:
            data['marca']['id_marca'] = str(data['marca']['id_marca'])
        if 'fecha_inicio' in data and data['fecha_inicio'] is not None:
            data['fecha_inicio'] = data['fecha_inicio'].isoformat()
        if 'fecha_fin' in data and data['fecha_fin'] is not None:
            data['fecha_fin'] = data['fecha_fin'].isoformat()
        response = await servicio_afiliaciones.post("/afiliaciones/campana", data)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/campana/{id_campana}/iniciar")
async def iniciar_campana(id_campana: uuid.UUID):
    """Iniciar una campaña existente"""
    try:
        response = await servicio_afiliaciones.post(f"/afiliaciones/campana/{str(id_campana)}/iniciar", {})
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campana/{id_campana}")
async def obtener_campana(id_campana: uuid.UUID):
    """Obtener una campaña por ID"""
    try:
        response = await servicio_afiliaciones.get(f"/afiliaciones/campana/{str(id_campana)}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campanas")
async def obtener_todas_campanas():
    """Obtener todas las campañas"""
    try:
        response = await servicio_afiliaciones.get("/afiliaciones/campanas")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints Saga


@router.post("/campana-saga", response_model=dict)
async def crear_campana_con_saga(request: CrearCampanaRequest):
    """Crear campaña usando patrón Saga"""
    try:
        # Convertir UUIDs y datetime a strings para la serialización JSON
        data = request.dict()
        if 'marca' in data and 'id_marca' in data['marca']:
            data['marca']['id_marca'] = str(data['marca']['id_marca'])
        if 'fecha_inicio' in data and data['fecha_inicio'] is not None:
            data['fecha_inicio'] = data['fecha_inicio'].isoformat()
        if 'fecha_fin' in data and data['fecha_fin'] is not None:
            data['fecha_fin'] = data['fecha_fin'].isoformat()
        response = await servicio_afiliaciones.post("/afiliaciones/campana-saga", data)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saga/{id_saga}/estado", response_model=dict)
async def obtener_estado_saga(id_saga: uuid.UUID):
    """Obtener estado de una saga"""
    try:
        response = await servicio_afiliaciones.get(f"/afiliaciones/saga/{str(id_saga)}/estado")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sagas", response_model=dict)
async def obtener_todas_sagas():
    """Obtener todas las sagas"""
    try:
        response = await servicio_afiliaciones.get("/afiliaciones/sagas")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sagas/historial", response_model=dict)
async def obtener_historial_sagas():
    """Obtener historial de sagas"""
    try:
        response = await servicio_afiliaciones.get("/afiliaciones/sagas/historial")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sagas/estadisticas", response_model=dict)
async def obtener_estadisticas_sagas():
    """Obtener estadísticas de sagas"""
    try:
        response = await servicio_afiliaciones.get("/afiliaciones/sagas/estadisticas")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
