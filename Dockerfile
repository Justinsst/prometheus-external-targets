FROM python:3.11.4-slim-bullseye

ENV APP_GROUP=python \
    APP_USER=python \
    APP_USER_ID=9999 \
    POETRY_VERSION=1.4.2 \
    DUMB_INIT_VERSION=1.2.2
ENV PATH="$PATH:/home/$APP_USER/.local/bin" \
    APP_DIR="~${APP_USER}/content"

# Install packages.
RUN apt-get update -y && apt-get install dnsutils wget -y
RUN wget -O /usr/local/bin/dumb-init \
        https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_amd64 \
    && chmod +x /usr/local/bin/dumb-init \
    && apt-get remove wget -y

# Create user and setup directories.
RUN useradd -ms /bin/bash --uid ${APP_USER_ID} ${APP_USER} \
    && mkdir -p ${APP_DIR}/external_targets \
    && chown -R ${APP_USER}:${APP_GROUP} ${APP_DIR}
WORKDIR ${APP_DIR}

USER ${APP_USER_ID}

# Copy files and install the Python package.
COPY --chown=${APP_USER}:${APP_USER} entrypoint.sh pyproject.toml ./
COPY --chown=${APP_USER}:${APP_USER} external_targets/ ./external_targets/
RUN chmod +x entrypoint.sh \
    && pip install --user poetry==${POETRY_VERSION} \
    && poetry install --no-cache --only main

ENTRYPOINT ["dumb-init", "--", "./entrypoint.sh"]