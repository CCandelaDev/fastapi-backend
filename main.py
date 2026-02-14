from fastapi import FastAPI, staticfiles
from routers import products, users, customers, jwt_auth_users, users_db

app = FastAPI(
    title="My API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "🏠 Inicio",
            "description": "Endpoints principales de la API",
        }
    ],
    description="API para gestión de usuarios y productos",
)
# venv+uvicorn --> cd  BAckend/FastAPI  ---> startmain.bat
# Connect to DB local: E:\MongoDB\v8.2.4\bin\mongod.exe --config "E:\MongoDB\v8.2.4\mongod.cfg"
# uvicorn main:app --reload
# URL: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
# Docs2: http://127.0.0.1:8000/redoc
# mongodb+srv://test:test@cluster0.wivvqyh.mongodb.net/


# Routers

app.include_router(users.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
# Para cargar archivos estáticos
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")


@app.get("/", tags=["🏠 Inicio", "📋 Información"])
async def root():
    return {"message": "HelloWorld"}


@app.get("/url", tags=["✔ URL de referencia"])
async def url():
    return {"url": "https://www.grupotecnitenis.com"}
