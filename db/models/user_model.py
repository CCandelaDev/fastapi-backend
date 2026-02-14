from pydantic import BaseModel


# Creamos una entidad
# Base model hace las funciones del constructor
class User(BaseModel):
    id: str | None = None  # None: es opcional (puede que no le llegue el id)
    username: str
    email: str


""" id: str | None = None
# FastAPI piensa: "El usuario NO necesita enviar este campo,
# si no lo envía, usaré None por defecto" """
