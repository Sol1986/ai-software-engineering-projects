# Start from a small Linux image that already includes Python 3.11.
FROM python:3.11-slim

# Copy the uv and uvx executables from the official uv Docker image
# into this container's /bin folder.
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

# Set /app as the working folder for the following instructions
# and for the running application.
WORKDIR /app

# Tell uv not to install development-only packages such as pytest.
# Use copying instead of links when uv installs package files.
# Stop Python from creating __pycache__ files.
# Send Python output directly to the container logs without buffering.
ENV UV_NO_DEV=1 \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy only dependency-definition files first.
# Docker can reuse this cached layer when your source code changes
# but your dependencies do not.
COPY pyproject.toml uv.lock ./

# Install the exact locked production dependencies.
# --locked refuses to change uv.lock.
# --no-install-project delays installing your own application until its code is copied.
RUN uv sync --locked --no-install-project

# Copy the rest of your project files into /app.
COPY . .

# Synchronize again now that the application source code is available.
# --locked again ensures Docker uses the exact dependency versions in uv.lock.
RUN uv sync --locked

# Document that this container listens on port 8000.
# This does not open the port by itself; Docker or the cloud platform maps it.
EXPOSE 8000

# Ask Docker to check the /health endpoint every 30 seconds.
# A check may take up to 3 seconds.
# Give the app 10 seconds to start before considering failures.
# Mark the container unhealthy after 3 failed checks.
# Run a small Python command that opens the local health endpoint.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# The command Docker runs when the container starts.
# uv run uses the existing environment without syncing packages again.
# fastapi run starts the production server from main.py.
# --host 0.0.0.0 makes it reachable outside the container.
# --port 8000 tells it which port to listen on.
CMD ["uv", "run", "--no-sync", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]