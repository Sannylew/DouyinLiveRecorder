⚠️ **本项目测试中，请勿使用** ⚠️

## 💡简介
[![Python Version](https://img.shields.io/badge/python-3.11.6-blue.svg)](https://www.python.org/downloads/release/python-3116/)
[![Supported Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Linux-blue.svg)](https://github.com/Sannylew/DouyinLiveRecorder)
[![Docker Pulls](https://img.shields.io/docker/pulls/ihmily/douyin-live-recorder?label=Docker%20Pulls&color=blue&logo=docker)](https://hub.docker.com/r/ihmily/douyin-live-recorder/tags)
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

**🔧 手动安装**：
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

### 📦 **打包版本**（小白用户）

从[Releases](https://github.com/Sannylew/DouyinLiveRecorder/releases)下载最新版本，解压后直接运行。

**适用场景**: 不熟悉编程、Windows桌面用户

### 🐋 **Docker部署**（容器化）

```bash
docker-compose up -d
```

**适用场景**: 容器化环境、隔离运行

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

**Linux系统**：
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install epel-release && sudo yum install ffmpeg

# 或使用包管理器安装
```

**macOS系统**：
```bash
# 使用Homebrew
brew install ffmpeg
```

#### **4. 配置直播间**
```bash
# 编辑配置文件
nano config/URL_config.ini

# 添加直播间地址，一行一个
https://live.douyin.com/123456
https://www.tiktok.com/@username/live
https://live.kuaishou.com/u/username
```

#### **5. 启动程序**
```bash
# WebUI版本（推荐）
python start_webui.py
# 浏览器访问 http://localhost:8000

# 命令行版本
python main.py
```

### 🎯 **高级配置**

#### **录制设置**
编辑 `config/config.ini`：
```ini
[录制设置]
录制格式 = ts
录制码率 = 10000
循环时间(秒) = 300
录制结束后自动转换为mp4 = 否
```

#### **画质设置**
在URL前添加画质：
```
超清,https://live.douyin.com/123456
高清,https://www.kuaishou.com/live/123456
```

#### **代理设置**
```ini
[录制设置]
是否使用代理ip(是/否) = 是
代理地址 = 127.0.0.1:7890
```

## 🎈项目结构

```
DouyinLiveRecorder/
├── /config                 # 配置文件目录
│   ├── config.ini         # 主配置文件
│   └── URL_config.ini     # 直播间地址
├── /downloads             # 录制文件保存目录
├── /logs                  # 日志文件目录
├── /web                   # WebUI界面文件
│   ├── index.html        # 主界面
│   └── static/app.js     # 前端逻辑
├── /src                   # 核心功能模块
├── main.py               # 命令行版本主程序
├── app.py                # WebUI版本主程序
├── start_webui.py        # WebUI智能启动脚本
├── recording_service.py  # 录制服务核心
├── requirements.txt      # 基础依赖
└── requirements_webui.txt # WebUI依赖
```

## 🔧 **常见问题**

### **Q: 遇到"externally-managed-environment"错误？**
这是较新Linux系统（Ubuntu 23.04+, Debian 12+）的保护机制。

**解决方案（按推荐程度排序）**：
```bash
# 1. 使用虚拟环境（最推荐）
python3 -m venv douyin-env
source douyin-env/bin/activate
pip install -r requirements_webui.txt
python start_webui.py

# 2. 使用用户目录安装
pip install --user -r requirements_webui.txt

# 3. 使用系统包管理器
sudo apt install python3-fastapi python3-uvicorn python3-jinja2

# 4. 临时解决（不推荐，可能破坏系统）
pip install -r requirements_webui.txt --break-system-packages
```

### **Q: 安装依赖时出错？**
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements_webui.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 清华源（推荐）
pip install -r requirements_webui.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 阿里源
pip install -r requirements_webui.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### **Q: 虚拟环境相关问题**
```bash
# 检查虚拟环境是否激活
which python  # 应该显示虚拟环境路径

# 退出虚拟环境
deactivate

# 删除虚拟环境
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# 重新创建虚拟环境
python3 -m venv venv
source venv/bin/activate
```

### **Q: FFmpeg未找到？**
```bash
# 检查FFmpeg是否安装
ffmpeg -version

# 手动安装FFmpeg
python ffmpeg_install.py

# 系统包管理器安装
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
brew install ffmpeg      # macOS
```

### **Q: 配置文件BOM错误？**
使用UTF-8编码保存配置文件，避免BOM标记。已在recording_service.py中修复。

### **Q: 端口被占用？**
```bash
# 检查端口占用
netstat -tlnp | grep 8000
lsof -i :8000

# 修改端口
python start_webui.py --port 8080

# 杀死占用进程
sudo kill -9 <PID>
```

## 🐋 容器部署

```bash
# 快速启动
docker-compose up -d

# 自定义端口
docker run -d -p 8080:8000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/downloads:/app/downloads \
  ihmily/douyin-live-recorder:latest
```

## ❤️致谢

### 原作者
感谢 **[ihmily](https://github.com/ihmily)** 开发的 [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder) 项目，本WebUI版本基于该项目扩展开发。

---

## 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

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

## 🙏 致谢

### 原始项目
- **[ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** - 感谢原作者提供的强大直播录制引擎
- 本WebUI版本是在原项目基础上的功能扩展，保持了原有的核心录制逻辑

### 技术栈
- **[FastAPI](https://fastapi.tiangolo.com/)** - 现代化的Web框架
- **[Bootstrap](https://getbootstrap.com/)** - 响应式前端框架  
- **[FFmpeg](https://ffmpeg.org/)** - 强大的多媒体处理工具
- **[Python](https://www.python.org/)** - 优秀的编程语言生态

### 社区贡献
感谢所有为这个项目做出贡献的开发者们！

## 📝 项目声明

### 用途说明
- 本项目仅供**学习研究**和**技术交流**使用
- 请遵守各直播平台的服务条款和相关法律法规
- **禁止用于商业用途**或任何违法违规活动

### 免责声明
- 本项目不承担因使用本软件导致的任何法律责任
- 用户应自行承担使用本软件的风险
- 请合理使用，避免对直播平台造成过大压力

### 版权声明
- 本项目遵循MIT开源协议
- 录制的内容版权归原作者所有
- 请尊重原创作者的知识产权

---

## 有问题可以提issue，欢迎Star ⭐

> 如果这个项目对您有帮助，请给我们一个Star⭐  
> 有问题或建议请提交[Issue](https://github.com/Sannylew/DouyinLiveRecorder/issues)  
> 欢迎提交[Pull Request](https://github.com/Sannylew/DouyinLiveRecorder/pulls)参与贡献
