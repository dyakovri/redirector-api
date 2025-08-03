#!/bin/bash

alembic upgrade head

uvicorn redirector.main:app --host 0.0.0.0 --port 8000
