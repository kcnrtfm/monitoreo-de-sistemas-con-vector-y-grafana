# Monitoreo de sistemas con Vector y Grafana

Material de trabajo para el vivo del **3 de noviembre de 2026**.

**Transmisión en vivo:** https://youtube.com/live/oEYg71x0RoQ

## Descripción

En este encuentro vamos a trabajar con [Vector](https://vector.dev/), una herramienta de código abierto que permite recopilar, transformar y transmitir datos de observabilidad, incluidas métricas de diferentes sistemas.

Vamos a explorar cómo utilizarla para obtener información de nuestros servidores y enviarla a un sistema de monitoreo, donde podremos visualizarla mediante paneles gráficos con [Grafana](https://grafana.com/).

## Objetivo

Implementar un sistema de monitoreo de servidores GNU/Linux utilizando **Vector** para recopilar métricas de CPU, memoria, disco, red y tiempo de actividad, junto con información de identificación y características del sistema.

Las métricas serán enviadas a **Prometheus** para su almacenamiento y consulta, y posteriormente visualizadas mediante **Grafana**, a través de dashboards que permitan identificar cada servidor y observar su estado y comportamiento en tiempo real.

## Herramientas

- **Vector:** recopilación, procesamiento y envío de métricas.
- **Grafana:** visualización de métricas mediante paneles gráficos.

## Sistema de monitoreo

### Grafana

![Logo de Grafana](https://upload.wikimedia.org/wikipedia/commons/a/a1/Grafana_logo.svg)

#### ¿Qué es Grafana?

[Grafana](https://grafana.com/) es una plataforma de código abierto para consultar, analizar y visualizar datos provenientes de distintas fuentes mediante gráficos, indicadores y paneles interactivos (*dashboards*).

#### ¿Cómo funciona Grafana?

Grafana funciona como una plataforma de **consulta, análisis y visualización de datos**. Su arquitectura se basa en un servidor que se comunica con distintas fuentes de datos y una interfaz web desde la que se configuran las consultas y visualizaciones.

Sus componentes principales son:

1. **Fuentes de datos (Data Sources):** conexiones con sistemas externos como Prometheus, InfluxDB, PostgreSQL o Loki, que proporcionan los datos a visualizar.
2. **Consultas (Queries):** Grafana ejecuta consultas sobre las fuentes configuradas, utilizando el mecanismo o lenguaje correspondiente a cada sistema, como PromQL o SQL.
3. **Paneles (Panels):** los resultados se representan mediante gráficos temporales, tablas, indicadores numéricos y otras visualizaciones.
4. **Tableros (Dashboards):** agrupan múltiples paneles en una misma interfaz para observar diferentes variables.
5. **Alertas (Alerting):** permiten evaluar condiciones sobre los datos y generar notificaciones cuando se cumplen determinados criterios.

Grafana dispone de un **backend** que administra conexiones, consultas, usuarios, permisos y alertas, y un **frontend web** para construir consultas, configurar paneles y explorar resultados.

Los paneles pueden actualizarse automáticamente mediante consultas periódicas, permitiendo visualizar la evolución de los datos en el tiempo.

Grafana normalmente no almacena las métricas que visualiza: estas permanecen en sus sistemas de origen y Grafana las consulta cuando necesita representarlas.

![Ejemplo de dashboard de Grafana](https://grafana.com/media/products/assets/cloud-grafana-0.png)

### Prometheus

![Logo de Prometheus](https://raw.githubusercontent.com/prometheus/prometheus/main/documentation/images/prometheus-logo.svg)

#### ¿Qué es Prometheus?

[Prometheus](https://prometheus.io/) es un sistema de monitoreo de código abierto que recopila y almacena métricas en una base de datos de series temporales. Cada muestra queda asociada a un instante de tiempo y puede identificarse mediante etiquetas.

#### ¿Cómo funciona Prometheus?

Prometheus consulta periódicamente los endpoints HTTP de los sistemas que exponen métricas, normalmente en la ruta `/metrics`. Este mecanismo se conoce como **pull** o *scraping*.

Las métricas obtenidas se almacenan como series temporales y pueden consultarse mediante **PromQL**, su lenguaje de consultas. Prometheus también permite evaluar reglas y generar alertas.

Sus componentes principales son:

1. **Targets:** servicios o aplicaciones que exponen métricas.
2. **Scraping:** recopilación periódica de las métricas de esos targets.
3. **Almacenamiento de series temporales (TSDB):** conserva los valores recopilados y sus marcas de tiempo.
4. **PromQL:** permite seleccionar, filtrar y agregar métricas.
5. **Reglas y alertas:** evalúan expresiones sobre las métricas y detectan condiciones definidas.

#### ¿Cómo se relaciona con Grafana?

Prometheus **almacena las métricas** y ofrece una API HTTP para consultarlas. Grafana se conecta a Prometheus como fuente de datos, ejecuta consultas PromQL y representa los resultados en paneles y dashboards.

Así, Prometheus se encarga de obtener y conservar los datos, mientras que Grafana proporciona una interfaz para explorarlos y visualizarlos.

**Documentación:** [Prometheus](https://prometheus.io/docs/introduction/overview/) · [Integración con Grafana](https://prometheus.io/docs/visualization/grafana/)

### Instalación y configuración

Vamos a desplegar **Prometheus y Grafana con Docker Compose**, utilizando una red exclusiva para ambos servicios y volúmenes persistentes para conservar sus datos.

#### Requisitos

Git, Docker Engine y el complemento Docker Compose (`docker compose`).

#### Obtener el proyecto

```bash
git clone https://github.com/kcnrtfm/monitoreo-de-sistemas-con-vector-y-grafana.git
cd monitoreo-de-sistemas-con-vector-y-grafana/sistema-monitoreo
```

#### Estructura del despliegue

Todos los archivos de este despliegue se encuentran en `sistema-monitoreo/`:

```text
compose.yaml
.env.example
prometheus/
  prometheus.yml
grafana/
  provisioning/
    datasources/
      prometheus.yml
```

- `compose.yaml`: define los servicios, la red `monitoreo` y los volúmenes `prometheus_data` y `grafana_data`.
- `prometheus/prometheus.yml`: configura la recolección de métricas cada 15 segundos; inicialmente Prometheus recopila sus propias métricas.
- `grafana/provisioning/datasources/prometheus.yml`: registra automáticamente Prometheus como fuente de datos de Grafana.

#### Archivo Docker Compose

El archivo `sistema-monitoreo/compose.yaml` contiene la definición completa del despliegue:

```yaml
services:
  prometheus:
    image: prom/prometheus:v3.7.3
    restart: unless-stopped
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.enable-remote-write-receiver"
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - monitoreo

  grafana:
    image: grafana/grafana:12.2.1
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD:?Definir GRAFANA_ADMIN_PASSWORD en .env}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources:ro
    networks:
      - monitoreo
    depends_on:
      - prometheus

networks:
  monitoreo:

volumes:
  prometheus_data:
  grafana_data:
```

#### Iniciar los servicios

Desde el directorio `sistema-monitoreo/`:

```bash
cp .env.example .env
```

Editar `.env` y reemplazar `cambiar-esta-contrasena` por una contraseña propia. El archivo `.env` está excluido de Git.

```bash
docker compose up -d
```

El comando crea la red y los volúmenes, y pone en marcha ambos contenedores.

#### Acceder a las interfaces

- **Grafana:** http://IP_DEL_SERVIDOR:3000 — usuario `admin` y la contraseña definida en `.env`.
- **Prometheus:** http://IP_DEL_SERVIDOR:9090

Los puertos están publicados en las interfaces del servidor. Desde otro equipo de la red, acceder mediante `http://IP_DEL_SERVIDOR:3000` (Grafana) y `http://IP_DEL_SERVIDOR:9090` (Prometheus). En una VM o servidor en la nube, el firewall también debe permitir el acceso a esos puertos.

En Grafana, la fuente de datos **Prometheus** ya estará configurada con la URL interna `http://prometheus:9090`. Podemos comprobar su funcionamiento desde **Explore**, ejecutando la consulta PromQL `up`, que debería mostrar la serie correspondiente al propio Prometheus.

#### Modelo de métricas y configuración de Prometheus

Para el laboratorio monitorearemos CPU, memoria, disco, red y tiempo de actividad. Las series temporales tendrán un nombre, un valor y etiquetas que permitan distinguir el servidor y, cuando corresponda, el recurso medido.

| Datos | Métricas previstas de Vector | Tipo |
| --- | --- | --- |
| CPU y carga | `host_cpu_seconds_total`, `load1`, `load5`, `load15` | Contador / indicadores |
| Memoria | `memory_total_bytes`, `memory_used_bytes`, `memory_available_bytes` | Indicadores |
| Disco | `filesystem_total_bytes`, `filesystem_used_bytes`, `filesystem_free_bytes` | Indicadores |
| Red | `network_receive_bytes_total`, `network_transmit_bytes_total` | Contadores |
| Tiempo de actividad | `uptime` | Indicador (segundos) |

Vector incluye la etiqueta `host` para identificar el servidor y otras etiquetas según el recurso, como `cpu`, `mode`, `device` y `filesystem`.

Además, definimos una métrica informativa propia, `host_info`, cuyo valor será `1` y cuyas etiquetas contendrán el hostname, sistema operativo, versión del kernel, arquitectura y virtualización. Esta métrica **no se genera automáticamente** con `host_metrics`; la construiremos al configurar Vector.

Prometheus no requiere declarar estas métricas previamente: las almacena al recibirlas. Para que los agentes Vector de distintos servidores puedan **enviar métricas** sin registrar sus direcciones IP, habilitamos el receptor `remote_write` en Prometheus.

En `compose.yaml`, el servicio `prometheus` incorpora:

```yaml
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.enable-remote-write-receiver"
```

Con esto, Prometheus acepta envíos en `http://IP_DEL_SERVIDOR:9090/api/v1/write`. La dirección corresponde al **servidor central de monitoreo**, no al host monitoreado. Cada Vector deberá apuntar a esa URL desde su configuración.

El archivo `prometheus/prometheus.yml` mantiene solamente la recolección de métricas del propio Prometheus:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]
```

No se agregan targets ni IP de los servidores Vector: sus métricas ingresarán por `remote_write`.

**Nota:** este ejemplo está pensado para un laboratorio en una red controlada. El receptor `remote_write` no incorpora autenticación por sí mismo; no debe exponerse sin protección a Internet.

#### Dashboard de Grafana

Grafana organiza la visualización en **dashboards** (tableros), compuestos por **paneles**. Cada panel contiene una o más consultas a Prometheus y representa sus resultados como indicadores o gráficos.

Para este laboratorio utilizaremos un único dashboard con una **fila repetida por servidor**. Cada fila reúne los datos de identificación y las visualizaciones de CPU, carga del sistema, memoria, disco, red y uptime. Así podemos comparar varios servidores en una misma pantalla.

La variable `host` obtiene automáticamente los nombres de servidores de las métricas almacenadas en Prometheus. Al seleccionar **All**, Grafana repite la fila para cada host disponible. Por eso, cuando Vector comience a enviar datos de un servidor nuevo, podrá incorporarse al mismo dashboard sin crear paneles manualmente.

El archivo [`dashboard-servidores.json`](dashboard-servidores.json), ubicado en la raíz del repositorio, contiene la definición del dashboard.

Para importarlo desde el navegador:

1. Abrir Grafana en `http://IP_DEL_SERVIDOR:3000`.
2. Ir a **Dashboards → New → Import** (la opción también puede aparecer como **Import dashboard**).
3. Cargar el archivo `dashboard-servidores.json` descargado del repositorio.
4. Seleccionar la fuente de datos **Prometheus** y confirmar la importación.
5. En el selector **Servidores**, elegir **All** para visualizar los hosts disponibles.

Los paneles mostrarán datos cuando Vector envíe las métricas correspondientes. El panel de identificación requiere además la métrica personalizada `host_info`, que se generará en la etapa de configuración de Vector.

## Recolección y envío de métricas con Vector

En esta etapa instalaremos y configuraremos Vector en los servidores GNU/Linux que queremos monitorear. Vector recopilará las métricas de CPU, memoria, disco, red y tiempo de actividad, incorporará los metadatos de identificación del host y enviará los datos al servidor central de Prometheus mediante `remote_write`, para su visualización en Grafana.

### Instalación de Vector

En cada servidor GNU/Linux que queremos monitorear, instalamos Vector mediante el script oficial:

```bash
curl --proto '=https' --tlsv1.2 -sSfL https://sh.vector.dev | bash
```

Para utilizar el ejecutable en la sesión actual de la terminal:

```bash
export PATH="$HOME/.vector/bin:$PATH"
```

Verificamos la instalación:

```bash
vector --version
```

Este procedimiento instala Vector en el directorio del usuario; todavía no configura la recolección de métricas, su envío a Prometheus ni su ejecución como servicio.

**Documentación oficial:** https://vector.dev/docs/setup/installation/

> Repositorio en construcción durante el vivo.
