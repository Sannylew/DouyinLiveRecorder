#!/bin/bash

# DouyinLiveRecorder WebUI 一键部署脚本
# 适用于 Ubuntu/Debian/CentOS 系统

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查系统
check_system() {
    log_step "检查系统环境..."
    
    if [[ "$EUID" -eq 0 ]]; then
        log_error "请不要使用root用户运行此脚本"
        exit 1
    fi
    
    # 检查操作系统
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        log_info "检测到系统: $OS $VER"
    else
        log_error "无法检测操作系统"
        exit 1
    fi
    
    # 检查Python版本
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        log_info "Python版本: $PYTHON_VERSION"
        
        # 检查Python版本是否 >= 3.8
        if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            log_error "需要Python 3.8或更高版本"
            exit 1
        fi
    else
        log_error "未找到Python3"
        exit 1
    fi
}

# 安装系统依赖
install_system_deps() {
    log_step "安装系统依赖..."
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        sudo apt update
        sudo apt install -y python3-pip python3-venv ffmpeg curl git
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        sudo yum update -y
        sudo yum install -y python3-pip python3-venv ffmpeg curl git
    else
        log_warn "未识别的系统，请手动安装: python3-pip python3-venv ffmpeg curl git"
    fi
    
    log_info "系统依赖安装完成"
}

# 创建用户和目录
setup_user_and_dirs() {
    log_step "设置用户和目录..."
    
    # 创建应用目录
    INSTALL_DIR="/opt/DouyinLiveRecorder"
    sudo mkdir -p $INSTALL_DIR
    
    # 创建用户（如果不存在）
    if ! id "douyin" &>/dev/null; then
        sudo useradd -r -s /bin/false -d $INSTALL_DIR douyin
        log_info "创建用户: douyin"
    fi
    
    # 设置目录权限
    sudo chown -R douyin:douyin $INSTALL_DIR
    sudo chmod 755 $INSTALL_DIR
    
    log_info "用户和目录设置完成"
}

# 下载和安装应用
install_app() {
    log_step "下载和安装应用..."
    
    cd /tmp
    
    # 下载源码
    if [[ -d "DouyinLiveRecorder" ]]; then
        rm -rf DouyinLiveRecorder
    fi
    
    git clone https://github.com/Sannylew/DouyinLiveRecorder.git
    cd DouyinLiveRecorder
    
    # 复制文件到安装目录
    sudo cp -r * $INSTALL_DIR/
    
    # 设置权限
    sudo chown -R douyin:douyin $INSTALL_DIR
    
    log_info "应用安装完成"
}

# 设置Python环境
setup_python_env() {
    log_step "设置Python虚拟环境..."
    
    cd $INSTALL_DIR
    
    # 创建虚拟环境
    sudo -u douyin python3 -m venv venv
    
    # 安装依赖
    sudo -u douyin $INSTALL_DIR/venv/bin/pip install --upgrade pip
    sudo -u douyin $INSTALL_DIR/venv/bin/pip install -r requirements_webui.txt
    
    log_info "Python环境设置完成"
}

# 创建配置文件
create_config() {
    log_step "创建配置文件..."
    
    # 创建必要目录
    sudo -u douyin mkdir -p $INSTALL_DIR/{config,downloads,logs}
    
    # 如果不存在配置文件，创建默认配置
    if [[ ! -f "$INSTALL_DIR/config/config.ini" ]]; then
        sudo -u douyin cp $INSTALL_DIR/config/config.ini.example $INSTALL_DIR/config/config.ini 2>/dev/null || {
            log_warn "未找到配置文件模板，将在首次运行时自动创建"
        }
    fi
    
    log_info "配置文件创建完成"
}

# 安装systemd服务
install_systemd_service() {
    log_step "安装systemd服务..."
    
    # 复制服务文件
    sudo cp $INSTALL_DIR/systemd/douyin-webui.service /etc/systemd/system/
    
    # 修改服务文件中的路径
    sudo sed -i "s|/opt/DouyinLiveRecorder|$INSTALL_DIR|g" /etc/systemd/system/douyin-webui.service
    
    # 重载systemd
    sudo systemctl daemon-reload
    
    # 启用服务
    sudo systemctl enable douyin-webui
    
    log_info "systemd服务安装完成"
}

# 配置防火墙
configure_firewall() {
    log_step "配置防火墙..."
    
    if command -v ufw &> /dev/null; then
        sudo ufw allow 8000/tcp
        log_info "UFW防火墙规则已添加"
    elif command -v firewall-cmd &> /dev/null; then
        sudo firewall-cmd --permanent --add-port=8000/tcp
        sudo firewall-cmd --reload
        log_info "firewalld防火墙规则已添加"
    else
        log_warn "未检测到防火墙，请手动开放端口8000"
    fi
}

# 启动服务
start_service() {
    log_step "启动服务..."
    
    sudo systemctl start douyin-webui
    
    # 等待服务启动
    sleep 5
    
    if sudo systemctl is-active --quiet douyin-webui; then
        log_info "服务启动成功"
    else
        log_error "服务启动失败"
        sudo systemctl status douyin-webui
        exit 1
    fi
}

# 显示部署信息
show_deploy_info() {
    echo
    echo "=================================="
    echo -e "${GREEN}🎉 部署完成！${NC}"
    echo "=================================="
    echo
    echo "📱 Web界面访问地址:"
    echo "   本地: http://localhost:8000"
    echo "   局域网: http://$(hostname -I | awk '{print $1}'):8000"
    echo
    echo "🔧 服务管理命令:"
    echo "   启动服务: sudo systemctl start douyin-webui"
    echo "   停止服务: sudo systemctl stop douyin-webui"
    echo "   重启服务: sudo systemctl restart douyin-webui"
    echo "   查看状态: sudo systemctl status douyin-webui"
    echo "   查看日志: sudo journalctl -u douyin-webui -f"
    echo
    echo "📁 重要目录:"
    echo "   安装目录: $INSTALL_DIR"
    echo "   配置目录: $INSTALL_DIR/config"
    echo "   下载目录: $INSTALL_DIR/downloads"
    echo "   日志目录: $INSTALL_DIR/logs"
    echo
    echo "🛠️  配置建议:"
    echo "   1. 编辑配置文件: sudo nano $INSTALL_DIR/config/config.ini"
    echo "   2. 添加直播间: 通过Web界面或编辑 $INSTALL_DIR/config/URL_config.ini"
    echo "   3. 设置推送通知: 在Web界面的配置页面设置"
    echo
}

# 主函数
main() {
    echo "======================================"
    echo -e "${BLUE}DouyinLiveRecorder WebUI 一键部署脚本${NC}"
    echo "======================================"
    echo
    
    # 确认安装
    read -p "是否继续安装？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "安装已取消"
        exit 0
    fi
    
    # 执行安装步骤
    check_system
    install_system_deps
    setup_user_and_dirs
    install_app
    setup_python_env
    create_config
    install_systemd_service
    configure_firewall
    start_service
    show_deploy_info
}

# 错误处理
trap 'log_error "安装过程中发生错误，请检查日志"; exit 1' ERR

# 运行主函数
main "$@" 