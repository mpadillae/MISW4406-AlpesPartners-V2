# Alpes Partners (Patrón Saga)

Implementación del patrón **Saga con orquestación** para transacciones distribuidas en la creación de campañas publicitarias. El servicio de afiliaciones coordina las operaciones en los servicios de influencer, marca y tracking.

## Arquitectura

| Aspecto | Antes | Después (Saga con orquestación) |
|---------|-------------------|----------------------|
| **Flujo** | `Afiliaciones → Publica "CampanaCreada" → [Influencer, Marca, Tracking] procesan` | `Afiliaciones (Coordinador) → Secuencial: 1. Notificar Influencers → 2. Notificar Marca → 3. Inicializar Tracking` |
| **Control de fallos** | Sin control de fallos | Control centralizado con compensaciones automáticas |
| **Garantías transaccionales** | No existen | Consistencia transaccional garantizada |
| **Compensaciones** | No implementadas | Compensaciones en orden inverso automáticas |
| **Observabilidad** | Limitada | Logs detallados de cada paso y saga |

## Estructura

```
afiliaciones/
├── modulos/sagas/
│   ├── aplicacion/
│   │   ├── comandos/           # Comandos por servicio
│   │   └── coordinadores/      # Coordinador principal y logging
│   └── dominio/eventos/        # Eventos de saga
├── aplicacion/
│   ├── servicios.py           # Servicio original
│   └── servicios_saga.py      # Servicio con Saga
├── api/endpoints.py           # Endpoints REST
└── logs/sagas/               # Logs de saga
```

## Componentes

### Coordinador (`saga_campana.py`)
- `iniciar_saga_campana()`: Punto de entrada
- `_ejecutar_saga()`: Secuencia de pasos
- `_compensar_saga()`: Compensaciones en orden inverso

### Comandos
- `ComandoNotificarInfluencer`: Notificaciones a influencers
- `ComandoNotificarMarca`: Notificaciones a marca
- `ComandoInicializarTracking`: Setup de tracking

Cada comando implementa `ejecutar()` y `compensar()`.

## API Rest

#### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/campana-saga` | Crear campaña con patrón Saga |
| `GET` | `/saga/{id_saga}/estado` | Obtener estado de saga específica |
| `GET` | `/sagas/historial` | Obtener historial completo de sagas |
| `GET` | `/sagas/estadisticas` | Obtener estadísticas de rendimiento |

**Crear campaña con Saga:**
```bash
POST /campana-saga
{
    "nombre": "Campaña de Verano 2024",
    "descripcion": "Promoción de productos de verano con influencers",
    "tipo": "influencer",
    "fecha_inicio": "2025-01-01T00:00:00",
    "fecha_fin": "2025-12-31T23:59:59",
    "presupuesto": 15000,
    "marca": {
        "id_marca": "{{marca_id}}",
        "nombre_marca": "Nike"
    },
    "influencers": [
        {
            "nombre": "Ana García",
            "plataforma": "Instagram",
            "seguidores": 150000,
            "categoria": "Fitness"
        },
        {
            "nombre": "Carlos López",
            "plataforma": "TikTok",
            "seguidores": 300000,
            "categoria": "Lifestyle"
        }
    ]
}
```

**Consultar estado de saga:**
```bash
GET /saga/{id_saga}/estado
```

**Obtener estadísticas:**
```bash
GET /sagas/estadisticas
```

## Tipos de fallo simulados
- **Influencer** (5%)
- **Marca** (10%)
- **Tracking** (15%)

## Logging

### General
- Archivo: `logs/sagas/sagas_general.log`
- Incluye: inicio, finalización, errores.

### Por Saga
- Archivo: `logs/sagas/saga_{id}.log`
- Incluye: cada paso, compensaciones, métricas.

## Ventajas

- **Consistencia**: Garantías transaccionales
- **Observabilidad**: Logs detallados de cada paso
- **Recuperación**: Compensaciones automáticas
- **Escalabilidad**: Coordinación centralizada

## Limitaciones

- **Latencia**: Ejecución secuencial
- **Punto único**: Coordinador como dependencia crítica
- **Complejidad**: Lógica de compensación por comando