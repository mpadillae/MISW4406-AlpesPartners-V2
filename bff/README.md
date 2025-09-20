# BFF (Backend for Frontend) - Alpes Partners

Este es el BFF (Backend for Frontend) para el sistema Alpes Partners. Actúa como una capa de abstracción que expone los endpoints de los microservicios de Afiliaciones y Tracking de manera unificada.

## Arquitectura

El BFF se comunica con los siguientes servicios:

- **Afiliaciones Service** (puerto 8001): Gestión de campañas y sagas
- **Tracking Service** (puerto 8004): Métricas y eventos de campañas

## Características

- **REST API**: Expone endpoints REST que replican exactamente la funcionalidad de los servicios originales
- **Comunicación HTTP**: Se comunica con los servicios backend via HTTP
- **Comunicación Asíncrona**: Maneja eventos de Pulsar para funcionalidades en tiempo real
- **Proxy Transparente**: Actúa como proxy sin modificar las respuestas de los servicios originales
- **Health Checks**: Incluye endpoints de monitoreo y salud del sistema

## Endpoints Disponibles

### Afiliaciones

- `POST /afiliaciones/campana` - Crear campaña
- `POST /afiliaciones/campana/{id}/iniciar` - Iniciar campaña
- `GET /afiliaciones/campana/{id}` - Obtener campaña por ID
- `GET /afiliaciones/campanas` - Obtener todas las campañas
- `POST /afiliaciones/campana-saga` - Crear campaña con saga
- `GET /afiliaciones/saga/{id}/estado` - Obtener estado de saga
- `GET /afiliaciones/sagas` - Obtener todas las sagas
- `GET /afiliaciones/sagas/historial` - Obtener historial de sagas
- `GET /afiliaciones/sagas/estadisticas` - Obtener estadísticas de sagas

### Tracking

- `POST /tracking/evento` - Registrar evento de tracking
- `GET /tracking/metricas/{id_campana}` - Obtener métricas por campaña
- `GET /tracking/eventos/{id_campana}` - Obtener eventos por campaña
- `GET /tracking/metricas/marca/{id_marca}` - Obtener métricas por marca

### Sistema

- `GET /health` - Health check del BFF
- `GET /events` - Obtener eventos recientes de Pulsar

## Configuración

### Variables de Entorno

- `AFILIACIONES_SERVICE_URL`: URL del servicio de afiliaciones (default: http://afiliaciones-service:8000)
- `TRACKING_SERVICE_URL`: URL del servicio de tracking (default: http://tracking-service:8000)
- `PULSAR_URL`: URL de Pulsar (default: pulsar://pulsar:6650)
- `BROKER_HOST`: Host del broker de Pulsar (default: localhost)

### Puerto

El BFF se ejecuta en el puerto **8005**.

## Ejecución

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el BFF
uvicorn main:app --host 0.0.0.0 --port 8005 --reload
```

### Docker

```bash
# Construir imagen
docker build -t alpes-partners/bff .

# Ejecutar contenedor
docker run -p 8005:8005 alpes-partners/bff
```

### Docker Compose

```bash
# Ejecutar todos los servicios incluyendo el BFF
docker-compose up

# Ejecutar solo el BFF y sus dependencias
docker-compose up bff-service afiliaciones-service tracking-service pulsar
```

## Testing

### Postman

Se incluye una collection de Postman específica para el BFF:

- `Alpes Partners BFF.postman_collection.json`

### Health Check

```bash
curl http://localhost:8005/health
```

### Ejemplo de Uso

```bash
# Crear una campaña
curl -X POST http://localhost:8005/afiliaciones/campana \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Campaña Test",
    "descripcion": "Descripción de prueba",
    "tipo": "influencer",
    "presupuesto": 1000,
    "marca": {
      "id_marca": "123e4567-e89b-12d3-a456-426614174000",
      "nombre_marca": "Test Brand"
    },
    "influencers": []
  }'
```

## Estructura del Proyecto

```
bff/
├── main.py                 # Aplicación principal FastAPI
├── consumidores.py         # Consumidores de eventos de Pulsar
├── despachadores.py        # Despachadores de comandos a Pulsar
├── servicios.py            # Servicios HTTP para comunicación con backend
├── utils.py                # Utilidades comunes
├── api/
│   ├── afiliaciones.py     # Endpoints de afiliaciones
│   └── tracking.py         # Endpoints de tracking
├── requirements.txt        # Dependencias de Python
├── Dockerfile             # Imagen Docker
└── README.md              # Este archivo
```

## Dependencias

- **FastAPI**: Framework web para la API
- **httpx**: Cliente HTTP asíncrono
- **pulsar-client**: Cliente para Apache Pulsar
- **pydantic**: Validación de datos
- **uvicorn**: Servidor ASGI

## Monitoreo

El BFF incluye:

- Health checks para verificar el estado del servicio
- Endpoint de eventos para monitorear mensajes de Pulsar
- Logs estructurados para debugging
- Manejo de errores con códigos HTTP apropiados
