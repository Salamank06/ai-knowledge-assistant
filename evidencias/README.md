# Evidencias — AI Knowledge Assistant (Módulo 0)

Esta carpeta contiene las capturas y salidas crudas que respaldan la entrega del proyecto. Cada archivo está nombrado con un prefijo numérico que respeta el orden sugerido para la sustentación.

## Índice

| #   | Archivo                              | Qué demuestra                                                                                              |
| --- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| 01  | `01_swagger_docs.png`                | Documentación OpenAPI/Swagger accesible en `/docs` (RF-09).                                                |
| 02  | `02_get_health.png`                  | `GET /health` retorna 200 con `status: ok` (RF-01, T-02).                                                  |
| 03  | `03_get_info.png`                    | `GET /api/v1/info` retorna 200 con `llm_enabled: false` (RF-10, T-05).                                     |
| 04  | `04_post_chat_valido_200.png`        | `POST /api/v1/chat` con pregunta válida retorna 200 y `provider: bootstrap-local` (RF-02, RF-06, RF-07, T-03). |
| 05  | `05_post_chat_invalido_422.png`      | `POST /api/v1/chat` con `"ab"` retorna 422 por `min_length=3` (RF-05, T-04).                               |
| 06  | `06_post_chat_missing_field_422.png` | `POST /api/v1/chat` con body `{}` retorna 422 por campo obligatorio (robustez de Pydantic).                 |
| 07  | `07_pytest_output.png`               | `python -m pytest -v` con 11/11 pruebas en verde (gate de calidad).                                         |
| 08  | `08_flujo_request_response.png`      | Diagrama del flujo `Cliente → FastAPI → Pydantic → Service → Response` para la sustentación.                |
| 09  | `09_git_historia_ramas.png`          | `git log`, `git branch` y `git remote` con la historia de commits y el remoto en GitHub.                   |
| 10  | `10_pull_request_github.png`         | Pull Request #1 abierto en GitHub (`feat/bootstrap-api` → `main`).                                          |

## Archivos de soporte (texto plano)

| Archivo              | Contenido                                              |
| -------------------- | ------------------------------------------------------ |
| `pytest_output.txt`  | Salida cruda de `python -m pytest -v` (11/11 PASSED).  |
| `git_log.txt`        | Salida de `git log --oneline --decorate --all --graph`. |
| `git_branch.txt`     | Salida de `git branch -vv`.                            |
| `git_remote.txt`     | Salida de `git remote -v`.                             |

## Cómo reproducir las capturas

```bash
# 1. Activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
pip install -e ".[dev]"

# 2. Levantar la API
uvicorn app.main:app --reload

# 3. Probar los endpoints (en otra terminal)
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/info
curl -X POST http://127.0.0.1:8000/api/v1/chat -H "Content-Type: application/json" -d "{\"question\": \"¿Qué es FastAPI?\"}"
curl -X POST http://127.0.0.1:8000/api/v1/chat -H "Content-Type: application/json" -d "{\"question\": \"ab\"}"

# 4. Correr la suite
python -m pytest -v

# 5. Ver la documentación interactiva
#    Abrir http://127.0.0.1:8000/docs en el navegador
```
