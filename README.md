# Monitoreo de sistemas con Vector y Grafana

Material de trabajo para el vivo del **3 de noviembre de 2026**.

**Transmisión en vivo:** https://youtube.com/live/oEYg71x0RoQ

## Descripción

En este encuentro vamos a trabajar con [Vector](https://vector.dev/), una herramienta de código abierto que permite recopilar, transformar y transmitir datos de observabilidad, incluidas métricas de diferentes sistemas.

Vamos a explorar cómo utilizarla para obtener información de nuestros servidores y enviarla a un sistema de monitoreo, donde podremos visualizarla mediante paneles gráficos con [Grafana](https://grafana.com/).

## Objetivo

Explorar un flujo de monitoreo de sistemas basado en la recolección de métricas con Vector y su visualización en Grafana.

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

#### Detener los servicios

```bash
docker compose down
```

Los volúmenes conservan los datos aunque se eliminen los contenedores. **No utilizar `docker compose down -v`** si se desea conservarlos.

> Repositorio en construcción durante el vivo.
