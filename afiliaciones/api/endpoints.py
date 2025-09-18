from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from datetime import datetime
from aplicacion.dto import CrearCampanaRequest, CampanaResponse, IniciarCampanaRequest, CampanaListResponse
from aplicacion.comandos.crear_campana import CrearCampana
from aplicacion.comandos.iniciar_campana import IniciarCampana
from aplicacion.queries.obtener_campana import ObtenerCampana, ObtenerTodasCampanas
from aplicacion.handlers import (
    ManejadorCrearCampana,
    ManejadorIniciarCampana,
    ManejadorObtenerCampana,
    ManejadorObtenerTodasCampanas
)
from aplicacion.servicios import ServicioAplicacionCampana
from aplicacion.servicios_saga import ServicioAplicacionCampanaSaga
from infraestructura.fabricas import FabricaRepositorio, FabricaDespachador

router = APIRouter()

def obtener_servicio_campana() -> ServicioAplicacionCampana:
    repositorio = FabricaRepositorio.crear_repositorio_campana()
    despachador = FabricaDespachador.crear_despachador()
    return ServicioAplicacionCampana(repositorio, despachador)


def obtener_servicio_campana_saga() -> ServicioAplicacionCampanaSaga:
    repositorio = FabricaRepositorio.crear_repositorio_campana()
    despachador = FabricaDespachador.crear_despachador()
    return ServicioAplicacionCampanaSaga(repositorio, despachador)


@router.post("/campana", response_model=CampanaResponse)
async def crear_campana(
    request: CrearCampanaRequest,
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        comando = CrearCampana(
            id_marca=request.marca.id_marca,
            nombre=request.nombre,
            descripcion=request.descripcion,
            tipo=request.tipo,
            presupuesto=request.presupuesto,
            nombre_marca=request.marca.nombre_marca,
            influencers=request.influencers,
            fecha_inicio=request.fecha_inicio,
            fecha_fin=request.fecha_fin
        )

        manejador = ManejadorCrearCampana(servicio)
        resultado = await manejador.ejecutar(comando)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/campana/{id_campana}/iniciar", response_model=CampanaResponse)
async def iniciar_campana(
    id_campana: uuid.UUID,
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        comando = IniciarCampana(id_campana=id_campana)
        manejador = ManejadorIniciarCampana(servicio)
        resultado = await manejador.ejecutar(comando)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/campana/{id_campana}", response_model=CampanaResponse)
async def obtener_campana(
    id_campana: uuid.UUID,
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        query = ObtenerCampana(id_campana=id_campana)
        manejador = ManejadorObtenerCampana(servicio)
        resultado = await manejador.ejecutar(query)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/campanas", response_model=CampanaListResponse)
async def obtener_todas_campanas(
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        query = ObtenerTodasCampanas()
        manejador = ManejadorObtenerTodasCampanas(servicio)
        resultado = await manejador.ejecutar(query)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ENDPOINTS PARA SAGA

@router.post("/campana-saga", response_model=dict)
async def crear_campana_con_saga(
    request: CrearCampanaRequest,
    servicio: ServicioAplicacionCampanaSaga = Depends(obtener_servicio_campana_saga)
):
    try:
        resultado = await servicio.crear_campana_con_saga(
            id_marca=request.marca.id_marca,
            nombre=request.nombre,
            descripcion=request.descripcion,
            tipo=request.tipo,
            presupuesto=request.presupuesto,
            nombre_marca=request.marca.nombre_marca,
            influencers=request.influencers,
            fecha_inicio=request.fecha_inicio,
            fecha_fin=request.fecha_fin
        )

        return {
            "mensaje": "Campaña procesada con patrón Saga",
            "saga_exitosa": resultado["saga_exitosa"],
            "estado_saga": resultado["estado_saga"].estado,
            "id_saga": str(resultado["estado_saga"].id_saga),
            "id_campana": str(resultado["campana"].id),
            "pasos_completados": resultado["estado_saga"].pasos_completados,
            "pasos_compensados": resultado["estado_saga"].pasos_compensados,
            "error": resultado["estado_saga"].detalles_error,
            "campana": {
                "id": str(resultado["campana"].id),
                "nombre": resultado["campana"].nombre,
                "estado": resultado["campana"].estado.value,
                "presupuesto": resultado["campana"].presupuesto
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/saga/{id_saga}/estado", response_model=dict)
async def obtener_estado_saga(
    id_saga: uuid.UUID,
    servicio: ServicioAplicacionCampanaSaga = Depends(obtener_servicio_campana_saga)
):
    try:
        estado = await servicio.obtener_estado_saga(id_saga)
        if not estado:
            raise HTTPException(status_code=404, detail="Saga no encontrada")
        
        return {
            "id_saga": str(estado.id_saga),
            "id_campana": str(estado.id_campana),
            "estado": estado.estado,
            "fecha_inicio": estado.fecha_inicio.isoformat(),
            "pasos_completados": estado.pasos_completados,
            "pasos_fallidos": estado.pasos_fallidos,
            "pasos_compensados": estado.pasos_compensados,
            "detalles_error": estado.detalles_error,
            "resultados": estado.resultados
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sagas", response_model=dict)
async def obtener_todas_sagas(
    servicio: ServicioAplicacionCampanaSaga = Depends(obtener_servicio_campana_saga)
):
    try:
        sagas = await servicio.obtener_todas_sagas()
        
        sagas_info = {}
        for id_saga, estado in sagas.items():
            sagas_info[id_saga] = {
                "id_saga": str(estado.id_saga),
                "id_campana": str(estado.id_campana),
                "estado": estado.estado,
                "fecha_inicio": estado.fecha_inicio.isoformat(),
                "pasos_completados": estado.pasos_completados,
                "pasos_fallidos": estado.pasos_fallidos,
                "pasos_compensados": estado.pasos_compensados,
                "tiene_errores": bool(estado.detalles_error),
                "detalles_error": estado.detalles_error
            }
        
        # Obtener estadísticas
        estadisticas = await servicio.obtener_estadisticas_sagas()
        
        return {
            "total_sagas": len(sagas_info),
            "estadisticas": estadisticas,
            "sagas": sagas_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sagas/historial", response_model=dict)
async def obtener_historial_sagas(
    servicio: ServicioAplicacionCampanaSaga = Depends(obtener_servicio_campana_saga)
):
    try:
        sagas = await servicio.obtener_historial_sagas()
        
        sagas_info = {}
        for id_saga, estado in sagas.items():
            sagas_info[id_saga] = {
                "id_saga": str(estado.id_saga),
                "id_campana": str(estado.id_campana),
                "estado": estado.estado,
                "fecha_inicio": estado.fecha_inicio.isoformat(),
                "pasos_completados": estado.pasos_completados,
                "pasos_compensados": estado.pasos_compensados,
                "exitosa": estado.estado == "completada",
                "detalles_error": estado.detalles_error if estado.estado == "compensada" else None
            }
        
        return {
            "total_sagas_historial": len(sagas_info),
            "sagas_completadas": len([s for s in sagas.values() if s.estado == "completada"]),
            "sagas_compensadas": len([s for s in sagas.values() if s.estado == "compensada"]),
            "historial": sagas_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sagas/estadisticas", response_model=dict)
async def obtener_estadisticas_sagas(
    servicio: ServicioAplicacionCampanaSaga = Depends(obtener_servicio_campana_saga)
):
    try:
        estadisticas = await servicio.obtener_estadisticas_sagas()
        return estadisticas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
