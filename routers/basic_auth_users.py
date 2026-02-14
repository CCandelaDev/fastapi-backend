from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashlib

app = FastAPI()

# Creamos una instancia de la clase OAuth2PasswordBearer para la autenticación
# La función tokenUrl indica la ruta para el login y la llamamos login
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


# Heredamos de la clase User y le incluimos la propiedad password
class UserDB(User):
    password: str


def hash_password(password: str):
    """Convierte contraseña a hash SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "XOx6M@example.com",
        "disabled": False,
        "password": hash_password("123456"),  # Encriptamos la contraseña
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "XOx6M@example.com",
        "disabled": False,
        "password": hash_password("1234567"),  # Encriptamos la contraseña
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Wonderson",
        "email": "XOx6M@example.com",
        "disabled": True,
        "password": hash_password("12345678"),  # Encriptamos la contraseña
    },
}


# Creamos una función para buscar el usuario en la base de datos(devuelve un UserDB)
def search_user_db(username: str):
    if username in users_db:
        return UserDB(
            **users_db[username]
        )  # Con ** indicamos que pueden ir muchos argumentos


# Creamos una función para buscar el usuario pero sin la contraseña (devuelve un User)
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# Criterio de dependencia para la autenticación
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},  # Tipo de autenticación
        )
    if user.disabled:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    return user


# Creamos una ruta para el login===============================================
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_data_db = users_db.get(form.username)
    # Comprobamos que el usuario exista
    if not user_data_db:
        raise HTTPException(status_code=400, detail="User not founddddd")

    # Si existe el usuario, verificamos la contraseña hasheada
    user = search_user_db(form.username)
    if not hash_password(form.password) == user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Creamos el token de autenticación (será el nombre del usuario)
    return {"access_token": user.username, "token_type": "bearer"}


# Creamos una ruta para la información del usuario==============================
# criterio de dependencia para la autenticación, función current_user
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
