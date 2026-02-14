from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/customers", tags=["Customers"])


class Customers(BaseModel):
    id: int
    name: str
    surname: str
    code: str


customers_list = [
    Customers(id=1, name="Luis", surname="Lopez", code="001"),
    Customers(id=1, name="Pedro", surname="Ruiz", code="002"),
    Customers(id=1, name="Juan", surname="Fenoll", code="003"),
]


@router.get("/")
async def custommers():
    return customers_list
