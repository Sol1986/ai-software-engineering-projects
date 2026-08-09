import pytest
from fastapi.testclient import TestClient
from llm_client import LLMConfigurationError
from main import app, get_llm_client


# protect tests from real API calls by replacing the OpenAI dependency with a fake client.
class FakeLLMClient:
    def generate(self,business_request: str,context: dict[str, str]) -> str:
        return "Test AI answer"

def get_fake_llm_client() -> FakeLLMClient:
    return FakeLLMClient()


app.dependency_overrides[get_llm_client] = get_fake_llm_client

# Create a TestClient instance for testing the FastAPI app
client = TestClient(app)

# test the /health endpoint
def test_client_check() -> None:
    """Test the /health endpoint to ensure the API is running and responding correctly.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Test the /v1/business-responses endpoint
def test_business_response () -> None:
    """Test the /v1/business-responses endpoint to ensure it processes business requests correctly."""
    response = client.post ("/v1/business-responses",

        json = {
            "business_request": "Recommend ways to reduce customer issues",
            "context": {"industry": "Retail"},
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["answer"] == "Test AI answer"
    assert body["model"] == "gpt-5.6-luna"
    assert "request_id" in body # checks if the key "request_id" is present in the response body
    assert "created_at" in body # checks if the key "created_at" is present in the response body

# tests the minimum length of characters in the request
def test_business_request_rejects_short_text() -> None:

    response = client.post("/v1/business-responses",
                           json = {"business_request": "short"},
                           )

    body = response.json()

    assert response.status_code == 422
    assert body["error"] == "validation_error"
    # assert means: “This must be true for the test to pass.”
    # “Check that the validation error points to the business_request field. If it does not, fail this test.”
    assert body["detail"][0]["loc"][-1] == "business_request"

    assert response.status_code == 422

# test for when llm is not configured
def test_returns_503_when_llm_is_not_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    def get_missing_llm_client() -> FakeLLMClient:
        raise LLMConfigurationError("Missing API key.")

    # This temporarily tells FastAPI to use a fake replacement dependency during one test.
    # “For this test only, whenever FastAPI needs get_llm_client, use get_missing_llm_client instead.”
    # monkeypatch is a pytest testing tool that temporarily changes something while one test runs.
    # In a test, you may want to pretend the API key is missing. monkeypatch lets you temporarily replace the real LLM client setup with a fake one.
    monkeypatch.setitem(
        app.dependency_overrides,
        get_llm_client,
        get_missing_llm_client,
    )

    response = client.post("/v1/business-responses",
        json={
            "business_request": "Recommend ways to improve customer retention.",
        },
    )

    assert response.status_code == 503
    assert response.json()["error"] == "llm_not_configured"