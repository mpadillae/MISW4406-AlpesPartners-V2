import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'BROKER_HOST'


def time_millis():
    """Obtener timestamp en milisegundos"""
    return int(time.time() * 1000)


def unix_time_millis(dt):
    """Convertir datetime a milisegundos unix"""
    return (dt - epoch).total_seconds() * 1000.0


def millis_a_datetime(millis):
    """Convertir milisegundos a datetime"""
    return datetime.datetime.fromtimestamp(millis/1000.0)


def broker_host():
    """Obtener host del broker de Pulsar"""
    return os.getenv(PULSAR_ENV, default="localhost")


def consultar_schema_registry(topico: str) -> dict:
    """Consultar schema registry de Pulsar"""
    try:
        json_registry = requests.get(
            f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
        return json.loads(json_registry.get('data', {}))
    except Exception as e:
        print(f"Error consultando schema registry: {e}")
        return {}


def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    """Convertir schema JSON a AvroSchema"""
    try:
        definicion_schema = parse_schema(json_schema)
        return AvroSchema(None, schema_definition=definicion_schema)
    except Exception as e:
        print(f"Error creando schema Avro: {e}")
        return AvroSchema(None, schema_definition={})
