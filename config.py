"""
Configuração centralizada da aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Drive
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '')
GOOGLE_CREDENTIALS_FILE = 'credentials.json'

# Azure Blob Storage
AZURE_CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING', '')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME', 'Aluno_ViniciusRibeiro')

# Validar configurações
def validate_config():
    """Valida se todas as configurações estão presentes"""
    errors = []
    
    if not GOOGLE_DRIVE_FOLDER_ID:
        errors.append("❌ GOOGLE_DRIVE_FOLDER_ID não configurado no .env")
    
    if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
        errors.append(f"❌ {GOOGLE_CREDENTIALS_FILE} não encontrado")
    
    if not AZURE_CONNECTION_STRING:
        errors.append("❌ AZURE_CONNECTION_STRING não configurado no .env")
    
    if not AZURE_CONTAINER_NAME:
        errors.append("❌ AZURE_CONTAINER_NAME não configurado no .env")
    
    if errors:
        print("\n⚠️  ERROS DE CONFIGURAÇÃO:\n")
        for error in errors:
            print(f"  {error}")
        print("\n📋 Veja o arquivo SETUP_GOOGLE_DRIVE.md para instruções\n")
        return False
    
    return True
