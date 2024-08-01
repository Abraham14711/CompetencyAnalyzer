#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from competencyAnalyser.config import settings
from competencyAnalyser.db.database import init_db
from competencyAnalyser.routers import answers, questions, users, vacancies, hr
from competencyAnalyser.routers import business_types, competencies, main
from competencyAnalyser.routers.i18n_middleware import I18nMiddleware
from competencyAnalyser.scripts import ai
from pathlib import Path

from competencyAnalyser.config import MIDDLEWARE_KEY, templates
from starlette.middleware.sessions import SessionMiddleware

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from alembic.config import Config
from alembic import command

log = logging.getLogger("uvicorn")


async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up...")
    log.info("run alembic upgrade head...")
    if os.environ.get("RUN_MIGRATIONS", "True"):
        # await run_migrations()  # RUN THIS CODE WHEN UPDATE DATABASE
        os.environ["RUN_MIGRATIONS"] = "False"
    yield
    log.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(
        directory=Path(__file__).parent.parent.parent.absolute() / "static"
    ),
    name="static",
)

origins = [
    settings.CLIENT_ORIGIN
]

app.add_middleware(SessionMiddleware, secret_key=MIDDLEWARE_KEY)
app.add_middleware(I18nMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(hr.router, prefix="/hr", tags=["/hr"])
app.include_router(ai.router, prefix="/api/ai", tags=["/ai"])
app.include_router(main.router, tags=["Main"])
app.include_router(answers.router, prefix="/api/answers",
                   tags=["Answers"])
app.include_router(
    questions.router, prefix="/api/questions", tags=["Questions"]
)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(
    vacancies.router, prefix="/api/vacancies", tags=["Vacancies"]
)
app.include_router(
    business_types.router, prefix="/api/business-types",
    tags=["Business Types"]
)
app.include_router(
    competencies.router, prefix="/api/competencies",
    tags=["Competencies"]
)


@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello World'}


def start():
    init_db()
    """Launched with `poetry run start` at root level"""
    uvicorn.run("competencyAnalyser.scripts.competencyAnalyser:app",
                host="0.0.0.0", port=8000, reload=True,
                timeout_graceful_shutdown=10000000)


if __name__ == '__main__':
    start()
