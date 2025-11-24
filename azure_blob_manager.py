"""
Módulo para operações com Azure Blob Storage
"""
from azure.storage.blob import BlobServiceClient, BlobClient
from datetime import datetime
from config import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME

class AzureBlobManager:
    def __init__(self, container_name=None):
        """
        Inicializa conexão com Azure Blob Storage
        
        Args:
            container_name (str): Nome do contêiner
        """
        self.container_name = container_name or AZURE_CONTAINER_NAME
        self.connection_string = AZURE_CONNECTION_STRING
        self.blob_service_client = None
        self.authenticate()
    
    def authenticate(self):
        """Autentica com Azure Blob Storage"""
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            print("✅ Autenticação Azure Blob Storage bem-sucedida!")
            
            # Testa conexão listando contêineres
            containers = list(self.blob_service_client.list_containers())
            print(f"   Total de contêineres: {len(containers)}")
            
        except Exception as e:
            print(f"❌ Erro ao autenticar com Azure Blob Storage: {e}")
            raise
    
    def list_blobs(self, container_name=None):
        """
        Lista todos os blobs (arquivos) em um contêiner
        
        Args:
            container_name (str): Nome do contêiner
                                Se None, usa o padrão configurado
        
        Returns:
            list: Lista de blobs no contêiner
        """
        if container_name is None:
            container_name = self.container_name
        
        try:
            container_client = self.blob_service_client.get_container_client(
                container_name
            )
            
            blobs = list(container_client.list_blobs())
            
            print(f"\n☁️  Listando blobs do Azure Blob Storage...")
            print(f"   Contêiner: {container_name}\n")
            
            if not blobs:
                print("   Nenhum blob encontrado no contêiner!")
            else:
                print(f"   📊 Total de blobs: {len(blobs)}\n")
                for idx, blob in enumerate(blobs, 1):
                    size_mb = round(blob.size / (1024 * 1024), 2)
                    print(f"   {idx}. {blob.name}")
                    print(f"      Tamanho: {size_mb} MB")
                    print(f"      Última modificação: {blob.last_modified}\n")
            
            return blobs
            
        except Exception as e:
            print(f"❌ Erro ao listar blobs: {e}")
            return []
    
    def upload_blob(self, file_name, file_content, overwrite=False):
        """
        Faz upload de um arquivo para o Azure Blob Storage
        
        Args:
            file_name (str): Nome do blob (arquivo)
            file_content (bytes): Conteúdo do arquivo em bytes
            overwrite (bool): Se True, sobrescreve se já existir
        
        Returns:
            dict: Informações do blob enviado ou None se falhar
        """
        try:
            container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            
            # Fazer upload
            blob_client = container_client.get_blob_client(file_name)
            blob_client.upload_blob(file_content, overwrite=overwrite)
            
            # Obter informações do blob
            properties = blob_client.get_blob_properties()
            
            result = {
                'name': file_name,
                'size': properties.size,
                'size_mb': round(properties.size / (1024 * 1024), 2),
                'last_modified': properties.last_modified,
                'status': 'success'
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Erro ao fazer upload do blob {file_name}: {e}")
            return {
                'name': file_name,
                'status': 'error',
                'error': str(e)
            }
    
    def download_blob(self, file_name):
        """
        Faz download de um blob do Azure Blob Storage
        
        Args:
            file_name (str): Nome do blob
        
        Returns:
            bytes: Conteúdo do arquivo, ou None se falhar
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=file_name
            )
            
            download_stream = blob_client.download_blob()
            return download_stream.readall()
            
        except Exception as e:
            print(f"❌ Erro ao fazer download do blob {file_name}: {e}")
            return None
    
    def delete_blob(self, file_name):
        """
        Deleta um blob do Azure Blob Storage
        
        Args:
            file_name (str): Nome do blob
        
        Returns:
            bool: True se bem-sucedido
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=file_name
            )
            
            blob_client.delete_blob()
            print(f"✅ Blob '{file_name}' deletado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao deletar blob {file_name}: {e}")
            return False
    
    def create_container_if_not_exists(self, container_name=None):
        """
        Cria um contêiner se não existir
        
        Args:
            container_name (str): Nome do contêiner
        
        Returns:
            bool: True se bem-sucedido
        """
        if container_name is None:
            container_name = self.container_name
        
        try:
            container_client = self.blob_service_client.create_container(
                name=container_name
            )
            print(f"✅ Contêiner '{container_name}' criado com sucesso")
            return True
            
        except Exception as e:
            if "ContainerAlreadyExists" in str(e):
                print(f"ℹ️  Contêiner '{container_name}' já existe")
                return True
            else:
                print(f"❌ Erro ao criar contêiner: {e}")
                return False
