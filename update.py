#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def run_command(command, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git():
    """检查Git状态"""
    print("📊 检查Git状态...")
    
    # 检查是否有未提交的更改
    success, stdout, stderr = run_command("git status --porcelain")
    if stdout.strip():
        print("⚠️ 检测到本地有未提交的更改:")
        print(stdout)
        choice = input("是否放弃本地更改？(y/n): ").lower()
        if choice == 'y':
            success, _, _ = run_command("git reset --hard HEAD")
            if not success:
                print("❌ 放弃本地更改失败")
                return False
        else:
            print("❌ 请先处理本地更改")
            return False
    
    return True

def update_code():
    """更新代码"""
    print("\n🔄 正在更新代码...")
    
    # 拉取最新代码
    success, stdout, stderr = run_command("git pull")
    if not success:
        print(f"❌ 更新失败: {stderr}")
        return False
    
    print("✅ 代码更新成功")
    return True

def update_dependencies():
    """更新依赖"""
    print("\n📦 检查并更新依赖...")
    
    # 检查虚拟环境
    if not os.path.exists("venv"):
        print("⚠️ 未检测到虚拟环境，创建新的虚拟环境...")
        success, _, _ = run_command("python3 -m venv venv")
        if not success:
            print("❌ 创建虚拟环境失败")
            return False
    
    # 安装/更新依赖
    pip_cmd = "venv/bin/pip" if os.name != 'nt' else r"venv\Scripts\pip"
    success, _, stderr = run_command(f"{pip_cmd} install -r requirements_webui.txt --upgrade")
    if not success:
        print(f"❌ 依赖更新失败: {stderr}")
        return False
    
    print("✅ 依赖更新成功")
    return True

def restart_service():
    """重启服务"""
    print("\n🔄 重启服务...")
    
    # 查找现有的WebUI进程
    success, stdout, _ = run_command("ps aux | grep 'start_webui.py' | grep -v grep")
    if stdout:
        pid = stdout.split()[1]
        print(f"发现WebUI进程 (PID: {pid})")
        
        # 终止现有进程
        try:
            os.kill(int(pid), signal.SIGTERM)
            time.sleep(2)  # 等待进程终止
            print("✅ 已停止旧进程")
        except ProcessLookupError:
            pass
        except Exception as e:
            print(f"⚠️ 停止进程时出错: {e}")
    
    # 启动新进程
    python_cmd = "venv/bin/python" if os.name != 'nt' else r"venv\Scripts\python"
    success, _, stderr = run_command(f"nohup {python_cmd} start_webui.py > webui.log 2>&1 &")
    if not success:
        print(f"❌ 服务启动失败: {stderr}")
        return False
    
    print("✅ 服务重启成功")
    return True

def main():
    """主函数"""
    print("🚀 DouyinLiveRecorder 在线更新工具")
    print("=" * 50)
    
    # 1. 检查Git状态
    if not check_git():
        return
    
    # 2. 更新代码
    if not update_code():
        return
    
    # 3. 更新依赖
    if not update_dependencies():
        return
    
    # 4. 重启服务
    if not restart_service():
        return
    
    print("\n🎉 更新完成！")
    print("📝 查看日志: tail -f webui.log")

if __name__ == "__main__":
    main() 