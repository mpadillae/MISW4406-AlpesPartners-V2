import json
import pulsar
from pulsar.schema import *
from . import utils


class Despachador:
    def __init__(self):
        self.broker_host = utils.broker_host()
        self.client = pulsar.Client(f'pulsar://{self.broker_host}:6650')

    def publicar_mensaje(self, mensaje, topico, schema):
        """
        Publicar mensaje en un tópico de Pulsar
        """
        try:
            producer = self.client.create_producer(
                topico,
                schema=AvroSchema(None, schema_definition=schema)
            )
            producer.send(mensaje)
            producer.close()
            print(f"Mensaje publicado en {topico}: {mensaje}")
        except Exception as e:
            print(f"Error publicando mensaje: {e}")
            raise e

    def cerrar(self):
        """Cerrar conexión con Pulsar"""
        self.client.close()
