/**
 * DouyinLiveRecorder WebUI - Modern JavaScript
 * 现代化的前端交互逻辑
 */

class DouyinWebUI {
    constructor() {
        this.currentSection = 'dashboard';
        this.autoRefreshInterval = null;
        this.isAutoRefreshing = false;
        this.apiBaseUrl = '';
        
        this.init();
    }

    init() {
        console.log('🚀 DouyinLiveRecorder WebUI 初始化中...');
        
        // 绑定事件监听器
        this.bindEventListeners();
        
        // 初始化数据
        this.loadDashboardData();
        
        // 设置定时刷新
        this.setupAutoRefresh();
        
        console.log('✅ WebUI 初始化完成');
    }

    bindEventListeners() {
        // 添加直播间表单
        const addRoomForm = document.getElementById('add-room-form');
        if (addRoomForm) {
            addRoomForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.addRoom();
            });
        }

        // 录制配置表单
        const recordingConfigForm = document.getElementById('recording-config-form');
        if (recordingConfigForm) {
            recordingConfigForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveRecordingConfig();
            });
        }

        // 推送配置表单
        const pushConfigForm = document.getElementById('push-config-form');
        if (pushConfigForm) {
            pushConfigForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.savePushConfig();
            });
        }

        // 键盘快捷键
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case '1':
                        e.preventDefault();
                        this.showSection('dashboard');
                        break;
                    case '2':
                        e.preventDefault();
                        this.showSection('rooms');
                        break;
                    case '3':
                        e.preventDefault();
                        this.showSection('config');
                        break;
                    case '4':
                        e.preventDefault();
                        this.showSection('files');
                        break;
                    case '5':
                        e.preventDefault();
                        this.showSection('logs');
                        break;
                    case 'r':
                        e.preventDefault();
                        this.refreshCurrentSection();
                        break;
                }
            }
        });
    }

    setupAutoRefresh() {
        // 每30秒自动刷新仪表板数据
        setInterval(() => {
            if (this.currentSection === 'dashboard') {
                this.loadDashboardData();
            }
        }, 30000);
    }

    // API 请求方法
    async apiRequest(endpoint, method = 'GET', data = null) {
        const url = `${this.apiBaseUrl}/api${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            this.showAlert('API请求失败: ' + error.message, 'danger');
            throw error;
        }
    }

    // 显示提示信息
    showAlert(message, type = 'info', duration = 5000) {
        const alertId = 'alert-' + Date.now();
        const alertHtml = `
            <div id="${alertId}" class="alert-glass alert-${type}-glass" style="position: fixed; top: 100px; right: 20px; z-index: 1050; min-width: 300px;">
                <div class="d-flex align-items-center">
                    <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
                    <span>${message}</span>
                    <button type="button" class="btn-close btn-close-white ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', alertHtml);
        
        // 自动移除
        if (duration > 0) {
            setTimeout(() => {
                const alert = document.getElementById(alertId);
                if (alert) {
                    alert.style.animation = 'fadeOut 0.3s ease-out';
                    setTimeout(() => alert.remove(), 300);
                }
            }, duration);
        }
    }

    getAlertIcon(type) {
        const icons = {
            success: 'check-circle',
            danger: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // 显示加载动画
    showLoading(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = '<div class="loading-spinner"></div>';
        }
    }

    // 切换主题
    toggleTheme() {
        const html = document.documentElement;
        const themeIcon = document.getElementById('theme-icon');
        
        if (html.getAttribute('data-bs-theme') === 'dark') {
            html.setAttribute('data-bs-theme', 'light');
            themeIcon.className = 'fas fa-moon';
            localStorage.setItem('theme', 'light');
        } else {
            html.setAttribute('data-bs-theme', 'dark');
            themeIcon.className = 'fas fa-sun';
            localStorage.setItem('theme', 'dark');
        }
    }

    // 切换侧边栏（移动端）
    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.toggle('show');
    }

    // 显示指定部分
    showSection(sectionName) {
        // 隐藏所有部分
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });

        // 显示指定部分
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.style.display = 'block';
        }

        // 更新导航状态
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.querySelector(`[data-section="${sectionName}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        this.currentSection = sectionName;

        // 加载对应数据
        switch (sectionName) {
            case 'dashboard':
                this.loadDashboardData();
                break;
            case 'rooms':
                this.loadRooms();
                break;
            case 'config':
                this.loadConfig();
                break;
            case 'files':
                this.loadFiles();
                break;
            case 'logs':
                this.loadLogs();
                break;
        }

        // 移动端自动关闭侧边栏
        if (window.innerWidth < 768) {
            this.toggleSidebar();
        }
    }

    // 刷新当前部分
    refreshCurrentSection() {
        this.showSection(this.currentSection);
    }

    // 仪表板相关方法
    async loadDashboardData() {
        try {
            const [statusData, roomsData, filesData] = await Promise.all([
                this.apiRequest('/status'),
                this.apiRequest('/rooms'),
                this.apiRequest('/files')
            ]);

            this.updateDashboardStats(statusData, roomsData, filesData);
            this.updateRecordingActivity(roomsData.rooms);
        } catch (error) {
            console.error('加载仪表板数据失败:', error);
        }
    }

    updateDashboardStats(status, rooms, files) {
        document.getElementById('total-rooms').textContent = rooms.rooms.length;
        document.getElementById('recording-count').textContent = 
            rooms.rooms.filter(room => room.recording).length;
        document.getElementById('monitoring-status').textContent = 
            status.monitoring ? '运行中' : '已停止';
        document.getElementById('total-files').textContent = files.files ? files.files.length : 0;

        // 更新监控状态样式
        const statusElement = document.getElementById('monitoring-status');
        statusElement.className = status.monitoring ? 'text-success' : 'text-warning';
    }

    updateRecordingActivity(rooms) {
        const container = document.getElementById('recording-activity');
        const recordingRooms = rooms.filter(room => room.recording);

        if (recordingRooms.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-play-circle fa-3x text-white-50 mb-3"></i>
                    <p class="text-white-50">暂无录制活动</p>
                </div>
            `;
        } else {
            const activityHtml = recordingRooms.map(room => `
                <div class="d-flex justify-content-between align-items-center p-3 mb-2" 
                     style="background: rgba(255, 255, 255, 0.1); border-radius: 12px;">
                    <div>
                        <h6 class="text-white mb-1">${room.name || '未命名直播间'}</h6>
                        <small class="text-white-50">${room.url}</small>
                    </div>
                    <div class="text-end">
                        <span class="status-badge status-recording">录制中</span>
                        <br>
                        <small class="text-white-50">${room.start_time ? new Date(room.start_time).toLocaleTimeString() : ''}</small>
                    </div>
                </div>
            `).join('');

            container.innerHTML = activityHtml;
        }
    }

    // 监控控制
    async startMonitoring() {
        try {
            await this.apiRequest('/start-monitoring', 'POST');
            this.showAlert('监控已启动', 'success');
            this.loadDashboardData();
        } catch (error) {
            this.showAlert('启动监控失败', 'danger');
        }
    }

    async stopMonitoring() {
        try {
            await this.apiRequest('/stop-monitoring', 'POST');
            this.showAlert('监控已停止', 'success');
            this.loadDashboardData();
        } catch (error) {
            this.showAlert('停止监控失败', 'danger');
        }
    }

    // 直播间管理
    async loadRooms() {
        this.showLoading('rooms-list');
        
        try {
            const data = await this.apiRequest('/rooms');
            this.renderRoomsList(data.rooms);
        } catch (error) {
            document.getElementById('rooms-list').innerHTML = 
                '<p class="text-white-50 text-center">加载直播间列表失败</p>';
        }
    }

    renderRoomsList(rooms) {
        const container = document.getElementById('rooms-list');
        
        if (rooms.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-broadcast-tower fa-3x text-white-50 mb-3"></i>
                    <p class="text-white-50">暂无直播间，请添加直播间开始监控</p>
                </div>
            `;
            return;
        }

        const roomsHtml = rooms.map(room => `
            <div class="room-card">
                <div class="room-header">
                    <div>
                        <h6 class="room-title">${room.name || '未命名直播间'}</h6>
                        <p class="room-url">${room.url}</p>
                        <div class="d-flex gap-2 align-items-center">
                            <span class="badge bg-secondary">${room.quality}</span>
                            <span class="status-badge ${room.recording ? 'status-recording' : 'status-offline'}">
                                ${room.recording ? '录制中' : '离线'}
                            </span>
                        </div>
                    </div>
                    <div class="d-flex flex-column gap-2">
                        ${room.recording ? 
                            `<button class="btn btn-danger-glass btn-sm" onclick="webui.stopRecording('${room.url}')">
                                <i class="fas fa-stop me-1"></i>停止
                            </button>` :
                            `<button class="btn btn-success-glass btn-sm" onclick="webui.startRecording('${room.url}')">
                                <i class="fas fa-play me-1"></i>开始
                            </button>`
                        }
                        <button class="btn btn-glass btn-sm" onclick="webui.editRoom('${room.url}')">
                            <i class="fas fa-edit me-1"></i>编辑
                        </button>
                        <button class="btn btn-danger-glass btn-sm" onclick="webui.deleteRoom('${room.url}')">
                            <i class="fas fa-trash me-1"></i>删除
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = roomsHtml;
    }

    async addRoom() {
        const url = document.getElementById('room-url').value.trim();
        const quality = document.getElementById('room-quality').value;
        const name = document.getElementById('room-name').value.trim();

        if (!url) {
            this.showAlert('请输入直播间地址', 'warning');
            return;
        }

        try {
            await this.apiRequest('/rooms', 'POST', {
                url: url,
                quality: quality,
                name: name
            });

            this.showAlert('直播间添加成功', 'success');
            
            // 清空表单
            document.getElementById('add-room-form').reset();
            
            // 刷新列表
            this.loadRooms();
        } catch (error) {
            this.showAlert('添加直播间失败', 'danger');
        }
    }

    async startRecording(url) {
        try {
            await this.apiRequest(`/rooms/${encodeURIComponent(url)}/start`, 'POST');
            this.showAlert('录制已启动', 'success');
            this.loadRooms();
        } catch (error) {
            this.showAlert('启动录制失败', 'danger');
        }
    }

    async stopRecording(url) {
        try {
            await this.apiRequest(`/rooms/${encodeURIComponent(url)}/stop`, 'POST');
            this.showAlert('录制已停止', 'success');
            this.loadRooms();
        } catch (error) {
            this.showAlert('停止录制失败', 'danger');
        }
    }

    async deleteRoom(url) {
        if (!confirm('确定要删除这个直播间吗？')) {
            return;
        }

        try {
            await this.apiRequest(`/rooms/${encodeURIComponent(url)}`, 'DELETE');
            this.showAlert('直播间已删除', 'success');
            this.loadRooms();
        } catch (error) {
            this.showAlert('删除直播间失败', 'danger');
        }
    }

    refreshRooms() {
        this.loadRooms();
    }

    // 配置管理
    async loadConfig() {
        try {
            const config = await this.apiRequest('/config');
            this.populateConfigForms(config);
        } catch (error) {
            this.showAlert('加载配置失败', 'danger');
        }
    }

    populateConfigForms(config) {
        // 填充录制设置表单
        if (config['录制设置']) {
            const recordingForm = document.getElementById('recording-config-form');
            const formData = new FormData(recordingForm);
            
            for (const [key, value] of Object.entries(config['录制设置'])) {
                const input = recordingForm.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = value;
                }
            }
        }

        // 填充推送设置表单
        if (config['录制设置']) {
            const pushForm = document.getElementById('push-config-form');
            const enablePush = pushForm.querySelector('#enable-push');
            if (enablePush) {
                enablePush.checked = config['录制设置']['开启推送'] === '是';
            }
        }
    }

    async saveRecordingConfig() {
        const form = document.getElementById('recording-config-form');
        const formData = new FormData(form);

        try {
            for (const [key, value] of formData.entries()) {
                await this.apiRequest('/config', 'PUT', {
                    section: '录制设置',
                    key: key,
                    value: value
                });
            }

            this.showAlert('录制配置已保存', 'success');
        } catch (error) {
            this.showAlert('保存配置失败', 'danger');
        }
    }

    async savePushConfig() {
        const form = document.getElementById('push-config-form');
        const formData = new FormData(form);

        try {
            for (const [key, value] of formData.entries()) {
                if (key === '开启推送') {
                    continue; // 复选框单独处理
                }
                await this.apiRequest('/config', 'PUT', {
                    section: '录制设置',
                    key: key,
                    value: value
                });
            }

            // 处理开启推送复选框
            const enablePush = form.querySelector('#enable-push').checked;
            await this.apiRequest('/config', 'PUT', {
                section: '录制设置',
                key: '开启推送',
                value: enablePush ? '是' : '否'
            });

            this.showAlert('推送配置已保存', 'success');
        } catch (error) {
            this.showAlert('保存配置失败', 'danger');
        }
    }

    // 文件管理
    async loadFiles() {
        this.showLoading('files-list');
        
        try {
            const data = await this.apiRequest('/files');
            this.renderFilesList(data.files || []);
        } catch (error) {
            document.getElementById('files-list').innerHTML = 
                '<p class="text-white-50 text-center">加载文件列表失败</p>';
        }
    }

    renderFilesList(files) {
        const container = document.getElementById('files-list');
        
        if (files.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-file-video fa-3x text-white-50 mb-3"></i>
                    <p class="text-white-50">暂无录制文件</p>
                </div>
            `;
            return;
        }

        const filesHtml = files.map(file => `
            <div class="d-flex justify-content-between align-items-center p-3 mb-2" 
                 style="background: rgba(255, 255, 255, 0.1); border-radius: 12px;">
                <div class="d-flex align-items-center">
                    <i class="fas fa-file-video text-primary me-3 fa-2x"></i>
                    <div>
                        <h6 class="text-white mb-1">${file.name}</h6>
                        <small class="text-white-50">
                            大小: ${this.formatFileSize(file.size)} | 
                            修改时间: ${new Date(file.modified).toLocaleString()}
                        </small>
                    </div>
                </div>
                <div class="d-flex gap-2">
                    <button class="btn btn-glass btn-sm" onclick="webui.downloadFile('${file.path}')">
                        <i class="fas fa-download me-1"></i>下载
                    </button>
                    <button class="btn btn-danger-glass btn-sm" onclick="webui.deleteFile('${file.path}')">
                        <i class="fas fa-trash me-1"></i>删除
                    </button>
                </div>
            </div>
        `).join('');

        container.innerHTML = filesHtml;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async downloadFile(filePath) {
        try {
            window.open(`/api/files/${encodeURIComponent(filePath)}`, '_blank');
        } catch (error) {
            this.showAlert('下载文件失败', 'danger');
        }
    }

    async deleteFile(filePath) {
        if (!confirm('确定要删除这个文件吗？')) {
            return;
        }

        try {
            await this.apiRequest(`/files/${encodeURIComponent(filePath)}`, 'DELETE');
            this.showAlert('文件已删除', 'success');
            this.loadFiles();
        } catch (error) {
            this.showAlert('删除文件失败', 'danger');
        }
    }

    refreshFiles() {
        this.loadFiles();
    }

    openDownloadsFolder() {
        // 这个功能需要后端支持
        this.showAlert('请手动打开 downloads 文件夹', 'info');
    }

    // 日志管理
    async loadLogs() {
        try {
            const data = await this.apiRequest('/logs');
            document.getElementById('logs-content').textContent = data.logs || '暂无日志';
        } catch (error) {
            document.getElementById('logs-content').textContent = '加载日志失败';
        }
    }

    refreshLogs() {
        this.loadLogs();
    }

    clearLogs() {
        if (!confirm('确定要清空日志吗？')) {
            return;
        }
        
        document.getElementById('logs-content').textContent = '日志已清空';
        this.showAlert('日志已清空', 'success');
    }

    toggleAutoRefresh() {
        const button = document.querySelector('[onclick="toggleAutoRefresh()"]');
        const text = document.getElementById('auto-refresh-text');
        
        if (this.isAutoRefreshing) {
            clearInterval(this.autoRefreshInterval);
            this.isAutoRefreshing = false;
            button.innerHTML = '<i class="fas fa-play me-2"></i><span id="auto-refresh-text">自动刷新</span>';
            this.showAlert('自动刷新已停止', 'info');
        } else {
            this.autoRefreshInterval = setInterval(() => {
                if (this.currentSection === 'logs') {
                    this.loadLogs();
                }
            }, 5000);
            this.isAutoRefreshing = true;
            button.innerHTML = '<i class="fas fa-pause me-2"></i><span id="auto-refresh-text">停止刷新</span>';
            this.showAlert('自动刷新已启动', 'info');
        }
    }

    // 通用刷新方法
    refreshData() {
        this.refreshCurrentSection();
    }
}

// 全局实例
const webui = new DouyinWebUI();

// 全局函数（保持向后兼容）
function showSection(section) {
    webui.showSection(section);
}

function toggleSidebar() {
    webui.toggleSidebar();
}

function toggleTheme() {
    webui.toggleTheme();
}

function startMonitoring() {
    webui.startMonitoring();
}

function stopMonitoring() {
    webui.stopMonitoring();
}

function refreshData() {
    webui.refreshData();
}

function refreshRooms() {
    webui.refreshRooms();
}

function refreshFiles() {
    webui.refreshFiles();
}

function refreshLogs() {
    webui.refreshLogs();
}

function clearLogs() {
    webui.clearLogs();
}

function toggleAutoRefresh() {
    webui.toggleAutoRefresh();
}

function openDownloadsFolder() {
    webui.openDownloadsFolder();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 恢复主题设置
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
        const themeIcon = document.getElementById('theme-icon');
        if (themeIcon) {
            themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
    
    console.log('🎉 DouyinLiveRecorder WebUI 已就绪！');
}); 