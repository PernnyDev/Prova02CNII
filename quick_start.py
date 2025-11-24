#!/usr/bin/env python3
"""
🚀 QUICK START - Guia Rápido de 5 Minutos
Executável diretamente: python quick_start.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner inicial"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🚀 TRANSFERÊNCIA GOOGLE DRIVE → AZURE BLOB STORAGE             ║
║                                                                   ║
║   Quick Start - Começar em 5 minutos                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Verifica versão do Python"""
    print("1️⃣  Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor} OK\n")
        return True
    else:
        print(f"   ❌ Python 3.8+ necessário (você tem {version.major}.{version.minor})\n")
        return False

def check_files():
    """Verifica arquivos necessários"""
    print("2️⃣  Verificando arquivos...")
    files = ['.env', 'requirements.txt', 'main.py']
    all_ok = True
    
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} FALTANDO")
            all_ok = False
    
    print()
    return all_ok

def check_credentials():
    """Verifica credentials.json"""
    print("3️⃣  Verificando credentials.json...")
    
    if os.path.exists('credentials.json'):
        print("   ✅ credentials.json encontrado\n")
        return True
    else:
        print("   ⚠️  credentials.json NÃO ENCONTRADO")
        print("""
   Você precisa:
   1. Ir a: https://console.cloud.google.com/
   2. Criar Service Account
   3. Gerar chave JSON
   4. Salvar como 'credentials.json'
   
   Veja: SETUP_GOOGLE_DRIVE.md
        """)
        return False

def check_env():
    """Verifica .env"""
    print("4️⃣  Verificando .env...")
    
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'SUBSTITUA_PELO_SEU_ID' in content:
            print("   ⚠️  GOOGLE_DRIVE_FOLDER_ID não configurado")
            print("""
   Você precisa:
   1. Abrir Google Drive
   2. Copiar ID da pasta
   3. Editar .env
   4. Substituir: GOOGLE_DRIVE_FOLDER_ID=SEU_ID
            """)
            return False
        else:
            print("   ✅ .env configurado\n")
            return True
    except Exception as e:
        print(f"   ❌ Erro ao ler .env: {e}\n")
        return False

def create_venv():
    """Cria ambiente virtual"""
    print("5️⃣  Verificando ambiente virtual...")
    
    if os.path.exists('venv'):
        print("   ✅ venv já existe\n")
        return True
    
    print("   ⏳ Criando venv...")
    try:
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("   ✅ venv criado\n")
        return True
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        return False

def install_deps():
    """Instala dependências"""
    print("6️⃣  Instalando dependências...")
    
    try:
        if sys.platform == 'win32':
            pip = '.\\venv\\Scripts\\pip'
        else:
            pip = './venv/bin/pip'
        
        subprocess.run([pip, 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("   ✅ Dependências instaladas\n")
        return True
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        return False

def run_tests():
    """Executa testes de conexão"""
    print("7️⃣  Testando conexões...\n")
    
    try:
        if sys.platform == 'win32':
            python = '.\\venv\\Scripts\\python'
        else:
            python = './venv/bin/python'
        
        subprocess.run([python, 'teste_conexoes.py'], check=False)
        return True
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        return False

def show_next_steps():
    """Exibe próximos passos"""
    print("\n" + "="*70)
    print("  ✅ TUDO PRONTO!")
    print("="*70 + "\n")
    
    if sys.platform == 'win32':
        activate = ".\\venv\\Scripts\\Activate.ps1"
        python_cmd = ".\\venv\\Scripts\\python main.py"
    else:
        activate = "source ./venv/bin/activate"
        python_cmd = "python main.py"
    
    print("PRÓXIMO PASSO - Execute a aplicação:\n")
    print(f"  PowerShell/Terminal:")
    print(f"  {activate}")
    print(f"  {python_cmd}\n")
    
    print("OU execute este comando (todos de uma vez):\n")
    if sys.platform == 'win32':
        print("  .\\venv\\Scripts\\Activate.ps1; python main.py\n")
    else:
        print("  source venv/bin/activate && python main.py\n")

def show_menu():
    """Exibe menu de opções"""
    print("OPÇÕES:")
    print("  1. ✅ Continuar com setup automático")
    print("  2. 📖 Ver documentação")
    print("  3. 🧪 Testar conexões apenas")
    print("  4. ❌ Sair\n")

def main():
    """Função principal"""
    print_banner()
    
    # Checks iniciais
    if not check_python():
        return
    
    if not check_files():
        print("❌ Arquivos necessários faltando!\n")
        return
    
    if not check_credentials():
        print("⚠️  Configure credentials.json e tente novamente\n")
        return
    
    if not check_env():
        print("⚠️  Configure .env e tente novamente\n")
        return
    
    # Setup
    if not create_venv():
        return
    
    if not install_deps():
        print("Tente novamente mais tarde\n")
        return
    
    # Testes
    print("="*70)
    run_tests()
    
    # Próximos passos
    show_next_steps()
    
    print("="*70)
    print("📚 DOCUMENTAÇÃO:")
    print("  README.md           - Visão geral completa")
    print("  PASSO_A_PASSO.md    - Tutorial visual 20 passos")
    print("  FAQ.md              - Perguntas frequentes")
    print("  ARQUITETURA.md      - Estrutura técnica")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
