# 📁 Gerenciador de Arquivos Google Drive ↔ Azure Blob Storage

Sistema integrado para sincronizar e gerenciar arquivos entre Google Drive e Azure Blob Storage com interface web moderna e CLI interativo.

## 🎯 Funcionalidades

- ✅ **Interface Web Moderna** - Dashboard com dois painéis (Google Drive / Azure Blob)
- ✅ **CLI Interativo** - Menu de linha de comando para gerenciamento
- ✅ **Transferência de Arquivos** - Upload/download entre Google Drive e Azure
- ✅ **Autenticação Segura** - Google Service Account + Azure Connection String
- ✅ **Operações em Lote** - Transferir múltiplos arquivos simultaneamente
- ✅ **Gerenciamento** - Listar, deletar e organizar arquivos
- ✅ **Responsivo** - Funciona em desktop, tablet e mobile

---

## 🚀 Início Rápido

### 1. Pré-requisitos

- **Python 3.8+** instalado
- **Git** (para clone e deploy)
- **Conta Google Cloud** com API habilitada
- **Conta Microsoft Azure** com Storage habilitado
- **Vercel** account (para deploy do frontend)
- **GitHub** account (para versionamento)

### 2. Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/gerenciador-arquivos.git
cd gerenciador-arquivos

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as credenciais
# Edite o arquivo .env com suas credenciais
# GOOGLE_DRIVE_FOLDER_ID=seu_folder_id
# AZURE_CONNECTION_STRING=sua_connection_string
# AZURE_CONTAINER_NAME=seu_container
```

---

## 🎮 Executando a Aplicação

### Opção 1: Interface Web (Recomendada)

```bash
# Com ambiente virtual ativado
python app.py
```

Abra o navegador em: **http://localhost:5000**

**Funcionalidades da Web:**
- 📂 Painel esquerdo: Arquivos do Google Drive
- ☁️ Painel direito: Blobs do Azure Blob Storage
- ✅ Checkbox para selecionar múltiplos arquivos
- 🔄 Botão "Transferir Selecionados" para sincronizar
- 🗑️ Botão "Deletar" para remover arquivos
- 🔄 Auto-refresh a cada 30 segundos

### Opção 2: Interface CLI (Terminal)

```bash
# Com ambiente virtual ativado
python main.py
```

**Menu de Opções:**
```
╔════════════════════════════════════════╗
║  GERENCIADOR DE ARQUIVOS - MENU      ║
╠════════════════════════════════════════╣
║  1. Listar arquivos Google Drive       ║
║  2. Listar blobs Azure Storage         ║
║  3. Transferir todos os arquivos       ║
║  4. Sair                               ║
╚════════════════════════════════════════╝
```

Escolha uma opção digitando o número correspondente.

---

## ⚙️ Configuração das Credenciais

### Google Drive (Service Account)

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a "Google Drive API"
4. Crie uma "Service Account"
5. Gere uma chave JSON
6. Salve como `credentials.json` na raiz do projeto
7. Compartilhe a pasta Google Drive com o email da service account

### Azure Blob Storage

1. Acesse [Azure Portal](https://portal.azure.com/)
2. Crie uma conta de armazenamento
3. Vá para "Chaves de acesso"
4. Copie a "Cadeia de conexão"
5. Configure no arquivo `.env`:

```env
AZURE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=sua_conta;...
AZURE_CONTAINER_NAME=seu_container
GOOGLE_DRIVE_FOLDER_ID=seu_folder_id
```

---

## 🌐 Enviando para GitHub

### Passo 1: Inicializar Repositório Git

```bash
# No diretório do projeto
git init
```

### Passo 2: Adicionar Arquivos

```bash
git add .
```

### Passo 3: Criar Commit Inicial

```bash
git commit -m "Initial commit: Gerenciador de arquivos Google Drive ↔ Azure"
```

### Passo 4: Criar Repositório no GitHub

1. Acesse [GitHub.com](https://github.com/)
2. Clique em **+** no canto superior direito
3. Selecione **New repository**
4. Configure:
   - **Repository name**: gerenciador-arquivos
   - **Description**: Sistema de sincronização Google Drive ↔ Azure Blob
   - **Public** (se quiser público) ou **Private**
   - Não inicialize com README/gitignore (já temos)
5. Clique **Create repository**

### Passo 5: Adicionar Remote e Push

```bash
# Adicione o remote (substitua USERNAME pelo seu)
git remote add origin https://github.com/USERNAME/gerenciador-arquivos.git

# Renomeie branch para main (se necessário)
git branch -M main

# Faça push do código
git push -u origin main
```

### Passo 6: Verificar no GitHub

Abra `https://github.com/USERNAME/gerenciador-arquivos` para confirmar que o código foi enviado.

---

## 🚀 Enviando o Frontend para Vercel

### Passo 1: Preparar Projeto para Vercel

```bash
# Crie um arquivo vercel.json na raiz do projeto
```

Crie o arquivo `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "GOOGLE_DRIVE_FOLDER_ID": "@google_drive_folder_id",
    "AZURE_CONNECTION_STRING": "@azure_connection_string",
    "AZURE_CONTAINER_NAME": "@azure_container_name"
  }
}
```

### Passo 2: Fazer Push para GitHub

```bash
git add vercel.json
git commit -m "Add Vercel configuration"
git push origin main
```

### Passo 3: Criar Conta Vercel

1. Acesse [Vercel.com](https://vercel.com/)
2. Clique **Sign Up**
3. Autentique com GitHub
4. Autorize o Vercel a acessar seus repositórios

### Passo 4: Importar Projeto no Vercel

1. Após autenticação, clique **Add New** > **Project**
2. Selecione o repositório `gerenciador-arquivos`
3. Clique **Import**

### Passo 5: Configurar Variáveis de Ambiente

Na página de configuração do projeto:

1. Vá para **Settings** > **Environment Variables**
2. Adicione as seguintes variáveis:

| Nome da Variável | Valor |
|---|---|
| `GOOGLE_DRIVE_FOLDER_ID` | Seu ID da pasta Google Drive |
| `AZURE_CONNECTION_STRING` | Sua cadeia de conexão Azure |
| `AZURE_CONTAINER_NAME` | Nome do seu container Azure |

3. Clique **Save**

### Passo 6: Deploy Automático

1. Volte para **Overview**
2. O Vercel deve começar a fazer deploy automaticamente
3. Aguarde a conclusão (geralmente 2-3 minutos)
4. Quando pronto, você verá a URL: `https://seu-projeto.vercel.app`

### Passo 7: Acessar Aplicação

Abra a URL fornecida pelo Vercel no navegador para acessar sua aplicação online!

**Nota:** Cada vez que você fazer push para o repositório no GitHub, o Vercel fará um deploy automático da nova versão.

---

## 🔄 Deploy Automático (CI/CD)

O Vercel já vem com CI/CD integrado! Quando você faz:

```bash
git push origin main
```

Vercel automaticamente:
1. Detecta as mudanças
2. Faz build do projeto
3. Realiza testes (se configurados)
4. Faz deploy da nova versão
5. Atualiza a URL com a versão mais recente

---

## 📂 Estrutura do Projeto

```
gerenciador-arquivos/
├── app.py                      # Flask API (7 endpoints)
├── main.py                     # CLI interativo
├── config.py                   # Configurações
├── google_drive_manager.py     # Gerenciador Google Drive
├── azure_blob_manager.py       # Gerenciador Azure Blob
├── requirements.txt            # Dependências Python
├── .env                        # Credenciais (NÃO committar!)
├── credentials.json            # Service Account Google (NÃO committar!)
├── vercel.json                 # Configuração Vercel
├── static/
│   ├── app.js                  # Frontend JavaScript
│   └── styles.css              # Estilos CSS
├── templates/
│   └── index.html              # Página HTML principal
└── README.md                   # Este arquivo
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'google'"
```bash
# Reinstale as dependências
pip install -r requirements.txt
```

### "The specified container does not exist"
```bash
# O container será criado automaticamente na primeira execução
python app.py
```

### "GOOGLE_DRIVE_FOLDER_ID not found"
- Verifique se o `.env` está na raiz do projeto
- Certifique-se de que o ID está correto
- Compartilhe a pasta com o email da Service Account

### "Azure authentication failed"
- Verifique a `AZURE_CONNECTION_STRING` no `.env`
- Confirme se a conta de armazenamento está ativa
- Teste com `python teste_conexoes.py`

### Deploy no Vercel falha
1. Verifique as variáveis de ambiente no dashboard Vercel
2. Consulte os logs de build: **Deployments** > **Build & Logs**
3. Confirme que `vercel.json` está no repositório

---

## 📊 Endpoints da API

A aplicação expõe os seguintes endpoints REST:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Página principal |
| GET | `/api/health` | Status da API |
| GET | `/api/google-drive/files` | Lista arquivos Google Drive |
| GET | `/api/azure/blobs` | Lista blobs Azure |
| POST | `/api/transfer` | Transfere múltiplos arquivos |
| POST | `/api/transfer-single` | Transfere um arquivo |
| POST | `/api/delete-blob` | Deleta blob Azure |

---

## 📝 Dependências

- **google-auth-oauthlib** - Autenticação Google
- **google-api-python-client** - API Google Drive
- **azure-storage-blob** - API Azure Storage
- **python-dotenv** - Gerenciador de variáveis de ambiente
- **Flask** - Framework web
- **flask-cors** - Suporte CORS

---

## 👨‍💻 Desenvolvimento

### Adicionar nova funcionalidade:

1. Crie uma nova branch:
```bash
git checkout -b feature/sua-funcionalidade
```

2. Faça suas mudanças e commits:
```bash
git add .
git commit -m "Describe your changes"
```

3. Push da branch:
```bash
git push origin feature/sua-funcionalidade
```

4. Abra uma Pull Request no GitHub

---

## 📄 Licença

MIT - Livre para uso pessoal e comercial

---

## 🤝 Suporte

Para questões ou problemas:
1. Abra uma **Issue** no GitHub
2. Forneça detalhes do erro
3. Inclua logs de execução se possível

---

## 🎓 Autor

Vinicius Ribeiro

**Data**: 2025
**Status**: ✅ Production Ready

---

**Última atualização**: 24/11/2025
