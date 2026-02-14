from pymongo import MongoClient
import os

### MongoDB client ###

# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost

# Instancia de mongodb en localhost
# db_client = MongoClient().local

# Base de datos remota
MONGO_URI = os.getenv("MONGO_URI")

db_client = MongoClient("MONGO_URI").test


# Base de datos remota MongoDB Atlas (https://mongodb.com)
# db_client = MongoClient(
#     "mongodb+srv://<user>:<password>@<url>/?retryWrites=true&w=majority").test

# Despliegue API en la nube:
# Deta (deprecado) - https://www.deta.sh/
# Vercel - https://www.vercel.com
# Instrucciones - https://cleverzone.medium.com/fastapi-deployment-into-vercel-0fa4e6478014
# MUY IMPORTANTE - Al desplegar en producción, preparar el proyecto para trabajar con variables de entorno que hagan referencia a datos sensibles:
# - Nunca subas a un repositorio público el valor de las variables
# - Puedes usar dotenv en Python
# - Añade el valor de las variables desde el proveedor de hosting
