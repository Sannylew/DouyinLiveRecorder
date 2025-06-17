#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recording Service Module
Encapsulates the original recording logic from main.py into a service class
"""

import asyncio
import os
import sys
import subprocess
import threading
import time
import datetime
import re
import shutil
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import configparser

# Import original modules
from src import spider, stream
from src.utils import logger
from src import utils
from msg_push import dingtalk, xizhi, tg_bot, send_email, bark, ntfy
from ffmpeg_install import check_ffmpeg, ffmpeg_path, current_env_path

class RecordingService:
    """
    录制服务类，封装原main.py的录制逻辑
    """
    
    def __init__(self):
        self.recording_rooms: Dict[str, Dict] = {}  # 正在录制的房间
        self.monitoring = False
        self.monitor_thread = None
        self.config = self.load_config()
        self.script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.rstr = r"[\/\\\:\*\？?\"\<\>\|&#.。,， ~！· ]"
        self.recording_processes: Dict[str, subprocess.Popen] = {}
        
        # Set environment
        os.environ['PATH'] = ffmpeg_path + os.pathsep + current_env_path
        
    def load_config(self) -> configparser.ConfigParser:
        """加载配置文件"""
        config = configparser.ConfigParser()
        config_file = './config/config.ini'
        if os.path.exists(config_file):
            try:
                # 先读取文件内容
                with open(config_file, 'r', encoding='utf-8-sig') as f:
                    content = f.read()
                
                # 如果文件为空或只有BOM，创建默认配置
                if not content.strip():
                    self._create_default_config(config_file)
                    config.read(config_file, encoding='utf-8')
                else:
                    # 使用utf-8-sig编码自动处理BOM
                    config.read(config_file, encoding='utf-8-sig')
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
                # 如果读取失败，创建默认配置
                self._create_default_config(config_file)
                config.read(config_file, encoding='utf-8')
        else:
            # 配置文件不存在，创建默认配置
            self._create_default_config(config_file)
            config.read(config_file, encoding='utf-8')
        return config
    
    def _create_default_config(self, config_file: str):
        """创建默认配置文件"""
        default_config = """[录制设置]
原画|超清|高清|标清|流畅 = 原画
录制格式 = ts
录制码率 = 10000
录制时长 = 0
循环时间(秒) = 300
录制检测间隔 = 60
开启录制 = 是
开启推送 = 否
分段录制 = 否
分段时长(秒) = 3600
代理地址 = 
是否使用代理ip(是/否) = 否
录制结束后自动转换为mp4 = 否
只推送不录制 = 否
推送平台 = 钉钉
推送地址 = 
推送标题 = 【直播录制】
推送内容 = 
批量推送 = 否

[发送邮箱设置]
发送邮箱 = 
发送密码 = 
接收邮箱 = 
smtp地址 = 
smtp端口 = 587
ssl加密 = 是

[Cookie]
抖音cookie = 
快手cookie = 
虎牙cookie = 
斗鱼cookie = 
B站cookie = 
tiktok_cookie = 
"""
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(default_config)
        logger.info(f"Created default config file: {config_file}")
    
    def save_config(self):
        """保存配置文件"""
        config_file = './config/config.ini'
        with open(config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def read_config_value(self, section: str, option: str, default_value=None):
        """读取配置值"""
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
            return default_value
    
    def get_rooms_from_config(self) -> List[Dict]:
        """从配置文件中获取直播间列表"""
        rooms = []
        url_config_file = './config/URL_config.ini'
        
        if not os.path.exists(url_config_file):
            # 创建默认的URL配置文件
            os.makedirs(os.path.dirname(url_config_file), exist_ok=True)
            with open(url_config_file, 'w', encoding='utf-8') as f:
                f.write("# 添加直播间地址，一行一个\n# 格式：画质,地址,备注名\n# 示例：原画,https://live.douyin.com/123456,主播名\n")
            return rooms
            
        try:
            with open(url_config_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') and len(line.strip('#').strip()) < 18:
                        continue
                    
                    enabled = not line.startswith('#')
                    if not enabled:
                        line = line[1:].strip()
                    
                    # Parse quality,url,name format
                    if re.search('[,，]', line):
                        parts = re.split('[,，]', line)
                    else:
                        parts = [line, '']
                    
                    if len(parts) == 1:
                        url = parts[0]
                        quality, name = self.read_config_value('录制设置', '原画|超清|高清|标清|流畅', '原画'), ''
                    elif len(parts) == 2:
                        if self.contains_url(parts[0]):
                            quality = self.read_config_value('录制设置', '原画|超清|高清|标清|流畅', '原画')
                            url, name = parts
                        else:
                            quality, url = parts
                            name = ''
                    else:
                        quality, url, name = parts[0], parts[1], parts[2] if len(parts) > 2 else ''
                    
                    if quality not in ("原画", "蓝光", "超清", "高清", "标清", "流畅"):
                        quality = '原画'
                    
                    url = 'https://' + url if '://' not in url else url
                    
                    rooms.append({
                        'url': url,
                        'quality': quality,
                        'name': name,
                        'enabled': enabled,
                        'status': 'offline',
                        'recording': url in self.recording_rooms
                    })
        except Exception as e:
            logger.error(f"Error reading URL config file: {e}")
        
        return rooms
    
    def save_rooms_to_config(self, rooms: List[Dict]):
        """保存直播间列表到配置文件"""
        url_config_file = './config/URL_config.ini'
        with open(url_config_file, 'w', encoding='utf-8') as f:
            for room in rooms:
                prefix = "" if room['enabled'] else "#"
                line = f"{prefix}{room['quality']},{room['url']},{room['name']}\n"
                f.write(line)
    
    def contains_url(self, string: str) -> bool:
        """检查字符串是否包含URL"""
        pattern = r"(https?://)?(www\.)?[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+(:\d+)?(/.*)?"
        return re.search(pattern, string) is not None
    
    def clean_name(self, name: str) -> str:
        """清理文件名"""
        return re.sub(self.rstr, "_", name)
    
    def start_monitoring(self):
        """启动监控服务"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("Recording monitoring started")
            return True
        return False
    
    def stop_monitoring(self):
        """停止监控服务"""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=10)
            logger.info("Recording monitoring stopped")
            return True
        return False
    
    def _monitor_loop(self):
        """监控循环（后台线程）"""
        while self.monitoring:
            try:
                rooms = self.get_rooms_from_config()
                tasks = []
                
                for room in rooms:
                    if not room['enabled']:
                        continue
                    
                    # 创建异步任务检查直播状态
                    tasks.append(self._check_room_status(room))
                
                # 并发检查所有房间状态
                if tasks:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                    finally:
                        loop.close()
                
                # 获取循环间隔时间
                delay = int(self.read_config_value('录制设置', '循环时间(秒)', 300))
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                time.sleep(60)  # 出错后等待1分钟再重试
    
    async def _check_room_status(self, room: Dict):
        """检查单个房间的直播状态"""
        try:
            url = room['url']
            quality = room['quality']
            
            # 根据平台选择相应的spider函数
            platform_info = await self._get_platform_stream_data(url)
            
            if platform_info and platform_info.get('is_live'):
                # 直播中，开始录制
                if url not in self.recording_rooms:
                    await self._start_recording_room(room, platform_info)
            else:
                # 未直播，停止录制
                if url in self.recording_rooms:
                    await self._stop_recording_room(url)
                    
        except Exception as e:
            logger.error(f"Error checking room status for {room['url']}: {e}")
    
    async def _get_platform_stream_data(self, url: str) -> Optional[Dict]:
        """根据URL获取平台直播数据"""
        try:
            # 获取配置
            proxy_addr = self.read_config_value('录制设置', '代理地址', '')
            use_proxy = self.read_config_value('录制设置', '是否使用代理ip(是/否)', '否') == '是'
            proxy_address = proxy_addr if use_proxy else None
            
            # 根据URL判断平台并调用相应的spider函数
            if 'douyin.com' in url:
                cookie = self.read_config_value('Cookie', '抖音cookie', '')
                return await spider.get_douyin_app_stream_data(url, proxy_addr=proxy_address, cookies=cookie)
            
            elif 'kuaishou.com' in url:
                cookie = self.read_config_value('Cookie', '快手cookie', '')
                return await spider.get_kuaishou_stream_data(url, proxy_addr=proxy_address, cookies=cookie)
            
            elif 'huya.com' in url:
                cookie = self.read_config_value('Cookie', '虎牙cookie', '')
                return await spider.get_huya_app_stream_url(url, proxy_addr=proxy_address, cookies=cookie)
            
            elif 'douyu.com' in url:
                cookie = self.read_config_value('Cookie', '斗鱼cookie', '')
                return await spider.get_douyu_info_data(url, proxy_addr=proxy_address, cookies=cookie)
            
            elif 'bilibili.com' in url:
                cookie = self.read_config_value('Cookie', 'B站cookie', '')
                return await spider.get_bilibili_stream_data(url, proxy_addr=proxy_address, cookies=cookie)
            
            elif 'tiktok.com' in url:
                cookie = self.read_config_value('Cookie', 'tiktok_cookie', '')
                return await spider.get_tiktok_stream_data(url, proxy_addr=proxy_address, cookies=cookie)
            
            # 可以继续添加其他平台...
            
            else:
                logger.warning(f"Unsupported platform for URL: {url}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting platform stream data for {url}: {e}")
            return None
    
    async def _start_recording_room(self, room: Dict, stream_info: Dict):
        """开始录制房间"""
        try:
            url = room['url']
            quality = room['quality']
            
            # 获取录制URL
            record_url = stream_info.get('record_url') or stream_info.get('flv_url') or stream_info.get('m3u8_url')
            if not record_url:
                logger.error(f"No recording URL found for {url}")
                return
            
            # 生成文件名
            anchor_name = self.clean_name(stream_info.get('anchor_name', 'Unknown'))
            title = self.clean_name(stream_info.get('title', ''))
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 构建保存路径
            save_path = self._get_save_path(room, anchor_name)
            os.makedirs(save_path, exist_ok=True)
            
            # 文件名
            filename = f"{anchor_name}_{timestamp}"
            if title and self.read_config_value('录制设置', '保存文件名是否包含标题', '否') == '是':
                filename += f"_{title}"
            
            # 视频格式
            video_format = self.read_config_value('录制设置', '视频保存格式ts|mkv|flv|mp4|mp3音频|m4a音频', 'ts').upper()
            if video_format not in ['TS', 'MKV', 'FLV', 'MP4', 'MP3', 'M4A']:
                video_format = 'TS'
            
            file_path = os.path.join(save_path, f"{filename}.{video_format.lower()}")
            
            # 启动录制进程
            process = await self._start_ffmpeg_recording(record_url, file_path, video_format)
            
            if process:
                # 记录录制信息
                self.recording_rooms[url] = {
                    'room': room,
                    'stream_info': stream_info,
                    'start_time': datetime.datetime.now(),
                    'file_path': file_path,
                    'process': process,
                    'title': stream_info.get('title', ''),
                    'anchor_name': anchor_name,
                    'quality': quality
                }
                
                logger.info(f"Started recording: {url} -> {file_path}")
                
                # 发送开播通知
                await self._send_notification(room, stream_info, "开播")
                
        except Exception as e:
            logger.error(f"Error starting recording for {room['url']}: {e}")
    
    async def _stop_recording_room(self, url: str):
        """停止录制房间"""
        try:
            if url in self.recording_rooms:
                room_info = self.recording_rooms[url]
                process = room_info['process']
                
                # 终止录制进程
                if process and process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                
                # 处理录制完成的文件
                await self._post_process_recording(room_info)
                
                # 发送关播通知
                await self._send_notification(room_info['room'], room_info['stream_info'], "关播")
                
                # 移除录制记录
                del self.recording_rooms[url]
                
                logger.info(f"Stopped recording: {url}")
                
        except Exception as e:
            logger.error(f"Error stopping recording for {url}: {e}")
    
    def _get_save_path(self, room: Dict, anchor_name: str) -> str:
        """获取保存路径"""
        base_path = self.read_config_value('录制设置', '直播保存路径(不填则默认)', '')
        if not base_path:
            base_path = os.path.join(self.script_path, 'downloads')
        
        # 按作者分类
        if self.read_config_value('录制设置', '保存文件夹是否以作者区分', '是') == '是':
            base_path = os.path.join(base_path, anchor_name)
        
        # 按时间分类
        if self.read_config_value('录制设置', '保存文件夹是否以时间区分', '否') == '是':
            date_folder = datetime.datetime.now().strftime("%Y-%m")
            base_path = os.path.join(base_path, date_folder)
        
        # 按平台分类
        url = room['url']
        if 'douyin.com' in url:
            platform = '抖音'
        elif 'kuaishou.com' in url:
            platform = '快手'
        elif 'huya.com' in url:
            platform = '虎牙'
        elif 'douyu.com' in url:
            platform = '斗鱼'
        elif 'bilibili.com' in url:
            platform = 'B站'
        else:
            platform = '其他'
        
        base_path = os.path.join(base_path, platform)
        
        return base_path
    
    async def _start_ffmpeg_recording(self, stream_url: str, output_path: str, video_format: str) -> Optional[subprocess.Popen]:
        """启动FFmpeg录制进程"""
        try:
            # 构建FFmpeg命令
            ffmpeg_command = [
                "ffmpeg",
                "-i", stream_url,
                "-c", "copy",
                "-f", video_format.lower(),
                "-y",  # 覆盖输出文件
                output_path
            ]
            
            # 启动进程
            process = subprocess.Popen(
                ffmpeg_command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            return process
            
        except Exception as e:
            logger.error(f"Error starting FFmpeg: {e}")
            return None
    
    async def _post_process_recording(self, room_info: Dict):
        """录制后处理"""
        try:
            file_path = room_info['file_path']
            
            # 检查文件是否存在且有内容
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                logger.warning(f"Recording file is empty or missing: {file_path}")
                return
            
            # 转换格式（如果配置了）
            if self.read_config_value('录制设置', '录制完成后自动转为mp4格式', '否') == '是':
                await self._convert_to_mp4(file_path)
            
            # 生成字幕文件（如果配置了）
            if self.read_config_value('录制设置', '生成时间字幕文件', '否') == '是':
                await self._generate_subtitle(room_info)
                
        except Exception as e:
            logger.error(f"Error in post processing: {e}")
    
    async def _convert_to_mp4(self, file_path: str):
        """转换为MP4格式"""
        try:
            mp4_path = file_path.rsplit('.', 1)[0] + '.mp4'
            
            convert_command = [
                "ffmpeg",
                "-i", file_path,
                "-c", "copy",
                "-y",
                mp4_path
            ]
            
            process = subprocess.run(convert_command, capture_output=True)
            
            if process.returncode == 0:
                # 删除原文件（如果配置了）
                if self.read_config_value('录制设置', '追加格式后删除原文件', '否') == '是':
                    os.remove(file_path)
                logger.info(f"Converted to MP4: {mp4_path}")
            else:
                logger.error(f"Failed to convert to MP4: {file_path}")
                
        except Exception as e:
            logger.error(f"Error converting to MP4: {e}")
    
    async def _generate_subtitle(self, room_info: Dict):
        """生成字幕文件"""
        try:
            # 这里可以实现字幕生成逻辑
            # 目前只是占位符
            pass
        except Exception as e:
            logger.error(f"Error generating subtitle: {e}")
    
    async def _send_notification(self, room: Dict, stream_info: Dict, event_type: str):
        """发送通知"""
        try:
            push_channels = self.read_config_value('推送配置', '直播状态推送渠道', '')
            if not push_channels:
                return
            
            title = f"直播{event_type}通知"
            content = f"主播: {stream_info.get('anchor_name', '未知')}\n"
            content += f"房间: {room['url']}\n"
            content += f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            if '微信' in push_channels:
                api_url = self.read_config_value('推送配置', '微信推送接口链接', '')
                if api_url:
                    await xizhi(api_url, title, content)
            
            if '钉钉' in push_channels:
                api_url = self.read_config_value('推送配置', '钉钉推送接口链接', '')
                if api_url:
                    await dingtalk(api_url, title, content)
            
            # 可以添加更多推送渠道...
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    async def start_recording_manual(self, url: str) -> bool:
        """手动开始录制"""
        try:
            rooms = self.get_rooms_from_config()
            room = next((r for r in rooms if r['url'] == url), None)
            
            if not room:
                logger.error(f"Room not found: {url}")
                return False
            
            if url in self.recording_rooms:
                logger.warning(f"Room already recording: {url}")
                return False
            
            # 获取直播信息
            stream_info = await self._get_platform_stream_data(url)
            if not stream_info or not stream_info.get('is_live'):
                logger.warning(f"Room is not live: {url}")
                return False
            
            await self._start_recording_room(room, stream_info)
            return True
            
        except Exception as e:
            logger.error(f"Error starting manual recording for {url}: {e}")
            return False
    
    async def stop_recording_manual(self, url: str) -> bool:
        """手动停止录制"""
        try:
            if url not in self.recording_rooms:
                logger.warning(f"Room not recording: {url}")
                return False
            
            await self._stop_recording_room(url)
            return True
            
        except Exception as e:
            logger.error(f"Error stopping manual recording for {url}: {e}")
            return False
    
    def get_recording_status(self) -> Dict:
        """获取录制状态"""
        rooms = self.get_rooms_from_config()
        recording_count = len(self.recording_rooms)
        total_rooms = len([r for r in rooms if r['enabled']])
        
        return {
            "monitoring": self.monitoring,
            "total_rooms": total_rooms,
            "recording_count": recording_count,
            "recording_rooms": list(self.recording_rooms.keys())
        }
    
    def cleanup(self):
        """清理资源"""
        # 停止监控
        self.stop_monitoring()
        
        # 停止所有录制
        for url in list(self.recording_rooms.keys()):
            asyncio.run(self._stop_recording_room(url))
        
        logger.info("Recording service cleaned up")

# 全局录制服务实例
recording_service = RecordingService() 