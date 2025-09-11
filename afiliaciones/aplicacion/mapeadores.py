from .dto import CampanaResponse, InfluencerResponse, MarcaResponse
from dominio.entidades import Campana


class MapeadorCampana:
    @staticmethod
    def entidad_a_dto(campana: Campana) -> CampanaResponse:
        influencers_dto = [
            InfluencerResponse(
                nombre=inf.nombre,
                plataforma=inf.plataforma,
                seguidores=inf.seguidores,
                categoria=inf.categoria
            ) for inf in campana.influencers
        ]
        
        marca_dto = MarcaResponse(
            id_marca=campana.id_marca,
            nombre_marca=campana.nombre_marca or ""
        )
        
        return CampanaResponse(
            id=campana.id,
            marca=marca_dto,
            nombre=campana.nombre,
            descripcion=campana.descripcion,
            tipo=campana.tipo.value if campana.tipo else "influencer",
            estado=campana.estado.value if campana.estado else "creada",
            fecha_creacion=campana.fecha_creacion,
            fecha_inicio=campana.fecha_inicio,
            fecha_fin=campana.fecha_fin,
            presupuesto=campana.presupuesto,
            influencers=influencers_dto
        )

    @staticmethod
    def dto_a_entidad(dto: CampanaResponse) -> Campana:
        from dominio.objetos_valor import TipoCampana, EstadoCampana, InfluencerInfo

        influencers_info = [
            InfluencerInfo(
                nombre=inf.nombre,
                plataforma=inf.plataforma,
                seguidores=inf.seguidores,
                categoria=inf.categoria
            ) for inf in dto.influencers
        ]

        return Campana(
            id=dto.id,
            id_marca=dto.marca.id_marca,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            tipo=TipoCampana(dto.tipo),
            estado=EstadoCampana(dto.estado),
            fecha_creacion=dto.fecha_creacion,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            presupuesto=dto.presupuesto,
            nombre_marca=dto.marca.nombre_marca,
            influencers=influencers_info
        )
