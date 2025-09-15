from sqlalchemy import Column, String, DateTime, Float, UUID, JSON
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import json
from datetime import datetime

from dominio.entidades import Campana
from dominio.repositorios import RepositorioCampana
from dominio.objetos_valor import InfluencerInfo
from .dto import CampanaDTO
from .database import Base, db_manager


class CampanaDB(Base):
    __tablename__ = "campanas"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    tipo = Column(String(20), nullable=False)
    estado = Column(String(20), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    presupuesto = Column(Float, nullable=False)
    nombre_marca = Column(String(100), nullable=True)
    influencers = Column(JSON, nullable=True)


class RepositorioCampanaSQLAlchemy(RepositorioCampana):
    def __init__(self):
        pass

    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[Campana]:
        with db_manager.get_session() as session:
            campana_db = session.query(CampanaDB).filter(
                CampanaDB.id == id_campana).first()
            if campana_db:
                return self._db_a_entidad(campana_db)
            return None

    def obtener_todas(self) -> List[Campana]:
        with db_manager.get_session() as session:
            campanas_db = session.query(CampanaDB).all()
            return [self._db_a_entidad(campana_db) for campana_db in campanas_db]

    def agregar(self, campana: Campana) -> Campana:
        with db_manager.get_session() as session:
            campana_db = self._entidad_a_db(campana)
            session.add(campana_db)
            session.flush()  # Para obtener el ID generado
            session.refresh(campana_db)
            return self._db_a_entidad(campana_db)

    def actualizar(self, campana: Campana) -> Campana:
        with db_manager.get_session() as session:
            campana_db = session.query(CampanaDB).filter(
                CampanaDB.id == campana.id).first()
            if campana_db:
                campana_db.nombre = campana.nombre
                campana_db.descripcion = campana.descripcion
                campana_db.tipo = campana.tipo.value if campana.tipo else "influencer"
                campana_db.estado = campana.estado.value if campana.estado else "creada"
                campana_db.fecha_inicio = campana.fecha_inicio
                campana_db.fecha_fin = campana.fecha_fin
                campana_db.presupuesto = campana.presupuesto
                campana_db.nombre_marca = campana.nombre_marca
                campana_db.influencers = json.dumps([{
                    'nombre': inf.nombre,
                    'plataforma': inf.plataforma,
                    'seguidores': inf.seguidores,
                    'categoria': inf.categoria
                } for inf in campana.influencers]) if campana.influencers else "[]"
                session.flush()
                return self._db_a_entidad(campana_db)
            return campana

    def eliminar(self, id_campana: uuid.UUID) -> bool:
        with db_manager.get_session() as session:
            campana_db = session.query(CampanaDB).filter(
                CampanaDB.id == id_campana).first()
            if campana_db:
                session.delete(campana_db)
                return True
            return False

    def _entidad_a_db(self, campana: Campana) -> CampanaDB:
        return CampanaDB(
            id=campana.id,
            id_marca=campana.id_marca,
            nombre=campana.nombre,
            descripcion=campana.descripcion,
            tipo=campana.tipo.value if campana.tipo else "influencer",
            estado=campana.estado.value if campana.estado else "creada",
            fecha_creacion=campana.fecha_creacion,
            fecha_inicio=campana.fecha_inicio,
            fecha_fin=campana.fecha_fin,
            presupuesto=campana.presupuesto,
            nombre_marca=campana.nombre_marca,
            influencers=json.dumps([{
                'nombre': inf.nombre,
                'plataforma': inf.plataforma,
                'seguidores': inf.seguidores,
                'categoria': inf.categoria
            } for inf in campana.influencers]) if campana.influencers else "[]"
        )

    def _db_a_entidad(self, campana_db: CampanaDB) -> Campana:
        from dominio.objetos_valor import TipoCampana, EstadoCampana, InfluencerInfo
        
        influencers = []
        if campana_db.influencers:
            try:
                influencers_data = json.loads(campana_db.influencers) if isinstance(campana_db.influencers, str) else campana_db.influencers
                influencers = [
                    InfluencerInfo(
                        nombre=inf['nombre'],
                        plataforma=inf['plataforma'],
                        seguidores=inf['seguidores'],
                        categoria=inf['categoria']
                    ) for inf in influencers_data
                ]
            except (json.JSONDecodeError, KeyError):
                influencers = []

        return Campana(
            id=campana_db.id,
            id_marca=campana_db.id_marca,
            nombre=campana_db.nombre,
            descripcion=campana_db.descripcion,
            tipo=TipoCampana(campana_db.tipo),
            estado=EstadoCampana(campana_db.estado),
            fecha_creacion=campana_db.fecha_creacion,
            fecha_inicio=campana_db.fecha_inicio,
            fecha_fin=campana_db.fecha_fin,
            presupuesto=campana_db.presupuesto,
            nombre_marca=campana_db.nombre_marca,
            influencers=influencers
        )
