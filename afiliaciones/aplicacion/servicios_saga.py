from typing import List
import uuid
from dominio.servicios import ServicioCampana
from dominio.repositorios import RepositorioCampana
from dominio.eventos import CampanaCreada
from dominio.objetos_valor import InfluencerInfo
from infraestructura.despachadores import Despachador
from modulos.sagas.aplicacion.coordinadores.saga_campana import CoordinadorSagaCampana


class ServicioAplicacionCampanaSaga:
    _coordinador_saga = None
    
    def __init__(self, repositorio: RepositorioCampana, despachador: Despachador):
        self.servicio_dominio = ServicioCampana(repositorio)
        self.despachador = despachador
        
        if ServicioAplicacionCampanaSaga._coordinador_saga is None:
            ServicioAplicacionCampanaSaga._coordinador_saga = CoordinadorSagaCampana()
        self.coordinador_saga = ServicioAplicacionCampanaSaga._coordinador_saga

    async def crear_campana_con_saga(self, id_marca: uuid.UUID, nombre: str, descripcion: str,
                                    tipo: str, presupuesto: float, nombre_marca: str, influencers: List,
                                    fecha_inicio=None, fecha_fin=None):
        try:
            influencers_info = [
                InfluencerInfo(
                    nombre=inf.nombre,
                    plataforma=inf.plataforma,
                    seguidores=inf.seguidores,
                    categoria=inf.categoria
                ) for inf in influencers
            ]
            
            campana = self.servicio_dominio.crear_campana(
                id_marca=id_marca,
                nombre=nombre,
                descripcion=descripcion,
                tipo=tipo,
                presupuesto=presupuesto,
                nombre_marca=nombre_marca,
                influencers=influencers_info,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            detalles_campana = {
                'id_campana': campana.id,
                'id_marca': campana.id_marca,
                'nombre': campana.nombre,
                'descripcion': campana.descripcion,
                'tipo': campana.tipo.value,
                'estado': campana.estado.value,
                'fecha_creacion': campana.fecha_creacion,
                'presupuesto': campana.presupuesto,
                'nombre_marca': campana.nombre_marca,
                'influencers': [{
                    'nombre': inf.nombre,
                    'plataforma': inf.plataforma,
                    'seguidores': inf.seguidores,
                    'categoria': inf.categoria
                } for inf in campana.influencers],
                'metricas_objetivo': {
                    'impresiones_objetivo': presupuesto * 100,
                    'engagement_objetivo': 0.05,
                    'conversiones_objetivo': presupuesto * 0.02
                }
            }

            estado_saga = await self.coordinador_saga.iniciar_saga_campana(
                id_campana=campana.id,
                id_marca=campana.id_marca,
                detalles_campana=detalles_campana
            )

            if estado_saga.estado == 'completada':
                evento = CampanaCreada(
                    id_campana=campana.id,
                    id_marca=campana.id_marca,
                    nombre=campana.nombre,
                    descripcion=campana.descripcion,
                    tipo=campana.tipo.value,
                    estado=campana.estado.value,
                    fecha_creacion=campana.fecha_creacion,
                    presupuesto=campana.presupuesto,
                    nombre_marca=campana.nombre_marca,
                    influencers=[{
                        'nombre': inf.nombre,
                        'plataforma': inf.plataforma,
                        'seguidores': inf.seguidores,
                        'categoria': inf.categoria
                    } for inf in campana.influencers]
                )

                await self.despachador.publicar_evento(evento, "eventos-campana")
            
            elif estado_saga.estado == 'compensada':
                raise Exception(f"Error en procesamiento distribuido: {estado_saga.detalles_error}")

            return {
                'campana': campana,
                'estado_saga': estado_saga,
                'saga_exitosa': estado_saga.estado == 'completada'
            }

        except Exception as e:
            raise

    async def iniciar_campana(self, id_campana: uuid.UUID):
        campana = self.servicio_dominio.iniciar_campana(id_campana)
        eventos = campana.obtener_eventos()
        for evento in eventos:
            await self.despachador.publicar_evento(evento, "eventos-campana")
        campana.limpiar_eventos()
        return campana

    async def obtener_campana(self, id_campana: uuid.UUID):
        return self.servicio_dominio.obtener_campana(id_campana)

    async def obtener_todas_campanas(self) -> List:
        return self.servicio_dominio.obtener_todas_campanas()
    
    async def obtener_estado_saga(self, id_saga: uuid.UUID):
        return self.coordinador_saga.obtener_estado_saga(id_saga)
    
    async def obtener_todas_sagas(self):
        return self.coordinador_saga.obtener_todas_sagas()
    
    async def obtener_historial_sagas(self):
        return self.coordinador_saga.obtener_historial_sagas()
    
    async def obtener_estadisticas_sagas(self):
        return self.coordinador_saga.obtener_estadisticas_sagas()