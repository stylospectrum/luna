import subprocess

from .config.settings import settings


def start():
    command = f"bentoml serve-grpc luna.bentoml_service:svc --port {settings.PORT} --api-workers 1 --reload"
    subprocess.run(command, shell=True)
