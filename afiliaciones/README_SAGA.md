# Patrón Saga con Orquestación - Alpes Partners

## Descripción

Implementación del patrón Saga con orquestación para transacciones distribuidas en la creación de campañas publicitarias. El servicio de afiliaciones coordina las operaciones en los servicios de influencer, marca y tracking.

## Arquitectura

### Antes (Coreografía)
```
Afiliaciones → Publica "CampanaCreada" → [Influencer, Marca, Tracking] procesan
```
Sin control de fallos, sin compensaciones, sin garantías transaccionales.

### Después (Orquestación)
```
Afiliaciones (Coordinador) → Secuencial:
  1. Notificar Influencers
  2. Notificar Marca  
  3. Inicializar Tracking
  
Si falla → Compensa en orden inverso
```
Control centralizado, compensaciones automáticas, consistencia transaccional.

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

## Flujo

### Exitoso
1. Crear Campaña → 2. Notificar Influencers → 3. Notificar Marca → 4. Inicializar Tracking → Completar

### Con Fallo
1-3. Exitosos → 4. Tracking falla → Compensar: Tracking, Marca, Influencers → Estado consistente

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

## Uso

### API REST

#### Crear campaña con Saga:
```bash
POST /campana-saga
{
  "nombre": "Campaña Demo",
  "tipo": "influencer_marketing", 
  "presupuesto": 50000,
  "marca": {"id_marca": "uuid", "nombre_marca": "Alpes"},
  "influencers": [{"nombre": "Tech", "plataforma": "Instagram"}]
}
```

#### Estado de saga:
```bash
GET /saga/{id_saga}/estado
```

## Respuestas

### Saga Exitosa
```json
{
  "id_saga": "uuid",
  "estado": "COMPLETADA",
  "pasos_ejecutados": ["influencer", "marca", "tracking"],
  "tiempo_total": "2.3s"
}
```

### Saga con Compensación
```json
{
  "id_saga": "uuid",
  "estado": "COMPENSADA",
  "paso_fallido": "tracking",
  "compensaciones": ["tracking", "marca", "influencer"],
  "error": "Error en base de datos"
}
```

## Manejo de Errores

### Tipos de Fallo Simulados
- **Influencer** (5%): Error de red
- **Marca** (10%): Error en sistema de notificaciones  
- **Tracking** (15%): Error en base de datos

### Estrategias de Compensación
- **Inmediata**: Al primer fallo
- **Orden inverso**: Último exitoso primero
- **Idempotente**: Compensaciones seguras

## Logging

### General
- Archivo: `logs/sagas/sagas_general.log`
- Incluye: inicio, finalización, errores

### Por Saga
- Archivo: `logs/sagas/saga_{id}.log`
- Incluye: cada paso, compensaciones, métricas

## Ventajas

- **Consistencia**: Garantías transaccionales
- **Observabilidad**: Logs detallados de cada paso
- **Recuperación**: Compensaciones automáticas
- **Escalabilidad**: Coordinación centralizada

## Limitaciones

- **Latencia**: Ejecución secuencial
- **Punto único**: Coordinador como dependencia crítica
- **Complejidad**: Lógica de compensación por comando