from typing import List
import uuid
from dominio.servicios import ServicioCampana
from dominio.repositorios import RepositorioCampana
from dominio.eventos import CampanaCreada
from dominio.objetos_valor import InfluencerInfo
from infraestructura.despachadores import Despachador


class ServicioAplicacionCampana:
    def __init__(self, repositorio: RepositorioCampana, despachador: Despachador):
        self.servicio_dominio = ServicioCampana(repositorio)
        self.despachador = despachador

    async def crear_campana(self, id_marca: uuid.UUID, nombre: str, descripcion: str,
                            tipo: str, presupuesto: float, nombre_marca: str, influencers: List,
                            fecha_inicio=None, fecha_fin=None):
        influencers_info = [
            InfluencerInfo(
                nombre=inf.nombre,
                plataforma=inf.plataforma,
                seguidores=inf.seguidores,
                categoria=inf.categoria
            ) for inf in influencers
        ]
        
        # Crear campaña usando el servicio de dominio
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

        # Crear evento de dominio
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

        # Publicar evento
        await self.despachador.publicar_evento(evento, "eventos-campana")

        return campana

    async def iniciar_campana(self, id_campana: uuid.UUID):
        campana = self.servicio_dominio.iniciar_campana(id_campana)

        # Obtener eventos de la campaña
        eventos = campana.obtener_eventos()
        for evento in eventos:
            await self.despachador.publicar_evento(evento, "eventos-campana")

        campana.limpiar_eventos()
        return campana

    async def obtener_campana(self, id_campana: uuid.UUID):
        return self.servicio_dominio.obtener_campana(id_campana)

    async def obtener_todas_campanas(self) -> List:
        return self.servicio_dominio.obtener_todas_campanas()
