<div align="center">
  <img src="images/file-HYLKSWrPaUzdU9vvnyxGif.webp" alt="JhoomMusic Banner" width="100%">
  
  <h1>🎵 JhoomMusic - Telegram Music Bot</h1>
  
  <p><strong>A powerful Telegram music bot that can play high-quality music in voice chats with advanced features like queue management, admin controls, and live streaming support.</strong></p>
  
  <p>
    <a href="https://github.com/yourusername/JhoomMusic/stargazers"><img src="https://img.shields.io/github/stars/yourusername/JhoomMusic?color=yellow&style=for-the-badge" alt="Stars"></a>
    <a href="https://github.com/yourusername/JhoomMusic/network/members"><img src="https://img.shields.io/github/forks/yourusername/JhoomMusic?color=orange&style=for-the-badge" alt="Forks"></a>
    <a href="https://github.com/yourusername/JhoomMusic/issues"><img src="https://img.shields.io/github/issues/yourusername/JhoomMusic?color=red&style=for-the-badge" alt="Issues"></a>
    <a href="https://github.com/yourusername/JhoomMusic/blob/main/LICENSE"><img src="https://img.shields.io/github/license/yourusername/JhoomMusic?color=blue&style=for-the-badge" alt="License"></a>
  </p>
  
  <p>
    <a href="https://t.me/JhoomMusicSupport"><img src="https://img.shields.io/badge/Support-Group-blue?style=for-the-badge&logo=telegram" alt="Support Group"></a>
    <a href="https://t.me/JhoomMusicChannel"><img src="https://img.shields.io/badge/Updates-Channel-blue?style=for-the-badge&logo=telegram" alt="Updates Channel"></a>
  </p>
</div>

---

## 🌟 Features

- 🎵 **High Quality Music Streaming**
- 🎬 **Video Playback Support**
- 📱 **Live Stream Support**
- 🎛️ **Advanced Queue Management**
- 👥 **Admin Controls**
- 🔐 **Authorization System**
- 📊 **Statistics & Analytics**
- 🌍 **Multi-language Support**
- 🎨 **Beautiful UI with Inline Buttons**
- ⚡ **Fast and Reliable**

## 🚀 Quick Deploy

<div align="center">
  
### One-Click Deployment

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/JhoomMusic)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/JhoomMusic)

</div>

## 🖥️ VPS Deployment

### Basic VPS Setup

1. **Connect to your VPS:**
   ```bash
   ssh root@your-server-ip
   ```

2. **Install Dependencies:**
   ```bash
   # Update system
   apt update && apt upgrade -y
   
   # Install Python and required packages
   apt install python3 python3-pip git ffmpeg -y
   ```

3. **Deploy Bot:**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/JhoomMusic
   cd JhoomMusic
   
   # Install Python dependencies
   pip3 install -r requirements.txt
   
   # Setup environment
   cp .env.example .env
   nano .env  # Edit with your values
   
   # Generate string session
   python3 generate_session.py
   
   # Run bot with screen
   screen -S jhoommusic
   python3 main.py
   # Press Ctrl+A then D to detach
   ```

### Systemd Service (Recommended)

Create a systemd service for automatic startup:

```bash
sudo nano /etc/systemd/system/jhoommusic.service
```

```ini
[Unit]
Description=JhoomMusic Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/JhoomMusic
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jhoommusic
sudo systemctl start jhoommusic

# Check status
sudo systemctl status jhoommusic
```

## 🐳 Docker Deployment

### Deploy with Docker

1. **Clone and setup:**
   ```bash
   git clone https://github.com/yourusername/JhoomMusic
   cd JhoomMusic
   cp .env.example .env
   # Edit .env file with your values
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the bot:**
   ```bash
   docker-compose down
   ```

## ⚙️ Configuration

### Required Variables

- `API_ID` - Get from [my.telegram.org](https://my.telegram.org/apps)
- `API_HASH` - Get from [my.telegram.org](https://my.telegram.org/apps)
- `BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
- `STRING_SESSION` - Generate using `python3 generate_session.py`
- `LOG_GROUP_ID` - Chat ID of your log group
- `OWNER_ID` - Your Telegram user ID

### Optional Variables

- `MONGO_DB_URI` - MongoDB connection string
- `SUDO_USERS` - Space-separated user IDs for sudo access
- `SUPPORT_CHAT` - Link to your support group
- `SUPPORT_CHANNEL` - Link to your updates channel
- `DURATION_LIMIT` - Maximum song duration in minutes (default: 60)
- `VIDEO_STREAM_LIMIT` - Maximum concurrent video streams (default: 3)

## 📋 Commands

### Music Commands
- `/play <song name>` - Play music from YouTube
- `/pause` - Pause the current song
- `/resume` - Resume the paused song
- `/skip` - Skip to next song in queue
- `/stop` - Stop playing and clear queue
- `/queue` - Show current queue
- `/shuffle` - Shuffle the queue

### Admin Commands
- `/auth <username>` - Add user to auth list
- `/unauth <username>` - Remove user from auth list
- `/authusers` - Show authorized users

### Other Commands
- `/ping` - Check bot ping and stats
- `/help` - Show help menu
- `/settings` - Open settings panel

## 🛠️ Requirements

- Python 3.9+
- FFmpeg
- MongoDB (optional)
- Telegram API credentials
- Bot token from BotFather

## 📦 Dependencies

- `pyrogram` - Telegram MTProto API framework
- `py-tgcalls` - Voice chat integration
- `yt-dlp` - YouTube video/audio downloader
- `motor` - Async MongoDB driver
- `aiohttp` - HTTP client/server
- `pillow` - Image processing
- `psutil` - System monitoring

## 🔧 Troubleshooting

### Common Issues

1. **Bot not responding:**
   ```bash
   # Check if bot is running
   ps aux | grep python3
   
   # Check logs
   tail -f bot.log
   ```

2. **Permission errors:**
   ```bash
   # Make sure bot is admin in log group
   # Check if assistant account is added to log group
   ```

3. **Audio not playing:**
   ```bash
   # Ensure FFmpeg is installed
   ffmpeg -version
   
   # Check voice chat is active in group
   ```

4. **Memory issues:**
   ```bash
   # Monitor memory usage
   htop
   
   # Restart bot if needed
   sudo systemctl restart jhoommusic
   ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

<div align="center">
  
**Need Help? Join our community!**

[![Support Group](https://img.shields.io/badge/Support-Group-blue?style=for-the-badge&logo=telegram)](https://t.me/JhoomMusicSupport)
[![Updates Channel](https://img.shields.io/badge/Updates-Channel-blue?style=for-the-badge&logo=telegram)](https://t.me/JhoomMusicChannel)

</div>

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/JhoomMusic&type=Date)](https://star-history.com/#yourusername/JhoomMusic&Date)

## 🙏 Acknowledgments

- [Pyrogram](https://github.com/pyrogram/pyrogram) for the amazing MTProto framework
- [PyTgCalls](https://github.com/pytgcalls/pytgcalls) for voice chat integration
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube support
- All contributors and users of this project

---

<div align="center">
  
**Made with ❤️ by JhoomMusic Team**

*If you found this project helpful, please consider giving it a ⭐*

</div>