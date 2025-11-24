"""
API Flask para Transferência de Arquivos
Google Drive → Azure Blob Storage
"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import sys
from datetime import datetime
from google_drive_manager import GoogleDriveManager
from azure_blob_manager import AzureBlobManager
from config import validate_config, AZURE_CONTAINER_NAME

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Variáveis globais
gdrive_manager = None
azure_manager = None

def initialize_managers():
    """Inicializa gerenciadores"""
    global gdrive_manager, azure_manager
    try:
        gdrive_manager = GoogleDriveManager()
        azure_manager = AzureBlobManager()
        azure_manager.create_container_if_not_exists()
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se a API está funcionando"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'API está operacional'
    })

@app.route('/')
def index():
    """Retorna página principal"""
    return render_template('index.html')

@app.route('/api/google-drive/files', methods=['GET'])
def get_google_drive_files():
    """Lista arquivos do Google Drive"""
    try:
        files = gdrive_manager.list_files_in_folder()
        
        # Filtrar apenas arquivos (não pastas)
        files = [f for f in files if f.get('mimetype', '').lower() != 'application/vnd.google-apps.folder']
        
        # Formatar resposta
        formatted_files = []
        for file in files:
            formatted_files.append({
                'id': file['id'],
                'name': file['name'],
                'size_mb': round(int(file.get('size', 0)) / (1024 * 1024), 2),
                'mime_type': file.get('mimeType', 'unknown'),
                'created': file.get('createdTime', 'N/A'),
                'modified': file.get('modifiedTime', 'N/A')
            })
        
        return jsonify({
            'status': 'success',
            'count': len(formatted_files),
            'files': formatted_files
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/azure/blobs', methods=['GET'])
def get_azure_blobs():
    """Lista blobs do Azure Blob Storage"""
    try:
        blobs = azure_manager.list_blobs()
        
        # Formatar resposta
        formatted_blobs = []
        for blob in blobs:
            formatted_blobs.append({
                'name': blob.name,
                'size_mb': round(blob.size / (1024 * 1024), 2),
                'last_modified': blob.last_modified.isoformat() if blob.last_modified else 'N/A'
            })
        
        return jsonify({
            'status': 'success',
            'count': len(formatted_blobs),
            'blobs': formatted_blobs
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/transfer', methods=['POST'])
def transfer_files():
    """Transfere arquivos selecionados"""
    try:
        data = request.json
        file_ids = data.get('file_ids', [])
        
        if not file_ids:
            return jsonify({
                'status': 'error',
                'message': 'Nenhum arquivo selecionado'
            }), 400
        
        # Obter arquivos do Google Drive
        all_files = gdrive_manager.list_files_in_folder()
        all_files = [f for f in all_files if f.get('mimetype', '').lower() != 'application/vnd.google-apps.folder']
        
        # Filtrar apenas os selecionados
        files_to_transfer = [f for f in all_files if f['id'] in file_ids]
        
        results = {
            'success': [],
            'failed': [],
            'total': len(files_to_transfer)
        }
        
        # Transferir cada arquivo
        for file in files_to_transfer:
            file_id = file['id']
            file_name = file['name']
            
            try:
                # Baixar do Google Drive
                file_content = gdrive_manager.download_file(file_id, file_name)
                
                if file_content is None:
                    results['failed'].append({
                        'name': file_name,
                        'error': 'Falha ao baixar do Google Drive'
                    })
                    continue
                
                # Enviar para Azure
                upload_result = azure_manager.upload_blob(file_name, file_content, overwrite=True)
                
                if upload_result['status'] == 'success':
                    results['success'].append({
                        'name': file_name,
                        'size_mb': upload_result['size_mb']
                    })
                else:
                    results['failed'].append({
                        'name': file_name,
                        'error': upload_result.get('error', 'Erro desconhecido')
                    })
            
            except Exception as e:
                results['failed'].append({
                    'name': file_name,
                    'error': str(e)
                })
        
        return jsonify({
            'status': 'success' if results['success'] else 'partial',
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/transfer-single', methods=['POST'])
def transfer_single_file():
    """Transfere um arquivo individual"""
    try:
        data = request.json
        file_id = data.get('file_id')
        file_name = data.get('file_name')
        
        if not file_id or not file_name:
            return jsonify({
                'status': 'error',
                'message': 'file_id e file_name são obrigatórios'
            }), 400
        
        # Baixar do Google Drive
        file_content = gdrive_manager.download_file(file_id, file_name)
        
        if file_content is None:
            return jsonify({
                'status': 'error',
                'message': 'Falha ao baixar do Google Drive'
            }), 500
        
        # Enviar para Azure
        upload_result = azure_manager.upload_blob(file_name, file_content, overwrite=True)
        
        return jsonify({
            'status': 'success' if upload_result['status'] == 'success' else 'error',
            'result': upload_result
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/delete-blob', methods=['POST'])
def delete_blob():
    """Deleta um blob do Azure"""
    try:
        data = request.json
        blob_name = data.get('blob_name')
        
        if not blob_name:
            return jsonify({
                'status': 'error',
                'message': 'blob_name é obrigatório'
            }), 400
        
        result = azure_manager.delete_blob(blob_name)
        
        return jsonify({
            'status': 'success' if result else 'error',
            'message': f'Blob deletado com sucesso' if result else 'Falha ao deletar blob'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Validar configurações
    if not validate_config():
        print("❌ Configurações inválidas")
        sys.exit(1)
    
    # Inicializar gerenciadores
    if not initialize_managers():
        print("❌ Erro ao inicializar gerenciadores")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("  API Flask iniciada com sucesso!")
    print("="*70)
    print("\n🌐 Acesse a aplicação em: http://localhost:5000")
    print("📡 Documentação da API disponível em: http://localhost:5000/api/docs\n")
    
    # Iniciar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
