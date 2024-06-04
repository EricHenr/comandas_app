from dotenv import load_dotenv, find_dotenv
import os
from flask import session

# Locate the .env file
dotenv_file = find_dotenv()

# Load the .env file
load_dotenv(dotenv_file)

# APP settings
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEBUG = os.getenv("DEBUG")

# API settings
URL_API = os.getenv("URL_API")

# Endpoint configuration
ENDPOINT_TOKEN = os.getenv("ENDPOINT_TOKEN")
ENDPOINT_FUNCIONARIO = os.getenv("ENDPOINT_FUNCIONARIO")
ENDPOINT_CLIENTE = os.getenv("ENDPOINT_CLIENTE")
ENDPOINT_PRODUTO = os.getenv("ENDPOINT_PRODUTO")

# Security settings
def getHeadersAPI():
    return {
        'accept': 'application/json',
        'Authorization': f'Bearer {session["access_token"] if "access_token" in session else ""}'
    }
# Variável para o tempo de sessão - minutos
TEMPO_SESSION = os.getenv("TEMPO_SESSION")