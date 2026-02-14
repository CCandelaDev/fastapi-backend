# id: str | None
# username: str
# email: str

"""
Transforma un documento MongoDB en un diccionario Python
con el formato requerido por nuestra API.

MongoDB devuelve: {"_id": ObjectId(...), "username": "...", "email": "..."}
Nosotros queremos: {"id": "string", "username": "...", "email": "..."}

Args:
    user (dict): Documento MongoDB con campos _id, username, email

Returns:
    dict: Diccionario con id (string), username, email
"""


def user_schema(user) -> dict:

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
    }


# --------------------------------------------------------------------------------
"""
    Transforma una lista (o cursor) de documentos MongoDB 
    en una lista de diccionarios con formato API.
    
    Aplica user_schema() a cada documento de la lista.
    
    Args:
        users (list/cursor): Lista de documentos MongoDB
        
    Returns:
        list: Lista de diccionarios transformados
    """


# Funcion que recibe una lista de usuarios y los transforma en una lista de diccionarios
def users_schema(users) -> list:
    return [user_schema(user) for user in users]
