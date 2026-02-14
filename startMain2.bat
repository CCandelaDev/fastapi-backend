@echo off
cls
echo FASTAPI DEVELOPMENT SERVER
echo ============================
echo.

if not exist "main.py" (
    echo Error: main.py no encontrado
    pause
    exit
)

if not exist "venv\Scripts\activate.bat" (
    echo Error: Entorno virtual no encontrado
    pause
    exit
)

call venv\Scripts\activate.bat
echo Servidor iniciando...
echo.
echo URL: http://127.0.0.1:8000
echo Docs: http://127.0.0.1:8000/docs
echo.
echo Ctrl+C para detener
echo ============================
echo.

uvicorn main:users --reload

echo.
echo Servidor detenido.
pause