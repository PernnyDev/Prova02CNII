/**
 * Application JavaScript
 * Gerenciamento de interface e chamadas API
 */

const API_BASE = 'http://localhost:5000/api';

// Estado da aplicação
const appState = {
    googleDriveFiles: [],
    azureBlobs: [],
    selectedGDriveFiles: new Set(),
    selectedAzureBlobs: new Set(),
    isTransferring: false
};

/**
 * Inicializa a aplicação
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Aplicação iniciada');
    
    // Verificar conexão com API
    checkHealthStatus();
    
    // Carregar dados iniciais
    loadGoogleDriveFiles();
    loadAzureBlobs();
    
    // Event listeners - Google Drive
    document.getElementById('refresh-gdrive').addEventListener('click', loadGoogleDriveFiles);
    document.getElementById('select-all-gdrive').addEventListener('click', selectAllGDrive);
    document.getElementById('deselect-all-gdrive').addEventListener('click', deselectAllGDrive);
    document.getElementById('transfer-selected').addEventListener('click', transferSelectedFiles);
    
    // Event listeners - Azure
    document.getElementById('refresh-azure').addEventListener('click', loadAzureBlobs);
    document.getElementById('select-all-azure').addEventListener('click', selectAllAzure);
    document.getElementById('deselect-all-azure').addEventListener('click', deselectAllAzure);
    document.getElementById('delete-selected').addEventListener('click', deleteSelectedBlobs);
    
    // Atualizar a cada 30 segundos
    setInterval(() => {
        loadGoogleDriveFiles();
        loadAzureBlobs();
    }, 30000);
});

/**
 * Verifica status de conexão com a API
 */
async function checkHealthStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        if (data.status === 'ok') {
            updateStatusIndicator('connected', 'Conectado');
        }
    } catch (error) {
        console.error('❌ Erro ao verificar conexão:', error);
        updateStatusIndicator('error', 'Desconectado');
    }
}

/**
 * Atualiza indicador de status
 */
function updateStatusIndicator(status, text) {
    const indicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    indicator.className = `status-dot ${status}`;
    statusText.textContent = text;
}

/**
 * Carrega arquivos do Google Drive
 */
async function loadGoogleDriveFiles() {
    const loader = document.getElementById('gdrive-loader');
    const list = document.getElementById('gdrive-list');
    const empty = document.getElementById('gdrive-empty');
    const error = document.getElementById('gdrive-error');
    
    loader.style.display = 'flex';
    list.style.display = 'none';
    empty.style.display = 'none';
    error.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/google-drive/files`);
        const data = await response.json();
        
        if (data.status === 'success') {
            appState.googleDriveFiles = data.files;
            renderGoogleDriveFiles();
            loader.style.display = 'none';
            list.style.display = 'flex';
            
            if (data.count === 0) {
                list.style.display = 'none';
                empty.style.display = 'block';
            }
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        console.error('❌ Erro ao carregar Google Drive:', error);
        loader.style.display = 'none';
        error.style.display = 'block';
        showToast('Erro ao carregar arquivos do Google Drive', 'error');
    }
}

/**
 * Renderiza lista de arquivos do Google Drive
 */
function renderGoogleDriveFiles() {
    const list = document.getElementById('gdrive-list');
    list.innerHTML = '';
    
    appState.googleDriveFiles.forEach(file => {
        const isSelected = appState.selectedGDriveFiles.has(file.id);
        const item = createFileItem(file, isSelected, () => {
            toggleGDriveSelection(file.id);
        }, () => {
            transferSingleFile(file.id, file.name);
        });
        list.appendChild(item);
    });
    
    updateTransferButtonState();
}

/**
 * Carrega blobs do Azure
 */
async function loadAzureBlobs() {
    const loader = document.getElementById('azure-loader');
    const list = document.getElementById('azure-list');
    const empty = document.getElementById('azure-empty');
    const error = document.getElementById('azure-error');
    
    loader.style.display = 'flex';
    list.style.display = 'none';
    empty.style.display = 'none';
    error.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/azure/blobs`);
        const data = await response.json();
        
        if (data.status === 'success') {
            appState.azureBlobs = data.blobs;
            renderAzureBlobs();
            loader.style.display = 'none';
            list.style.display = 'flex';
            
            if (data.count === 0) {
                list.style.display = 'none';
                empty.style.display = 'block';
            }
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        console.error('❌ Erro ao carregar Azure Blobs:', error);
        loader.style.display = 'none';
        error.style.display = 'block';
        showToast('Erro ao carregar blobs do Azure', 'error');
    }
}

/**
 * Renderiza lista de blobs do Azure
 */
function renderAzureBlobs() {
    const list = document.getElementById('azure-list');
    list.innerHTML = '';
    
    appState.azureBlobs.forEach(blob => {
        const isSelected = appState.selectedAzureBlobs.has(blob.name);
        const item = createBlobItem(blob, isSelected, () => {
            toggleAzureSelection(blob.name);
        }, () => {
            deleteBlob(blob.name);
        });
        list.appendChild(item);
    });
    
    updateDeleteButtonState();
}

/**
 * Cria elemento de arquivo
 */
function createFileItem(file, isSelected, onToggle, onTransfer) {
    const div = document.createElement('div');
    div.className = `file-item ${isSelected ? 'selected' : ''}`;
    
    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    };
    
    div.innerHTML = `
        <input type="checkbox" class="file-checkbox" ${isSelected ? 'checked' : ''} onchange="${onToggle.name}">
        <div class="file-info">
            <div class="file-name">📄 ${escapeHtml(file.name)}</div>
            <div class="file-details">
                <span>📦 ${file.size_mb} MB</span>
                <span>🏷️ ${file.mime_type}</span>
                <span>📅 ${formatDate(file.created)}</span>
            </div>
        </div>
        <div class="file-actions">
            <button class="btn btn-small btn-success" onclick="${onTransfer.name}">⬆️ Enviar</button>
        </div>
    `;
    
    div.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON' && e.target.type !== 'checkbox') {
            onToggle();
        }
    });
    
    return div;
}

/**
 * Cria elemento de blob
 */
function createBlobItem(blob, isSelected, onToggle, onDelete) {
    const div = document.createElement('div');
    div.className = `file-item ${isSelected ? 'selected' : ''}`;
    
    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    };
    
    div.innerHTML = `
        <input type="checkbox" class="file-checkbox" ${isSelected ? 'checked' : ''} onchange="${onToggle.name}">
        <div class="file-info">
            <div class="file-name">☁️ ${escapeHtml(blob.name)}</div>
            <div class="file-details">
                <span>📦 ${blob.size_mb} MB</span>
                <span>📅 ${formatDate(blob.last_modified)}</span>
            </div>
        </div>
        <div class="file-actions">
            <button class="btn btn-small btn-danger" onclick="${onDelete.name}">🗑️ Deletar</button>
        </div>
    `;
    
    div.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON' && e.target.type !== 'checkbox') {
            onToggle();
        }
    });
    
    return div;
}

/**
 * Toggle seleção Google Drive
 */
function toggleGDriveSelection(fileId) {
    if (appState.selectedGDriveFiles.has(fileId)) {
        appState.selectedGDriveFiles.delete(fileId);
    } else {
        appState.selectedGDriveFiles.add(fileId);
    }
    renderGoogleDriveFiles();
}

/**
 * Selecionar tudo Google Drive
 */
function selectAllGDrive() {
    appState.googleDriveFiles.forEach(file => appState.selectedGDriveFiles.add(file.id));
    renderGoogleDriveFiles();
}

/**
 * Desselecionar tudo Google Drive
 */
function deselectAllGDrive() {
    appState.selectedGDriveFiles.clear();
    renderGoogleDriveFiles();
}

/**
 * Toggle seleção Azure
 */
function toggleAzureSelection(blobName) {
    if (appState.selectedAzureBlobs.has(blobName)) {
        appState.selectedAzureBlobs.delete(blobName);
    } else {
        appState.selectedAzureBlobs.add(blobName);
    }
    renderAzureBlobs();
}

/**
 * Selecionar tudo Azure
 */
function selectAllAzure() {
    appState.azureBlobs.forEach(blob => appState.selectedAzureBlobs.add(blob.name));
    renderAzureBlobs();
}

/**
 * Desselecionar tudo Azure
 */
function deselectAllAzure() {
    appState.selectedAzureBlobs.clear();
    renderAzureBlobs();
}

/**
 * Atualiza estado do botão de transferência
 */
function updateTransferButtonState() {
    const btn = document.getElementById('transfer-selected');
    btn.disabled = appState.selectedGDriveFiles.size === 0;
}

/**
 * Atualiza estado do botão de delete
 */
function updateDeleteButtonState() {
    const btn = document.getElementById('delete-selected');
    btn.disabled = appState.selectedAzureBlobs.size === 0;
}

/**
 * Transfere arquivo único
 */
async function transferSingleFile(fileId, fileName) {
    appState.selectedGDriveFiles.clear();
    appState.selectedGDriveFiles.add(fileId);
    await transferSelectedFiles();
}

/**
 * Transfere arquivos selecionados
 */
async function transferSelectedFiles() {
    if (appState.selectedGDriveFiles.size === 0) {
        showToast('Selecione pelo menos um arquivo', 'warning');
        return;
    }
    
    if (appState.isTransferring) {
        showToast('Transferência em andamento...', 'warning');
        return;
    }
    
    appState.isTransferring = true;
    openTransferModal();
    
    try {
        const fileIds = Array.from(appState.selectedGDriveFiles);
        const response = await fetch(`${API_BASE}/transfer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ file_ids: fileIds })
        });
        
        const data = await response.json();
        
        if (data.status === 'success' || data.status === 'partial') {
            showTransferResults(data.results);
        } else {
            throw new Error(data.message);
        }
        
    } catch (error) {
        console.error('❌ Erro ao transferir:', error);
        showToast('Erro ao transferir arquivos: ' + error.message, 'error');
    } finally {
        appState.isTransferring = false;
        
        // Limpar seleção e recarregar listas
        setTimeout(() => {
            appState.selectedGDriveFiles.clear();
            renderGoogleDriveFiles();
            loadAzureBlobs();
        }, 2000);
    }
}

/**
 * Deleta blobs selecionados
 */
async function deleteSelectedBlobs() {
    if (appState.selectedAzureBlobs.size === 0) {
        showToast('Selecione pelo menos um blob', 'warning');
        return;
    }
    
    if (!confirm(`Tem certeza que deseja deletar ${appState.selectedAzureBlobs.size} arquivo(s)?`)) {
        return;
    }
    
    const blobNames = Array.from(appState.selectedAzureBlobs);
    let deleteCount = 0;
    let errorCount = 0;
    
    for (const blobName of blobNames) {
        try {
            const response = await fetch(`${API_BASE}/delete-blob`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ blob_name: blobName })
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                deleteCount++;
                showToast(`Deletado: ${blobName}`, 'success');
            } else {
                errorCount++;
                showToast(`Erro ao deletar: ${blobName}`, 'error');
            }
        } catch (error) {
            errorCount++;
            showToast(`Erro ao deletar: ${blobName}`, 'error');
        }
    }
    
    appState.selectedAzureBlobs.clear();
    renderAzureBlobs();
    loadAzureBlobs();
    
    showToast(`Deletados: ${deleteCount}, Erros: ${errorCount}`, deleteCount > errorCount ? 'success' : 'error');
}

/**
 * Deleta um blob individual
 */
async function deleteBlob(blobName) {
    if (!confirm(`Deletar "${blobName}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/delete-blob`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ blob_name: blobName })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            showToast(`Deletado: ${blobName}`, 'success');
            loadAzureBlobs();
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        showToast(`Erro ao deletar: ${error.message}`, 'error');
    }
}

/**
 * Abre modal de transferência
 */
function openTransferModal() {
    const modal = document.getElementById('transfer-modal');
    modal.classList.add('active');
    
    const progress = document.getElementById('transfer-progress');
    const results = document.getElementById('transfer-results');
    progress.style.display = 'block';
    results.style.display = 'none';
    
    const fill = document.getElementById('progress-fill');
    const text = document.getElementById('progress-text');
    fill.style.width = '0%';
    text.textContent = 'Iniciando transferência...';
}

/**
 * Fecha modal de transferência
 */
function closeTransferModal() {
    const modal = document.getElementById('transfer-modal');
    modal.classList.remove('active');
}

/**
 * Mostra resultados de transferência
 */
function showTransferResults(results) {
    const progress = document.getElementById('transfer-progress');
    const resultsDiv = document.getElementById('transfer-results');
    const resultsList = document.getElementById('results-list');
    
    const total = results.total;
    const success = results.success.length;
    const failed = results.failed.length;
    
    // Atualizar barra de progresso
    const percentage = (success / total) * 100;
    document.getElementById('progress-fill').style.width = percentage + '%';
    
    // Atualizar resumo
    document.getElementById('result-total').textContent = total;
    document.getElementById('result-success').textContent = success;
    document.getElementById('result-failed').textContent = failed;
    
    // Listar resultados
    resultsList.innerHTML = '';
    
    results.success.forEach(file => {
        const item = document.createElement('div');
        item.className = 'result-item success';
        item.innerHTML = `
            <div class="result-item name">✅ ${escapeHtml(file.name)}</div>
            <div class="result-item message">${file.size_mb} MB enviado</div>
        `;
        resultsList.appendChild(item);
    });
    
    results.failed.forEach(file => {
        const item = document.createElement('div');
        item.className = 'result-item error';
        item.innerHTML = `
            <div class="result-item name">❌ ${escapeHtml(file.name)}</div>
            <div class="result-item message">${file.error}</div>
        `;
        resultsList.appendChild(item);
    });
    
    progress.style.display = 'none';
    resultsDiv.style.display = 'block';
    document.getElementById('close-modal-btn').style.display = 'block';
}

/**
 * Mostra notificação toast
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Escapa HTML
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Adicionar animação de slide out right ao CSS dinamicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
