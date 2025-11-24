"""
Script para testar as conexões (teste_conexoes.py)
"""

def testar_google_drive():
    """Testa conexão com Google Drive"""
    print("\n" + "="*70)
    print("  TESTE DE CONEXÃO - GOOGLE DRIVE")
    print("="*70 + "\n")
    
    try:
        from google_drive_manager import GoogleDriveManager
        from config import GOOGLE_DRIVE_FOLDER_ID
        
        print("1️⃣  Inicializando Google Drive Manager...")
        gdrive = GoogleDriveManager()
        
        print("\n2️⃣  Testando acesso à pasta...")
        print(f"   ID da pasta: {GOOGLE_DRIVE_FOLDER_ID}")
        
        files = gdrive.list_files_in_folder()
        
        print("\n✅ CONEXÃO COM GOOGLE DRIVE OK!")
        print(f"   Total de arquivos encontrados: {len(files)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO NA CONEXÃO COM GOOGLE DRIVE:")
        print(f"   {e}")
        return False

def testar_azure():
    """Testa conexão com Azure Blob Storage"""
    print("\n" + "="*70)
    print("  TESTE DE CONEXÃO - AZURE BLOB STORAGE")
    print("="*70 + "\n")
    
    try:
        from azure_blob_manager import AzureBlobManager
        from config import AZURE_CONTAINER_NAME
        
        print("1️⃣  Inicializando Azure Blob Manager...")
        azure = AzureBlobManager()
        
        print("\n2️⃣  Testando acesso ao contêiner...")
        print(f"   Nome do contêiner: {AZURE_CONTAINER_NAME}")
        
        blobs = azure.list_blobs()
        
        print("\n✅ CONEXÃO COM AZURE BLOB STORAGE OK!")
        print(f"   Total de blobs encontrados: {len(blobs)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO NA CONEXÃO COM AZURE BLOB STORAGE:")
        print(f"   {e}")
        return False

def testar_configuracoes():
    """Testa se as configurações estão corretas"""
    print("\n" + "="*70)
    print("  VERIFICAÇÃO DE CONFIGURAÇÕES")
    print("="*70 + "\n")
    
    import os
    from config import (
        GOOGLE_DRIVE_FOLDER_ID,
        GOOGLE_CREDENTIALS_FILE,
        AZURE_CONNECTION_STRING,
        AZURE_CONTAINER_NAME
    )
    
    checks = []
    
    # Check 1: credentials.json
    print("1️⃣  Verificando credentials.json...")
    if os.path.exists(GOOGLE_CREDENTIALS_FILE):
        print(f"   ✅ {GOOGLE_CREDENTIALS_FILE} encontrado")
        checks.append(True)
    else:
        print(f"   ❌ {GOOGLE_CREDENTIALS_FILE} NÃO encontrado")
        checks.append(False)
    
    # Check 2: GOOGLE_DRIVE_FOLDER_ID
    print("\n2️⃣  Verificando GOOGLE_DRIVE_FOLDER_ID...")
    if GOOGLE_DRIVE_FOLDER_ID and GOOGLE_DRIVE_FOLDER_ID != "SUBSTITUA_PELO_SEU_ID":
        print(f"   ✅ GOOGLE_DRIVE_FOLDER_ID configurado")
        print(f"      Valor: {GOOGLE_DRIVE_FOLDER_ID[:30]}...")
        checks.append(True)
    else:
        print(f"   ❌ GOOGLE_DRIVE_FOLDER_ID não está configurado")
        checks.append(False)
    
    # Check 3: AZURE_CONNECTION_STRING
    print("\n3️⃣  Verificando AZURE_CONNECTION_STRING...")
    if AZURE_CONNECTION_STRING:
        print(f"   ✅ AZURE_CONNECTION_STRING configurado")
        print(f"      Comprimento: {len(AZURE_CONNECTION_STRING)} caracteres")
        checks.append(True)
    else:
        print(f"   ❌ AZURE_CONNECTION_STRING não está configurado")
        checks.append(False)
    
    # Check 4: AZURE_CONTAINER_NAME
    print("\n4️⃣  Verificando AZURE_CONTAINER_NAME...")
    if AZURE_CONTAINER_NAME:
        print(f"   ✅ AZURE_CONTAINER_NAME configurado")
        print(f"      Valor: {AZURE_CONTAINER_NAME}")
        checks.append(True)
    else:
        print(f"   ❌ AZURE_CONTAINER_NAME não está configurado")
        checks.append(False)
    
    # Resumo
    print("\n" + "-"*70)
    total = len(checks)
    passed = sum(checks)
    
    if passed == total:
        print(f"✅ TODAS AS CONFIGURAÇÕES OK! ({passed}/{total})")
        return True
    else:
        print(f"⚠️  ALGUMAS CONFIGURAÇÕES FALTAM ({passed}/{total})")
        return False

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("  TESTE DE CONEXÕES - APLICAÇÃO DE TRANSFERÊNCIA")
    print("="*70)
    
    # Testar configurações
    config_ok = testar_configuracoes()
    
    if not config_ok:
        print("\n❌ Por favor, configure os arquivos antes de continuar.")
        print("   Veja SETUP_GOOGLE_DRIVE.md e .env")
        return
    
    # Testar Google Drive
    gdrive_ok = testar_google_drive()
    
    # Testar Azure
    azure_ok = testar_azure()
    
    # Resumo final
    print("\n" + "="*70)
    print("  RESUMO DOS TESTES")
    print("="*70 + "\n")
    
    print("Status das Conexões:")
    print(f"  Configurações:   {'✅ OK' if config_ok else '❌ ERRO'}")
    print(f"  Google Drive:    {'✅ OK' if gdrive_ok else '❌ ERRO'}")
    print(f"  Azure Storage:   {'✅ OK' if azure_ok else '❌ ERRO'}")
    
    if gdrive_ok and azure_ok:
        print("\n✅ TUDO PRONTO! Execute 'python main.py' para começar.")
    else:
        print("\n❌ Verifique os erros acima e tente novamente.")
    
    print()

if __name__ == "__main__":
    main()
