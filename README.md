⚠️ **本项目测试中，请勿使用** ⚠️

![video_spider](https://socialify.git.ci/ihmily/DouyinLiveRecorder/image?font=Inter&forks=1&language=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Light)

## 💡简介
[![Python Version](https://img.shields.io/badge/python-3.11.6-blue.svg)](https://www.python.org/downloads/release/python-3116/)
[![Supported Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Linux-blue.svg)](https://github.com/ihmily/DouyinLiveRecorder)
[![Docker Pulls](https://img.shields.io/docker/pulls/ihmily/douyin-live-recorder?label=Docker%20Pulls&color=blue&logo=docker)](https://hub.docker.com/r/ihmily/douyin-live-recorder/tags)
![GitHub issues](https://img.shields.io/github/issues/ihmily/DouyinLiveRecorder.svg)
[![Latest Release](https://img.shields.io/github/v/release/ihmily/DouyinLiveRecorder)](https://github.com/ihmily/DouyinLiveRecorder/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/ihmily/DouyinLiveRecorder/total)](https://github.com/ihmily/DouyinLiveRecorder/releases/latest)

一款**简易**的可循环值守的直播录制工具，基于FFmpeg实现多平台直播源录制，支持自定义配置录制以及直播状态推送。

## 🌟 WebUI版本 - 全新体验！

现在提供了**两种运行方式**：

### 🖥️ WebUI版本（推荐）
- **🎨 现代化Web界面** - 基于Bootstrap的响应式设计
- **📊 可视化管理** - 直播间管理、配置设置、文件管理
- **🌐 远程访问** - 支持局域网和公网访问
- **🔄 实时监控** - 实时状态显示和日志查看
- **🚀 一键部署** - 支持Docker、systemd服务等部署方式

```bash
# WebUI版本快速启动
python start_webui.py
# 访问 http://localhost:8000
```

**详细文档**: [README_WebUI.md](README_WebUI.md)

### 🖤 命令行版本（经典）
- **⚡ 轻量级** - 纯命令行操作
- **🔧 配置文件驱动** - 通过INI文件配置
- **📱 适合自动化** - 脚本友好，资源占用低

```bash
# 命令行版本启动
python main.py
```

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

## 🎈项目结构

```
DouyinLiveRecorder/
├── /config -> 配置文件目录
├── /logs -> 日志文件目录
├── /downloads -> 录制视频保存目录
├── /douyinliverecorder -> 核心包
├── /web -> WebUI界面文件
├── main.py -> 命令行版本主程序
├── app.py -> WebUI版本主程序
├── start_webui.py -> WebUI智能启动脚本
└── requirements.txt -> 依赖库清单
```

## 🌱使用说明

### 快速开始

1. **下载程序**：进入[Releases](https://github.com/ihmily/DouyinLiveRecorder/releases)下载最新版本
2. **配置直播间**：在`config/URL_config.ini`中添加录制地址，一行一个
3. **启动程序**：
   - WebUI版本：运行`start_webui.py`，访问 http://localhost:8000
   - 命令行版本：运行`DouyinLiveRecorder.exe`或`main.py`

### 直播间链接示例

```
# 抖音
https://live.douyin.com/745964462470
https://v.douyin.com/iQFeBnt/

# TikTok
https://www.tiktok.com/@pearlgaga88/live

# 快手
https://live.kuaishou.com/u/yall1102

# 虎牙
https://www.huya.com/52333

# 斗鱼
https://www.douyu.com/3637778

# B站
https://live.bilibili.com/320

# 更多平台请参考完整文档...
```

### 高级配置

- **画质设置**：在链接前添加画质，如`超清，https://live.douyin.com/745964462470`
- **暂停录制**：在链接前添加`#`符号
- **代理设置**：海外平台需在配置文件中设置代理地址

## 🎃源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/ihmily/DouyinLiveRecorder.git
cd DouyinLiveRecorder

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 安装FFmpeg（Linux系统）
# Ubuntu/Debian
apt update && apt install ffmpeg
# CentOS
yum install epel-release && yum install ffmpeg

# 4. 运行程序
python main.py  # 命令行版本
python start_webui.py  # WebUI版本
```

## 🐋容器运行

```bash
# 快速启动
docker-compose up -d

# 或者单独运行
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/downloads:/app/downloads \
  ihmily/douyin-live-recorder:latest
```

## ❤️贡献者

[![Hmily](https://github.com/ihmily.png?size=50)](https://github.com/ihmily)
[![iridescentGray](https://github.com/iridescentGray.png?size=50)](https://github.com/iridescentGray)
[![annidy](https://github.com/annidy.png?size=50)](https://github.com/annidy)
[![wwkk2580](https://github.com/wwkk2580.png?size=50)](https://github.com/wwkk2580)
[![missuo](https://github.com/missuo.png?size=50)](https://github.com/missuo)
<a href="https://github.com/xueli12" target="_blank"><img src="https://github.com/xueli12.png?size=50" alt="xueli12" style="width:53px; height:51px;" /></a>
[![justdoiting](https://github.com/justdoiting.png?size=50)](https://github.com/justdoiting)
[![dhbxs](https://github.com/dhbxs.png?size=50)](https://github.com/dhbxs)

## ⏳最近更新

- **20250127** - 新增淘宝、京东、faceit直播录制；修复小红书直播流录制；重构包为异步函数
- **20241130** - 新增shopee、youtube直播录制；支持自定义m3u8、flv地址录制
- **20241030** - 新增10个直播平台；修复小红书直播录制；新增ntfy消息推送
- **20240928** - 新增知乎直播、CHZZK直播录制
- **20240903** - 新增抖音双屏录制、音播直播录制

<details><summary>点击查看完整更新日志</summary>

- 20240713 - 新增映客直播录制
- 20240705 - 新增时光直播录制
- 20240701 - 修复虎牙直播录制2分钟断流问题；新增自定义直播推送内容
- 20240621 - 新增Acfun、ShowRoom直播录制；修复微博录制
- 20240510 - 修复部分虎牙直播间录制错误
- 20240508 - 修复花椒直播录制
- 20240506 - 修复抖音录制画质解析bug；修复虎牙录制60帧问题
- 20240427 - 新增LiveMe、花椒直播录制
- 20240425 - 新增TwitchTV直播录制
- 20240424 - 新增酷狗直播录制、优化PopkonTV直播录制
- 20240423 - 新增百度直播录制、微博直播录制
- 20240311 - 修复海外平台录制bug，增加画质选择
- 20240309 - 修复虎牙、小红书、B站直播录制；新增5个直播平台
- 20240209 - 优化AfreecaTV录制；修复小红书直播录制

</details>

## 有问题可以提issue，欢迎Star ⭐
