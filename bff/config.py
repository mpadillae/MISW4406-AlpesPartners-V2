import os


class Config:
    AFILIACIONES_SERVICE_URL = os.getenv(
        "AFILIACIONES_SERVICE_URL", "http://afiliaciones-service:8000")
    TRACKING_SERVICE_URL = os.getenv(
        "TRACKING_SERVICE_URL", "http://tracking-service:8000")
    PULSAR_URL = os.getenv("PULSAR_URL", "pulsar://pulsar:6650")


settings = Config()
