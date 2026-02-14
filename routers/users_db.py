from fastapi import APIRouter, HTTPException, status
from db.models.user_model import User  # Import de la entidad
from db.client import db_client  # Import de la base de datos
from db.schemas.user import (  # Import del schema para transformar el usuario
    user_schema,
    users_schema,
)
from bson import ObjectId  # Para inportar ObjectId de la base de datos

router = APIRouter(
    prefix="/usersdb",
    tags=["usersdb MongoDB"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "No encontrado"},
        status.HTTP_403_FORBIDDEN: {"description": "Prohibido"},
        status.HTTP_401_UNAUTHORIZED: {"description": "No autorizado"},
    },
)

# uvicorn users:app --reload
# Entidad users


# Funcion para retornar todos los users
@router.get("/list", response_model=list[User])
async def get_all_users_db():
    return users_schema(db_client.users.find())


# LLamar por Path Ej:http://127.0.0.1:8000/user/1
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# LLamar por Query Ej:http://127.0.0.1:8000/user/?id=1
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Creacion de un POST
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    existing_user = search_user("email", user.email)
    if existing_user is not None:
        # Si search_user_by_username() devuelve un objeto de tipo User (no None)
        # significa que el usuario ya existe
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists"
        )

    # Crear un esquema local de la base de datos e insertar el usuario
    # (transformar en JSON(como dict)--->user.model_dump)
    user_dict = user.model_dump()
    del user_dict["id"]  # El id lo genera mongo al insertar

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(
        db_client.users.find_one({"_id": id})
    )  # Transformar el usuario en un diccionario con user_schema(buscar el usuario por id)

    return User(
        **new_user
    )  # ** Se usa para devolver todo los campos de la entidad User


# Funcion para modificar usuario---> PUT
# model_dump() convierte un objeto Pydantic (User) en un diccionario Python.
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = user.model_dump()
    del user_dict["id"]  # El id lo genera mongo al insertar --> evita id duplicado

    try:
        # Buscar el usuario por _id y actualizarlo
        result = db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict, return_document=True
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error updating user")

    if result is None:  # Si no encuentra el usuario
        raise HTTPException(status_code=404, detail="User not found")

    return search_user("_id", ObjectId(user.id))  # Devuelve el usuario actualizado


# Función para borrar el ususario---> por PATH
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(user_id: str):
    # Buscar usuario por id y eliminarlo
    found = db_client.users.find_one_and_delete({"_id": ObjectId(user_id)})

    if not found:  # Si no encuentra nada para borrar con ese id
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"status": "ok", "detail": "User deleted"}


# Fuction generica para buscar con criterio busqueda por campo / clave de la base de datos
# Hago el key generico porque le puede llegar tambien un ObjectId( de MongoDB)
def search_user(field: str, key):
    user = db_client.users.find_one({field: key})

    if user is None:
        return None  # Devolvemos None si no encuentra usuario con esa clave

    try:

        return User(**user_schema(user))
    except Exception:
        return None  # Devolvemos None en caso de error


# ---------------------------------------------------

# "PATH para lo único, QUERY para lo múltiple"

# Path: Un usuario específico

# Query: Muchos usuarios filtrados

# "PATH para lo obligatorio, QUERY para lo opcional"

# "PATH identifica, QUERY modifica"
