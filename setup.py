"""
Script de setup automático
Instala dependências e valida configurações
"""
import os
import subprocess
import sys

def run_command(command):
    """Executa comando no terminal"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def print_section(title):
    """Imprime título de seção"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def main():
    print_section("SETUP - TRANSFERÊNCIA GOOGLE DRIVE → AZURE")
    
    # 1. Verificar Python
    print("1️⃣  Verificando Python...")
    python_version = sys.version.split()[0]
    print(f"   ✅ Python {python_version} encontrado\n")
    
    # 2. Criar venv se não existir
    print("2️⃣  Verificando ambiente virtual...")
    if not os.path.exists("venv"):
        print("   ⏳ Criando ambiente virtual...")
        success, _, error = run_command(f"{sys.executable} -m venv venv")
        if success:
            print("   ✅ Ambiente virtual criado\n")
        else:
            print(f"   ❌ Erro: {error}\n")
            return False
    else:
        print("   ✅ Ambiente virtual já existe\n")
    
    # 3. Instalar dependências
    print("3️⃣  Instalando dependências...")
    
    # Detectar sistema operacional
    if sys.platform == "win32":
        pip_cmd = ".\\venv\\Scripts\\pip"
        activate_cmd = ".\\venv\\Scripts\\Activate.ps1"
    else:
        pip_cmd = "./venv/bin/pip"
        activate_cmd = "source ./venv/bin/activate"
    
    success, stdout, stderr = run_command(f"{pip_cmd} install -r requirements.txt")
    if success:
        print("   ✅ Dependências instaladas\n")
    else:
        print(f"   ❌ Erro: {stderr}\n")
        return False
    
    # 4. Verificar arquivos necessários
    print("4️⃣  Verificando arquivos de configuração...")
    
    files_check = {
        ".env": "Variáveis de ambiente",
        "credentials.json": "Credenciais Google Drive"
    }
    
    missing_files = []
    for filename, description in files_check.items():
        if os.path.exists(filename):
            print(f"   ✅ {filename} - {description}")
        else:
            print(f"   ⚠️  {filename} - {description} (AUSENTE)")
            missing_files.append(filename)
    
    print()
    
    # 5. Validar configurações
    if not missing_files:
        print("5️⃣  Validando configurações...")
        
        try:
            from config import validate_config
            if validate_config():
                print("   ✅ Todas as configurações validadas\n")
            else:
                print("   ⚠️  Algumas configurações faltam\n")
        except Exception as e:
            print(f"   ⚠️  Erro ao validar: {e}\n")
    else:
        print("5️⃣  Configuração Incompleta\n")
        print("   ⚠️  Arquivos faltando:")
        for file in missing_files:
            print(f"      - {file}")
        print()
    
    # 6. Resumo
    print_section("PRÓXIMOS PASSOS")
    
    if missing_files:
        print("1. Configure o arquivo `.env` com seus dados Azure")
        print("2. Baixe o arquivo `credentials.json` do Google Cloud Console")
        print("3. Coloque ambos os arquivos na raiz do projeto")
        print("4. Consulte SETUP_GOOGLE_DRIVE.md para instruções detalhadas")
    else:
        print("✅ Tudo pronto! Execute a aplicação com:")
        if sys.platform == "win32":
            print(f"   .\\venv\\Scripts\\Activate.ps1")
        else:
            print(f"   source ./venv/bin/activate")
        print("   python main.py")
    
    print()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
