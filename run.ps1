# Script para executar a aplicação
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
& .\venv\Scripts\Activate.ps1
python main.py
