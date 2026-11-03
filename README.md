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

## Grafana

![Logo de Grafana](https://upload.wikimedia.org/wikipedia/commons/a/a1/Grafana_logo.svg)

### ¿Qué es Grafana?

[Grafana](https://grafana.com/) es una plataforma de código abierto para consultar, analizar y visualizar datos provenientes de distintas fuentes mediante gráficos, indicadores y paneles interactivos (*dashboards*).

### ¿Cómo funciona Grafana?

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

> Repositorio en construcción durante el vivo.
