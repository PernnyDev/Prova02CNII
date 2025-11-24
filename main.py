"""
Aplicação Principal - Transferência de Arquivos do Google Drive para Azure Blob Storage
"""
import sys
from datetime import datetime
from google_drive_manager import GoogleDriveManager
from azure_blob_manager import AzureBlobManager
from config import validate_config, GOOGLE_DRIVE_FOLDER_ID, AZURE_CONTAINER_NAME

def print_header(title):
    """Exibe um cabeçalho formatado"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_status(message, status_type="info"):
    """Exibe mensagem com formatação de status"""
    icons = {
        "info": "ℹ️ ",
        "success": "✅ ",
        "error": "❌ ",
        "warning": "⚠️  ",
        "progress": "⏳ "
    }
    icon = icons.get(status_type, "ℹ️ ")
    print(f"{icon} {message}")

def list_google_drive_files(gdrive_manager):
    """Lista arquivos do Google Drive"""
    print_header("LISTAR ARQUIVOS DO GOOGLE DRIVE")
    files = gdrive_manager.list_files_in_folder()
    return files

def list_azure_blobs(azure_manager):
    """Lista blobs do Azure Blob Storage"""
    print_header("LISTAR BLOBS DO AZURE BLOB STORAGE")
    blobs = azure_manager.list_blobs()
    return blobs

def transfer_files(gdrive_manager, azure_manager, files_to_transfer=None):
    """
    Transfere arquivos do Google Drive para Azure Blob Storage
    
    Args:
        gdrive_manager: Gerenciador do Google Drive
        azure_manager: Gerenciador do Azure Blob Storage
        files_to_transfer: Lista de IDs de arquivos ou None (para transferir todos)
    """
    print_header("INICIANDO TRANSFERÊNCIA DE ARQUIVOS")
    
    # Obter lista de arquivos
    all_files = gdrive_manager.list_files_in_folder()
    
    if not all_files:
        print_status("Nenhum arquivo para transferir", "warning")
        return None
    
    # Filtrar apenas ARQUIVOS (não pastas/folders)
    # Pastas têm tipo 'application/vnd.google-apps.folder'
    all_files = [f for f in all_files if f.get('mimetype', '').lower() != 'application/vnd.google-apps.folder']
    
    if not all_files:
        print_status("Nenhum arquivo encontrado (apenas pastas no Google Drive)", "warning")
        return None
    
    # Filtrar arquivos se especificado
    if files_to_transfer:
        files = [f for f in all_files if f['id'] in files_to_transfer]
    else:
        files = all_files
    
    if not files:
        print_status("Nenhum arquivo encontrado para transferência", "warning")
        return None
    
    # Estatísticas
    total_files = len(files)
    print_status(f"Total de arquivos para transferir: {total_files}", "progress")
    print()
    
    # Resultados
    transfer_results = {
        'success': [],
        'failed': [],
        'total': total_files,
        'timestamp': datetime.now().isoformat()
    }
    
    # Transferir cada arquivo
    for idx, file in enumerate(files, 1):
        file_id = file['id']
        file_name = file['name']
        file_size_mb = round(int(file.get('size', 0)) / (1024 * 1024), 2)
        
        print(f"[{idx}/{total_files}] Transferindo: {file_name}")
        print(f"          Tamanho: {file_size_mb} MB")
        
        # Baixar do Google Drive
        print(f"          ⬇️  Baixando do Google Drive...", end=" ")
        file_content = gdrive_manager.download_file(file_id, file_name)
        
        if file_content is None:
            print("❌ Falha!")
            transfer_results['failed'].append({
                'name': file_name,
                'error': 'Falha ao baixar do Google Drive'
            })
            continue
        
        print("✅ OK")
        
        # Enviar para Azure Blob Storage
        print(f"          ⬆️  Enviando para Azure...", end=" ")
        upload_result = azure_manager.upload_blob(file_name, file_content, overwrite=True)
        
        if upload_result['status'] == 'success':
            print("✅ OK")
            transfer_results['success'].append({
                'name': file_name,
                'size_mb': upload_result['size_mb']
            })
        else:
            print("❌ Falha!")
            transfer_results['failed'].append({
                'name': file_name,
                'error': upload_result.get('error', 'Erro desconhecido')
            })
        
        print()
    
    return transfer_results

def print_transfer_report(results):
    """Exibe relatório de transferência"""
    if results is None:
        return
    
    print_header("RELATÓRIO DE TRANSFERÊNCIA")
    
    success_count = len(results['success'])
    failed_count = len(results['failed'])
    total_count = results['total']
    
    print(f"Timestamp: {results['timestamp']}\n")
    
    # Resumo
    print("📊 RESUMO:")
    print(f"   Total de arquivos: {total_count}")
    print(f"   ✅ Sucesso: {success_count}")
    print(f"   ❌ Falhas: {failed_count}")
    print(f"   Taxa de sucesso: {round((success_count/total_count)*100, 1)}%\n")
    
    # Arquivos bem-sucedidos
    if results['success']:
        print("✅ ARQUIVOS TRANSFERIDOS COM SUCESSO:")
        total_size = 0
        for file in results['success']:
            print(f"   • {file['name']} ({file['size_mb']} MB)")
            total_size += file['size_mb']
        print(f"   Total transferido: {round(total_size, 2)} MB\n")
    
    # Arquivos com falha
    if results['failed']:
        print("❌ ARQUIVOS COM FALHA:")
        for file in results['failed']:
            print(f"   • {file['name']}")
            print(f"     Erro: {file['error']}\n")

def interactive_menu():
    """Menu interativo da aplicação"""
    print_header("TRANSFERÊNCIA GOOGLE DRIVE → AZURE BLOB STORAGE")
    
    # Validar configurações
    if not validate_config():
        sys.exit(1)
    
    # Inicializar gerenciadores
    print("\n⏳ Inicializando conexões...")
    try:
        gdrive_manager = GoogleDriveManager()
        azure_manager = AzureBlobManager()
        
        # Criar contêiner se não existir
        print("\n⏳ Verificando contêiner do Azure...")
        azure_manager.create_container_if_not_exists()
        
    except Exception as e:
        print_status(f"Erro ao inicializar: {e}", "error")
        sys.exit(1)
    
    print("\n" + "="*70 + "\n")
    
    while True:
        print("OPÇÕES:")
        print("  1. Listar arquivos do Google Drive")
        print("  2. Listar blobs do Azure Blob Storage")
        print("  3. Transferir TODOS os arquivos")
        print("  4. Sair\n")
        
        choice = input("Selecione uma opção (1-4): ").strip()
        
        if choice == '1':
            list_google_drive_files(gdrive_manager)
        
        elif choice == '2':
            list_azure_blobs(azure_manager)
        
        elif choice == '3':
            results = transfer_files(gdrive_manager, azure_manager)
            print_transfer_report(results)
        
        elif choice == '4':
            print_status("Encerrando aplicação", "info")
            break
        
        else:
            print_status("Opção inválida", "error")

def main():
    """Função principal"""
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\n⚠️  Aplicação interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro não tratado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
