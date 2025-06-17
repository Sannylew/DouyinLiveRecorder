# 📦 DouyinLiveRecorder 安装指南

## 🎯 解决"externally-managed-environment"错误

在较新的Linux系统（Ubuntu 23.04+、Debian 12+等）中，系统禁止直接在全局Python环境中安装包，会出现以下错误：

```
error: externally-managed-environment
```

## 🚀 推荐解决方案

### 方案1: 一键安装脚本（Linux/macOS推荐）

```bash
git clone https://github.com/ihmily/DouyinLiveRecorder.git
cd DouyinLiveRecorder
chmod +x install.sh
./install.sh
```

**脚本功能**：
- ✅ 自动检查Python版本（需要3.10+）
- ✅ 自动创建虚拟环境
- ✅ 智能安装依赖（支持国内镜像源）
- ✅ 自动检查/安装FFmpeg
- ✅ 创建必要的配置目录

### 方案2: 虚拟环境手动安装（所有系统）

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements_webui.txt

# 4. 启动
python start_webui.py
```

### 方案3: 系统包管理器（Ubuntu/Debian）

```bash
# 安装主要依赖
sudo apt update
sudo apt install python3-pip python3-venv python3-fastapi python3-uvicorn

# 创建虚拟环境安装其他依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_webui.txt
```

### 方案4: 用户目录安装

```bash
pip install --user -r requirements_webui.txt
```

## 🔧 常见问题解决

### Q: Python版本不够？
```bash
# Ubuntu/Debian安装Python 3.11
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-venv python3.11-pip

# 使用Python 3.11创建虚拟环境
python3.11 -m venv venv
```

### Q: pip安装速度慢？
```bash
# 使用国内镜像源
pip install -r requirements_webui.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或阿里源
pip install -r requirements_webui.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### Q: FFmpeg未安装？
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg

# macOS
brew install ffmpeg

# 或使用项目自带安装脚本
python ffmpeg_install.py
```

### Q: 权限问题？
```bash
# 确保用户有权限访问项目目录
sudo chown -R $USER:$USER /path/to/DouyinLiveRecorder

# 或在用户目录运行
cp -r DouyinLiveRecorder ~/
cd ~/DouyinLiveRecorder
```

## 🎮 启动方式

### 使用运行脚本（推荐）
```bash
./run.sh
```

### 手动启动
```bash
# 激活虚拟环境
source venv/bin/activate

# 启动WebUI
python start_webui.py

# 或启动命令行版本
python main.py
```

### 后台运行
```bash
# 使用nohup
nohup ./run.sh > webui.log 2>&1 &

# 使用screen
screen -S douyin-webui
./run.sh
# Ctrl+A+D 分离会话

# 查看screen会话
screen -r douyin-webui
```

## 🌐 访问WebUI

启动成功后，在浏览器中访问：
- 本地访问: http://localhost:8000
- 局域网访问: http://你的IP:8000

## 📝 注意事项

1. **虚拟环境**: 推荐使用虚拟环境，避免污染系统Python环境
2. **权限管理**: 确保当前用户有读写项目目录的权限
3. **防火墙**: 如需远程访问，请开放8000端口
4. **系统资源**: WebUI需要额外内存，建议512MB+
5. **Python版本**: 最低要求Python 3.10，推荐3.11+

## 🆘 获取帮助

如果遇到其他问题：
1. 查看日志文件: `logs/app.log`
2. 检查配置文件: `config/config.ini`
3. 提交Issue: [GitHub Issues](https://github.com/ihmily/DouyinLiveRecorder/issues)
4. 查看详细文档: `README_WebUI.md` 