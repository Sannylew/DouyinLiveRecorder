#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DouyinLiveRecorder WebUI Version
Author: Modified for WebUI
Date: 2025-01-XX
Function: Web interface for live stream recording
"""

import asyncio
import json
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import configparser

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    import uvicorn
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import HTMLResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
except ImportError as e:
    print(f"❌ 缺少必要依赖: {e}")
    print("请运行: pip install -r requirements_webui.txt")
    sys.exit(1)

# Import recording service with error handling
try:
    from recording_service import recording_service
except ImportError as e:
    print(f"❌ 无法导入录制服务: {e}")
    print("请确保recording_service.py文件存在")
    sys.exit(1)

# Global variables for recording state
app = FastAPI(title="DouyinLiveRecorder WebUI", version="4.0.3")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class LiveRoomAdd(BaseModel):
    url: str
    quality: str = "原画"
    name: str = ""

class LiveRoomUpdate(BaseModel):
    url: str
    quality: Optional[str] = None
    name: Optional[str] = None
    enabled: Optional[bool] = None

class ConfigUpdate(BaseModel):
    section: str
    key: str
    value: str

# API Routes
@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main web interface"""
    return FileResponse("web/index.html")

@app.get("/api/rooms")
async def get_rooms():
    """Get all configured rooms"""
    rooms = recording_service.get_rooms_from_config()
    
    # Add recording status
    for room in rooms:
        url = room['url']
        if url in recording_service.recording_rooms:
            room['recording'] = True
            room['status'] = 'recording'
            room['start_time'] = recording_service.recording_rooms[url]['start_time'].isoformat()
        else:
            room['recording'] = False
            room['status'] = 'offline'
    
    return {"rooms": rooms}

@app.post("/api/rooms")
async def add_room(room: LiveRoomAdd):
    """Add a new room to monitor"""
    rooms = recording_service.get_rooms_from_config()
    
    # Check if room already exists
    for existing_room in rooms:
        if existing_room['url'] == room.url:
            raise HTTPException(status_code=400, detail="Room already exists")
    
    new_room = {
        'url': room.url,
        'quality': room.quality,
        'name': room.name,
        'enabled': True,
        'status': 'offline',
        'recording': False
    }
    
    rooms.append(new_room)
    recording_service.save_rooms_to_config(rooms)
    
    return {"message": "Room added successfully", "room": new_room}

@app.put("/api/rooms/{room_url:path}")
async def update_room(room_url: str, update: LiveRoomUpdate):
    """Update room configuration"""
    rooms = recording_service.get_rooms_from_config()
    
    for room in rooms:
        if room['url'] == room_url:
            if update.quality is not None:
                room['quality'] = update.quality
            if update.name is not None:
                room['name'] = update.name
            if update.enabled is not None:
                room['enabled'] = update.enabled
            
            recording_service.save_rooms_to_config(rooms)
            return {"message": "Room updated successfully", "room": room}
    
    raise HTTPException(status_code=404, detail="Room not found")

@app.delete("/api/rooms/{room_url:path}")
async def delete_room(room_url: str):
    """Delete a room"""
    rooms = recording_service.get_rooms_from_config()
    
    # Remove from recording if active
    if room_url in recording_service.recording_rooms:
        await recording_service.stop_recording_manual(room_url)
    
    # Remove from config
    rooms = [room for room in rooms if room['url'] != room_url]
    recording_service.save_rooms_to_config(rooms)
    
    return {"message": "Room deleted successfully"}

@app.post("/api/rooms/{room_url:path}/start")
async def start_recording(room_url: str):
    """Manually start recording a room"""
    success = await recording_service.start_recording_manual(room_url)
    if success:
        return {"message": f"Recording started for {room_url}"}
    else:
        raise HTTPException(status_code=400, detail="Failed to start recording")

@app.post("/api/rooms/{room_url:path}/stop")
async def stop_recording(room_url: str):
    """Manually stop recording a room"""
    success = await recording_service.stop_recording_manual(room_url)
    if success:
        return {"message": f"Recording stopped for {room_url}"}
    else:
        raise HTTPException(status_code=404, detail="Room not recording")

@app.get("/api/status")
async def get_status():
    """Get overall system status"""
    return recording_service.get_recording_status()

@app.post("/api/start-monitoring")
async def start_monitoring():
    """Start the monitoring service"""
    success = recording_service.start_monitoring()
    if success:
        return {"message": "Monitoring started"}
    else:
        return {"message": "Monitoring already running"}

@app.post("/api/stop-monitoring")
async def stop_monitoring():
    """Stop the monitoring service"""
    success = recording_service.stop_monitoring()
    if success:
        return {"message": "Monitoring stopped"}
    else:
        return {"message": "Monitoring already stopped"}

@app.get("/api/config")
async def get_config():
    """Get current configuration"""
    config_dict = {}
    for section in recording_service.config.sections():
        config_dict[section] = dict(recording_service.config.items(section))
    return config_dict

@app.put("/api/config")
async def update_config(config_update: ConfigUpdate):
    """Update configuration"""
    if not recording_service.config.has_section(config_update.section):
        recording_service.config.add_section(config_update.section)
    
    recording_service.config.set(config_update.section, config_update.key, config_update.value)
    recording_service.save_config()
    
    return {"message": "Configuration updated"}

@app.get("/api/logs")
async def get_logs():
    """Get recent log entries"""
    try:
        log_file = Path("logs") / "app.log"
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Return last 100 lines
                return {"logs": lines[-100:]}
        else:
            return {"logs": ["No log file found"]}
    except Exception as e:
        return {"logs": [f"Error reading logs: {e}"]}

@app.get("/api/files") 
async def get_files():
    """Get list of recorded files"""
    downloads_dir = Path("downloads")
    if not downloads_dir.exists():
        return {"files": []}
    
    files = []
    for file_path in downloads_dir.glob("**/*"):
        if file_path.is_file() and file_path.suffix.lower() in ['.mp4', '.ts', '.flv', '.mkv', '.m4a', '.mp3']:
            files.append({
                "name": file_path.name,
                "path": str(file_path.relative_to(downloads_dir)),
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime
            })
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x['modified'], reverse=True)
    return {"files": files}

@app.get("/api/files/{file_path:path}")
async def download_file(file_path: str):
    """Download a recorded file"""
    full_path = Path("downloads") / file_path
    if full_path.exists() and full_path.is_file():
        return FileResponse(
            path=str(full_path),
            filename=full_path.name,
            media_type='application/octet-stream'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")

# Mount static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup when shutting down"""
    recording_service.cleanup()

def main():
    """Main entry point for WebUI version"""
    print("🚀 Starting DouyinLiveRecorder WebUI...")
    print("📱 Web interface will be available at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop")
    
    # Ensure directories exist
    os.makedirs("config", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("web", exist_ok=True)
    os.makedirs("web/static", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Start the web server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        access_log=True
    )

if __name__ == "__main__":
    main() 