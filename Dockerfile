# 1. Base Image
# Start with the lean Python image we prefer.
FROM python:3.11-slim

# 2. Install uv and set up Working Directory/Environment
# Set up the working directory.
WORKDIR /app


# Install uv utility from its container image.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set the cache directory to a writable location before dependencies are installed.
ENV XDG_CACHE_HOME=/app/whisper_cache

# 3. Install OS Dependencies
# Combine apt-get steps to leverage caching and minimize image size.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir -p ${XDG_CACHE_HOME} && \
    chmod -R a+w ${XDG_CACHE_HOME}

# 4. Install Python Dependencies
# Only copy files necessary for dependency resolution (best for caching).
COPY README.md .
COPY uv.lock .
COPY pyproject.toml .

# This guarantees the path /app/.venv/bin/python will exist.
RUN uv sync --no-dev --frozen

# 5. Copy Application Code
# Changes to source code here won't invalidate the slow dependency layer above.
COPY src src

# 6. Final Command
CMD [ "/app/.venv/bin/python", "src/transcriber/transcribe.py" ]

# # Install uv
# FROM python:3.11-slim
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# # Change the working directory to the `app` directory
# WORKDIR /app

# # Copy the lockfile and `pyproject.toml` into the image
# COPY README.md .
# COPY uv.lock /app/uv.lock
# COPY pyproject.toml /app/pyproject.toml

# # Install OS updates and dependencies
# RUN apt-get update && apt-get install -y ffmpeg

# # Install our python requirements.
# RUN uv sync --no-dev --frozen
# #     uv sync --no-deps --frozen --no-install-project

# COPY src src

# # Sync the project
# # RUN uv sync --frozen

# # Set the cache directory to a writable location within the app directory
# ENV XDG_CACHE_HOME=/app/whisper_cache

# CMD [ "/app/.venv/binpython", "src/transcriber/transcribe.py" ]
