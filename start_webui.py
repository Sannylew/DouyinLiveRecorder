#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DouyinLiveRecorder WebUI 启动脚本 - 服务器版
自动检查环境并启动Web界面（专为Linux服务器优化）
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要Python 3.8+")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本: {sys.version.split()[0]}")
    return True

def check_system():
    """检查系统环境"""
    import platform
    system = platform.system()
    print(f"🖥️  操作系统: {system} {platform.release()}")
    
    if system not in ['Linux', 'Darwin']:  # Darwin is macOS
        print("⚠️  警告: 此WebUI版本专为Linux/macOS服务器设计")
    
    return True

def check_package(package_name):
    """检查包是否已安装"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_requirements():
    """安装依赖包"""
    requirements_file = "requirements_webui.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ 找不到依赖文件: {requirements_file}")
        return False
    
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file, "--upgrade"
        ])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def check_ffmpeg():
    """检查FFmpeg是否可用"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg 已安装: {version_line}")
            return True
        else:
            print("❌ FFmpeg 不可用")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  FFmpeg 未找到，录制功能可能无法正常工作")
        print("安装FFmpeg:")
        print("  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
        print("  CentOS/RHEL: sudo yum install ffmpeg")
        print("  macOS: brew install ffmpeg")
        return False

def check_network_access():
    """检查网络访问配置"""
    print("\n🌐 网络访问配置:")
    print("本地访问: http://localhost:8000")
    print("局域网访问: http://YOUR_SERVER_IP:8000")
    print("公网访问: 需要配置防火墙开放端口8000")
    print("\n防火墙配置示例:")
    print("  Ubuntu: sudo ufw allow 8000")
    print("  CentOS: sudo firewall-cmd --add-port=8000/tcp --permanent")

def create_directories():
    """创建必要的目录"""
    directories = ["config", "downloads", "web", "web/static", "logs"]
    
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)
        print(f"📁 目录: {dir_name}")

def check_files():
    """检查必要文件是否存在"""
    required_files = [
        "app.py",
        "recording_service.py", 
        "web/index.html",
        "web/static/app.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ 文件: {file_path}")
    
    if missing_files:
        print(f"❌ 缺少必要文件: {missing_files}")
        return False
    
    return True

def check_permissions():
    """检查文件权限"""
    dirs_to_check = ["config", "downloads", "logs"]
    
    for dir_name in dirs_to_check:
        if os.path.exists(dir_name):
            if os.access(dir_name, os.W_OK):
                print(f"✅ 目录权限: {dir_name} (可写)")
            else:
                print(f"❌ 目录权限: {dir_name} (不可写)")
                return False
    
    return True

def get_server_info():
    """获取服务器信息"""
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"🖥️  主机名: {hostname}")
        print(f"🌐 本机IP: {local_ip}")
    except Exception as e:
        print(f"⚠️  无法获取网络信息: {e}")

def start_webui():
    """启动WebUI"""
    print("\n🚀 启动DouyinLiveRecorder WebUI...")
    print("=" * 60)
    print("📱 本地访问: http://localhost:8000")
    print("🌐 局域网访问: http://YOUR_SERVER_IP:8000")
    print("🛑 按 Ctrl+C 停止服务")
    print("=" * 60)
    
    try:
        import uvicorn
        # 检查是否在虚拟环境中
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("🔧 检测到虚拟环境")
        
        uvicorn.run(
            "app:app",
            host="0.0.0.0",  # 默认允许外部访问
            port=8000,
            reload=False,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 WebUI已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("\n故障排除:")
        print("1. 检查端口8000是否被占用: netstat -tlnp | grep 8000")
        print("2. 检查防火墙设置: sudo ufw status")
        print("3. 查看详细错误信息，检查依赖是否完整安装")
        return False
    
    return True

def show_post_install_info():
    """显示安装后信息"""
    print("\n" + "=" * 60)
    print("🎉 WebUI启动成功！")
    print("=" * 60)
    print("\n📋 管理命令:")
    print("  启动: python start_webui.py")
    print("  后台运行: nohup python app.py > webui.log 2>&1 &")
    print("  查看进程: ps aux | grep python")
    print("  停止进程: pkill -f app.py")
    
    print("\n🔧 系统服务配置:")
    print("  创建服务: sudo nano /etc/systemd/system/douyin-webui.service")
    print("  启动服务: sudo systemctl start douyin-webui")
    print("  开机自启: sudo systemctl enable douyin-webui")
    
    print("\n📊 监控命令:")
    print("  查看日志: tail -f logs/app.log")
    print("  查看端口: netstat -tlnp | grep 8000")
    print("  系统资源: htop")

def main():
    """主函数"""
    print("🎯 DouyinLiveRecorder WebUI 启动程序 - 服务器版")
    print("=" * 60)
    
    # 1. 检查系统环境
    if not check_python_version():
        sys.exit(1)
    
    check_system()
    get_server_info()
    
    # 2. 创建必要目录
    print("\n📁 创建目录...")
    create_directories()
    
    # 3. 检查文件权限
    print("\n🔐 检查权限...")
    if not check_permissions():
        print("❌ 权限检查失败，请检查目录权限")
        sys.exit(1)
    
    # 4. 检查必要文件
    print("\n📄 检查文件...")
    if not check_files():
        print("\n❌ 缺少必要文件，请检查项目完整性")
        sys.exit(1)
    
    # 5. 检查关键依赖包
    print("\n📦 检查依赖...")
    required_packages = ["fastapi", "uvicorn", "requests", "loguru"]
    missing_packages = []
    
    for package in required_packages:
        if check_package(package):
            print(f"✅ 包: {package}")
        else:
            missing_packages.append(package)
            print(f"❌ 包: {package}")
    
    # 6. 安装缺失的依赖
    if missing_packages:
        print(f"\n📦 需要安装依赖包: {missing_packages}")
        if install_requirements():
            print("✅ 依赖安装完成")
        else:
            print("❌ 安装失败，请手动运行: pip install -r requirements_webui.txt")
            sys.exit(1)
    
    # 7. 检查FFmpeg（可选）
    print("\n🎬 检查FFmpeg...")
    check_ffmpeg()
    
    # 8. 显示网络配置信息
    check_network_access()
    
    # 9. 启动WebUI
    print("\n✨ 环境检查完成，准备启动WebUI...")
    
    # 在服务器环境中，通常不需要用户交互
    if os.getenv('CI') or os.getenv('AUTOMATED'):
        print("🤖 检测到自动化环境，直接启动...")
    else:
        try:
            input("按回车键继续启动，或按Ctrl+C取消...")
        except KeyboardInterrupt:
            print("\n👋 启动已取消")
            sys.exit(0)
    
    if start_webui():
        show_post_install_info()

if __name__ == "__main__":
    main() 