@echo off
REM Script para setup automático do projeto
REM Execute este arquivo: setup.bat

cd /d "%~dp0"

echo.
echo ============================================================
echo   SETUP AUTOMATICO - Transferencia Google Drive para Azure
echo ============================================================
echo.

REM 1. Criar venv se nao existir
echo 1. Criando ambiente virtual...
if not exist venv (
    python -m venv venv
    echo   OK - venv criado
) else (
    echo   OK - venv ja existe
)

REM 2. Ativar venv
echo.
echo 2. Ativando venv...
call venv\Scripts\activate.bat
echo   OK - venv ativado

REM 3. Instalar dependencias
echo.
echo 3. Instalando dependencias...
pip install -r requirements.txt
echo   OK - dependencias instaladas

REM 4. Testar conexoes
echo.
echo 4. Testando conexoes...
python teste_conexoes.py

REM 5. Sucesso
echo.
echo ============================================================
echo   SETUP CONCLUIDO COM SUCESSO!
echo ============================================================
echo.
echo Para usar a aplicacao, execute:
echo   python main.py
echo.
pause
