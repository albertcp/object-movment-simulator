# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm

# Runtime libraries required by pygame (SDL2, X11, OpenGL).
# Build tooling is not needed: pygame/pydantic ship manylinux wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libx11-6 \
    libxext6 \
    libxrandr2 \
    libxcursor1 \
    libxi6 \
    libxinerama1 \
    libxss1 \
    libsm6 \
    libice6 \
    libgl1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    SDL_VIDEODRIVER=x11

WORKDIR /app

# Install dependencies first so this layer is cached while source changes.
COPY requirements.txt .
RUN python -m venv .venv \
    && .venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as an unprivileged user; the app only needs the X11 socket/TCP display.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# DISPLAY is supplied at runtime (X11 socket mount or XQuartz TCP).
CMD [".venv/bin/python", "Simulator.py"]
