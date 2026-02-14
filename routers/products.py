from fastapi import APIRouter

# Prefix para que sea suficiente con "/"men los endpoints
# tag, para agrupar "products" en la documentación
# response, para documentar errores conmunes con respuestas especificas
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        400: {"description": "Datos de entrada inválidos"},
        401: {"description": "No autorizado - Token inválido o expirado"},
        403: {"description": "Prohibido - Permisos insuficientes"},
        404: {"description": "Usuario no encontrado"},
        500: {"description": "Error interno del servidor - Contacte al administrador"},
    },
)

products_list = [
    "Product 1",
    "Product 2",
    "Product 3",
    "Product 4",
    "Product 5",
]


# Funcion para retornar todos productos path/query
@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products():
    return products_list[id]
