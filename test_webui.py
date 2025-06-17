#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for DouyinLiveRecorder WebUI
"""

import requests
import json
import time

def test_webui():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing DouyinLiveRecorder WebUI...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Test 2: Get system status
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ System status: {status}")
        else:
            print(f"❌ Failed to get status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting status: {e}")
    
    # Test 3: Get rooms list
    try:
        response = requests.get(f"{base_url}/api/rooms")
        if response.status_code == 200:
            rooms = response.json()
            print(f"✅ Rooms list retrieved: {len(rooms.get('rooms', []))} rooms")
        else:
            print(f"❌ Failed to get rooms: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting rooms: {e}")
    
    # Test 4: Add a test room
    test_room = {
        "url": "https://live.douyin.com/test",
        "quality": "原画",
        "name": "测试直播间"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/rooms",
            json=test_room,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Test room added successfully")
            
            # Test 5: Delete the test room
            import urllib.parse
            encoded_url = urllib.parse.quote(test_room["url"], safe='')
            response = requests.delete(f"{base_url}/api/rooms/{encoded_url}")
            
            if response.status_code == 200:
                print("✅ Test room deleted successfully")
            else:
                print(f"❌ Failed to delete test room: {response.status_code}")
                
        else:
            print(f"❌ Failed to add test room: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error with room operations: {e}")
    
    # Test 6: Get configuration
    try:
        response = requests.get(f"{base_url}/api/config")
        if response.status_code == 200:
            config = response.json()
            print(f"✅ Configuration retrieved: {len(config)} sections")
        else:
            print(f"❌ Failed to get config: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting config: {e}")
    
    # Test 7: Get files list
    try:
        response = requests.get(f"{base_url}/api/files")
        if response.status_code == 200:
            files = response.json()
            print(f"✅ Files list retrieved: {len(files.get('files', []))} files")
        else:
            print(f"❌ Failed to get files: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting files: {e}")
    
    print("\n🎉 WebUI testing completed!")

if __name__ == "__main__":
    test_webui() 