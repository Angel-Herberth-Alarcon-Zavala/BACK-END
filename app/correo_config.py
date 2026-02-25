from fastapi_mail import ConnectionConfig
import os
from dotenv import load_dotenv

# Esto carga las variables del archivo .env a la memoria del sistema
load_dotenv()

conf = ConnectionConfig(
    # REEMPLAZAMOS LOS TEXTOS POR os.getenv
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)