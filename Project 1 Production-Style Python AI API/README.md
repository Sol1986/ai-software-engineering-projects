{
  "business_request": "Give three practical ways a small e-commerce store can reduce customer support response time.",
  "context": {
    "business_size": "small",
    "industry": "e-commerce"
  }
}

Docker image
= the packaged blueprint containing Python, uv, dependencies, and your code

Docker container
= a live running instance of that blueprint

When a container starts, it runs your Dockerfile’s final command:
CMD ["uv", "run", "--no-sync", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]