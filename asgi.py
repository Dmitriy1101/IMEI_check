"""ASGI for project"""

from fastapi import FastAPI

from back.main import app

application: FastAPI = app
