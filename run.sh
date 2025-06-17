#!/bin/bash

# DouyinLiveRecorder WebUI 启动脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查虚拟环境
if [ ! -d "venv" ]; then
    print_error "虚拟环境不存在，请先运行安装脚本:"
    echo "  chmod +x install.sh"
    echo "  ./install.sh"
    exit 1
fi

# 检查虚拟环境是否完整
if [ ! -f "venv/bin/activate" ] && [ ! -f "venv/Scripts/activate" ]; then
    print_error "虚拟环境不完整，请重新安装:"
    echo "  rm -rf venv"
    echo "  ./install.sh"
    exit 1
fi

# 激活虚拟环境
print_info "激活虚拟环境..."
if [ -f "venv/bin/activate" ]; then
    # Linux/macOS
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    # Windows (Git Bash)
    source venv/Scripts/activate
else
    print_error "找不到虚拟环境激活脚本"
    exit 1
fi

# 验证虚拟环境是否激活成功
if [ -z "$VIRTUAL_ENV" ]; then
    print_error "虚拟环境激活失败"
    exit 1
fi

# 检查依赖是否安装
if ! python -c "import fastapi" 2>/dev/null; then
    print_error "依赖包未安装，请先运行安装脚本"
    exit 1
fi

# 启动WebUI
print_info "启动 DouyinLiveRecorder WebUI..."
print_info "访问地址: http://localhost:8000"
print_info "按 Ctrl+C 停止服务"
echo ""

python start_webui.py 