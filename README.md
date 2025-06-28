# JhoomMusic - Telegram Music Bot

A powerful Telegram music bot that can play high-quality music in voice chats with advanced features like queue management, admin controls, and live streaming support.

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

## 🚀 Deployment

### Deploy on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/JhoomMusic)

### Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/JhoomMusic)

## 🖥️ VPS Deployment Options

### 1. Hetzner Cloud

**Recommended Plan:** CX11 (1 vCPU, 2GB RAM) - €3.29/month

1. **Create Hetzner Cloud Account:**
   - Visit [Hetzner Cloud](https://www.hetzner.com/cloud)
   - Sign up and verify your account

2. **Create Server:**
   ```bash
   # Choose Ubuntu 22.04 LTS
   # Select CX11 or higher plan
   # Add SSH key for secure access
   ```

3. **Connect to Server:**
   ```bash
   ssh root@your-server-ip
   ```

4. **Install Dependencies:**
   ```bash
   # Update system
   apt update && apt upgrade -y
   
   # Install Python and required packages
   apt install python3 python3-pip git ffmpeg -y
   
   # Install Node.js (for some dependencies)
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   apt install nodejs -y
   ```

5. **Deploy Bot:**
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

### 2. Contabo VPS

**Recommended Plan:** VPS S (4 vCPU, 8GB RAM) - €4.99/month

1. **Create Contabo Account:**
   - Visit [Contabo](https://contabo.com/en/vps/)
   - Choose VPS S or higher plan

2. **Server Setup:**
   ```bash
   # Connect via SSH
   ssh root@your-server-ip
   
   # Update system
   apt update && apt upgrade -y
   
   # Install required packages
   apt install python3 python3-pip git ffmpeg screen htop -y
   ```

3. **Deploy Application:**
   ```bash
   # Clone and setup
   git clone https://github.com/yourusername/JhoomMusic
   cd JhoomMusic
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   nano .env  # Add your configuration
   
   # Generate session
   python3 generate_session.py
   
   # Run with systemd service (recommended)
   sudo nano /etc/systemd/system/jhoommusic.service
   ```

4. **Create Systemd Service:**
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

### 3. DigitalOcean

**Recommended Plan:** Basic Droplet (1 vCPU, 1GB RAM) - $6/month

1. **Create DigitalOcean Account:**
   - Visit [DigitalOcean](https://www.digitalocean.com/)
   - Get $200 credit with referral links

2. **Create Droplet:**
   ```bash
   # Choose Ubuntu 22.04 LTS
   # Select Basic plan ($6/month)
   # Add SSH keys
   # Choose datacenter region
   ```

3. **Initial Setup:**
   ```bash
   # Connect to droplet
   ssh root@your-droplet-ip
   
   # Create non-root user (recommended)
   adduser jhoommusic
   usermod -aG sudo jhoommusic
   su - jhoommusic
   
   # Install dependencies
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip git ffmpeg -y
   ```

4. **Deploy Bot:**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/JhoomMusic
   cd JhoomMusic
   
   # Install requirements
   pip3 install -r requirements.txt
   
   # Setup configuration
   cp .env.example .env
   nano .env  # Configure your variables
   
   # Generate session
   python3 generate_session.py
   
   # Use PM2 for process management
   sudo npm install -g pm2
   pm2 start main.py --name jhoommusic --interpreter python3
   pm2 startup
   pm2 save
   ```

### 4. Linode

**Recommended Plan:** Nanode 1GB - $5/month

1. **Create Linode Account:**
   - Visit [Linode](https://www.linode.com/)
   - Choose Nanode 1GB plan

2. **Create Linode:**
   ```bash
   # Select Ubuntu 22.04 LTS
   # Choose Nanode 1GB plan
   # Set root password
   # Add SSH keys
   ```

3. **Server Configuration:**
   ```bash
   # Connect via SSH
   ssh root@your-linode-ip
   
   # Update system
   apt update && apt upgrade -y
   
   # Install dependencies
   apt install python3 python3-pip git ffmpeg supervisor -y
   ```

4. **Deploy with Supervisor:**
   ```bash
   # Clone and setup
   git clone https://github.com/yourusername/JhoomMusic
   cd JhoomMusic
   pip3 install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   nano .env
   
   # Generate session
   python3 generate_session.py
   
   # Create supervisor config
   sudo nano /etc/supervisor/conf.d/jhoommusic.conf
   ```

   ```ini
   [program:jhoommusic]
   command=/usr/bin/python3 main.py
   directory=/root/JhoomMusic
   user=root
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/jhoommusic.err.log
   stdout_logfile=/var/log/jhoommusic.out.log
   ```

   ```bash
   # Start supervisor
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start jhoommusic
   ```

### 5. Oracle Cloud (Free Tier)

**Free Plan:** VM.Standard.E2.1.Micro (1 vCPU, 1GB RAM) - Always Free

1. **Create Oracle Cloud Account:**
   - Visit [Oracle Cloud](https://www.oracle.com/cloud/free/)
   - Sign up for Always Free account

2. **Create Compute Instance:**
   ```bash
   # Go to Compute > Instances
   # Click "Create Instance"
   # Choose VM.Standard.E2.1.Micro (Always Free)
   # Select Ubuntu 22.04
   # Add SSH keys
   ```

3. **Configure Firewall:**
   ```bash
   # In Oracle Cloud Console
   # Go to Networking > Virtual Cloud Networks
   # Edit Security List
   # Add Ingress Rule for port 22 (SSH)
   ```

4. **Deploy Application:**
   ```bash
   # Connect via SSH
   ssh ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install python3 python3-pip git ffmpeg -y
   
   # Clone repository
   git clone https://github.com/yourusername/JhoomMusic
   cd JhoomMusic
   
   # Install requirements
   pip3 install -r requirements.txt
   
   # Setup environment
   cp .env.example .env
   nano .env
   
   # Generate session
   python3 generate_session.py
   
   # Run with nohup
   nohup python3 main.py > bot.log 2>&1 &
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

- **Support Group:** [JhoomMusic Support](https://t.me/JhoomMusicSupport)
- **Updates Channel:** [JhoomMusic Channel](https://t.me/JhoomMusicChannel)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/JhoomMusic&type=Date)](https://star-history.com/#yourusername/JhoomMusic&Date)

## 🙏 Acknowledgments

- [Pyrogram](https://github.com/pyrogram/pyrogram) for the amazing MTProto framework
- [PyTgCalls](https://github.com/pytgcalls/pytgcalls) for voice chat integration
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube support
- All contributors and users of this project

---

**Made with ❤️ by JhoomMusic Team**