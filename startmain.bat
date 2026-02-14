@echo off
::cd  Backend/FastAPI
echo Iniciando FastAPI...
echo.
echo Servidor: http://127.0.0.1:8000
echo Documentacion: http://127.0.0.1:8000/docs
echo Documentacion: http://127.0.0.1:8000/redoc
echo.
:: Activar entorno y ejecutar uvicorn en la misma sesión
cmd /k "venv\Scripts\activate.bat && echo Entorno activado. && uvicorn main:app --reload"