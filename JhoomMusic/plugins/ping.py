import time
import psutil
import platform
from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JhoomMusic import app
from config import BANNED_USERS, PING_IMG_URL, BOT_NAME

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format"""
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    
    time_list.reverse()
    ping_time += ":".join(time_list)
    
    return ping_time

@app.on_message(filters.command(["ping", "alive"]) & ~filters.user(BANNED_USERS))
async def ping_pong(client, message: Message):
    """Handle ping command"""
    start = time.time()
    response = await message.reply_text("🏓 **Pinging...**")
    end = time.time()
    
    ping_time = round((end - start) * 1000, 2)
    
    # Get system info
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime = get_readable_time(int(uptime_seconds))
    
    await response.edit_text(
        f"🏓 **Pong!**\n\n"
        f"📊 **Bot Statistics:**\n"
        f"• **Ping:** `{ping_time}ms`\n"
        f"• **Uptime:** `{uptime}`\n"
        f"• **Bot Name:** {BOT_NAME}\n"
        f"• **Python Version:** `{platform.python_version()}`\n"
        f"• **Platform:** `{platform.system()} {platform.release()}`\n\n"
        f"💻 **System Resources:**\n"
        f"• **CPU Usage:** `{cpu_percent}%`\n"
        f"• **RAM Usage:** `{memory.percent}%`\n"
        f"• **Disk Usage:** `{disk.percent}%`\n"
        f"• **Total RAM:** `{round(memory.total / (1024**3), 2)} GB`\n"
        f"• **Available RAM:** `{round(memory.available / (1024**3), 2)} GB`",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🆘 Support", url="https://t.me/JhoomMusicSupport"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/JhoomMusicChannel")
            ],
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="ping_refresh")
            ]
        ])
    )

@app.on_callback_query(filters.regex("ping_refresh"))
async def ping_refresh(client, callback_query):
    """Handle ping refresh callback"""
    start = time.time()
    end = time.time()
    
    ping_time = round((end - start) * 1000, 2)
    
    # Get system info
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime = get_readable_time(int(uptime_seconds))
    
    await callback_query.message.edit_text(
        f"🏓 **Pong!**\n\n"
        f"📊 **Bot Statistics:**\n"
        f"• **Ping:** `{ping_time}ms`\n"
        f"• **Uptime:** `{uptime}`\n"
        f"• **Bot Name:** {BOT_NAME}\n"
        f"• **Python Version:** `{platform.python_version()}`\n"
        f"• **Platform:** `{platform.system()} {platform.release()}`\n\n"
        f"💻 **System Resources:**\n"
        f"• **CPU Usage:** `{cpu_percent}%`\n"
        f"• **RAM Usage:** `{memory.percent}%`\n"
        f"• **Disk Usage:** `{disk.percent}%`\n"
        f"• **Total RAM:** `{round(memory.total / (1024**3), 2)} GB`\n"
        f"• **Available RAM:** `{round(memory.available / (1024**3), 2)} GB`",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🆘 Support", url="https://t.me/JhoomMusicSupport"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/JhoomMusicChannel")
            ],
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="ping_refresh")
            ]
        ])
    )
    
    await callback_query.answer("🔄 Stats refreshed!")

@app.on_message(filters.command(["stats", "statistics"]) & ~filters.user(BANNED_USERS))
async def bot_stats(client, message: Message):
    """Show detailed bot statistics"""
    # Get system info
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime = get_readable_time(int(uptime_seconds))
    
    # Get network info
    network = psutil.net_io_counters()
    
    stats_text = f"""
📊 **Detailed Bot Statistics**

🖥️ **System Information:**
• **OS:** `{platform.system()} {platform.release()}`
• **Architecture:** `{platform.machine()}`
• **Processor:** `{platform.processor()}`
• **Python Version:** `{platform.python_version()}`

⏱️ **Uptime Information:**
• **System Uptime:** `{uptime}`
• **Boot Time:** `{datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}`

💾 **Memory Usage:**
• **Total RAM:** `{round(memory.total / (1024**3), 2)} GB`
• **Used RAM:** `{round(memory.used / (1024**3), 2)} GB`
• **Available RAM:** `{round(memory.available / (1024**3), 2)} GB`
• **RAM Usage:** `{memory.percent}%`

💽 **Disk Usage:**
• **Total Disk:** `{round(disk.total / (1024**3), 2)} GB`
• **Used Disk:** `{round(disk.used / (1024**3), 2)} GB`
• **Free Disk:** `{round(disk.free / (1024**3), 2)} GB`
• **Disk Usage:** `{disk.percent}%`

🌐 **Network Statistics:**
• **Bytes Sent:** `{round(network.bytes_sent / (1024**2), 2)} MB`
• **Bytes Received:** `{round(network.bytes_recv / (1024**2), 2)} MB`

🔧 **CPU Information:**
• **CPU Usage:** `{cpu_percent}%`
• **CPU Cores:** `{psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical`
"""
    
    await message.reply_text(
        stats_text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Refresh Stats", callback_data="stats_refresh")
            ]
        ])
    )

@app.on_callback_query(filters.regex("stats_refresh"))
async def stats_refresh(client, callback_query):
    """Handle stats refresh callback"""
    # Get system info
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime = get_readable_time(int(uptime_seconds))
    
    # Get network info
    network = psutil.net_io_counters()
    
    stats_text = f"""
📊 **Detailed Bot Statistics**

🖥️ **System Information:**
• **OS:** `{platform.system()} {platform.release()}`
• **Architecture:** `{platform.machine()}`
• **Processor:** `{platform.processor()}`
• **Python Version:** `{platform.python_version()}`

⏱️ **Uptime Information:**
• **System Uptime:** `{uptime}`
• **Boot Time:** `{datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}`

💾 **Memory Usage:**
• **Total RAM:** `{round(memory.total / (1024**3), 2)} GB`
• **Used RAM:** `{round(memory.used / (1024**3), 2)} GB`
• **Available RAM:** `{round(memory.available / (1024**3), 2)} GB`
• **RAM Usage:** `{memory.percent}%`

💽 **Disk Usage:**
• **Total Disk:** `{round(disk.total / (1024**3), 2)} GB`
• **Used Disk:** `{round(disk.used / (1024**3), 2)} GB`
• **Free Disk:** `{round(disk.free / (1024**3), 2)} GB`
• **Disk Usage:** `{disk.percent}%`

🌐 **Network Statistics:**
• **Bytes Sent:** `{round(network.bytes_sent / (1024**2), 2)} MB`
• **Bytes Received:** `{round(network.bytes_recv / (1024**2), 2)} MB`

🔧 **CPU Information:**
• **CPU Usage:** `{cpu_percent}%`
• **CPU Cores:** `{psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical`
"""
    
    await callback_query.message.edit_text(
        stats_text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Refresh Stats", callback_data="stats_refresh")
            ]
        ])
    )
    
    await callback_query.answer("🔄 Statistics refreshed!")