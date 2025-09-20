# BFF (Backend for Frontend) - Alpes Partners

## Resumen

Se ha implementado exitosamente un BFF (Backend for Frontend) para el sistema Alpes Partners que actúa como una capa de abstracción unificada para los microservicios de Afiliaciones y Tracking.

## 🏗️ Arquitectura Implementada

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   BFF Service   │    │  Microservices  │
│   (Cliente)     │◄──►│   (Puerto 8005) │◄──►│  Afiliaciones   │
└─────────────────┘    │                 │    │  (Puerto 8001)  │
                       │                 │    └─────────────────┘
                       │                 │    ┌─────────────────┐
                       │                 │◄──►│  Tracking       │
                       │                 │    │  (Puerto 8004)  │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Apache Pulsar  │
                       │  (Eventos)      │
                       └─────────────────┘
```

## ✅ Funcionalidades Implementadas

### 1. **Endpoints de Afiliaciones** (Replicados exactamente)

- `POST /afiliaciones/campana` - Crear campaña
- `POST /afiliaciones/campana/{id}/iniciar` - Iniciar campaña
- `GET /afiliaciones/campana/{id}` - Obtener campaña por ID
- `GET /afiliaciones/campanas` - Obtener todas las campañas
- `POST /afiliaciones/campana-saga` - Crear campaña con saga
- `GET /afiliaciones/saga/{id}/estado` - Obtener estado de saga
- `GET /afiliaciones/sagas` - Obtener todas las sagas
- `GET /afiliaciones/sagas/historial` - Obtener historial de sagas
- `GET /afiliaciones/sagas/estadisticas` - Obtener estadísticas de sagas

### 2. **Endpoints de Tracking** (Replicados exactamente)

- `POST /tracking/evento` - Registrar evento de tracking
- `GET /tracking/metricas/{id_campana}` - Obtener métricas por campaña
- `GET /tracking/eventos/{id_campana}` - Obtener eventos por campaña
- `GET /tracking/metricas/marca/{id_marca}` - Obtener métricas por marca

### 3. **Endpoints del Sistema**

- `GET /health` - Health check del BFF
- `GET /events` - Obtener eventos recientes de Pulsar
- `GET /docs` - Documentación automática (Swagger)

## 🚀 Cómo Ejecutar

### Opción 1: Docker Compose (Recomendado)

```bash
# Ejecutar todos los servicios incluyendo el BFF
docker-compose up

# Verificar que el BFF esté funcionando
curl http://localhost:8005/health
```

### Opción 2: Desarrollo Local

```bash
# 1. Ejecutar servicios base
docker-compose up pulsar afiliaciones-service tracking-service

# 2. En otra terminal, ejecutar el BFF
cd bff
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8005 --reload
```

## 🧪 Testing

### Script de Prueba Automatizado

```bash
# Ejecutar script de prueba
python test_bff.py
```

### Postman

1. Importar la collection: `collections/Alpes Partners BFF.postman_collection.json`
2. Importar el environment: `collections/Alpes Partners.postman_environment.json`
3. Ejecutar las pruebas en el orden sugerido

### Pruebas Manuales

```bash
# Health check
curl http://localhost:8005/health

# Crear campaña
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

## 📊 Monitoreo y Logs

### Health Checks

- **BFF**: `http://localhost:8005/health`
- **Afiliaciones**: `http://localhost:8001/health`
- **Tracking**: `http://localhost:8004/health`

### Eventos en Tiempo Real

- **Eventos BFF**: `http://localhost:8005/events`

### Documentación API

- **Swagger UI**: `http://localhost:8005/docs`
- **ReDoc**: `http://localhost:8005/redoc`

## 🔧 Configuración

### Variables de Entorno del BFF

```bash
AFILIACIONES_SERVICE_URL=http://afiliaciones-service:8000
TRACKING_SERVICE_URL=http://tracking-service:8000
PULSAR_URL=pulsar://pulsar:6650
BROKER_HOST=pulsar
```

### Puertos Utilizados

- **BFF**: 8005
- **Afiliaciones**: 8001
- **Tracking**: 8004
- **Marca**: 8002
- **Influencer**: 8003
- **Pulsar**: 6650 (cliente), 8080 (admin)

## 📁 Estructura del Proyecto

```
MISW4406-AlpesPartners-V2/
├── bff/                          # 🆕 BFF Service
│   ├── main.py                   # Aplicación principal
│   ├── consumidores.py           # Consumidores Pulsar
│   ├── despachadores.py          # Despachadores Pulsar
│   ├── servicios.py              # Servicios HTTP
│   ├── utils.py                  # Utilidades
│   ├── api/
│   │   ├── afiliaciones.py       # Endpoints afiliaciones
│   │   └── tracking.py           # Endpoints tracking
│   ├── requirements.txt          # Dependencias
│   ├── Dockerfile               # Imagen Docker
│   └── README.md                # Documentación BFF
├── afiliaciones/                 # Servicio original
├── tracking/                     # Servicio original
├── marca/                        # Servicio original
├── influencer/                   # Servicio original
├── collections/                  # 🆕 Postman Collections
│   ├── Alpes Partners BFF.postman_collection.json
│   └── Alpes Partners.postman_environment.json
├── docker-compose.yml            # 🆕 Actualizado con BFF
├── test_bff.py                  # 🆕 Script de pruebas
└── README_BFF.md                # 🆕 Este archivo
```

## 🎯 Beneficios del BFF

1. **Unificación**: Un solo punto de entrada para el frontend
2. **Abstracción**: El frontend no necesita conocer la estructura interna de microservicios
3. **Flexibilidad**: Fácil agregación de datos de múltiples servicios
4. **Mantenibilidad**: Cambios en microservicios no afectan al frontend
5. **Escalabilidad**: El BFF puede ser escalado independientemente
6. **Monitoreo**: Punto centralizado para logs y métricas

## 🔄 Flujo de Comunicación

1. **Frontend** → **BFF** (HTTP REST)
2. **BFF** → **Microservicios** (HTTP REST)
3. **BFF** ↔ **Pulsar** (Eventos asíncronos)
4. **Microservicios** → **BFF** (Respuestas HTTP)
5. **BFF** → **Frontend** (Respuestas HTTP)

## 📈 Próximos Pasos

1. **Autenticación**: Implementar JWT o OAuth2
2. **Caché**: Agregar Redis para mejorar performance
3. **Rate Limiting**: Implementar límites de velocidad
4. **Logging**: Integrar con ELK Stack o similar
5. **Métricas**: Integrar con Prometheus/Grafana
6. **Circuit Breaker**: Implementar patrón Circuit Breaker
7. **API Gateway**: Considerar usar Kong o similar para funcionalidades avanzadas

## 🐛 Troubleshooting

### Problemas Comunes

1. **BFF no responde**:

   - Verificar que los servicios backend estén ejecutándose
   - Revisar logs: `docker-compose logs bff-service`

2. **Error de conexión a servicios**:

   - Verificar variables de entorno
   - Comprobar que los servicios estén en la misma red Docker

3. **Eventos no llegan**:
   - Verificar conexión a Pulsar
   - Revisar configuración de tópicos

### Logs Útiles

```bash
# Logs del BFF
docker-compose logs -f bff-service

# Logs de todos los servicios
docker-compose logs -f

# Estado de contenedores
docker-compose ps
```

## 📞 Soporte

Para problemas o preguntas sobre el BFF:

1. Revisar este README
2. Consultar logs de los servicios
3. Ejecutar el script de prueba `test_bff.py`
4. Verificar la documentación automática en `/docs`
