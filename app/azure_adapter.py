import azure.functions as func
from fastapi import FastAPI
from app.main import app as fastapi_app
from mangum import Mangum


handler = Mangum(fastapi_app)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return handler(req, context)