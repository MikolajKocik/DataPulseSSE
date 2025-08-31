import azure.functions as func
from fastapi import FastAPI # important due to use with mangum from app
from app.main import app as fastapi_app # main application
from mangum import Mangum

# Azure func sdk python dont run http trigger ASGI as native
# so mangum is a adapter to translate http requests from azure to ASGI fast api

handler = Mangum(fastapi_app) # bridge for fast api

# example how to integrate az func with sse server
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return handler(req, context)

# main is just a name