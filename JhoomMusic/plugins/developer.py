import os
import sys
import asyncio
import subprocess
from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.misc import SUDOERS
from JhoomMusic.utils.pastebin import paste
from config import BANNED_USERS, OWNER_ID

@app.on_message(filters.command(["eval", "py"]) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def eval_code(client, message: Message):
    """Execute Python code (Owner only)"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/eval <code>` - Execute Python code\n"
            "• `/eval` (reply to code) - Execute replied code"
        )
    
    # Get code to execute
    if message.reply_to_message:
        code = message.reply_to_message.text
    else:
        code = " ".join(message.command[1:])
    
    if not code:
        return await message.reply_text("❌ **No code provided!**")
    
    mystic = await message.reply_text("🔄 **Executing code...**")
    
    try:
        # Prepare execution environment
        exec_globals = {
            'app': app,
            'client': client,
            'message': message,
            'chat': message.chat,
            'user': message.from_user,
            'asyncio': asyncio,
            'os': os,
            'sys': sys
        }
        
        # Execute code
        if code.startswith('await '):
            # Async code
            result = await eval(code[6:], exec_globals)
        else:
            # Sync code
            result = eval(code, exec_globals)
        
        # Format result
        if result is None:
            output = "✅ **Code executed successfully (no output)**"
        else:
            output = f"**Result:**\n```python\n{result}\n```"
        
        if len(output) > 4000:
            paste_url = await paste(str(result), "Python Eval Result")
            if paste_url:
                await mystic.edit_text(
                    f"✅ **Code executed successfully!**\n\n"
                    f"**Result:** {paste_url}"
                )
            else:
                await mystic.edit_text("✅ **Code executed (result too long)**")
        else:
            await mystic.edit_text(output)
    
    except Exception as e:
        error_text = f"❌ **Error:**\n```python\n{str(e)}\n```"
        
        if len(error_text) > 4000:
            paste_url = await paste(str(e), "Python Eval Error")
            if paste_url:
                await mystic.edit_text(
                    f"❌ **Execution failed!**\n\n"
                    f"**Error:** {paste_url}"
                )
            else:
                await mystic.edit_text("❌ **Execution failed (error too long)**")
        else:
            await mystic.edit_text(error_text)

@app.on_message(filters.command(["exec", "bash"]) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def exec_code(client, message: Message):
    """Execute Python code with exec (Owner only)"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/exec <code>` - Execute Python code with exec\n"
            "• `/exec` (reply to code) - Execute replied code"
        )
    
    # Get code to execute
    if message.reply_to_message:
        code = message.reply_to_message.text
    else:
        code = " ".join(message.command[1:])
    
    if not code:
        return await message.reply_text("❌ **No code provided!**")
    
    mystic = await message.reply_text("🔄 **Executing code...**")
    
    try:
        # Prepare execution environment
        exec_globals = {
            'app': app,
            'client': client,
            'message': message,
            'chat': message.chat,
            'user': message.from_user,
            'asyncio': asyncio,
            'os': os,
            'sys': sys,
            'print': print
        }
        
        # Capture output
        import io
        import contextlib
        
        output_buffer = io.StringIO()
        
        with contextlib.redirect_stdout(output_buffer):
            if 'await ' in code:
                # Async code
                exec(f"async def __exec_func():\n" + "\n".join(f"    {line}" for line in code.split('\n')), exec_globals)
                await exec_globals['__exec_func']()
            else:
                # Sync code
                exec(code, exec_globals)
        
        output = output_buffer.getvalue()
        
        if not output:
            output = "✅ **Code executed successfully (no output)**"
        else:
            output = f"**Output:**\n```\n{output}\n```"
        
        if len(output) > 4000:
            paste_url = await paste(output, "Python Exec Output")
            if paste_url:
                await mystic.edit_text(
                    f"✅ **Code executed successfully!**\n\n"
                    f"**Output:** {paste_url}"
                )
            else:
                await mystic.edit_text("✅ **Code executed (output too long)**")
        else:
            await mystic.edit_text(output)
    
    except Exception as e:
        error_text = f"❌ **Error:**\n```python\n{str(e)}\n```"
        
        if len(error_text) > 4000:
            paste_url = await paste(str(e), "Python Exec Error")
            if paste_url:
                await mystic.edit_text(
                    f"❌ **Execution failed!**\n\n"
                    f"**Error:** {paste_url}"
                )
            else:
                await mystic.edit_text("❌ **Execution failed (error too long)**")
        else:
            await mystic.edit_text(error_text)

@app.on_message(filters.command(["gitpull", "pull"]) & SUDOERS & ~BANNED_USERS)
async def git_pull(client, message: Message):
    """Pull latest changes from git"""
    
    mystic = await message.reply_text("🔄 **Pulling latest changes...**")
    
    try:
        if not os.path.exists(".git"):
            return await mystic.edit_text("❌ **Not a git repository!**")
        
        # Execute git pull
        process = await asyncio.create_subprocess_shell(
            "git pull origin main",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        output = ""
        if stdout:
            output += f"**Output:**\n```\n{stdout.decode().strip()}\n```\n"
        if stderr:
            output += f"**Error:**\n```\n{stderr.decode().strip()}\n```"
        
        if process.returncode == 0:
            if "Already up to date" in stdout.decode():
                await mystic.edit_text("✅ **Repository is already up to date!**")
            else:
                await mystic.edit_text(
                    f"✅ **Successfully pulled changes!**\n\n{output}\n\n"
                    f"**Use `/restart` to apply changes**"
                )
        else:
            await mystic.edit_text(f"❌ **Git pull failed!**\n\n{output}")
    
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["speedtest", "speed"]) & SUDOERS & ~BANNED_USERS)
async def speed_test(client, message: Message):
    """Run internet speed test"""
    
    mystic = await message.reply_text("🔄 **Running speed test...**")
    
    try:
        import speedtest
        
        st = speedtest.Speedtest()
        
        # Get best server
        await mystic.edit_text("🔄 **Finding best server...**")
        st.get_best_server()
        
        # Download test
        await mystic.edit_text("🔄 **Testing download speed...**")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # Upload test
        await mystic.edit_text("🔄 **Testing upload speed...**")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # Ping test
        ping = st.results.ping
        
        # Server info
        server = st.results.server
        
        result_text = f"""
🌐 **Internet Speed Test Results**

**📊 Speed:**
• **Download:** {download_speed:.2f} Mbps
• **Upload:** {upload_speed:.2f} Mbps
• **Ping:** {ping:.2f} ms

**🖥️ Server:**
• **Name:** {server['name']}
• **Country:** {server['country']}
• **Sponsor:** {server['sponsor']}

**📍 Location:**
• **Distance:** {server['d']:.2f} km
"""
        
        await mystic.edit_text(result_text)
    
    except ImportError:
        await mystic.edit_text(
            "❌ **Speedtest module not installed!**\n\n"
            "Install with: `pip install speedtest-cli`"
        )
    except Exception as e:
        await mystic.edit_text(f"❌ **Speed test failed:** {str(e)}")

@app.on_message(filters.command(["pip"]) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def pip_install(client, message: Message):
    """Install Python packages with pip"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/pip <package_name>`\n\n"
            "**Example:** `/pip requests`"
        )
    
    package = " ".join(message.command[1:])
    mystic = await message.reply_text(f"📦 **Installing {package}...**")
    
    try:
        process = await asyncio.create_subprocess_shell(
            f"pip install {package}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        output = ""
        if stdout:
            output += f"**Output:**\n```\n{stdout.decode().strip()}\n```\n"
        if stderr:
            output += f"**Error:**\n```\n{stderr.decode().strip()}\n```"
        
        if process.returncode == 0:
            await mystic.edit_text(f"✅ **Successfully installed {package}!**\n\n{output}")
        else:
            await mystic.edit_text(f"❌ **Failed to install {package}!**\n\n{output}")
    
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["db", "database"]) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def database_info(client, message: Message):
    """Show database information"""
    
    mystic = await message.reply_text("📊 **Getting database info...**")
    
    try:
        from JhoomMusic.utils.database.database import temp_db
        
        # Get database stats
        stats = await temp_db.command("dbStats")
        
        # Get collection info
        collections = await temp_db.list_collection_names()
        
        db_text = f"""
📊 **Database Information**

**📈 Statistics:**
• **Database:** {stats.get('db', 'Unknown')}
• **Collections:** {stats.get('collections', 0)}
• **Objects:** {stats.get('objects', 0)}
• **Data Size:** {stats.get('dataSize', 0) / 1024 / 1024:.2f} MB
• **Storage Size:** {stats.get('storageSize', 0) / 1024 / 1024:.2f} MB

**📋 Collections:**
"""
        
        for collection in collections:
            count = await temp_db[collection].count_documents({})
            db_text += f"• **{collection}:** {count} documents\n"
        
        await mystic.edit_text(db_text)
    
    except Exception as e:
        await mystic.edit_text(f"❌ **Error getting database info:** {str(e)}")