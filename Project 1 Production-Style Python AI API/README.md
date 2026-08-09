# Production-Style Python AI API

## Overview
A FastAPI service that accepts a business request, validates it with Pydantic, calls OpenAI GPT-5.6 Luna, and returns a structured JSON response.

## Features
- FastAPI REST API with automatic OpenAPI documentation
- Pydantic request and response validation
- Typed Python code
- OpenAI Responses API integration
- Structured JSON logging
- Environment-based configuration
- Error handling for validation, missing configuration, and provider failures
- Unit tests with a fake LLM client
- Docker containerization
- GitHub Actions CI

## API Endpoints
- `GET /health` — confirms the service is running
- `POST /v1/business-responses` — generates a structured AI response

## Local Setup
## Testing
## Docker
## CI
## API Documentation
## Architecture
## Future Improvements

## For Testing

```json
{
  "business_request": "Give three practical ways a small e-commerce store can reduce customer support response time.",
  "context": {
    "business_size": "small",
    "industry": "e-commerce"
  }
}
```

## Notes

Docker image = the packaged blueprint containing Python, uv, dependencies, and your code

Docker container = a live running instance of that blueprint

When a container starts, it runs your Dockerfile’s final command:
CMD ["uv", "run", "--no-sync", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]


## Local Setup

1. Install Python 3.11 and uv.
2. Run `uv sync` to install locked dependencies.
3. Create a local `.env` file from `.env.example`.
4. Add your OpenAI API key to `.env`.
5. Start the API with `uv run fastapi dev main.py`.
6. Open `http://127.0.0.1:8000/docs`.

## Testing

Run the quality checks before committing:

- `uv run ruff check .`
- `uv run python -m mypy .`
- `uv run python -m pytest`

The test suite uses a fake LLM client, so automated tests do not make paid OpenAI API calls.

## Docker

Build the image:

`docker build -t production-style-python-ai-api:0.1.0 .`

Run the container:

`docker run --rm -p 8000:8000 --env-file .env production-style-python-ai-api:0.1.0`

Then open `http://localhost:8000/docs`.

## CI

GitHub Actions runs Ruff, mypy, and pytest whenever Project 1 or its workflow changes.

## API Documentation

FastAPI generates interactive OpenAPI documentation at `/docs` and the raw OpenAPI schema at `/openapi.json`.

## Architecture

Client → FastAPI route → Pydantic validation → LLM client → OpenAI Responses API

Structured logging records operational events. Exception handlers return consistent JSON errors for invalid requests, missing configuration, and LLM provider failures.

## Future Improvements

- Add authentication and rate limiting.
- Add request tracing and cloud monitoring.
- Add retry handling for temporary provider errors.
- Return a stricter AI-generated response schema.
- Deploy the container to a cloud service.