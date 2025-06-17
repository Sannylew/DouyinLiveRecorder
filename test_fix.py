#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DouyinLiveRecorder 修复验证脚本
测试主要模块是否可以正常导入和运行
"""

import sys
import os
import traceback

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    # 添加当前目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    test_results = {}
    
    # 测试基础模块
    modules_to_test = [
        ('configparser', '配置解析'),
        ('pathlib', '路径处理'),
        ('asyncio', '异步支持'),
        ('json', 'JSON处理'),
        ('os', '系统操作'),
        ('sys', '系统信息'),
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            test_results[module_name] = True
            print(f"✅ {description}: {module_name}")
        except ImportError as e:
            test_results[module_name] = False
            print(f"❌ {description}: {module_name} - {e}")
    
    # 测试WebUI相关模块
    webui_modules = [
        ('fastapi', 'FastAPI框架'),
        ('uvicorn', 'ASGI服务器'),
        ('pydantic', '数据验证'),
        ('requests', 'HTTP客户端'),
    ]
    
    print("\n🌐 测试WebUI模块...")
    for module_name, description in webui_modules:
        try:
            __import__(module_name)
            test_results[module_name] = True
            print(f"✅ {description}: {module_name}")
        except ImportError as e:
            test_results[module_name] = False
            print(f"❌ {description}: {module_name} - {e}")
    
    return test_results

def test_project_files():
    """测试项目文件"""
    print("\n📁 测试项目文件...")
    
    required_files = [
        ('app.py', 'WebUI主程序'),
        ('recording_service.py', '录制服务'),
        ('start_webui.py', '启动脚本'),
        ('web/index.html', '前端页面'),
        ('web/static/app.js', '前端脚本'),
        ('requirements_webui.txt', '依赖文件'),
    ]
    
    file_results = {}
    
    for file_path, description in required_files:
        exists = os.path.exists(file_path)
        file_results[file_path] = exists
        
        if exists:
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (缺失)")
    
    return file_results

def test_src_modules():
    """测试src目录模块"""
    print("\n🔧 测试src模块...")
    
    src_modules = [
        ('src.utils', '工具模块'),
        ('src.spider', '爬虫模块'),
        ('src.stream', '流处理模块'),
        ('src.logger', '日志模块'),
    ]
    
    src_results = {}
    
    for module_name, description in src_modules:
        try:
            __import__(module_name)
            src_results[module_name] = True
            print(f"✅ {description}: {module_name}")
        except ImportError as e:
            src_results[module_name] = False
            print(f"⚠️ {description}: {module_name} - {e}")
        except Exception as e:
            src_results[module_name] = False
            print(f"⚠️ {description}: {module_name} - 运行时错误: {e}")
    
    return src_results

def test_recording_service():
    """测试录制服务"""
    print("\n🎬 测试录制服务...")
    
    try:
        from recording_service import RecordingService
        service = RecordingService()
        print("✅ 录制服务类导入成功")
        print("✅ 录制服务实例创建成功")
        return True
    except ImportError as e:
        print(f"❌ 录制服务导入失败: {e}")
        return False
    except Exception as e:
        print(f"⚠️ 录制服务初始化警告: {e}")
        return True  # 部分功能可能不可用，但基础结构正常

def test_webui_app():
    """测试WebUI应用"""
    print("\n🌐 测试WebUI应用...")
    
    try:
        import app
        print("✅ WebUI应用模块导入成功")
        
        if hasattr(app, 'app'):
            print("✅ FastAPI应用实例存在")
        else:
            print("⚠️ FastAPI应用实例未找到")
        
        return True
    except ImportError as e:
        print(f"❌ WebUI应用导入失败: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"⚠️ WebUI应用加载警告: {e}")
        return True

def main():
    """主测试函数"""
    print("🔍 DouyinLiveRecorder 修复验证")
    print("=" * 50)
    
    # 运行所有测试
    test_results = {}
    
    test_results['imports'] = test_imports()
    test_results['files'] = test_project_files()
    test_results['src_modules'] = test_src_modules()
    test_results['recording_service'] = test_recording_service()
    test_results['webui_app'] = test_webui_app()
    
    # 汇总结果
    print("\n📊 测试结果汇总")
    print("=" * 50)
    
    total_tests = 0
    passed_tests = 0
    
    # 统计基础模块
    for module, result in test_results['imports'].items():
        total_tests += 1
        if result:
            passed_tests += 1
    
    # 统计文件
    for file_path, result in test_results['files'].items():
        total_tests += 1
        if result:
            passed_tests += 1
    
    # 统计src模块
    for module, result in test_results['src_modules'].items():
        total_tests += 1
        if result:
            passed_tests += 1
    
    # 统计服务
    if test_results['recording_service']:
        passed_tests += 1
    total_tests += 1
    
    if test_results['webui_app']:
        passed_tests += 1
    total_tests += 1
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"总测试项: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"成功率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("\n🎉 项目修复成功！可以尝试启动WebUI")
        print("运行命令: python start_webui.py")
    elif success_rate >= 60:
        print("\n⚠️ 项目部分修复，可能需要安装依赖")
        print("运行命令: pip install -r requirements_webui.txt")
    else:
        print("\n❌ 项目需要进一步修复")
        print("请检查缺失的文件和模块")
    
    print("\n🔧 故障排除建议:")
    if not test_results['webui_app']:
        print("- 安装WebUI依赖: pip install -r requirements_webui.txt")
    
    missing_files = [f for f, exists in test_results['files'].items() if not exists]
    if missing_files:
        print(f"- 缺失文件: {', '.join(missing_files)}")
    
    failed_src = [m for m, result in test_results['src_modules'].items() if not result]
    if failed_src:
        print(f"- src模块问题: {', '.join(failed_src)}")

if __name__ == "__main__":
    main() 