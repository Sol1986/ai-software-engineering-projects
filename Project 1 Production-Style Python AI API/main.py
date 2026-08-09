import logging
from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from llm_client import (
    LLMClient,
    LLMConfigurationError,
    LLMProviderError,
    get_llm_client,  #2
)
from logging_config import configure_logging
from schemas import BusinessRequest, BusinessResponse
from settings import Settings

settings = Settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__) # Creates a logger for this file, using the file’s name as the logger name.

llm_client = get_llm_client(settings) #3

app = FastAPI(
    title = "settings.app_name",
    version = "0.1.0",
    description = "A simple API for business AI applications."
)

# Registers this function as the handler for RequestValidationError errors.
# FastAPI calls it automatically when request validation fails.
# Defines an asynchronous function named request_validation_error_handler.
# async lets FastAPI run it properly within its asynchronous request system.
# An asynchronous function is a function that can pause while it waits for something slow—such as an LLM API call, database query, or network request—so your server can handle other requests instead of sitting idle.
@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:

    """If a request fails validation, log a warning with the endpoint path and number of problems. 
    Then return a clear JSON error response with status code 422 and the details needed to fix the request."""

    logger.warning(
        "request_validation_failed",
        extra={
            "path": request.url.path,
            "error_count": len(exc.errors()),
        },
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",

            # jsonable_encoder converts them into data that JSON can safely represent.
            "detail": jsonable_encoder(exc.errors()),
        },
    )

@app.exception_handler(LLMConfigurationError)
async def llm_configuration_error_handler(request: Request,exc: LLMConfigurationError) -> JSONResponse:
    logger.error("llm_configuration_error", extra={"path": request.url.path})

    return JSONResponse(
        status_code=503,
        content={
            "error": "llm_not_configured",
            "detail": "The AI service is not configured.",
        },
    )


@app.exception_handler(LLMProviderError)
async def llm_provider_error_handler(request: Request,exc: LLMProviderError) -> JSONResponse:
    logger.error("llm_provider_error", extra={"path": request.url.path})

    return JSONResponse(
        status_code=502,
        content={
            "error": "llm_provider_error",
            "detail": "The AI service could not generate a response.",
        },
    )



@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """
    Health check on the endpoint
    """
    logger.info("Health check endpoint called.") # Logs an informational message when the health check endpoint is accessed.
    return {"status": "ok"}

@app.post("/v1/business-responses", response_model = BusinessResponse, tags=["AI"])
def create_business_response(request:BusinessRequest, llm_client: Annotated[LLMClient, Depends(get_llm_client)]) -> BusinessResponse:
    """
    Process a business request and return a response.
    """

    # “Before running this endpoint, create or get an LLM client using get_llm_client, then place it in the llm_client variable.”
    

    answer=llm_client.generate(business_request=request.business_request, context=request.context)

    request_id = uuid4()
    logger.info("business_response_created", # An event named business_response_created happened.
                # extra adds useful details to that log event
                extra= { 
                    "request_id": str(request_id),
                    "llm_provider": settings.llm_provider,  
                }
    )
    return BusinessResponse(
        request_id = request_id,
        answer = answer,
        model = settings.llm_model,
        created_at = datetime.now(UTC)
    )
    

