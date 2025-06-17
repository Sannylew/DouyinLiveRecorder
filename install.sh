#!/bin/bash

# DouyinLiveRecorder WebUI 智能安装脚本
# 自动处理虚拟环境和依赖安装

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查Python版本
check_python() {
    print_info "检查Python环境..."
    
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "未找到Python，请先安装Python 3.10+"
        exit 1
    fi
    
    # 检查Python版本
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    MIN_VERSION="3.10"
    
    if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
        print_error "Python版本过低: $PYTHON_VERSION，需要3.10+"
        exit 1
    fi
    
    print_success "Python版本: $PYTHON_VERSION ✓"
}

# 创建虚拟环境
create_venv() {
    print_info "创建虚拟环境..."
    
    if [ -d "venv" ]; then
        print_warning "虚拟环境已存在，删除旧环境..."
        rm -rf venv
    fi
    
    $PYTHON_CMD -m venv venv
    print_success "虚拟环境创建成功 ✓"
}

# 激活虚拟环境
activate_venv() {
    print_info "激活虚拟环境..."
    source venv/bin/activate
    print_success "虚拟环境激活成功 ✓"
}

# 安装依赖
install_dependencies() {
    print_info "安装Python依赖包..."
    
    # 升级pip
    pip install --upgrade pip
    
    # 尝试安装依赖
    if pip install -r requirements_webui.txt; then
        print_success "依赖安装成功 ✓"
    else
        print_warning "使用国内镜像源重试..."
        if pip install -r requirements_webui.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/; then
            print_success "依赖安装成功（使用清华源）✓"
        else
            print_error "依赖安装失败"
            exit 1
        fi
    fi
}

# 检查FFmpeg
check_ffmpeg() {
    print_info "检查FFmpeg..."
    
    if command_exists ffmpeg; then
        FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1)
        print_success "FFmpeg已安装: $FFMPEG_VERSION ✓"
    else
        print_warning "FFmpeg未安装，尝试自动安装..."
        
        # 尝试使用系统包管理器安装
        if command_exists apt-get; then
            print_info "使用apt安装FFmpeg..."
            sudo apt update && sudo apt install -y ffmpeg
        elif command_exists yum; then
            print_info "使用yum安装FFmpeg..."
            sudo yum install -y epel-release && sudo yum install -y ffmpeg
        elif command_exists brew; then
            print_info "使用brew安装FFmpeg..."
            brew install ffmpeg
        else
            print_warning "无法自动安装FFmpeg，请手动安装"
            print_info "或运行: python ffmpeg_install.py"
        fi
    fi
}

# 创建配置目录
setup_config() {
    print_info "设置配置目录..."
    mkdir -p config downloads logs
    print_success "配置目录创建成功 ✓"
}

# 主安装流程
main() {
    echo "================================================"
    echo "  DouyinLiveRecorder WebUI 智能安装脚本"
    echo "================================================"
    echo ""
    
    # 检查是否在项目根目录
    if [ ! -f "requirements_webui.txt" ]; then
        print_error "请在项目根目录运行此脚本"
        exit 1
    fi
    
    check_python
    create_venv
    activate_venv
    install_dependencies
    check_ffmpeg
    setup_config
    
    echo ""
    echo "================================================"
    print_success "安装完成！"
    echo "================================================"
    echo ""
    print_info "启动WebUI:"
    echo "  source venv/bin/activate"
    echo "  python start_webui.py"
    echo ""
    print_info "或者直接运行:"
    echo "  ./run.sh"
    echo ""
    print_info "访问地址: http://localhost:8000"
    echo ""
}

# 运行主程序
main "$@" 