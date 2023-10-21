####################################################################################################
# Base image
####################################################################################################
FROM python:3.11 AS base

# Set the working directory to /app
ENV APP_HOME /app
WORKDIR $APP_HOME

####################################################################################################
# Builder image
####################################################################################################
FROM base AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install the requirements
COPY pyproject.toml ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR pip install --upgrade pip \
 && pip install --no-cache-dir poetry \
 && poetry install --no-root \
 && rm -rf \
       ~/.cache/pip \
       POETRY_CACHE_DIR \
       poetry.lock

####################################################################################################
# Application image
####################################################################################################
FROM base AS app

# Copy the installed dependencies from the builder image
COPY --from=builder $APP_HOME/.venv $APP_HOME/.venv
ENV PATH="$APP_HOME/.venv/bin:$PATH"

# Copy application files
COPY app /app/

# Run the application
CMD ["python3", "app/bot.py"]  # FIXME: poetry is useless
