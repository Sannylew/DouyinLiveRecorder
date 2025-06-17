⚠️ **本项目测试中，请勿使用** ⚠️

## 💡简介
[![Python Version](https://img.shields.io/badge/python-3.11.6-blue.svg)](https://www.python.org/downloads/release/python-3116/)
[![Supported Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Linux-blue.svg)](https://github.com/Sannylew/DouyinLiveRecorder)
![GitHub issues](https://img.shields.io/github/issues/Sannylew/DouyinLiveRecorder.svg)
[![Latest Release](https://img.shields.io/github/v/release/Sannylew/DouyinLiveRecorder)](https://github.com/Sannylew/DouyinLiveRecorder/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/Sannylew/DouyinLiveRecorder/total)](https://github.com/Sannylew/DouyinLiveRecorder/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

一款**简易**的可循环值守的直播录制工具，基于FFmpeg实现多平台直播源录制，支持自定义配置录制以及直播状态推送。

> **项目来源**: 本项目基于 [ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder) 开发  
> **扩展功能**: 在保持原有功能基础上，新增了现代化的WebUI管理界面  
> **开源协议**: 遵循 MIT 协议，自由使用和修改

## 🚀 快速开始

### 📦 **源码安装**

```bash
# 1. 克隆仓库
git clone https://github.com/Sannylew/DouyinLiveRecorder.git
cd DouyinLiveRecorder

# 2. 创建虚拟环境（推荐，避免系统环境冲突）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# Windows用户使用: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements_webui.txt

# 4. 启动WebUI版本
python start_webui.py
# 访问 http://localhost:8000

# 或启动命令行版本
python main.py
```

**适用场景**: 开发测试、个人使用、需要自定义修改

---

## 🌟 两种运行模式

### 🖥️ **WebUI版本**（现代化界面）
- **🎨 Bootstrap响应式设计** - 支持手机、平板、电脑
- **📊 可视化管理** - 直播间管理、实时监控、文件管理
- **🌐 远程访问** - 支持局域网和公网访问
- **🔄 实时更新** - 状态同步、日志查看

### 🖤 **命令行版本**（轻量级）
- **⚡ 资源占用低** - 适合VPS、服务器后台运行
- **🔧 配置文件驱动** - 纯文本配置，脚本友好
- **📱 自动化友好** - 适合定时任务、批处理

---

## 😺已支持平台

支持40+直播平台，包括但不限于：

- [x] 抖音、TikTok、快手、虎牙、斗鱼、YY、B站
- [x] 小红书、bigo、blued、SOOP、网易cc、千度热播
- [x] PandaTV、猫耳FM、Look直播、WinkTV、FlexTV
- [x] PopkonTV、TwitCasting、百度直播、微博直播、酷狗直播
- [x] TwitchTV、LiveMe、花椒直播、流星直播、ShowRoom
- [x] Acfun、映客直播、音播直播、知乎直播、CHZZK
- [x] 嗨秀直播、vv星球直播、17Live、浪Live、畅聊直播
- [x] 飘飘直播、六间房直播、乐嗨直播、花猫直播
- [x] Shopee、Youtube、淘宝、京东、Faceit
- [ ] 更多平台正在更新中

## 📋 **源码安装详细步骤**

### 🔧 **环境要求**
- **Python**: 3.10+ （推荐3.11）
- **系统**: Windows 10+, Ubuntu 18.04+, CentOS 7+, macOS 10.15+
- **内存**: 512MB+
- **存储**: 1GB+（用于录制文件）

### 📥 **安装步骤**

#### **1. 获取源码**
```bash
# 方式1：Git克隆（推荐）
git clone https://github.com/Sannylew/DouyinLiveRecorder.git
cd DouyinLiveRecorder

# 方式2：直接下载
# 访问 https://github.com/Sannylew/DouyinLiveRecorder/archive/main.zip
# 下载并解压到本地
```

#### **2. 安装Python依赖**

**推荐方式：使用虚拟环境（避免系统环境冲突）**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装WebUI依赖
pip install -r requirements_webui.txt
```

**其他安装方式**：
```bash
# 方式1: 直接安装（可能在新系统中报错）
pip install -r requirements_webui.txt

# 方式2: 使用用户目录安装
pip install --user -r requirements_webui.txt

# 方式3: 系统包管理器（Ubuntu/Debian）
sudo apt update
sudo apt install python3-fastapi python3-uvicorn python3-jinja2

# 方式4: 使用pipx（如果遇到externally-managed-environment错误）
pipx install --include-deps -r requirements_webui.txt
```

**解决"externally-managed-environment"错误**：
```bash
# 推荐：使用虚拟环境（最安全）
python3 -m venv douyin-env
source douyin-env/bin/activate  # Linux/macOS
# 或 douyin-env\Scripts\activate  # Windows
pip install -r requirements_webui.txt

# 或使用系统包管理器
sudo apt install python3-pip python3-venv
```

#### **3. 安装FFmpeg**

**Windows系统**（自动安装）：
```bash
python ffmpeg_install.py
```