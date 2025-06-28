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

### Deploy on VPS

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/JhoomMusic
   cd JhoomMusic
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file with your values
   ```

4. **Generate string session:**
   ```bash
   python3 generate_session.py
   ```

5. **Run the bot:**
   ```bash
   python3 main.py
   ```

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