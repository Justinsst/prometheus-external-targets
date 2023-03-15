FROM python:3.8.16-slim-bullseye

ARG APP_DIR="/home/python/external_targets"
ARG USERNAME="python"

ENV APP_DIR $APP_DIR
ENV DUMB_INIT_VERSION=1.2.2

RUN apt-get update -y && apt-get install dnsutils wget -y
RUN useradd -ms /bin/bash ${USERNAME} \
    && mkdir ${APP_DIR} \
    && chown -R ${USERNAME}:${USERNAME} ${APP_DIR}

WORKDIR ${APP_DIR}

RUN  wget -O /usr/local/bin/dumb-init \
        https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_amd64 \
    && chmod +x /usr/local/bin/dumb-init \
    && apt-get remove wget -y

USER 1000
COPY --chown=${USERNAME}:${USERNAME} entrypoint.sh requirements.txt ./
RUN chmod +x entrypoint.sh \
    && pip install --user -r requirements.txt
COPY --chown=${USERNAME}:${USERNAME} external_targets/ ./

ENTRYPOINT ["dumb-init", "--", "./entrypoint.sh"]