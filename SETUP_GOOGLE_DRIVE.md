# GUIA: Como Criar Credenciais do Google Drive

## 1. Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Select a Project"** → **"New Project"**
3. Nome: `Google-Drive-Azure-App`
4. Clique em **"Create"** e aguarde

## 2. Ativar Google Drive API

1. Na barra de pesquisa do console, procure por **"Google Drive API"**
2. Clique no resultado
3. Clique em **"ENABLE"** (Ativar)
4. Aguarde ativar

## 3. Criar Service Account

1. No menu esquerdo, procure por **"Service Accounts"** (Contas de Serviço)
2. Clique em **"Create Service Account"**
3. Preencha:
   - **Service account name**: `google-drive-app`
   - **Service account ID**: Preenchido automaticamente
   - **Description**: `App para transferência de arquivos`
4. Clique em **"Create and Continue"**

## 4. Criar Chave JSON

1. Na página da Service Account criada, clique na aba **"Keys"**
2. Clique em **"Add Key"** → **"Create new key"**
3. Selecione **"JSON"**
4. Clique em **"Create"**
5. Um arquivo JSON será baixado automaticamente
6. **Salve este arquivo como `credentials.json` na pasta do projeto**

## 5. Compartilhar Pasta com Service Account

1. No arquivo `credentials.json` baixado, copie o valor de **"client_email"**
   - Exemplo: `google-drive-app@seu-projeto.iam.gserviceaccount.com`

2. No Google Drive:
   - Crie uma pasta ou use uma existente
   - Clique com botão direito → **"Share"** (Compartilhar)
   - Cole o email do Service Account
   - Conceda **"Editor"** (acesso de edição)
   - Clique em **"Share"**

3. Copie o **ID da pasta** da URL:
   - URL exemplo: `https://drive.google.com/drive/folders/1ABC2def_GGHIJ456klMN7-OPQ_RSTuvwxYZ`
   - ID da pasta: `1ABC2def_GGHIJ456klMN7-OPQ_RSTuvwxYZ`

## 6. Configurar .env

Crie um arquivo `.env` na pasta do projeto com:

```
GOOGLE_DRIVE_FOLDER_ID=SEU_ID_AQUI
AZURE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=sua_conta;AccountKey=SUA_CHAVE_AQUI;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME=seu_container
```

## Pronto!

Você agora tem tudo configurado para usar a aplicação. Certifique-se de que:
- ✅ `credentials.json` está na pasta do projeto
- ✅ `.env` está preenchido corretamente
- ✅ A pasta foi compartilhada com o Service Account
