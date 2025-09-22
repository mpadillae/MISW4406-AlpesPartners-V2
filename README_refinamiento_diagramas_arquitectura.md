# Mapa de Contexto: TO-BE

### Diagrama del Mapa de Contexto

![Mapa de Contexto TO-BE](./arquitectura/modelo-contexto-TO-BE.png)

### Explicación del Mapa de Contexto

El mapa de contexto representa la arquitectura de Alpes Partners, basada en los principios de **Domain-Driven Design (DDD)**. Esta arquitectura define cómo los diferentes contextos de negocio interactúan entre sí y establece las relaciones y patrones de integración.

#### Bounded Contexts Identificados:

**1. BC_BFF (Backend for Frontend)**
- **Rol:** Punto de entrada y orquestador del sistema
- **Responsabilidad:** Actúa como gateway que coordina las operaciones entre los diferentes bounded contexts
- **Patrón:** Implementa **OHS** (Open Host Service) y **PL** (Published Language) para exponer servicios públicos

**2. BC_Afiliaciones**
- **Rol:** Contexto central del dominio de negocio
- **Responsabilidad:** Gestiona el core del negocio relacionado con afiliaciones, campañas y relaciones comerciales
- **Posición:** Contexto upstream que provee servicios a otros contextos y downstream que consume servicios del BFF

**3. BC_Influencers**
- **Rol:** Gestión especializada de influencers
- **Responsabilidad:** Maneja perfiles, métricas y comportamiento de influencers
- **Patrón:** Utiliza **ACL** (Anti-Corruption Layer) para mantener su integridad mientras se integra con Afiliaciones

**4. BC_Marcas**
- **Rol:** Gestión de marcas y productos
- **Responsabilidad:** Administra información de marcas, catálogos y productos
- **Patrón:** Implementa **ACL** para protegerse de cambios en otros contextos

**5. BC_Tracking**
- **Rol:** Sistema de seguimiento y métricas
- **Responsabilidad:** Recopila, procesa y reporta métricas de rendimiento y seguimiento
- **Patrón:** Utiliza **ACL** para mantener independencia en su modelo de datos

#### Patrones de Integración Utilizados:

- **U (Upstream):** Indica que el contexto es proveedor de servicios
- **D (Downstream):** Indica que el contexto es consumidor de servicios
- **ACL (Anti-Corruption Layer):** Patrón que protege la integridad de un contexto de cambios en otros contextos
- **OHS (Open Host Service):** Define una API pública y estable para que otros contextos la consuman
- **PL (Published Language):** Establece un lenguaje común y bien documentado para la integración

#### Características de la Arquitectura:

- **Autonomía:** Cada bounded context mantiene su propia lógica de dominio y modelo de datos
- **Acoplamiento bajo:** Los contextos interactúan a través de interfaces bien definidas
- **Escalabilidad:** Cada contexto puede evolucionar y escalarse independientemente
- **Integridad:** Los patrones ACL protegen cada contexto de cambios externos no deseados
- **Claridad:** Separación clara de responsabilidades según el dominio de negocio

***

# Refinamiento de Diagramas de Arquitectura

## Descripción

Este documento presenta el refinamiento de los diagramas de los diferentes puntos de vista presentados en la segunda entrega, con base a los resultados y conclusiones de la experimentación.

## Cambios Realizados

### Principales Refinamientos

1. **Cambio de nomenclatura del servicio principal:**

   - Se cambió el nombre del servicio de "Campañas" por "Afiliaciones" para mejor reflejar el dominio de negocio y la funcionalidad específica del microservicio.

2. **Adición de nuevos servicios:**
   - Se añadieron los servicios de **Marca** e **Influencers** como microservicios independientes en la arquitectura.
   - Estos servicios complementan la funcionalidad del sistema de afiliaciones, proporcionando gestión específica para marcas e influencers.

## Diagramas Refinados

A continuación se presentan los tres diagramas actualizados con los cambios específicos realizados:

### 1. Diagrama de Contexto

![Diagrama de Contexto](./arquitectura/diagramas-Contexto.jpg)

> **Nota:** Si las imágenes no se muestran, puedes encontrarlas en la carpeta `arquitectura/`:
>
> - `diagramas-Contexto.jpg`
> - `diagramas-Funcional.jpg`
> - `diagramas-modulo.jpg`

**Cambios específicos en el diagrama de contexto:**

- ✅ **Renombramiento del servicio principal:** "Campañas" → "Afiliaciones"
- ✅ **Adición de nuevos actores:** Servicios de Marca e Influencers como entidades independientes
- ✅ **Actualización de las interacciones:** Nuevas relaciones entre Afiliaciones, Marca e Influencers
- ✅ **Refinamiento del contexto de negocio:** Mejor representación del ecosistema de afiliaciones

### 2. Diagrama Funcional

![Diagrama Funcional](./arquitectura/diagramas-Funcional.jpg)

**Cambios específicos en el diagrama funcional:**

- ✅ **Separación de responsabilidades:** División clara entre gestión de afiliaciones, marcas e influencers
- ✅ **Nuevas funcionalidades:** Procesos específicos para cada microservicio
- ✅ **Flujos de comunicación:** Actualización de los flujos entre los servicios refinados
- ✅ **Arquitectura de eventos:** Implementación de patrones de comunicación asíncrona

### 3. Diagrama de Módulos

![Diagrama de Módulos](./arquitectura/diagramas-modulo.jpg)

**Cambios específicos en el diagrama de módulos:**

- ✅ **Estructura modular actualizada:** Cada servicio (Afiliaciones, Marca, Influencers) con su propia estructura
- ✅ **Nuevos componentes:** Módulos específicos para gestión de marcas e influencers
- ✅ **Dependencias refinadas:** Actualización de las dependencias entre módulos
- ✅ **Separación de capas:** Dominio, aplicación e infraestructura para cada microservicio

## Acceso a los Diagramas

Si las imágenes no se muestran correctamente en tu visor de Markdown, puedes acceder a los diagramas directamente:

### Ubicación de los archivos:

```
📁 arquitectura/
├── 📄 diagramas-Contexto.jpg    (Diagrama de contexto del sistema)
├── 📄 diagramas-Funcional.jpg   (Diagrama funcional de la arquitectura)
└── 📄 diagramas-modulo.jpg      (Diagrama de módulos y componentes)
```

### Rutas alternativas:

- **Ruta relativa:** `./arquitectura/diagramas-Contexto.jpg`
- **Ruta absoluta:** `/arquitectura/diagramas-Contexto.jpg`
- **Desde la raíz del proyecto:** `arquitectura/diagramas-Contexto.jpg`

## Resumen de Cambios por Diagrama

| Diagrama      | Cambio Principal                                                                  | Impacto                                        |
| ------------- | --------------------------------------------------------------------------------- | ---------------------------------------------- |
| **Contexto**  | Renombramiento "Campañas" → "Afiliaciones" + Nuevos servicios Marca e Influencers | Mejor representación del dominio de negocio    |
| **Funcional** | Separación de responsabilidades en microservicios independientes                  | Arquitectura más granular y escalable          |
| **Módulos**   | Estructura modular completa para cada servicio                                    | Mejor organización del código y mantenibilidad |

## Justificación de los Cambios

Los refinamientos realizados se basan en:

1. **Resultados de la experimentación:** La implementación y pruebas del sistema revelaron la necesidad de separar las responsabilidades en servicios más específicos.

2. **Mejora en la claridad del dominio:** El cambio de "Campañas" a "Afiliaciones" proporciona mayor claridad sobre el propósito específico del servicio principal.

3. **Arquitectura más granular:** La adición de los servicios de Marca e Influencers permite una mejor separación de responsabilidades y escalabilidad del sistema.

4. **Alineación con el dominio de negocio:** Los cambios reflejan mejor la realidad del negocio de afiliaciones y marketing de influencers.

## Estructura Final de la Arquitectura

La arquitectura refinada incluye los siguientes microservicios:

### Microservicios Principales

| Servicio            | Estado       | Descripción                       | Cambio                      |
| ------------------- | ------------ | --------------------------------- | --------------------------- |
| **🏢 Afiliaciones** | ✅ Refinado  | Gestión de campañas de afiliación | Renombrado desde "Campañas" |
| **🏷️ Marca**        | 🆕 Nuevo     | Gestión de marcas y productos     | Agregado en refinamiento    |
| **👥 Influencers**  | 🆕 Nuevo     | Gestión de influencers y perfiles | Agregado en refinamiento    |
| **📊 Tracking**     | ✅ Existente | Seguimiento y métricas            | Sin cambios                 |
| **🌐 BFF**          | ✅ Existente | Backend for Frontend              | Sin cambios                 |

### Características de la Arquitectura Refinada

- ✅ **Independencia de servicios:** Cada microservicio mantiene su propia base de datos y lógica de negocio
- ✅ **Comunicación asíncrona:** Eventos y mensajería para la comunicación entre servicios
- ✅ **APIs bien definidas:** Interfaces claras para la integración entre servicios
- ✅ **Escalabilidad:** Cada servicio puede escalarse independientemente según la demanda
- ✅ **Mantenibilidad:** Separación clara de responsabilidades facilita el mantenimiento

### Flujo de Comunicación

```
BFF ↔ Afiliaciones ↔ Marca
  ↕        ↕         ↕
Tracking  Influencers
```

Cada servicio se comunica a través de eventos y APIs REST, siguiendo los principios de arquitectura de microservicios y Domain-Driven Design.
