from fastapi import HTTPException, Depends, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

# uvicorn jwt_auth_users:app --reload
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
# openssl rand -hex 32 (para generar la clace de encriptación)
SECRET_KEY = "0895e3cea9a59f8ea182e9b862734f35ba6f926cf3fcead04fc097f81ead7390"

router = APIRouter(tags=["jwt Authentication"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Encriptamos la contraseña con passlib (contexto de encriptación)
cript = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


# Heredamos de la clase User y le incluimos la propiedad password
class UserDB(User):
    password: str


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "XOx6M@example.com",
        "disabled": False,
        "password": cript.hash("123456"),  # Hashear la contraseña
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "XOx6M@example.com",
        "disabled": False,
        "password": cript.hash("1234567"),
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Wonderson",
        "email": "XOx6M@example.com",
        "disabled": True,
        "password": cript.hash("12345678"[:72]),
    },
}


# Creamos una función para buscar el usuario pero sin la contraseña (devuelve un User)
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# Creamos una función para buscar el usuario en la base de datos(devuelve un UserDB)
def search_user_db(username: str):
    if username in users_db:
        return UserDB(
            **users_db[username]
        )  # Con ** indicamos que pueden ir muchos argumentos


# Creamos nuevo critero de depencia para encontrar el usuario autenticado (devuelve usuario)
# La dependencia es la de nuestro sistema de autenticación (token)
async def auth_user(token: str = Depends(oauth2)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificamos el token (nombre del usuario)
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get(
            "sub"
        )  # Datos del token
        if username is None:
            raise credentials_exception
        # Si no da error buscamos el usuario en la base de datos(sin la contraseña)
        user = search_user(username)

    except InvalidTokenError:
        raise credentials_exception

    return user  # Devolvemos el usuario autenticado


# Criterio de dependencia para la autenticación (Busca el usuario y lo devuelve)
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo"
        )

    return user


# Creamos una ruta para el login===============================================
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_data_db = users_db.get(form.username)
    # Comprobamos que el usuario exista
    if not user_data_db:
        raise HTTPException(status_code=400, detail="User not found")

    # Si existe el usuario, verificamos la contraseña hasheada
    user = search_user_db(form.username)

    if not cript.verify(form.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Con timedelta creamos el tiempo de expiración (1 minuto mas tarde)
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(tz=timezone.utc) + access_token_expiration

    access_token = {
        "sub": user.username,
        "exp": expire,
    }

    # Creamos el token de autenticación (será el nombre del usuario)
    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


# Ruta para acceder a mis datos
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
