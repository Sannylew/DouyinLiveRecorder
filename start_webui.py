#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DouyinLiveRecorder WebUI 启动脚本
简化版启动脚本，专注于快速启动和问题诊断
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("�?Python版本过低，需要Python 3.8+")
        print(f"当前版本: {sys.version}")
        return False
    print(f"�?Python版本: {sys.version.split()[0]}")
    return True

def check_package(package_name):
    """检查包是否已安�?""
    try:
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    except ImportError:
        return False

def install_requirements():
    """安装依赖�?""
    requirements_file = "requirements_webui.txt"
    
    if not os.path.exists(requirements_file):
        print(f"�?找不到依赖文�? {requirements_file}")
        print("正在创建基础依赖文件...")
        
        # 创建基础依赖文件
        basic_requirements = """fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
requests>=2.31.0
loguru>=0.7.0
configparser
pathlib
"""
        with open(requirements_file, 'w', encoding='utf-8') as f:
            f.write(basic_requirements)
        print(f"�?已创建基础依赖文件: {requirements_file}")
    
    print("📦 安装依赖�?..")
    try:
        # 使用更简单的安装命令
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("�?依赖包安装完�?)
            return True
        else:
            print(f"�?依赖包安装失�? {result.stderr}")
            print("尝试使用国内镜像�?..")
            
            # 尝试使用国内镜像�?
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", requirements_file,
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("�?依赖包安装完成（使用国内镜像源）")
                return True
            else:
                print(f"�?依赖包安装失�? {result.stderr}")
                return False
                
    except Exception as e:
        print(f"�?安装过程中出�? {e}")
        return False

def create_directories():
    """创建必要的目�?""
    directories = ["config", "downloads", "logs", "web", "web/static"]
    
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)
        print(f"📁 目录: {dir_name}")

def check_files():
    """检查必要文件是否存�?""
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
            print(f"�?文件: {file_path}")
    
    if missing_files:
        print(f"�?缺少必要文件: {missing_files}")
        return False
    
    return True

def create_minimal_config():
    """创建最小化配置文件"""
    config_file = "./config/config.ini"
    if not os.path.exists(config_file):
        print("📝 创建默认配置文件...")
        default_config = """[录制设置]
录制格式 = ts
录制码率 = 10000
循环时间(�? = 300
开启录�?= �?
开启推�?= �?

[Cookie]
抖音cookie = 
快手cookie = 
虎牙cookie = 
斗鱼cookie = 
B站cookie = 
"""
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(default_config)
        print(f"�?已创建配置文�? {config_file}")

def start_webui():
    """启动WebUI"""
    print("\n🚀 启动DouyinLiveRecorder WebUI...")
    print("=" * 50)
    print("📱 访问地址: http://localhost:8000")
    print("🛑 �?Ctrl+C 停止服务")
    print("=" * 50)
    
    try:
        # 直接启动app.py
        import app
        print("�?WebUI模块加载成功")
        
        # 如果app.py有main函数，调用它
        if hasattr(app, 'main'):
            app.main()
        else:
            # 否则直接运行uvicorn
            import uvicorn
            uvicorn.run(
                "app:app",
                host="0.0.0.0",
                port=8000,
                reload=False,
                access_log=True
            )
            
    except ImportError as e:
        print(f"�?导入失败: {e}")
        print("\n🔧 请检查以下问�?")
        print("1. 是否安装了所有依�? pip install -r requirements_webui.txt")
        print("2. 是否在正确的目录中运�?)
        print("3. Python路径是否正确")
        return False
    except KeyboardInterrupt:
        print("\n👋 WebUI已停�?)
        return True
    except Exception as e:
        print(f"�?启动失败: {e}")
        print("\n🔧 故障排除:")
        print("1. 检查端�?000是否被占�?)
        print("2. 检查防火墙设置")
        print("3. 查看详细错误信息")
        return False

def main():
    """主函�?""
    print("🎯 DouyinLiveRecorder WebUI 启动程序")
    print("=" * 50)
    
    # 1. 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 2. 创建必要目录
    print("\n📁 创建目录...")
    create_directories()
    
    # 3. 创建配置文件
    create_minimal_config()
    
    # 4. 检查必要文�?
    print("\n📄 检查文�?..")
    if not check_files():
        print("\n�?缺少必要文件，请检查项目完整�?)
        print("请确保以下文件存�?")
        print("- app.py (WebUI主程�?")
        print("- recording_service.py (录制服务)")
        print("- web/index.html (前端页面)")
        print("- web/static/app.js (前端脚本)")
        sys.exit(1)
    
    # 5. 检查关键依赖包
    print("\n📦 检查依�?..")
    required_packages = ["fastapi", "uvicorn", "requests"]
    missing_packages = []
    
    for package in required_packages:
        if check_package(package):
            print(f"�?�? {package}")
        else:
            missing_packages.append(package)
            print(f"�?�? {package}")
    
    # 6. 安装缺失的依�?
    if missing_packages:
        print(f"\n📦 需要安装依赖包: {missing_packages}")
        if not install_requirements():
            print("�?安装失败，请手动运行: pip install -r requirements_webui.txt")
            sys.exit(1)
    
    # 7. 启动WebUI
    print("\n�?环境检查完成，准备启动WebUI...")
    
    try:
        input("按回车键继续启动，或按Ctrl+C取消...")
    except KeyboardInterrupt:
        print("\n👋 启动已取�?)
        sys.exit(0)
    
    if start_webui():
        print("\n🎉 WebUI启动成功�?)
    else:
        print("\n�?WebUI启动失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 
