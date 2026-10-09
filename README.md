# AI Knowledge Assistant — Bootstrap API

> Módulo 0 · Ingeniería de Sistemas de IA · Incremento bootstrap (sin LLM todavía)

Esta es la **base técnica** del asistente de conocimiento: una API asíncrona con FastAPI, validada con Pydantic, probada con pytest y preparada para que en los próximos módulos se le conecte un proveedor de modelos de lenguaje (LLM), RAG, agentes, observabilidad, etc.

Hoy **no** integra ningún LLM: la ruta `POST /api/v1/chat` devuelve una respuesta determinista de marcador de posición marcada con `provider: "bootstrap-local"`.

---

## 1. Stack

| Capa            | Tecnología                                |
| --------------- | ----------------------------------------- |
| Lenguaje        | Python 3.12+                              |
| Framework HTTP  | FastAPI                                   |
| Validación      | Pydantic v2                               |
| Concurrencia    | AsyncIO                                   |
| Cliente HTTP    | HTTPX (asíncrono)                         |
| Tests           | pytest + pytest-asyncio                   |
| Empaquetado     | pyproject.toml                            |
| Versionamiento  | Git / GitHub                              |

**No incluye (por restricción del módulo 0):** OpenAI, Anthropic, Gemini, Ollama, LangChain, LangGraph, PostgreSQL, Redis, bases vectoriales, Docker, RAG, agentes ni memoria conversacional.

---

## 2. Estructura del proyecto

```
ai-knowledge-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Factoría create_app + instancia app
│   ├── config.py               # Configuración / metadata
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py       # GET /health
│   │       ├── chat.py         # POST /api/v1/chat
│   │       └── info.py         # GET /api/v1/info
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py             # ChatRequest, ChatResponse
│   │   ├── info.py             # AppInfo
│   │   └── health.py           # HealthResponse
│   └── services/
│       ├── __init__.py
│       └── chat_service.py     # Lógica de respuesta bootstrap
├── scripts/
│   └── async_demo.py           # Demo AsyncIO + HTTPX concurrentes
├── tests/
│   ├── conftest.py             # Fixture TestClient
│   ├── unit/
│   │   └── test_chat_service.py
│   └── integration/
│       ├── test_health.py
│       ├── test_chat.py
│       ├── test_info.py
│       ├── test_docs.py
│       └── test_async_client.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Flujo de una petición: **Cliente → FastAPI (router) → Pydantic (validación) → Servicio → Respuesta tipada**

---

## 3. Instalación y ejecución local

### 3.1 Clonar (cuando ya esté en GitHub)

```bash
git clone https://github.com/<tu-usuario>/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

### 3.2 Crear y activar el entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3.3 Instalar dependencias (incluye las de desarrollo)

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 3.4 Levantar la API

```bash
uvicorn app.main:app --reload
```

- API:        <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc:      <http://127.0.0.1:8000/redoc>
- OpenAPI:    <http://127.0.0.1:8000/openapi.json>

### 3.5 Probar manualmente

**Health:**
```bash
curl http://127.0.0.1:8000/health
```

**Chat (válido):**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"¿Qué es FastAPI?\"}"
```

**Chat (inválido — debe devolver 422):**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"ab\"}"
```

**Info:**
```bash
curl http://127.0.0.1:8000/api/v1/info
```

### 3.6 Demo asíncrona (AsyncIO + HTTPX)

Con la API levantada en otra terminal:

```bash
python scripts/async_demo.py
```

Verás cómo 3 peticiones se disparan en paralelo con `asyncio.gather` y se serializa el resultado.

---

## 4. Pruebas automatizadas

```bash
python -m pytest -q
```

Salida esperada: todas las pruebas en verde, incluyendo:

| ID    | Descripción                                                                  |
| ----- | ---------------------------------------------------------------------------- |
| T-01  | Unit test del servicio: responde correctamente a una pregunta conocida.     |
| T-02  | `GET /health` retorna HTTP 200.                                              |
| T-03  | `POST /api/v1/chat` con pregunta válida retorna HTTP 200.                    |
| T-04  | `POST /api/v1/chat` con pregunta demasiado corta retorna HTTP 422.           |
| T-05  | `GET /api/v1/info` retorna HTTP 200 y `llm_enabled = false`.                 |

Además se incluye:
- Test del esquema OpenAPI y de Swagger UI.
- Test de cliente HTTPX asíncrono lanzando 3 requests concurrentes (evidencia de AsyncIO).

---

## 5. Contratos HTTP

### `GET /health` → 200
```json
{ "status": "ok", "service": "AI Knowledge Assistant", "version": "0.1.0" }
```

### `POST /api/v1/chat` (request)
```json
{ "question": "¿Qué es FastAPI?" }
```

### `POST /api/v1/chat` (response, 200)
```json
{
  "answer": "[bootstrap-local] Recibí tu pregunta...",
  "provider": "bootstrap-local"
}
```

### `POST /api/v1/chat` (entrada inválida, 422)
Pydantic rechaza cuando `question`:
- Tiene menos de 3 o más de 2000 caracteres.
- Está compuesta solo por espacios.
- Falta en el body.

### `GET /api/v1/info` → 200
```json
{
  "name": "AI Knowledge Assistant",
  "version": "0.1.0",
  "environment": "development",
  "llm_enabled": false
}
```

---

## 6. Decisiones de diseño

- **Separación de responsabilidades.** El router valida y delega; el servicio concentra la lógica; los schemas aíslan la forma del contrato HTTP. Esto facilita sustituir el `ChatService` por uno que invoque un LLM sin tocar el router.
- **`async def` en los endpoints.** Aunque el bootstrap no hace I/O externa, mantener la firma asíncrona evita romper consumidores cuando se conecte un proveedor real.
- **Pydantic v2 con `field_validator`.** Permite limpiar espacios y reforzar la regla "mínimo 3 caracteres reales" más allá de `min_length`.
- **`create_app()` factoría.** Permite que las pruebas instancien la app en proceso sin un servidor HTTP real.
- **Sin secretos en el repo.** `.env*` está ignorado por `.gitignore` y solo se versiona `.env.example`.

---

## 7. Próximos módulos (lo que cambiará vs. lo que permanece estable)

| Permanecerá estable                        | Cambiará                                          |
| ------------------------------------------ | ------------------------------------------------- |
| Contrato HTTP (`/api/v1/chat`, `/info`)    | Implementación del `ChatService` (LLM real)       |
| Estructura `router → service → schema`     | Config (proveedor, modelo, temperatura)           |
| Suite de tests (se ampliará)               | Scripts de demo (probabilidad, embeddings, RAG)   |
| Flujo de Git: rama feature + PR            | Despliegue / observabilidad                       |

---

## 8. Evidencias

Las capturas y salidas que respaldan la entrega están en la carpeta [`evidencias/`](./evidencias/) e incluyen:

- Swagger UI en `/docs`, `GET /health`, `GET /api/v1/info`
- `POST /api/v1/chat` con respuesta válida (200) y con validación 422 (pregunta corta y campo faltante)
- Salida completa de `pytest -v` con 11/11 pruebas en verde
- Diagrama del flujo `Cliente → FastAPI → Pydantic → Service → Response`
- Historia de Git (commits, ramas y remoto)
- Pull Request abierto en GitHub

Ver el índice completo en [`evidencias/README.md`](./evidencias/README.md).

---

## 9. Checklist de entrega

- [x] Python 3.12+ · `.venv` creado y excluido del repo
- [x] `pyproject.toml` con dependencias y extras `dev`
- [x] Endpoints `/health`, `/api/v1/chat`, `/api/v1/info` funcionales
- [x] Pydantic valida longitud mínima/máxima y entradas vacías
- [x] Servicio separado del router
- [x] Evidencia de `async/await` (routers, servicio, script y test)
- [x] HTTPX usado de forma asíncrona (`scripts/async_demo.py`, `test_async_client.py`)
- [x] Tests unitarios + integración, suite en verde con `python -m pytest -q`
- [x] `/docs` y `/openapi.json` operativos
- [x] README reproducible
- [x] `.gitignore` ignora `.venv`, caches, `.env*`
- [x] Sin secretos en el repositorio
- [x] Rama `feat/bootstrap-api` con commits pequeños y PR (evidencia)

---

## 10. Licencia

Material académico del curso **Ingeniería de Sistemas de IA** — uso educativo.
