from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        400: {"description": "Datos de entrada inválidos"},
        401: {"description": "No autorizado - Token inválido o expirado"},
        403: {"description": "Prohibido - Permisos insuficientes"},
        404: {"description": "Usuario no encontrado"},
        500: {"description": "Error interno del servidor - Contacte al administrador"},
    },
)

# uvicorn users:app --reload
# Entidad users


# Base model hace las funciones del constructor
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


# Crea una entidad
users_list = [
    User(
        id=1,
        name="Cayetano",
        surname="Candela",
        url="https://www.grupotecnitenis.com",
        age=20,
    ),
    User(
        id=2,
        name="CCandelaDev",
        surname="Developer",
        url="https://www.grupotecnitenis.com",
        age=20,
    ),
    User(
        id=3,
        name="Emilio",
        surname="Soler",
        url="https://www.grupotecnitenis.com",
        age=20,
    ),
]


# Ejemplo de como seria sin crear la  entidad
@router.get("/usersjson")
async def usersjson():
    return [
        {
            "name": "Cayetano",
            "surname": "Candela",
            "age": 20,
            "url": "https://www.grupotecnitenis.com",
        },
        {
            "name": "CCandelaDev",
            "surname": "Developer",
            "age": 30,
            "url": "https://www.grupotecnitenis.com",
        },
        {
            "name": "Emilio",
            "surname": "Soler",
            "age": 40,
            "url": "https://www.grupotecnitenis.com",
        },
    ]


# Funcion para retornar todos los users
@router.get("/list")
async def get_all_users():
    return users_list


# LLamar por Path Ej:http://127.0.0.1:8000/user/1
@router.get("/{id}", status_code=201)
async def user(id: int):
    return search_user(id)


# LLamar por Query Ej:http://127.0.0.1:8000/user/?id=1
@router.get("/", status_code=201)
async def user(id: int):
    return search_user(id)


# Creacion de un POST
@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return {"status": "ok", "detail": "Usuario creado"}


# Funcion para modificar usuario---> PUT
@router.put("/", status_code=201)
async def user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return {"status": "ok", "detail": "Usuario actualizado", "user: ": user}

    raise HTTPException(status_code=404, detail="Usuario no actualizado")


# Función para borrar el ususario---> por PATH
@router.delete("/{user_id}", status_code=201)
async def user(user_id: int):
    for index, delete_user in enumerate(users_list):
        if delete_user.id == user_id:
            # Guardo el usuario antes de borrarlo(Tambien lo prodria hacer con pop)
            userDeleted = users_list[index]
            # Borro el usuario
            del users_list[index]
            return {
                "message": f"Usuario {userDeleted.name} eliminado",
                "deleted_user": userDeleted,
                "remaining:": users_list,
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# Fuction reutilizable para llamar por Query/Path
def search_user(id: int):
    users = filter(
        lambda user: user.id == id, users_list
    )  # filter(función, lista a filtrar)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": "No se ha encontrado usuario"}


# ---------------------------------------------------

# "PATH para lo único, QUERY para lo múltiple"

# Path: Un usuario específico

# Query: Muchos usuarios filtrados

# "PATH para lo obligatorio, QUERY para lo opcional"

# "PATH identifica, QUERY modifica"
