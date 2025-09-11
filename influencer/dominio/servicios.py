from typing import List
import uuid
import json
from .entidades import Influencer, CampanaInfluencer
from .repositorios import RepositorioInfluencer, RepositorioCampanaInfluencer
from .eventos import InfluencerAsignado, CampanaProcesada


class ServicioInfluencer:
    def __init__(self, repositorio_influencer: RepositorioInfluencer, repositorio_campana: RepositorioCampanaInfluencer):
        self.repositorio_influencer = repositorio_influencer
        self.repositorio_campana = repositorio_campana

    def procesar_campana_creada(self, evento_data: dict) -> CampanaInfluencer:
        # Procesar y guardar influencers del evento
        influencers_creados = self._procesar_influencers_del_evento(evento_data)
        
        # Crear campaña de influencer
        campana = CampanaInfluencer()
        campana.procesar_campana_creada(evento_data)

        # Asignar influencer automáticamente (lógica de negocio)
        influencer = self._asignar_influencer_automatico(campana)
        if influencer:
            campana.asignar_influencer(influencer.id)

        # Guardar en repositorio
        campana_guardada = self.repositorio_campana.agregar(campana)

        # Crear evento de dominio
        evento = CampanaProcesada(
            id_campana=campana_guardada.id_campana,
            id_influencer=campana_guardada.id_influencer,
            id_marca=campana_guardada.id_marca,
            nombre_campana=campana_guardada.nombre_campana,
            estado=campana_guardada.estado,
            fecha_procesamiento=campana_guardada.fecha_asignacion
        )
        campana_guardada.agregar_evento(evento)

        return campana_guardada

    def procesar_campana_iniciada(self, evento_data: dict) -> CampanaInfluencer:
        # Buscar campaña existente
        id_campana = uuid.UUID(evento_data.get('id_campana'))
        campana = self.repositorio_campana.obtener_por_id(id_campana)

        if campana:
            campana.procesar_campana_iniciada(evento_data)
            return self.repositorio_campana.actualizar(campana)

        return None

    def _procesar_influencers_del_evento(self, evento_data: dict) -> List[Influencer]:
        influencers_creados = []
        
        # Obtener la cadena JSON de influencers
        influencers_json = evento_data.get('influencers', '[]')
        
        try:
            influencers_data = json.loads(influencers_json)
            
            for influencer_info in influencers_data:
                # Verificar si el influencer ya existe por nombre y plataforma
                influencer_existente = self._buscar_influencer_por_nombre_y_plataforma(
                    influencer_info.get('nombre'), 
                    influencer_info.get('plataforma')
                )
                
                if not influencer_existente:
                    # Crear nuevo influencer
                    influencer = Influencer()
                    influencer.nombre = influencer_info.get('nombre')
                    influencer.plataforma = influencer_info.get('plataforma')
                    influencer.seguidores = influencer_info.get('seguidores', 0)
                    influencer.categoria = influencer_info.get('categoria')
                    
                    # Guardar en repositorio
                    influencer_guardado = self.repositorio_influencer.agregar(influencer)
                    influencers_creados.append(influencer_guardado)
                else:
                    # Actualizar datos si es necesario
                    influencer_existente.seguidores = influencer_info.get('seguidores', influencer_existente.seguidores)
                    influencer_existente.categoria = influencer_info.get('categoria', influencer_existente.categoria)
                    self.repositorio_influencer.actualizar(influencer_existente)
                    influencers_creados.append(influencer_existente)
                    
        except json.JSONDecodeError:
            pass
            
        return influencers_creados

    def _buscar_influencer_por_nombre_y_plataforma(self, nombre: str, plataforma: str) -> Influencer:
        """Busca un influencer existente por nombre y plataforma"""
        influencers = self.repositorio_influencer.obtener_todos()
        for influencer in influencers:
            if influencer.nombre == nombre and influencer.plataforma == plataforma:
                return influencer
        return None

    def _asignar_influencer_automatico(self, campana: CampanaInfluencer) -> Influencer:
        # Lógica simple: obtener el primer influencer disponible
        influencers = self.repositorio_influencer.obtener_todos()
        if influencers:
            return influencers[0]
        return None

    def obtener_campanas_por_influencer(self, id_influencer: uuid.UUID) -> List[CampanaInfluencer]:
        return self.repositorio_campana.obtener_por_influencer(id_influencer)

    def obtener_todas_campanas(self) -> List[CampanaInfluencer]:
        return self.repositorio_campana.obtener_todas()
