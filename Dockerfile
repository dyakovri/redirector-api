FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ARG APP_NAME
ENV APP_NAME=${APP_NAME}
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

ENV UV_LINK_MODE=copy

WORKDIR /apps
ADD . /apps/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --active --locked --no-install-project

CMD ["python", "-m", "redirector"]
