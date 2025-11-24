"""
Módulo para operações com Google Drive
"""
import io
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_DRIVE_FOLDER_ID

# Escopo necessário para acessar Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveManager:
    def __init__(self):
        """Inicializa conexão com Google Drive"""
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Autentica com Google Drive usando Service Account"""
        try:
            credentials = Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS_FILE, 
                scopes=SCOPES
            )
            self.service = build('drive', 'v3', credentials=credentials)
            print("✅ Autenticação Google Drive bem-sucedida!")
        except Exception as e:
            print(f"❌ Erro ao autenticar com Google Drive: {e}")
            raise
    
    def list_files_in_folder(self, folder_id=None):
        """
        Lista todos os arquivos em uma pasta específica do Google Drive
        
        Args:
            folder_id (str): ID da pasta no Google Drive
                           Se None, usa o ID configurado
        
        Returns:
            list: Lista de dicionários com info dos arquivos
        """
        if folder_id is None:
            folder_id = GOOGLE_DRIVE_FOLDER_ID
        
        if not folder_id:
            print("❌ Nenhum ID de pasta foi fornecido!")
            return []
        
        try:
            files = []
            query = f"'{folder_id}' in parents and trashed=false"
            
            print(f"\n📂 Listando arquivos da pasta Google Drive...")
            print(f"   ID da Pasta: {folder_id}\n")
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, mimeType, size, createdTime, modifiedTime)',
                pageSize=100
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                print("   Nenhum arquivo encontrado na pasta!")
            else:
                print(f"   📊 Total de arquivos: {len(files)}\n")
                for idx, file in enumerate(files, 1):
                    size_mb = round(int(file.get('size', 0)) / (1024 * 1024), 2)
                    print(f"   {idx}. {file['name']}")
                    print(f"      ID: {file['id']}")
                    print(f"      Tamanho: {size_mb} MB")
                    print(f"      Tipo: {file['mimeType']}")
                    print(f"      Criado: {file.get('createdTime', 'N/A')}\n")
            
            return files
            
        except Exception as e:
            print(f"❌ Erro ao listar arquivos: {e}")
            return []
    
    def download_file(self, file_id, file_name):
        """
        Baixa um arquivo do Google Drive
        
        Args:
            file_id (str): ID do arquivo no Google Drive
            file_name (str): Nome do arquivo para exibição
        
        Returns:
            bytes: Conteúdo do arquivo em bytes
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file.seek(0)
            return file.getvalue()
            
        except Exception as e:
            print(f"❌ Erro ao baixar arquivo {file_name}: {e}")
            return None
    
    def create_folder(self, folder_name, parent_id=None):
        """
        Cria uma nova pasta no Google Drive
        
        Args:
            folder_name (str): Nome da pasta a criar
            parent_id (str): ID da pasta pai (opcional)
        
        Returns:
            str: ID da pasta criada, ou None se falhar
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            file = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            folder_id = file.get('id')
            print(f"✅ Pasta '{folder_name}' criada com sucesso!")
            print(f"   ID: {folder_id}")
            return folder_id
            
        except Exception as e:
            print(f"❌ Erro ao criar pasta: {e}")
            return None
    
    def share_folder(self, folder_id, email):
        """
        Compartilha uma pasta com um email específico
        
        Args:
            folder_id (str): ID da pasta
            email (str): Email para compartilhar
        
        Returns:
            bool: True se bem-sucedido
        """
        try:
            permission = {
                'type': 'user',
                'role': 'editor',
                'emailAddress': email
            }
            
            self.service.permissions().create(
                fileId=folder_id,
                body=permission,
                fields='id'
            ).execute()
            
            print(f"✅ Pasta compartilhada com {email}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao compartilhar pasta: {e}")
            return False
