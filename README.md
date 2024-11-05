# Proyecto de Pipeline de Datos con Apache Airflow

Este proyecto implementa una pipeline de datos utilizando Apache Airflow para extraer, transformar y cargar datos de usuarios en una base de datos PostgreSQL.

## Estructura del Proyecto

```
airflow_dag_1
├── dags
│   ├── user_pipeline.py          # Definición del DAG para la pipeline
├── docker-compose.yml            # Configuración de servicios para Airflow y PostgreSQL
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Documentación del proyecto
```

## Requisitos

Asegúrate de tener Docker y Docker Compose instalados en tu máquina.

## Instalación

1. Clona este repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Ejecuta el siguiente comando para construir y ejecutar los contenedores:

   ```bash
   docker-compose up -d
   ```

## Uso

Una vez que los contenedores estén en funcionamiento, puedes acceder a la interfaz de usuario de Airflow en `http://localhost:8080`.

## Descripción de Archivos

- **dags/user_pipeline.py**: Define el DAG que orquesta las tareas de extracción, transformación y carga.
- **scripts/extract_users.py**: Contiene la función `extract_users()` para obtener datos de usuarios desde PostgreSQL.
- **scripts/transform_users.py**: Contiene la función `transform_users(data)` para aplicar transformaciones a los datos extraídos.
- **scripts/load_users.py**: Contiene la función `load_users(transformed_data)` para insertar los datos transformados en PostgreSQL.
- **docker-compose.yml**: Define los servicios necesarios para ejecutar Airflow y PostgreSQL.
- **requirements.txt**: Lista las dependencias necesarias para el proyecto.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.