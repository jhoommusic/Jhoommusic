import os
import sys
import asyncio
from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.misc import SUDOERS
from JhoomMusic.utils.sys import restart_bot, get_system_info, get_readable_time
from JhoomMusic.utils.pastebin import paste
from config import BANNED_USERS

@app.on_message(filters.command(["restart", "reboot"]) & SUDOERS & ~BANNED_USERS)
async def restart_command(client, message: Message):
    """Restart the bot"""
    
    mystic = await message.reply_text("🔄 **Restarting Bot...**")
    
    try:
        await mystic.edit_text(
            "✅ **Bot Restarted Successfully!**\n\n"
            "**The bot will be back online in a few seconds.**"
        )
        
        # Small delay before restart
        await asyncio.sleep(2)
        restart_bot()
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Restart Failed:** {str(e)}")

@app.on_message(filters.command(["logs", "log"]) & SUDOERS & ~BANNED_USERS)
async def logs_command(client, message: Message):
    """Get bot logs"""
    
    mystic = await message.reply_text("📝 **Getting logs...**")
    
    try:
        if os.path.exists("log.txt"):
            with open("log.txt", "r") as f:
                logs = f.read()
            
            if len(logs) > 4000:
                # Upload to pastebin if too long
                paste_url = await paste(logs, "JhoomMusic Bot Logs")
                if paste_url:
                    await mystic.edit_text(
                        f"📝 **Bot Logs**\n\n"
                        f"**Logs are too long, uploaded to:** {paste_url}"
                    )
                else:
                    # Send as file
                    await message.reply_document(
                        "log.txt",
                        caption="📝 **Bot Logs**"
                    )
                    await mystic.delete()
            else:
                await mystic.edit_text(f"📝 **Bot Logs:**\n\n```\n{logs}\n```")
        else:
            await mystic.edit_text("❌ **No log file found!**")
            
    except Exception as e:
        await mystic.edit_text(f"❌ **Error getting logs:** {str(e)}")

@app.on_message(filters.command(["update"]) & SUDOERS & ~BANNED_USERS)
async def update_command(client, message: Message):
    """Update the bot"""
    
    mystic = await message.reply_text("🔄 **Checking for updates...**")
    
    try:
        # Check if git is available
        if not os.path.exists(".git"):
            return await mystic.edit_text("❌ **Git repository not found!**")
        
        # Pull latest changes
        process = await asyncio.create_subprocess_shell(
            "git pull origin main",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            output = stdout.decode().strip()
            if "Already up to date" in output:
                await mystic.edit_text("✅ **Bot is already up to date!**")
            else:
                await mystic.edit_text(
                    "✅ **Bot updated successfully!**\n\n"
                    "**Restarting bot to apply changes...**"
                )
                await asyncio.sleep(2)
                restart_bot()
        else:
            error = stderr.decode().strip()
            await mystic.edit_text(f"❌ **Update failed:**\n```\n{error}\n```")
            
    except Exception as e:
        await mystic.edit_text(f"❌ **Error updating bot:** {str(e)}")

@app.on_message(filters.command(["maintenance"]) & SUDOERS & ~BANNED_USERS)
async def maintenance_command(client, message: Message):
    """Toggle maintenance mode"""
    
    # This is a placeholder for maintenance mode
    # You can implement actual maintenance logic here
    
    await message.reply_text(
        "🛠️ **Maintenance Mode**\n\n"
        "**This feature is under development.**\n"
        "**Use `/restart` to restart the bot.**"
    )

@app.on_message(filters.command(["sysinfo", "system"]) & SUDOERS & ~BANNED_USERS)
async def system_info_command(client, message: Message):
    """Get system information"""
    
    mystic = await message.reply_text("💻 **Getting system information...**")
    
    try:
        sys_info = get_system_info()
        
        if not sys_info:
            return await mystic.edit_text("❌ **Failed to get system information!**")
        
        system = sys_info.get("system", {})
        cpu = sys_info.get("cpu", {})
        memory = sys_info.get("memory", {})
        disk = sys_info.get("disk", {})
        
        info_text = f"""
💻 **System Information**

**🖥️ System:**
• **OS:** {system.get('platform', 'Unknown')} {system.get('platform_release', '')}
• **Architecture:** {system.get('architecture', 'Unknown')}
• **Python:** {system.get('python_version', 'Unknown')}
• **Uptime:** {get_readable_time(int(system.get('uptime', 0)))}

**🔧 CPU:**
• **Usage:** {cpu.get('usage_percent', 0)}%
• **Cores:** {cpu.get('count_physical', 0)} physical, {cpu.get('count_logical', 0)} logical

**💾 Memory:**
• **Total:** {memory.get('total', 0) // (1024**3):.1f} GB
• **Used:** {memory.get('used', 0) // (1024**3):.1f} GB ({memory.get('percent', 0)}%)
• **Available:** {memory.get('available', 0) // (1024**3):.1f} GB

**💽 Disk:**
• **Total:** {disk.get('total', 0) // (1024**3):.1f} GB
• **Used:** {disk.get('used', 0) // (1024**3):.1f} GB ({disk.get('percent', 0)}%)
• **Free:** {disk.get('free', 0) // (1024**3):.1f} GB
"""
        
        await mystic.edit_text(info_text)
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Error getting system info:** {str(e)}")

@app.on_message(filters.command(["shell", "sh"]) & SUDOERS & ~BANNED_USERS)
async def shell_command(client, message: Message):
    """Execute shell commands"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/shell <command>`\n\n"
            "**Example:** `/shell ls -la`"
        )
    
    command = " ".join(message.command[1:])
    mystic = await message.reply_text(f"🔄 **Executing:** `{command}`")
    
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        output = ""
        if stdout:
            output += f"**Output:**\n```\n{stdout.decode().strip()}\n```\n"
        if stderr:
            output += f"**Error:**\n```\n{stderr.decode().strip()}\n```"
        
        if not output:
            output = "✅ **Command executed successfully (no output)**"
        
        if len(output) > 4000:
            paste_url = await paste(output, f"Shell Command: {command}")
            if paste_url:
                await mystic.edit_text(
                    f"📝 **Command Output**\n\n"
                    f"**Command:** `{command}`\n"
                    f"**Output:** {paste_url}"
                )
            else:
                await mystic.edit_text("❌ **Output too long and failed to upload!**")
        else:
            await mystic.edit_text(f"**Command:** `{command}`\n\n{output}")
            
    except Exception as e:
        await mystic.edit_text(f"❌ **Error executing command:** {str(e)}")