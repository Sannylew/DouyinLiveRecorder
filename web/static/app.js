// Global variables
let updateInterval;
let startTime = Date.now();

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    refreshStatus();
    startUpdateTimer();
    loadRooms();
});

// Timer functions
function startUpdateTimer() {
    updateInterval = setInterval(() => {
        updateUptime();
        refreshStatus();
    }, 5000); // Update every 5 seconds
}

function updateUptime() {
    const now = Date.now();
    const uptime = Math.floor((now - startTime) / 1000);
    const hours = Math.floor(uptime / 3600).toString().padStart(2, '0');
    const minutes = Math.floor((uptime % 3600) / 60).toString().padStart(2, '0');
    const seconds = (uptime % 60).toString().padStart(2, '0');
    document.getElementById('uptime').textContent = `${hours}:${minutes}:${seconds}`;
}

// Section navigation
function showSection(section) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.style.display = 'none';
    });
    
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(section + '-section').style.display = 'block';
    
    // Add active class to clicked nav link
    event.target.classList.add('active');
    
    // Load section-specific data
    switch(section) {
        case 'dashboard':
            refreshStatus();
            break;
        case 'rooms':
            loadRooms();
            break;
        case 'config':
            loadConfig();
            break;
        case 'files':
            loadFiles();
            break;
        case 'logs':
            loadLogs();
            break;
    }
}

// API functions
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showToast('API请求失败: ' + error.message, 'error');
        throw error;
    }
}

// Status functions
async function refreshStatus() {
    try {
        const status = await apiCall('/api/status');
        
        document.getElementById('total-rooms').textContent = status.total_rooms;
        document.getElementById('recording-count').textContent = status.recording_count;
        
        const monitoringStatusEl = document.getElementById('monitoring-status');
        if (status.monitoring) {
            monitoringStatusEl.textContent = '运行中';
            monitoringStatusEl.className = 'text-success';
        } else {
            monitoringStatusEl.textContent = '已停止';
            monitoringStatusEl.className = 'text-danger';
        }
        
        // Update recording rooms display
        displayRecordingRooms(status.recording_rooms);
        
    } catch (error) {
        console.error('Failed to refresh status:', error);
    }
}

function displayRecordingRooms(recordingRooms) {
    const container = document.getElementById('recording-rooms');
    
    if (recordingRooms.length === 0) {
        container.innerHTML = '<div class="col-12"><p class="text-muted">当前没有正在录制的直播间</p></div>';
        return;
    }
    
    container.innerHTML = recordingRooms.map(url => `
        <div class="col-md-6 col-lg-4 mb-3">
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title text-truncate">${url}</h6>
                    <span class="recording-badge">
                        <i class="fas fa-circle me-1"></i>录制中
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

// Monitoring control functions
async function startMonitoring() {
    try {
        await apiCall('/api/start-monitoring', { method: 'POST' });
        showToast('监控已启动', 'success');
        refreshStatus();
    } catch (error) {
        showToast('启动监控失败', 'error');
    }
}

async function stopMonitoring() {
    try {
        await apiCall('/api/stop-monitoring', { method: 'POST' });
        showToast('监控已停止', 'success');
        refreshStatus();
    } catch (error) {
        showToast('停止监控失败', 'error');
    }
}

// Room management functions
async function loadRooms() {
    try {
        const data = await apiCall('/api/rooms');
        displayRooms(data.rooms);
    } catch (error) {
        console.error('Failed to load rooms:', error);
    }
}

function displayRooms(rooms) {
    const container = document.getElementById('rooms-list');
    
    if (rooms.length === 0) {
        container.innerHTML = '<div class="alert alert-info">还没有配置任何直播间，点击上方按钮添加第一个直播间吧！</div>';
        return;
    }
    
    container.innerHTML = rooms.map(room => `
        <div class="room-card">
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <h5 class="mb-2">
                        ${room.name || '未命名直播间'}
                        ${room.recording ? 
                            '<span class="recording-badge ms-2"><i class="fas fa-circle me-1"></i>录制中</span>' : 
                            '<span class="offline-badge ms-2">离线</span>'
                        }
                    </h5>
                    <p class="text-muted mb-2">${room.url}</p>
                    <div class="d-flex gap-2">
                        <span class="badge bg-secondary">${room.quality}</span>
                        <span class="badge ${room.enabled ? 'bg-success' : 'bg-warning'}">
                            ${room.enabled ? '已启用' : '已禁用'}
                        </span>
                    </div>
                </div>
                <div class="dropdown">
                    <button class="btn btn-outline-secondary btn-sm" type="button" data-bs-toggle="dropdown">
                        <i class="fas fa-ellipsis-v"></i>
                    </button>
                    <ul class="dropdown-menu">
                        <li>
                            <a class="dropdown-item" href="#" onclick="toggleRoom('${room.url}', ${!room.enabled})">
                                <i class="fas fa-${room.enabled ? 'pause' : 'play'} me-2"></i>
                                ${room.enabled ? '禁用' : '启用'}
                            </a>
                        </li>
                        ${room.recording ? 
                            `<li><a class="dropdown-item" href="#" onclick="stopRecording('${room.url}')">
                                <i class="fas fa-stop me-2"></i>停止录制
                            </a></li>` : 
                            `<li><a class="dropdown-item" href="#" onclick="startRecording('${room.url}')">
                                <i class="fas fa-play me-2"></i>开始录制
                            </a></li>`
                        }
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item text-danger" href="#" onclick="deleteRoom('${room.url}')">
                                <i class="fas fa-trash me-2"></i>删除
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    `).join('');
}

async function addRoom() {
    const url = document.getElementById('roomUrl').value;
    const quality = document.getElementById('roomQuality').value;
    const name = document.getElementById('roomName').value;
    
    if (!url) {
        showToast('请输入直播间地址', 'error');
        return;
    }
    
    try {
        await apiCall('/api/rooms', {
            method: 'POST',
            body: JSON.stringify({ url, quality, name })
        });
        
        showToast('直播间添加成功', 'success');
        
        // Close modal and refresh rooms
        const modal = bootstrap.Modal.getInstance(document.getElementById('addRoomModal'));
        modal.hide();
        
        // Clear form
        document.getElementById('addRoomForm').reset();
        
        loadRooms();
    } catch (error) {
        showToast('添加直播间失败', 'error');
    }
}

async function deleteRoom(url) {
    if (!confirm('确定要删除这个直播间吗？')) {
        return;
    }
    
    try {
        await apiCall(`/api/rooms/${encodeURIComponent(url)}`, { method: 'DELETE' });
        showToast('直播间删除成功', 'success');
        loadRooms();
    } catch (error) {
        showToast('删除直播间失败', 'error');
    }
}

async function toggleRoom(url, enabled) {
    try {
        await apiCall(`/api/rooms/${encodeURIComponent(url)}`, {
            method: 'PUT',
            body: JSON.stringify({ url, enabled })
        });
        
        showToast(`直播间${enabled ? '启用' : '禁用'}成功`, 'success');
        loadRooms();
    } catch (error) {
        showToast('操作失败', 'error');
    }
}

async function startRecording(url) {
    try {
        await apiCall(`/api/rooms/${encodeURIComponent(url)}/start`, { method: 'POST' });
        showToast('开始录制', 'success');
        loadRooms();
    } catch (error) {
        showToast('启动录制失败', 'error');
    }
}

async function stopRecording(url) {
    try {
        await apiCall(`/api/rooms/${encodeURIComponent(url)}/stop`, { method: 'POST' });
        showToast('停止录制', 'success');
        loadRooms();
    } catch (error) {
        showToast('停止录制失败', 'error');
    }
}

// Configuration functions
async function loadConfig() {
    try {
        const config = await apiCall('/api/config');
        displayConfig(config);
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

function displayConfig(config) {
    const container = document.getElementById('config-content');
    
    let html = '';
    
    for (const [section, settings] of Object.entries(config)) {
        html += `
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">${section}</h5>
                </div>
                <div class="card-body">
                    <div class="row">
        `;
        
        for (const [key, value] of Object.entries(settings)) {
            html += `
                <div class="col-md-6 mb-3">
                    <label class="form-label">${key}</label>
                    <input type="text" class="form-control" 
                           value="${value}" 
                           onchange="updateConfig('${section}', '${key}', this.value)">
                </div>
            `;
        }
        
        html += `
                    </div>
                </div>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

async function updateConfig(section, key, value) {
    try {
        await apiCall('/api/config', {
            method: 'PUT',
            body: JSON.stringify({ section, key, value })
        });
        showToast('配置更新成功', 'success');
    } catch (error) {
        showToast('配置更新失败', 'error');
    }
}

// Files functions
async function loadFiles() {
    try {
        const data = await apiCall('/api/files');
        displayFiles(data.files);
    } catch (error) {
        console.error('Failed to load files:', error);
    }
}

function displayFiles(files) {
    const container = document.getElementById('files-list');
    
    if (files.length === 0) {
        container.innerHTML = '<div class="alert alert-info">还没有录制任何文件</div>';
        return;
    }
    
    const html = `
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>文件名</th>
                        <th>大小</th>
                        <th>修改时间</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    ${files.map(file => `
                        <tr>
                            <td>${file.name}</td>
                            <td>${formatFileSize(file.size)}</td>
                            <td>${new Date(file.modified * 1000).toLocaleString()}</td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary" onclick="downloadFile('${file.path}')">
                                    <i class="fas fa-download"></i> 下载
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function downloadFile(path) {
    window.open(`/api/files/${encodeURIComponent(path)}`, '_blank');
}

// Logs functions
async function loadLogs() {
    try {
        const data = await apiCall('/api/logs');
        document.getElementById('logs-content').textContent = data.logs.join('\n');
    } catch (error) {
        console.error('Failed to load logs:', error);
        document.getElementById('logs-content').textContent = '加载日志失败';
    }
}

// Utility functions
function showToast(message, type = 'info') {
    // Create toast element
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Add to toast container
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    container.insertAdjacentHTML('beforeend', toastHtml);
    
    // Show toast
    const toastElement = container.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove after hiding
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
} 