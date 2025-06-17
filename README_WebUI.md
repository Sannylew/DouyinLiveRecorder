# 🌟 DouyinLiveRecorder WebUI 版本

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple.svg)](https://getbootstrap.com/)

> 现代化的Web管理界面，让直播录制变得简单优雅

## 🚀 推荐安装方式：源码安装

### ✨ **为什么选择源码安装？**

- **🔧 灵活定制** - 可根据需求修改功能
- **🐛 问题排查** - 便于调试和问题定位  
- **📈 功能扩展** - 支持二次开发和功能增强
- **🔄 版本控制** - 通过Git获取最新功能
- **💡 学习研究** - 理解工作原理，便于优化
- **🚀 性能优化** - 可针对环境进行个性化配置

### 📦 **快速开始**

```bash
# 1. 获取最新源码
git clone https://github.com/Sannylew/DouyinLiveRecorder.git
cd DouyinLiveRecorder

# 2. 创建虚拟环境（避免系统环境冲突）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements_webui.txt

# 4. 启动WebUI
python start_webui.py

# 5. 浏览器访问
# http://localhost:8000
```

🎉 **就是这么简单！** 几条命令即可拥有现代化的直播录制管理界面。

**💡 小贴士**: 使用虚拟环境可以避免在新系统中遇到"externally-managed-environment"错误。

---

## 📊 **界面预览**

### 🏠 **仪表盘**
- 实时系统状态监控
- 录制任务统计
- 平台分布图表
- 最近录制文件

### 📺 **直播间管理**  
- 可视化添加/删除直播间
- 批量启用/禁用
- 实时状态显示
- 一键开始/停止录制

### ⚙️ **配置管理**
- 在线编辑配置文件
- 实时保存生效  
- 配置验证提示
- 恢复默认设置

### 📁 **文件管理**
- 录制文件浏览
- 在线播放预览
- 批量下载
- 存储空间统计

### 📋 **日志查看**
- 实时日志流
- 日志级别过滤
- 搜索和导出
- 系统运行状态

---

## 🔧 **详细安装指南**

### 🌍 **环境要求**

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| **Python** | 3.10+ | 推荐 3.11，支持异步特性 |
| **系统** | Windows 10+<br>Ubuntu 18.04+<br>CentOS 7+<br>macOS 10.15+ | 跨平台支持 |
| **内存** | 512MB+ | WebUI需要额外内存 |
| **存储** | 1GB+ | 录制文件和日志存储 |
| **网络** | 10Mbps+ | 直播流下载和Web访问 |

### 📋 **安装步骤详解**

#### **步骤1: 环境准备**

**检查Python版本**:
```bash
python --version  # 应该显示 3.10 或更高版本
# 如果版本过低，请到 https://www.python.org 下载最新版本
```

**检查pip和git**:
```bash
pip --version
git --version
```

#### **步骤2: 获取源码**

**方式1: Git克隆（推荐）**
```bash
git clone https://github.com/Sannylew/DouyinLiveRecorder.git
cd DouyinLiveRecorder

# 切换到最新开发分支（可选）
git checkout dev
```

**方式2: 直接下载**
```bash
# 访问以下链接下载ZIP文件
# https://github.com/Sannylew/DouyinLiveRecorder/archive/main.zip
wget https://github.com/Sannylew/DouyinLiveRecorder/archive/main.zip
unzip main.zip
cd DouyinLiveRecorder-main
```

#### **步骤3: 安装依赖**

**推荐：使用虚拟环境**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装WebUI依赖
pip install -r requirements_webui.txt
```

**国内网络优化**:
```bash
# 使用国内镜像源加速安装
pip install -r requirements_webui.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### **步骤4: FFmpeg安装**

**自动安装（Windows）**:
```bash
python ffmpeg_install.py
```

**手动安装**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg

# macOS
brew install ffmpeg

# 验证安装
ffmpeg -version
```

#### **步骤5: 初始配置**

```bash
# 创建配置目录（如果不存在）
mkdir -p config

# 启动程序（会自动创建默认配置）
python start_webui.py
```

### 🎯 **高级配置选项**

#### **自定义端口**
```bash
# 方式1: 命令行参数
python start_webui.py --port 8080

# 方式2: 环境变量
export PORT=8080
python start_webui.py

# 方式3: 修改start_webui.py
# 找到 DEFAULT_PORT = 8000，修改为所需端口
```

#### **外网访问配置**
```bash
# 绑定所有网络接口
python start_webui.py --host 0.0.0.0 --port 8000

# 设置nginx反向代理（推荐生产环境）
cp nginx.conf /etc/nginx/sites-available/douyin-webui
sudo nginx -s reload
```

#### **开机自启动**
```bash
# Linux系统服务
sudo cp systemd/douyin-webui.service /etc/systemd/system/
sudo systemctl enable douyin-webui
sudo systemctl start douyin-webui

# Windows计划任务
# 使用任务计划程序创建开机启动任务
```

---

## 🎯 WebUI 特性

### ✨ 核心功能
- 🖥️ **现代化Web界面** - 基于Bootstrap的响应式设计，支持移动端访问
- 📊 **实时监控面板** - 显示录制状态、监控数量等统计信息
- 🎮 **直播间管理** - 可视化添加、编辑、删除直播间
- ⚙️ **配置管理** - 通过Web界面修改所有配置项
- 📁 **文件管理** - 查看、下载录制的视频文件
- 📝 **日志查看** - 实时查看系统运行日志
- 🔔 **状态通知** - 支持多种推送方式的开播/关播通知
- 🌐 **远程访问** - 支持局域网和公网访问

### 🛠️ 技术架构
- **后端**: FastAPI + 异步编程
- **前端**: Bootstrap 5 + Vanilla JavaScript
- **录制引擎**: 保持原项目的完整录制逻辑
- **多线程**: 后台监控 + Web服务并行运行
- **部署**: 专为Linux服务器优化

## 📦 安装和部署

### 方法1: 快速部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/Sannylew/DouyinLiveRecorder.git
cd DouyinLiveRecorder

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements_webui.txt

# 4. 启动WebUI
python start_webui.py
```

### 方法2: 生产环境部署

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements_webui.txt

# 3. 直接启动
python app.py
```

### 方法3: 后台运行（服务器推荐）

```bash
# 使用 nohup 后台运行
nohup python app.py > webui.log 2>&1 &

# 或使用 screen
screen -S douyin-webui
python app.py
# Ctrl+A+D 分离会话

# 或使用 systemd 服务（推荐生产环境）
sudo systemctl start douyin-webui
sudo systemctl enable douyin-webui
```

## 🌐 网络访问配置

### 本地访问
```
http://localhost:8000
```

### 局域网访问
修改 `app.py` 中的host配置：
```python
uvicorn.run(
    "app:app",
    host="0.0.0.0",  # 允许外部访问
    port=8000,
    reload=False,
    access_log=True
)
```

### 公网访问（需要配置防火墙）
```bash
# 开放端口 8000
sudo ufw allow 8000
# 或
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

## 🐳 Docker 部署

### 快速启动
```bash
# 构建镜像
docker build -t douyin-webui .

# 运行容器
docker run -d \
  --name douyin-recorder \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/downloads:/app/downloads \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  douyin-webui
```

### Docker Compose（推荐）
```yaml
version: '3.8'
services:
  douyin-webui:
    build: .
    container_name: douyin-recorder
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./downloads:/app/downloads
      - ./logs:/app/logs
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
```

## 🔧 系统服务配置

### 创建 systemd 服务文件
```bash
sudo nano /etc/systemd/system/douyin-webui.service
```

```ini
[Unit]
Description=DouyinLiveRecorder WebUI
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/DouyinLiveRecorder
ExecStart=/path/to/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 启动和管理服务
```bash
# 重载服务配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start douyin-webui

# 开机自启
sudo systemctl enable douyin-webui

# 查看状态
sudo systemctl status douyin-webui

# 查看日志
sudo journalctl -u douyin-webui -f
```

## 🎮 使用说明

### 1. 仪表盘
- 查看系统总体运行状态
- 监控直播间数量和录制状态
- 启动/停止监控服务
- 查看正在录制的直播间

### 2. 直播间管理
- **添加直播间**: 点击"添加直播间"按钮，输入URL、选择画质、设置备注
- **管理直播间**: 启用/禁用、手动开始/停止录制、删除直播间
- **批量操作**: 支持批量启用/禁用直播间

### 3. 配置设置
- **录制设置**: 修改视频格式、画质、保存路径等
- **推送配置**: 设置微信、钉钉、邮箱等通知方式
- **Cookie配置**: 设置各平台的登录凭据

### 4. 文件管理
- 查看所有录制的视频文件
- 显示文件大小、修改时间
- 支持直接下载文件

### 5. 日志查看
- 实时查看系统运行日志
- 监控录制状态和错误信息

## 🔧 配置说明

### 支持的直播平台
与原项目相同，支持40+个直播平台：
- 国内：抖音、快手、虎牙、斗鱼、B站、小红书等
- 海外：TikTok、YouTube、Twitch、Shopee等

### 录制配置
所有原项目的配置都可以通过Web界面进行设置：
- 视频格式：TS、MP4、FLV、MKV等
- 录制画质：原画、超清、高清、标清、流畅
- 保存路径：支持按作者、时间、平台分类
- 代理设置：支持海外平台代理录制

### 推送通知
支持多种推送方式：
- 微信推送
- 钉钉推送
- Telegram Bot
- 邮箱通知
- Bark推送
- Ntfy推送

## 🌐 API接口

WebUI提供了完整的RESTful API接口：

### 直播间管理
- `GET /api/rooms` - 获取直播间列表
- `POST /api/rooms` - 添加直播间
- `PUT /api/rooms/{url}` - 更新直播间
- `DELETE /api/rooms/{url}` - 删除直播间

### 录制控制
- `POST /api/rooms/{url}/start` - 手动开始录制
- `POST /api/rooms/{url}/stop` - 手动停止录制
- `POST /api/start-monitoring` - 启动监控
- `POST /api/stop-monitoring` - 停止监控

### 系统管理
- `GET /api/status` - 获取系统状态
- `GET /api/config` - 获取配置
- `PUT /api/config` - 更新配置
- `GET /api/files` - 获取文件列表
- `GET /api/logs` - 获取日志

## 🔄 与原版差异

### 运行方式改变
- **原版**: 命令行 + 配置文件驱动
- **WebUI版**: Web服务 + 可视化界面操作

### 新增功能
- 🖥️ 现代化Web界面
- 📊 实时状态监控
- 🎮 可视化操作
- 📱 响应式设计（支持手机访问）
- 🌐 远程管理能力

### 保持兼容
- ✅ 完全兼容原配置文件
- ✅ 保持原有录制逻辑
- ✅ 支持所有原有平台
- ✅ 保持文件保存格式

## 🚀 性能优化

### 服务器资源优化
- **异步处理**: 使用asyncio提高并发性能
- **资源管理**: 合理的线程和进程管理
- **内存优化**: 避免内存泄漏
- **网络优化**: 支持HTTP/2和连接池

### 生产环境建议
- 使用反向代理（Nginx）
- 配置SSL证书（HTTPS）
- 设置日志轮转
- 监控资源使用情况

## 🔒 安全配置

### 基础安全
```bash
# 1. 修改默认端口
# 在 app.py 中修改 port=8000 为其他端口

# 2. 配置防火墙
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 8000/tcp

# 3. 限制访问IP（可选）
# 在Nginx中配置IP白名单
```

### Nginx 反向代理配置
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🛠️ 开发说明

### 项目结构
```
DouyinLiveRecorder/
├── app.py                 # FastAPI主应用
├── recording_service.py   # 录制服务封装
├── start_webui.py         # 启动脚本
├── web/                   # Web界面
│   ├── index.html        # 主页面
│   └── static/
│       └── app.js        # 前端逻辑
├── src/                   # 原项目核心模块
├── config/                # 配置文件
├── downloads/             # 录制文件保存
└── logs/                  # 日志文件
```

### 扩展开发
如需添加新功能：
1. 在 `recording_service.py` 中添加业务逻辑
2. 在 `app.py` 中添加API接口
3. 在 `web/static/app.js` 中添加前端交互
4. 在 `web/index.html` 中添加界面元素

## 📊 监控和维护

### 日志管理
```bash
# 查看实时日志
tail -f logs/app.log

# 查看WebUI访问日志
tail -f webui.log

# 日志轮转配置
sudo nano /etc/logrotate.d/douyin-webui
```

### 性能监控
```bash
# 查看进程状态
ps aux | grep python

# 查看端口占用
netstat -tlnp | grep 8000

# 查看系统资源
htop
```

## ❓ 常见问题

### Q: 如何在服务器上远程访问WebUI？
A: 修改`app.py`中的host为"0.0.0.0"，并开放防火墙端口8000。

### Q: 如何设置开机自启动？
A: 使用systemd服务，参考上面的系统服务配置章节。

### Q: 如何备份配置和录制文件？
A: 备份`config/`目录和`downloads/`目录即可。

### Q: 服务器重启后如何自动恢复录制？
A: 配置systemd服务并启用开机自启，WebUI会自动恢复之前的监控状态。

### Q: 如何升级到最新版本？
A: 
```bash
git pull origin main
pip install -r requirements_webui.txt --upgrade
sudo systemctl restart douyin-webui
```

## 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

### 完整许可证文本

```
MIT License

Copyright (c) 2024 DouyinLiveRecorder Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 如何贡献
1. Fork 这个项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 贡献指南
- 遵循现有代码风格
- 添加适当的测试
- 更新相关文档
- 确保所有测试通过

## 💖 致谢

### 原始项目
- **[ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** - 感谢原作者提供的强大直播录制引擎
- 本WebUI版本完全基于原项目开发，在保持原有核心功能的基础上增加了Web管理界面

### 技术依赖
- **[FastAPI](https://fastapi.tiangolo.com/)** - 现代化、快速的Web框架
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器实现
- **[Bootstrap](https://getbootstrap.com/)** - 响应式前端UI框架
- **[FFmpeg](https://ffmpeg.org/)** - 强大的多媒体处理工具
- **[Python](https://www.python.org/)** - 优秀的编程语言和生态系统

### 开源社区
感谢所有开源项目的贡献者，是你们让这个项目得以存在！

## 📝 项目声明

### 🎯 项目定位
- **功能扩展**: 本项目是原 DouyinLiveRecorder 的 WebUI 扩展版本
- **核心保持**: 完全保留原项目的录制引擎和核心功能
- **界面增强**: 新增现代化的Web管理界面，提供更好的用户体验

### 📋 使用说明
- 本项目仅供**学习研究**和**个人使用**
- 请遵守各直播平台的使用条款和相关法律法规
- **严禁商业用途**和任何违法违规行为
- 使用时请合理控制频率，避免对平台造成压力

### ⚖️ 法律声明
- 录制内容的版权归原作者所有
- 用户需自行承担使用软件的一切风险和责任
- 项目作者不承担任何法律责任
- 请尊重知识产权，合法合规使用

### 🌟 开源精神
- 遵循MIT开源协议，自由使用和修改
- 鼓励社区贡献和技术交流
- 欢迎提交问题反馈和功能建议
- 共同推动项目发展和完善

---

**如果这个项目对您有帮助，请给我们一个 ⭐Star！**

> 📧 问题反馈: [提交Issue](https://github.com/Sannylew/DouyinLiveRecorder/issues)  
> 🔧 功能建议: [提交Pull Request](https://github.com/Sannylew/DouyinLiveRecorder/pulls)  
> �� 技术交流: 欢迎在项目讨论区交流 