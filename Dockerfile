FROM python:3.7-slim

CMD ["bin/entrypoint.sh"]

EXPOSE 8000

HEALTHCHECK --interval=5m --timeout=15s --start-period=30s \
    CMD curl --fail http://127.0.0.1:8000/admin/ || exit 1

ENV APP_ROOT=/opt/app \
    APP_USER=django \
    LOG_LEVEL=info \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR $APP_ROOT

RUN useradd -d $APP_ROOT -r $APP_USER

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        postgresql-client \
    && \
    apt-get clean

RUN pip install --upgrade pip

ADD requirements.txt $APP_ROOT

RUN pip install -r requirements.txt

ADD . $APP_ROOT

RUN python3 manage.py collectstatic --no-input

USER $APP_USER
