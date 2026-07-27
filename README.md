# ⚽ Football World Cup ETL Pipeline

Pipeline de datos automatizado que extrae, transforma y carga información de partidos del Mundial 2026 desde una API pública, orquestado con Apache Airflow y corriendo completamente en contenedores Docker.

## 📋 Descripción

Este proyecto simula un flujo de trabajo real de Data Engineering: extrae datos en vivo de una API de fútbol, los limpia y transforma con Pandas, y los carga en una base de datos PostgreSQL — todo de forma automatizada mediante Airflow, ejecutándose cada 6 horas sin intervención manual.

## 🏗️ Arquitectura

┌─────────────────┐ ┌──────────┐ ┌───────────────┐ ┌────────────┐
│ football-data.org│ --> │ Extract │ --> │ Transform │ --> │ Load │
│ API │ │ (requests)│ │ (Pandas) │ │ (psycopg2) │
└─────────────────┘ └──────────┘ └───────────────┘ └────────────┘
│
v
┌──────────────┐
│ PostgreSQL │
│ (Docker) │
└──────────────┘

Todo orquestado por Apache Airflow (Docker), corriendo cada 6 horas.

**Flujo del DAG:** `extract_matches` → `transform_matches` → `load_matches`

## 🛠️ Stack tecnológico

- **Python** — lenguaje principal
- **Pandas** — transformación y limpieza de datos
- **Requests** — consumo de la API REST
- **psycopg2** — conexión a PostgreSQL
- **PostgreSQL 16** — almacenamiento de datos
- **Apache Airflow 2.10.5** — orquestación del pipeline
- **Docker & Docker Compose** — contenerización de todos los servicios
- **python-dotenv** — manejo seguro de credenciales
- **Git & GitHub** — control de versiones

## 📁 Estructura del proyecto

football-pipeline/
├── dags/
│ ├── football_dag.py # Definición del DAG de Airflow
│ └── scripts/
│ ├── extract.py # Extracción de datos desde la API
│ ├── transform.py # Limpieza y transformación con Pandas
│ └── load.py # Carga a PostgreSQL (upsert)
├── data/
│ ├── raw/ # JSON crudo de la API (respaldo)
│ └── processed/ # CSV limpio y transformado
├── docker-compose.yml # Contenedor de PostgreSQL (datos)
├── docker-compose-airflow.yaml # Stack completo de Airflow
├── .env.example # Plantilla de variables de entorno
└── README.md

## 🚀 Cómo levantarlo

### Requisitos previos
- Docker Desktop con WSL2 (Windows) o Docker nativo (Linux/Mac)
- Python 3.10+
- Una cuenta gratuita en [football-data.org](https://www.football-data.org/) para obtener tu API token

### 1. Clonar el repositorio
```bash
git clone https://github.com/GonzaaFuness/football-pipeline.git
cd football-pipeline
```

### 2. Configurar variables de entorno
Copiá `.env.example` a `.env` y completá tus credenciales:

FOOTBALL_API_TOKEN=tu_token_de_football-data.org
DB_HOST=localhost
DB_PORT=5432
DB_NAME=football_db
DB_USER=football_user
DB_PASSWORD=football_pass
FOOTBALL_DB_HOST=localhost
FOOTBALL_DB_PORT=5432
FOOTBALL_DB_NAME=football_db
FOOTBALL_DB_USER=football_user
FOOTBALL_DB_PASSWORD=football_pass
AIRFLOW_UID=50000

### 3. Levantar PostgreSQL (datos del pipeline)
```bash
docker compose -p football_data up -d
```

### 4. Levantar Airflow
```bash
docker compose -f docker-compose-airflow.yaml -p airflow_orchestration up airflow-init
docker compose -f docker-compose-airflow.yaml -p airflow_orchestration up -d
```

### 5. Acceder a la interfaz de Airflow
Abrí [http://localhost:8080](http://localhost:8080) — usuario y contraseña por defecto: `airflow` / `airflow`.

Activá el DAG `football_world_cup_pipeline` y disparalo manualmente, o esperá su ejecución programada (cada 6 horas).

### 6. Ejecutar los scripts manualmente (opcional)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt

python dags\scripts\extract.py
python dags\scripts\transform.py
python dags\scripts\load.py
```

## 📊 Ejemplo de datos cargados

| home_team | away_team | home_score | away_score | status |
|-----------|-----------|------------|------------|--------|
| Mexico | South Africa | 2 | 0 | FINISHED |
| South Korea | Czechia | 2 | 1 | FINISHED |

## 📈 Dashboard interactivo

El proyecto incluye un dashboard con Streamlit para visualizar los datos cargados: métricas generales, ranking de goles por equipo, distribución de partidos por fase, y tabla filtrable.

```bash
pip install streamlit plotly
streamlit run dashboard.py
```

Se abre automáticamente en `http://localhost:8501`.

## 🔮 Posibles mejoras futuras

- Dashboard de visualización (Streamlit / Metabase)
- Extensión a más competencias (Champions League, Copa Libertadores)
- Tests automatizados con pytest
- CI/CD con GitHub Actions

## 👤 Autor

Gonzalo Funes

