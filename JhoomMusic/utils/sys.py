import os
import sys
import time
import psutil
import platform
from typing import Dict, Any

def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information"""
    try:
        # CPU Information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        
        # Memory Information
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk Information
        disk = psutil.disk_usage('/')
        
        # Network Information
        network = psutil.net_io_counters()
        
        # System Information
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        
        return {
            "system": {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "boot_time": boot_time,
                "uptime": uptime
            },
            "cpu": {
                "usage_percent": cpu_percent,
                "count_physical": cpu_count_physical,
                "count_logical": cpu_count_logical,
                "frequency_current": cpu_freq.current if cpu_freq else 0,
                "frequency_min": cpu_freq.min if cpu_freq else 0,
                "frequency_max": cpu_freq.max if cpu_freq else 0
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "free": memory.free,
                "percent": memory.percent,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_free": swap.free,
                "swap_percent": swap.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            },
            "network": {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
        }
    except Exception as e:
        print(f"Error getting system info: {e}")
        return {}

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    else:
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        return f"{days}d {hours}h"

def get_size(bytes_size: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"

def restart_bot():
    """Restart the bot"""
    try:
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Error restarting bot: {e}")
        sys.exit(1)

def get_bot_uptime() -> str:
    """Get bot uptime"""
    try:
        with open("bot_start_time.txt", "r") as f:
            start_time = float(f.read().strip())
        uptime = time.time() - start_time
        return get_readable_time(uptime)
    except:
        return "Unknown"

def save_bot_start_time():
    """Save bot start time"""
    try:
        with open("bot_start_time.txt", "w") as f:
            f.write(str(time.time()))
    except Exception as e:
        print(f"Error saving start time: {e}")