@echo off
REM Script para iniciar a aplicação web
REM Execute este arquivo: start_web.bat

cd /d "%~dp0"

echo.
echo ============================================================
echo   INICIANDO INTERFACE WEB
echo   Transferencia Google Drive → Azure Blob Storage
echo ============================================================
echo.

REM Ativar venv
call venv\Scripts\activate.bat

REM Iniciar servidor
echo.
echo ✅ Servidor iniciando...
echo.
echo 🌐 Acesse em: http://localhost:5000
echo.
echo (Pressione CTRL+C para parar o servidor)
echo.

python app.py

pause
