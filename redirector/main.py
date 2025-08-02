import uvicorn
from redirector.api import app


def main():
    uvicorn.run(app)
