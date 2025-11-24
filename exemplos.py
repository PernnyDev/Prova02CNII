"""
Exemplos de Uso - Como usar a aplicação programaticamente
"""

from google_drive_manager import GoogleDriveManager
from azure_blob_manager import AzureBlobManager
from config import GOOGLE_DRIVE_FOLDER_ID, AZURE_CONTAINER_NAME

def exemplo_1_listar_google_drive():
    """Exemplo 1: Listar arquivos do Google Drive"""
    print("=" * 70)
    print("EXEMPLO 1: Listar Arquivos do Google Drive")
    print("=" * 70 + "\n")
    
    # Criar gerenciador
    gdrive = GoogleDriveManager()
    
    # Listar arquivos
    files = gdrive.list_files_in_folder()
    
    print(f"\nTotal de arquivos: {len(files)}\n")
    
    # Processar cada arquivo
    for file in files:
        print(f"Nome: {file['name']}")
        print(f"ID: {file['id']}")
        print(f"Tamanho: {int(file.get('size', 0)) / (1024 * 1024):.2f} MB")
        print()

def exemplo_2_listar_azure():
    """Exemplo 2: Listar blobs do Azure"""
    print("=" * 70)
    print("EXEMPLO 2: Listar Blobs do Azure Blob Storage")
    print("=" * 70 + "\n")
    
    # Criar gerenciador
    azure = AzureBlobManager()
    
    # Listar blobs
    blobs = azure.list_blobs()
    
    print(f"\nTotal de blobs: {len(blobs)}\n")
    
    # Processar cada blob
    for blob in blobs:
        print(f"Nome: {blob.name}")
        print(f"Tamanho: {blob.size / (1024 * 1024):.2f} MB")
        print(f"Modificado: {blob.last_modified}")
        print()

def exemplo_3_transferir_um_arquivo():
    """Exemplo 3: Transferir um arquivo específico"""
    print("=" * 70)
    print("EXEMPLO 3: Transferir Um Arquivo Específico")
    print("=" * 70 + "\n")
    
    # Criar gerenciadores
    gdrive = GoogleDriveManager()
    azure = AzureBlobManager()
    
    # Listar arquivos do Google Drive
    print("Arquivos disponíveis:\n")
    files = gdrive.list_files_in_folder()
    
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file['name']} (ID: {file['id'][:20]}...)")
    
    # Pegar o primeiro arquivo como exemplo
    if files:
        file_to_transfer = files[0]
        file_id = file_to_transfer['id']
        file_name = file_to_transfer['name']
        
        print(f"\n\nTransferindo: {file_name}")
        print("-" * 70)
        
        # Baixar do Google Drive
        print("⬇️  Baixando do Google Drive...", end=" ", flush=True)
        file_content = gdrive.download_file(file_id, file_name)
        
        if file_content:
            print("✅ OK")
            
            # Fazer upload para Azure
            print("⬆️  Fazendo upload para Azure...", end=" ", flush=True)
            result = azure.upload_blob(file_name, file_content, overwrite=True)
            
            if result['status'] == 'success':
                print("✅ OK")
                print(f"\n✅ Arquivo transferido com sucesso!")
                print(f"   Tamanho: {result['size_mb']} MB")
            else:
                print("❌ Falha!")
                print(f"   Erro: {result.get('error')}")
        else:
            print("❌ Falha!")

def exemplo_4_transferir_com_filtro():
    """Exemplo 4: Transferir apenas arquivos PDF"""
    print("=" * 70)
    print("EXEMPLO 4: Transferir Apenas PDFs")
    print("=" * 70 + "\n")
    
    # Criar gerenciadores
    gdrive = GoogleDriveManager()
    azure = AzureBlobManager()
    
    # Listar arquivos
    files = gdrive.list_files_in_folder()
    
    # Filtrar apenas PDFs
    pdfs = [f for f in files if f['name'].lower().endswith('.pdf')]
    
    print(f"Total de arquivos: {len(files)}")
    print(f"PDFs encontrados: {len(pdfs)}\n")
    
    # Transferir PDFs
    for idx, pdf in enumerate(pdfs, 1):
        print(f"[{idx}/{len(pdfs)}] {pdf['name']}")
        
        # Baixar
        content = gdrive.download_file(pdf['id'], pdf['name'])
        if content:
            # Fazer upload
            result = azure.upload_blob(pdf['name'], content, overwrite=True)
            if result['status'] == 'success':
                print(f"       ✅ Transferido ({result['size_mb']} MB)")
            else:
                print(f"       ❌ Erro: {result.get('error')}")
        else:
            print(f"       ❌ Falha ao baixar")
        print()

def exemplo_5_criar_pasta_e_compartilhar():
    """Exemplo 5: Criar pasta no Google Drive e compartilhar"""
    print("=" * 70)
    print("EXEMPLO 5: Criar Pasta e Compartilhar")
    print("=" * 70 + "\n")
    
    gdrive = GoogleDriveManager()
    
    # Criar pasta
    print("Criando pasta 'Backups_Azure'...")
    folder_id = gdrive.create_folder("Backups_Azure")
    
    if folder_id:
        print(f"✅ Pasta criada (ID: {folder_id})")
        
        # Compartilhar
        email = "seu-email@gmail.com"
        print(f"\nCompartilhando com {email}...")
        gdrive.share_folder(folder_id, email)
    else:
        print("❌ Falha ao criar pasta")

def exemplo_6_download_azure():
    """Exemplo 6: Fazer download de arquivo do Azure"""
    print("=" * 70)
    print("EXEMPLO 6: Download de Arquivo do Azure")
    print("=" * 70 + "\n")
    
    azure = AzureBlobManager()
    
    # Listar blobs
    blobs = azure.list_blobs()
    
    if blobs:
        # Pegar o primeiro blob
        blob_name = blobs[0].name
        
        print(f"Fazendo download de: {blob_name}")
        print("-" * 70)
        
        # Download
        content = azure.download_blob(blob_name)
        
        if content:
            print(f"✅ Download concluído")
            print(f"   Tamanho: {len(content) / (1024 * 1024):.2f} MB")
            
            # Salvar em arquivo local
            local_file = f"downloaded_{blob_name}"
            with open(local_file, 'wb') as f:
                f.write(content)
            print(f"   Salvo como: {local_file}")
        else:
            print(f"❌ Falha no download")
    else:
        print("Nenhum blob encontrado no contêiner")

def exemplo_7_deletar_blob():
    """Exemplo 7: Deletar arquivo do Azure"""
    print("=" * 70)
    print("EXEMPLO 7: Deletar Blob do Azure")
    print("=" * 70 + "\n")
    
    azure = AzureBlobManager()
    
    # Listar blobs
    blobs = azure.list_blobs()
    
    if blobs:
        # Exibir opções
        print("Blobs disponíveis:")
        for idx, blob in enumerate(blobs, 1):
            print(f"{idx}. {blob.name}")
        
        # Deletar o primeiro como exemplo
        blob_to_delete = blobs[0].name
        
        print(f"\nDeletando: {blob_to_delete}")
        result = azure.delete_blob(blob_to_delete)
        
        if result:
            print("✅ Blob deletado com sucesso")
        else:
            print("❌ Falha ao deletar")
    else:
        print("Nenhum blob para deletar")

def menu():
    """Menu de exemplos"""
    examples = {
        '1': ('Listar Google Drive', exemplo_1_listar_google_drive),
        '2': ('Listar Azure Blob Storage', exemplo_2_listar_azure),
        '3': ('Transferir Um Arquivo', exemplo_3_transferir_um_arquivo),
        '4': ('Transferir Apenas PDFs', exemplo_4_transferir_com_filtro),
        '5': ('Criar e Compartilhar Pasta', exemplo_5_criar_pasta_e_compartilhar),
        '6': ('Download do Azure', exemplo_6_download_azure),
        '7': ('Deletar Blob do Azure', exemplo_7_deletar_blob),
    }
    
    print("\n" + "=" * 70)
    print("  EXEMPLOS DE USO")
    print("=" * 70 + "\n")
    
    for key, (description, _) in examples.items():
        print(f"{key}. {description}")
    print("\n0. Sair\n")
    
    choice = input("Selecione um exemplo (0-7): ").strip()
    
    if choice in examples:
        print()
        _, func = examples[choice]
        try:
            func()
        except Exception as e:
            print(f"\n❌ Erro ao executar exemplo: {e}")
    elif choice != '0':
        print("Opção inválida!")

def main():
    """Função principal"""
    while True:
        try:
            menu()
            input("\nPressione ENTER para continuar...")
            print("\n" * 2)
        except KeyboardInterrupt:
            print("\n\n⚠️  Aplicação interrompida")
            break

if __name__ == "__main__":
    # Para rodar automaticamente um exemplo:
    # exemplo_1_listar_google_drive()
    
    # Ou para usar o menu:
    main()
