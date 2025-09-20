# MISW4406 - Alpes Partners

Este repositorio contiene la implementación de un sistema distribuido de microservicios para la gestión de campañas de marketing utilizando arquitectura hexagonal, patrones DDD, CQRS y comunicación basada en eventos. El proyecto fue desarrollado utilizando [Python](https://www.python.org/downloads/) versión 3.12 con FastAPI y Apache Pulsar como broker de mensajes.

## 👥 Integrantes del equipo

| Nombre | Correo |
|--------|------------------|
| Miguel Fernando Padilla Espino | m.padillae@uniandes.edu.co |
| Johann Sebastian Páez Campos | js.paezc1@uniandes.edu.co |
| Julián Oliveros Forero | je.oliverosf@uniandes.edu.co |

## 📋 Actividades por miembro del equipo

### Miguel Fernando Padilla Espino
**Rol Principal**: Arquitecto de Microservicios y Patrón Saga
- **Microservicios a cargo**: 
  - Servicio de Afiliaciones (puerto 8001) - Orquestador principal
  - Implementación del patrón Saga con orquestación
- **Actividades realizadas**:
  - Diseño e implementación de la arquitectura hexagonal en el servicio de afiliaciones
  - Desarrollo del patrón Saga para transacciones distribuidas
  - Implementación de CQRS (Command Query Responsibility Segregation)
  - Creación de eventos de dominio y publicación en Apache Pulsar
  - Diseño de la lógica de negocio para campañas de marketing
  - Implementación de repositorios y servicios de dominio
  - Configuración de la base de datos PostgreSQL para afiliaciones
  - Documentación del patrón Saga en README_SAGA.md

### Johann Sebastian Páez Campos
**Rol Principal**: Desarrollador de Microservicios de Dominio y DevOps
- **Microservicios a cargo**:
  - Servicio de Marca (puerto 8002)
  - Servicio de Influencer (puerto 8003)
- **Actividades realizadas**:
  - Implementación de consumidores de eventos para el servicio de marca
  - Desarrollo del servicio de influencer con arquitectura hexagonal
  - Creación de proyecciones de datos basadas en eventos
  - Implementación de repositorios SQLAlchemy para ambos servicios
  - Configuración de bases de datos PostgreSQL independientes
  - Desarrollo de DTOs y mapeadores para transformación de datos
  - Implementación de handlers para eventos de integración
  - Configuración de Docker y Docker Compose para los servicios
  - **Despliegue de la infraestructura completa en Google Cloud Platform (GCP)**
  - Configuración de servicios en la nube para todos los microservicios
  - Gestión de recursos y optimización de costos en GCP

### Julián Oliveros Forero
**Rol Principal**: Desarrollador de Microservicios de Análisis y BFF
- **Microservicios a cargo**:
  - Servicio de Tracking (puerto 8004)
  - BFF - Backend for Frontend (puerto 8005)
- **Actividades realizadas**:
  - Implementación del servicio de tracking y métricas
  - Desarrollo del BFF como proxy unificado para frontend
  - Creación de endpoints para registro de eventos de tracking
  - Implementación de cálculo de métricas de campañas
  - Desarrollo de la colección de Postman para testing
  - Configuración de comunicación HTTP entre microservicios
  - Implementación de health checks para todos los servicios
  - Documentación técnica y guías de uso
  - Configuración de Docker Compose para el ecosistema completo
  - Resolución de problemas de serialización JSON (UUID, datetime)
  - Implementación de patrones de proxy y API Gateway

## 🔄 Distribución de responsabilidades

### Arquitectura y Patrones
- **Miguel**: Patrón Saga, CQRS, Event-Driven Architecture
- **Johann**: Event Consumers, Projections, Domain Modeling
- **Julián**: BFF Pattern, Proxy Pattern, API Integration

### Microservicios
- **Miguel**: Afiliaciones (Orquestador principal)
- **Johann**: Marca + Influencer (Consumidores de eventos)
- **Julián**: Tracking + BFF (Análisis y Frontend)

### Tecnologías y Herramientas
- **Miguel**: Apache Pulsar, Event Sourcing, PostgreSQL (Afiliaciones)
- **Johann**: Event Consumers, SQLAlchemy, PostgreSQL (Marca/Influencer), Google Cloud Platform, Docker
- **Julián**: FastAPI, HTTPX, Docker, Postman, PostgreSQL (Tracking)

### Documentación y Testing
- **Miguel**: README_SAGA.md, Documentación de patrones
- **Johann**: Documentación de servicios de dominio
- **Julián**: README principal, Colecciones Postman, Guías de uso

## 📊 Métricas del proyecto

### Estructura de archivos por miembro
```
📦 MISW4406-AlpesPartners-V2
├── afiliaciones/           # Miguel - 15 archivos
│   ├── aplicacion/         # CQRS, Handlers, DTOs
│   ├── dominio/            # Entidades, Eventos, Servicios
│   ├── infraestructura/    # Repositorios, Despachadores
│   └── modulos/sagas/      # Implementación del patrón Saga
├── marca/                  # Johann - 8 archivos
│   ├── dominio/            # Entidades de marca
│   └── infraestructura/    # Consumidores de eventos
├── influencer/             # Johann - 8 archivos
│   ├── dominio/            # Entidades de influencer
│   └── infraestructura/    # Consumidores de eventos
├── tracking/               # Julián - 8 archivos
│   ├── dominio/            # Entidades de tracking
│   └── infraestructura/    # Repositorios de métricas
├── bff/                    # Julián - 8 archivos
│   ├── api/                # Endpoints proxy
│   └── servicios.py        # Clientes HTTP
└── collections/            # Julián - 2 archivos
    ├── Alpes Partners.postman_collection.json
    └── Alpes Partners BFF.postman_collection.json
```

### Tecnologías implementadas por miembro
- **Miguel**: Python, FastAPI, Apache Pulsar, PostgreSQL, SQLAlchemy, Pydantic, Avro
- **Johann**: Python, FastAPI, Apache Pulsar, PostgreSQL, SQLAlchemy, Pydantic, Event Consumers, Google Cloud Platform, Docker
- **Julián**: Python, FastAPI, HTTPX, Docker, Postman, PostgreSQL, SQLAlchemy, Pydantic

### Patrones de diseño implementados
- **Miguel**: Saga Pattern, CQRS, Event Sourcing, Domain Events, Repository Pattern
- **Johann**: Event-Driven Architecture, Projection Pattern, Consumer Pattern, Domain Modeling, Cloud Deployment Pattern
- **Julián**: BFF Pattern, Proxy Pattern, API Gateway, Client-Server Pattern

### Endpoints desarrollados
- **Miguel**: 8 endpoints (Afiliaciones + Sagas)
- **Johann**: 0 endpoints directos (solo consumidores de eventos)
- **Julián**: 12 endpoints (Tracking: 4, BFF Proxy: 8)

## 🚀 Contribuciones técnicas detalladas

### Miguel Fernando Padilla Espino
**Commits principales y desarrollos**:
- Implementación completa del servicio de afiliaciones con arquitectura hexagonal
- Desarrollo del patrón Saga con orquestación para transacciones distribuidas
- Creación de 15+ archivos en el módulo de afiliaciones
- Implementación de CQRS con separación de comandos y queries
- Desarrollo de eventos de dominio y publicación en Apache Pulsar
- Configuración de la base de datos PostgreSQL para afiliaciones
- Documentación técnica del patrón Saga (README_SAGA.md)

### Johann Sebastian Páez Campos
**Commits principales y desarrollos**:
- Implementación de consumidores de eventos para marca e influencer
- Desarrollo de 16+ archivos en los módulos de marca e influencer
- Creación de proyecciones de datos basadas en eventos de integración
- Implementación de repositorios SQLAlchemy para ambos servicios
- Configuración de bases de datos PostgreSQL independientes
- Desarrollo de DTOs y mapeadores para transformación de datos
- Implementación de handlers para eventos de integración
- **Despliegue completo de la infraestructura en Google Cloud Platform (GCP)**
- Configuración y gestión de servicios en la nube
- Optimización de recursos y costos en GCP

### Julián Oliveros Forero
**Commits principales y desarrollos**:
- Implementación completa del servicio de tracking y métricas
- Desarrollo del BFF (Backend for Frontend) como proxy unificado
- Creación de 18+ archivos en los módulos de tracking y BFF
- Desarrollo de colecciones de Postman para testing integral
- Configuración de Docker Compose para el ecosistema completo
- Resolución de problemas de serialización JSON (UUID, datetime)
- Documentación principal del proyecto (README.md)
- Implementación de patrones de proxy y API Gateway
- Configuración de comunicación HTTP entre microservicios

## 📈 Resumen de contribuciones

| Miembro | Microservicios | Archivos | Endpoints | Patrones | Documentación | Infraestructura |
|---------|----------------|----------|-----------|----------|---------------|-----------------|
| Miguel | 1 (Afiliaciones) | 15+ | 8 | 5 | README_SAGA.md | - |
| Johann | 2 (Marca, Influencer) | 16+ | 0 | 5 | Servicios dominio | **GCP Deployment** |
| Julián | 2 (Tracking, BFF) | 18+ | 12 | 4 | README.md, Postman | - |

**Total del proyecto**: 5 microservicios, 49+ archivos, 20 endpoints, 13 patrones de diseño

***

## 🔥 Implementación con Patrón Saga 🔥

El proyecto ahora incluye una implementación del patrón Saga con orquestación para el manejo de transacciones distribuidas en la creación de campañas. Esta nueva funcionalidad proporciona:

- ✅ Transacciones distribuidas con garantías de consistencia
- ✅ Compensaciones automáticas en caso de fallos
- ✅ Coordinación centralizada desde el servicio de afiliaciones
- ✅ Trazabilidad completa del flujo de transacciones

> 📖 **Documentación detallada**: [README_SAGA.md](./README_SAGA.md)

***

## 📋 Tabla de contenidos
- [✅ Prerrequisitos](#-prerrequisitos)
- [🛠️ Tecnologías y herramientas utilizadas](#️-tecnologías-y-herramientas-utilizadas)
- [📁 Estructura del proyecto](#-estructura-del-proyecto)
- [🐳 Docker Compose](#-docker-compose)
- [🌐 URLs de los servicios](#-urls-de-los-servicios)
- [🏗️ Arquitectura de microservicios](#️-arquitectura-de-microservicios)
- [🎯 Patrones y tácticas implementadas](#-patrones-y-tácticas-implementadas)
- [📡 Comunicación por eventos](#-comunicación-por-eventos)
- [💾 Patrones de almacenamiento de datos](#-patrones-de-almacenamiento-de-datos)
- [⚙️ Configuración](#️-configuración)
- [� API Endpoints](#-api-endpoints)
- [🔵 Despliegue de la solución en Google Cloud Platform (GCP)](#-despliegue-de-la-solución-en-google-cloud-platform-gcp)
- [🧪 Colección de Postman](#-colección-de-postman)
- [🚀 Características del Sistema](#-características-del-sistema)

## ✅ Prerrequisitos

Para poder utilizar este proyecto necesitas:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y ejecutándose
* [Docker Compose](https://docs.docker.com/compose/) (incluido con Docker Desktop)
* [Python 3.12+](https://www.python.org/) (para desarrollo local)
* [Apache Pulsar](https://pulsar.apache.org/) (incluido en docker-compose)

## 🛠️ Tecnologías y herramientas utilizadas

* [Python 3.12](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido para construir APIs
* [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para aplicaciones Python
* [PostgreSQL](https://www.postgresql.org/) - Base de datos relacional (4 instancias)
* [Apache Pulsar](https://pulsar.apache.org/) - Message broker para eventos distribuidos
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para Python
* [Pydantic](https://pydantic-docs.helpmanual.io/) - Validación de datos
* [Apache Avro](https://avro.apache.org/) - Serialización de eventos
* [Docker](https://www.docker.com/) - Containerización de los servicios
* [Docker Compose](https://docs.docker.com/compose/) - Orquestación de múltiples contenedores

## 📁 Estructura del proyecto

```
📦 MISW4406-AlpesPartners-V2
│   .gitignore
│   docker-compose.yml
│   env.example
│   PORTS.md
│   README.md
├───collections/
│   ├───Alpes Partners.postman_collection.json
│   └───Alpes Partners.postman_environment.json
├───afiliaciones/              # 🎯 Microservicio principal
│   ├───aplicacion/
│   │   ├───comandos/
│   │   ├───queries/
│   │   ├───dto.py
│   │   ├───handlers.py
│   │   ├───mapeadores.py
│   │   └───servicios.py
│   ├───dominio/
│   │   ├───entidades.py
│   │   ├───eventos.py
│   │   ├───excepciones.py
│   │   ├───objetos_valor.py
│   │   ├───reglas.py
│   │   ├───repositorios.py
│   │   └───servicios.py
│   ├───infraestructura/
│   │   ├───despachadores.py
│   │   ├───repositorios.py
│   │   └───schema/v1/
│   │       ├───comandos.py
│   │       └───eventos.py
│   ├───api/
│   │   └───endpoints.py
│   ├───main.py
│   ├───requirements.txt
│   └───Dockerfile
├───marca/                     # 🏢 Microservicio de marca
├───influencer/               # 👥 Microservicio de influencer
└───tracking/                 # 📊 Microservicio de métricas
```

## 🐳 Docker Compose

### Comandos principales

```bash
# Construir y levantar todos los servicios
docker-compose up --build -d

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f afiliaciones-service
docker-compose logs -f marca-service
docker-compose logs -f influencer-service
docker-compose logs -f tracking-service

# Detener todos los servicios
docker-compose down

# Limpiar todo (incluyendo volúmenes)
docker-compose down -v
```

## 🌐 URLs de los servicios

| Servicio | URL base | Documentación API | Base de Datos |
|----------|----------|-------------------|---------------|
| **BFF (Backend for Frontend)** | http://localhost:8005 | http://localhost:8005/docs | - |
| **Afiliaciones** | http://localhost:8001 | http://localhost:8001/docs | localhost:5436 |
| **Marca** | http://localhost:8002 | http://localhost:8002/docs | localhost:5433 |
| **Influencer** | http://localhost:8003 | http://localhost:8003/docs | localhost:5434 |
| **Tracking** | http://localhost:8004 | http://localhost:8004/docs | localhost:5435 |
| **Pulsar Broker** | pulsar://localhost:6650 | - | - |

### Health checks

```bash
curl http://localhost:8005/health  # BFF
curl http://localhost:8001/health  # Afiliaciones
curl http://localhost:8002/health  # Marca
curl http://localhost:8003/health  # Influencer
curl http://localhost:8004/health  # Tracking
```

## 🏗️ Arquitectura de microservicios

<img width="1700" height="1100" alt="diagramas-Funcional entrega 4 drawio" src="https://github.com/user-attachments/assets/b34cbe9b-9da6-4ed0-a323-985c2af099d4" />

<img width="688" height="733" alt="diagramas-modulo entrega 4 drawio-2" src="https://github.com/user-attachments/assets/1987dc59-a49b-44bf-a3bf-6276331cc684" />

El sistema está compuesto por **5 microservicios independientes**:

### 1. 🌐 BFF (Puerto 8005) - Backend for Frontend
- **Función**: Proporciona una API unificada para el frontend, agregando endpoints de afiliaciones y tracking
- **Responsabilidades**: Proxy HTTP, agregación de servicios, simplificación de la comunicación frontend-backend
- **Endpoints**: 
  - `POST /afiliaciones/campana` - Crear campaña (proxy)
  - `GET /afiliaciones/campana/{id}` - Obtener campaña (proxy)
  - `GET /afiliaciones/campanas` - Listar campañas (proxy)
  - `POST /tracking/evento` - Registrar evento de tracking (proxy)
  - `GET /tracking/metricas/{id_campana}` - Obtener métricas (proxy)
- **Patrón**: API Gateway + Proxy Pattern
- **Comunicación**: HTTP síncrono con servicios downstream

### 2. 🎯 AFILIACIONES (Puerto 8001) - Servicio Orquestador
- **Función**: Coordina el flujo principal de campañas y publica eventos de integración
- **Responsabilidades**: Crear campañas, iniciar campañas, gestionar estados
- **Endpoints**: 
  - `POST /afiliaciones/campana` - Crear campaña
  - `GET /afiliaciones/campana/{id}` - Obtener campaña
  - `GET /afiliaciones/campanas` - Listar campañas
- **Evento que publica**: `CampanaCreada`
- **Base de datos**: `afiliaciones-db` (PostgreSQL - Puerto 5436)
- **Patrón**: Command Handler + Event Publisher

### 3. 🏢 MARCA (Puerto 8002) - Consumidor de Eventos
- **Función**: Procesa y almacena información específica de marcas participantes en campañas
- **Responsabilidades**: Sincronizar datos de marca, mantener contexto de marca por campaña
- **Evento que consume**: `CampanaCreada` 
- **Base de datos**: `marca-db` (PostgreSQL - Puerto 5433)
- **Patrón**: Event-Driven Consumer + Projection

### 4. 👥 INFLUENCER (Puerto 8003) - Consumidor de Eventos
- **Función**: Gestiona información de influencers asociados a las campañas
- **Responsabilidades**: Sincronizar datos de influencers, gestionar asignaciones
- **Evento que consume**: `CampanaCreada`
- **Base de datos**: `influencer-db` (PostgreSQL - Puerto 5434)
- **Patrón**: Event-Driven Consumer + Projection

### 5. 📊 TRACKING (Puerto 8004) - Métricas y Eventos
- **Función**: Rastrea métricas, eventos de usuario y genera análisis de rendimiento
- **Responsabilidades**: Registrar eventos de tracking, calcular métricas, generar reportes
- **Endpoints**: 
  - `POST /tracking/evento` - Registrar evento de tracking
  - `GET /tracking/eventos/{id_campana}` - Obtener eventos de campaña
- **Evento que consume**: `CampanaCreada`
- **Base de datos**: `tracking-db` (PostgreSQL - Puerto 5435)
- **Patrón**: Event-Driven Consumer + Analytics Engine

## 🎯 Patrones y tácticas implementadas

### Arquitectura Hexagonal (Ports & Adapters)
Cada microservicio implementa una arquitectura hexagonal clara con separación de responsabilidades:

```
📁 Microservicio/
├── 🧠 dominio/              # Lógica de negocio pura
│   ├── entidades.py         # Agregados y entidades
│   ├── eventos.py           # Domain Events
│   ├── objetos_valor.py     # Value Objects
│   ├── reglas.py           # Business Rules
│   ├── repositorios.py     # Repository Interfaces
│   └── servicios.py        # Domain Services
├── 🎯 aplicacion/          # Casos de uso (Application Layer)
│   ├── comandos/           # Command Handlers (CQRS Write)
│   ├── queries/            # Query Handlers (CQRS Read)
│   ├── dto.py             # Data Transfer Objects
│   ├── handlers.py        # Command/Query Handlers
│   ├── mapeadores.py      # Domain ↔ DTO Mappers
│   └── servicios.py       # Application Services
├── 🔌 infraestructura/    # Adaptadores externos
│   ├── repositorios.py    # Repository Implementations
│   ├── despachadores.py   # Event Publishers
│   ├── consumidores.py    # Event Consumers
│   └── schema/v1/         # Event Schema (Avro)
└── 🌐 api/                # Interfaz REST
    └── endpoints.py       # FastAPI Controllers
```

### CQRS (Command Query Responsibility Segregation)
- **Comandos (Write Operations)**: `CrearCampana`
- **Queries (Read Operations)**: `ObtenerCampana`, `ObtenerTodasCampanas`
- **Handlers Especializados**: Cada comando/query tiene su handler específico
- **Separación Clara**: Operaciones de escritura y lectura completamente separadas

### Domain-Driven Design (DDD)
- **Agregados**: `Campana` como agregado principal con invariantes de negocio
- **Entidades**: Objetos con identidad única y ciclo de vida
- **Value Objects**: `EstadoCampana`, `TipoCampana`, `InfluencerInfo`
- **Domain Events**: `CampanaCreada`
- **Bounded Contexts**: Cada microservicio representa un contexto delimitado

### Event-Driven Architecture
- **Publicación de Eventos**: El servicio Afiliaciones publica eventos de integración
- **Consumo Asíncrono**: Los demás servicios consumen eventos de forma independiente
- **Desacoplamiento**: Los servicios no se conocen entre sí directamente
- **Eventual Consistency**: Los datos se sincronizan eventualmente através de eventos

## 📡 Comunicación por eventos

### Estrategia de Eventos: Fat Events (Eventos con Carga de Estado)

El sistema utiliza **eventos gordos (Fat Events)** que contienen toda la información relevante del estado del agregado. Esta decisión arquitectural se tomó por las siguientes razones:

#### ✅ **Justificación para Fat Events:**

1. **Desacoplamiento Total**: Los consumidores obtienen toda la información necesaria sin requerir llamadas síncronas adicionales
2. **Simplicidad de Consumo**: Cada servicio puede procesar el evento de forma autónoma sin dependencias externas  
3. **Mejor Rendimiento**: Evita el anti-patrón de "event notification" que requiere múltiples llamadas para obtener datos
4. **Resiliencia**: Si un servicio está caído, puede procesar todos los eventos pendientes al recuperarse
5. **Contexto Completo**: Facilita la toma de decisiones de negocio con información completa

#### 📋 **Estructura de Eventos:**

```json
// Evento CampanaCreada (Fat Event)
{
  "id": "976c67a2-b333-4f77-a380-6108be2e9d35",
  "fecha_evento": "2025-09-15T01:45:19.889685",
  "id_campana": "c63c598a-186d-43eb-b52f-6f2963b39ec1",
  "id_marca": "123e4567-e89b-12d3-a456-426614174000",
  "nombre": "Campaña de Verano 2024",
  "descripcion": "Promoción de productos de verano con influencers",
  "tipo": "influencer",
  "estado": "creada",
  "fecha_creacion": "2025-09-15T01:45:19.871731",
  "presupuesto": 15000.0,
  "nombre_marca": "Nike",
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

### Apache Pulsar como Message Broker

#### ✅ **Justificación para Apache Pulsar:**

1. **Multi-Tenancy Nativo**: Soporte nativo para múltiples inquilinos y namespaces
2. **Durabilidad Garantizada**: Almacenamiento persistente con Apache BookKeeper
3. **Escalabilidad Horizontal**: Arquitectura separada de brokers y storage
4. **Schema Evolution**: Soporte nativo para evolución de esquemas con Avro
5. **Geo-Replication**: Replicación multi-región para disaster recovery
6. **Performance**: Mayor throughput que Kafka en muchos escenarios

### Serialización con Apache Avro

#### ✅ **Justificación para Apache Avro:**

1. **Schema Evolution**: Soporte robusto para evolución de esquemas (backward/forward compatibility)
2. **Compacidad**: Serialización binaria más eficiente que JSON o XML
3. **Tipado Fuerte**: Validación automática de tipos en tiempo de serialización
4. **Interoperabilidad**: Soporte multi-lenguaje (Python, Java, C#, etc.)
5. **Integración Nativa**: Pulsar tiene soporte nativo optimizado para Avro
6. **Schema Registry**: Control centralizado de versiones de esquemas

### Event Stream Versioning

#### ✅ **Estrategia de Versionado:**

El sistema implementa **versionado de esquemas a nivel de namespace** para mantener compatibilidad:

1. **Namespace Versioning**: `/infraestructura/schema/v1/`
2. **Backward Compatibility**: Los esquemas nuevos pueden leer eventos antiguos
3. **Forward Compatibility**: Los consumidores antiguos ignoran campos nuevos
4. **Deprecation Strategy**: Campos obsoletos se marcan como deprecated antes de eliminar

### Topología de Eventos

```
📡 Apache Pulsar
├── 📋 Topic: eventos-campana
│   ├── 🔔 CampanaCreada (Producer: Afiliaciones)
│   │   ├── Consumer: marca-subscription
│   │   ├── Consumer: influencer-subscription  
│   │   └── Consumer: tracking-subscription
```

## 💾 Patrones de almacenamiento de datos

### Estrategia Híbrida de Almacenamiento

El sistema implementa un **modelo híbrido de almacenamiento** que combina diferentes estrategias según las necesidades específicas de cada microservicio:

#### ✅ **Justificación del Modelo Híbrido:**

1. **Afiliaciones (Authoritative Source)**: 
   - **Patrón**: Database-per-Service + Event Sourcing parcial
   - **Justificación**: Mantiene el estado autorizado de las campañas y publica eventos
   - **Tecnología**: PostgreSQL con eventos persistidos

2. **Marca, Influencer, Tracking (Projections)**:
   - **Patrón**: Event-Driven Projections + CRUD
   - **Justificación**: Mantienen vistas especializadas derivadas de eventos
   - **Tecnología**: PostgreSQL con modelos desnormalizados

#### 📊 **Distribución de Datos:**

```
🏢 Afiliaciones DB          🏪 Marca DB              👥 Influencer DB        📊 Tracking DB
├── campanas (master)       ├── marcas               ├── influencers         ├── metricas_campana  
└── eventos_dominio         └── campanas_marca       └── campanas_influencer └── eventos_tracking
```

### CRUD vs Event Sourcing

#### ✅ **Decisión: CRUD Clásico**

Se eligió un **modelo CRUD tradicional** en lugar de Event Sourcing completo por las siguientes razones:

1. **Simplicidad de Implementación**: 
   - Menor curva de aprendizaje para el equipo
   - Debugging más directo y familiar
   - Menos complejidad en queries y reportes

2. **Requisitos del Negocio**:
   - No se requiere historial detallado de cambios de estado
   - Las campañas tienen ciclos de vida simples (Creada → Iniciada → Finalizada)

3. **Rendimiento**:
   - Queries directas sin necesidad de reconstruir estado
   - Menor latencia en consultas frecuentes
   - Menos carga computacional en reads

4. **Consistencia Eventual**:
   - Los eventos se usan para sincronización entre servicios
   - Cada servicio mantiene su vista optimizada
   - La consistencia fuerte solo se requiere dentro de cada contexto acotado

#### 🔄 **Flujo de Datos:**

```
1. Cliente → POST /campana
2. Afiliaciones → INSERT campana (CRUD)
3. Afiliaciones → PUBLISH CampanaCreada (Event)
4. Marca/Influencer/Tracking → CONSUME evento
5. Cada servicio → UPDATE/INSERT su vista local (CRUD)
```


## ⚙️ Configuración

### Variables de entorno

Cada servicio utiliza las siguientes variables de entorno configurables:

```properties
# Configuración de base de datos
DATABASE_URL=postgresql://postgres:postgres@[host]:[port]/[database]

# Configuración de Apache Pulsar  
PULSAR_URL=pulsar://pulsar:6650

# Configuración específica por servicio
SERVICE_PORT=8000
SERVICE_NAME=[afiliaciones|marca|influencer|tracking]

# Configuración de logging
LOG_LEVEL=INFO
```

### Configuración por servicio

```bash
# Afiliaciones
DATABASE_URL=postgresql://postgres:postgres@afiliaciones-db:5432/afiliaciones
PULSAR_URL=pulsar://pulsar:6650

# Marca  
DATABASE_URL=postgresql://postgres:postgres@marca-db:5432/marca
PULSAR_URL=pulsar://pulsar:6650

# Influencer
DATABASE_URL=postgresql://postgres:postgres@influencer-db:5432/influencer  
PULSAR_URL=pulsar://pulsar:6650

# Tracking
DATABASE_URL=postgresql://postgres:postgres@tracking-db:5432/tracking
PULSAR_URL=pulsar://pulsar:6650
```

## 📋 API Endpoints

### 🌐 BFF (Backend for Frontend) - Puerto 8005

El BFF actúa como un proxy unificado que expone todos los endpoints de afiliaciones y tracking a través de una sola API. Esto simplifica la comunicación del frontend al eliminar la necesidad de conocer múltiples URLs de servicios.

#### Endpoints de Afiliaciones (Proxy)
```http
# Crear campaña
POST /afiliaciones/campana
Content-Type: application/json

# Obtener campaña
GET /afiliaciones/campana/{id_campana}

# Listar campañas
GET /afiliaciones/campanas

# Iniciar campaña
POST /afiliaciones/campana/{id_campana}/iniciar

# Crear campaña con Saga
POST /afiliaciones/campana-saga

# Endpoints de Saga
GET /afiliaciones/saga/{id_saga}/estado
GET /afiliaciones/sagas
GET /afiliaciones/sagas/historial
GET /afiliaciones/sagas/estadisticas
```

#### Endpoints de Tracking (Proxy)
```http
# Registrar evento de tracking
POST /tracking/evento
Content-Type: application/json

# Obtener métricas de campaña
GET /tracking/metricas/{id_campana}

# Obtener eventos de campaña
GET /tracking/eventos/{id_campana}

# Obtener métricas por marca
GET /tracking/metricas/marca/{id_marca}
```

#### Health Check
```http
GET /health
```

### 🎯 Servicio Afiliaciones (Puerto 8001)

#### Crear Campaña
```http
POST /afiliaciones/campana
Content-Type: application/json

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


#### Obtener Campaña
```http
GET /afiliaciones/campana/{id_campana}
```

**Respuesta típica:**
```json
{
    "id": "c63c598a-186d-43eb-b52f-6f2963b39ec1",
    "marca": {
        "id_marca": "123e4567-e89b-12d3-a456-426614174000",
        "nombre_marca": "Nike"
    },
    "nombre": "Campaña de Verano 2024",
    "descripcion": "Promoción de productos de verano con influencers",
    "tipo": "influencer",
    "estado": "creada",
    "fecha_creacion": "2025-09-15T01:45:19.871731",
    "fecha_inicio": "2025-01-01T00:00:00",
    "fecha_fin": "2025-12-31T23:59:59",
    "presupuesto": 15000.0,
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

#### Listar Campañas  
```http
GET /afiliaciones/campanas
```

**Respuesta típica:**
```json
{
    "campanas": [
        {
            "id": "c63c598a-186d-43eb-b52f-6f2963b39ec1",
            "marca": {
                "id_marca": "123e4567-e89b-12d3-a456-426614174000",
                "nombre_marca": "Nike"
            },
            "nombre": "Campaña de Verano 2024",
            "descripcion": "Promoción de productos de verano con influencers",
            "tipo": "influencer",
            "estado": "creada",
            "fecha_creacion": "2025-09-15T01:45:19.871731",
            "fecha_inicio": "2025-01-01T00:00:00",
            "fecha_fin": "2025-12-31T23:59:59",
            "presupuesto": 15000.0,
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
    ],
    "total": 1
}
```

### 📊 Servicio Tracking (Puerto 8004)

#### Registrar Evento de Tracking
```http
POST /tracking/evento
Content-Type: application/json

{
  "id_campana": "{{campana_id}}",
  "tipo_evento": "vista",
  "datos": {
    "usuario": "user123",
    "timestamp": {{$timestamp}},
    "fuente": "instagram",
    "dispositivo": "mobile"
  }
}
```


#### Obtener Eventos de Campaña
```http
GET /tracking/eventos/{id_campana}
```

**Respuesta típica:**
```json
[
    {
        "id": "decbca03-ab04-4047-ad8e-b461c81cc6df",
        "id_campana": "c63c598a-186d-43eb-b52f-6f2963b39ec1",
        "tipo_evento": "vista",
        "datos": {
            "usuario": "user123",
            "timestamp": 1757902818,
            "fuente": "instagram",
            "dispositivo": "mobile"
        },
        "fecha_evento": "2025-09-15T02:20:18.253081"
    }
]
```

## 🔵 Despliegue de la solución en Google Cloud Platform (GCP)

### ✅ **Justificación para GCP:**

1. **Experiencia del Equipo**: 
   - El equipo tiene experiencia previa con GCP y sus servicios
   - Familiaridad con Cloud Pub/Sub como alternativa a Pulsar

2. **Beneficios Económicos**:
   - Créditos educativos disponibles ($50 USD para estudiantes)
   - Tier gratuito permanente para desarrollo y testing



## 🧪 Colección de Postman

El proyecto incluye colecciones completas de Postman para facilitar las pruebas:

### 📋 **Archivos Incluidos:**
- [`Alpes Partners.postman_collection.json`](./collections/Alpes%20Partners.postman_collection.json) - Colección principal con todos los endpoints de servicios individuales
- [`Alpes Partners BFF.postman_collection.json`](./collections/Alpes%20Partners%20BFF.postman_collection.json) - Colección específica para el BFF con endpoints unificados
- [`Alpes Partners.postman_environment.json`](./collections/Alpes%20Partners.postman_environment.json) - Variables de entorno configuradas (incluye `base_url_bff`)

### 🚀 **Uso Recomendado:**
- **Para desarrollo y testing de servicios individuales**: Usar `Alpes Partners.postman_collection.json`
- **Para frontend y testing integrado**: Usar `Alpes Partners BFF.postman_collection.json`

## 🚀 Características del Sistema

### ✅ **Características Implementadas:**

- **🏗️ Arquitectura Hexagonal**: Separación clara de responsabilidades
- **🌐 BFF Pattern**: Backend for Frontend para simplificar la comunicación frontend-backend
- **📡 Event-Driven**: Comunicación asíncrona mediante eventos
- **🔄 CQRS**: Separación de comandos y queries
- **🎯 DDD**: Domain-Driven Design con bounded contexts
- **📊 Fat Events**: Eventos con carga completa de estado
- **🔧 Apache Avro**: Serialización eficiente con schema evolution
- **🐳 Containerización**: Docker + Docker Compose
- **🔍 Health Checks**: Endpoints de salud en todos los servicios
- **📖 Documentación API**: Swagger/OpenAPI automático
- **🔐 Validación**: Pydantic para validación de datos
- **🎛️ Configuración**: Variables de entorno para todos los parámetros
- **🔄 Proxy Pattern**: BFF actúa como proxy transparente para servicios downstream

---

## License

Copyright © MISW4406 - Diseño y construcción de soluciones no monolíticas - 2025.