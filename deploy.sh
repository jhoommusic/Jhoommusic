#!/bin/bash

# JhoomMusic Bot One-Click Deployment Script
# This script will automatically set up and deploy the bot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🔸 $1${NC}"
}

# Banner
clear
echo -e "${CYAN}"
cat << "EOF"
     ██╗██╗  ██╗ ██████╗  ██████╗ ███╗   ███╗
     ██║██║  ██║██╔═══██╗██╔═══██╗████╗ ████║
     ██║███████║██║   ██║██║   ██║██╔████╔██║
██   ██║██╔══██║██║   ██║██║   ██║██║╚██╔╝██║
╚█████╔╝██║  ██║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
 ╚════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
                                              
    ███╗   ███╗██╗   ██╗███████╗██╗ ██████╗ 
    ████╗ ████║██║   ██║██╔════╝██║██╔════╝ 
    ██╔████╔██║██║   ██║███████╗██║██║      
    ██║╚██╔╝██║██║   ██║╚════██║██║██║      
    ██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗ 
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ 
                                              
EOF
echo -e "${NC}"
echo -e "${GREEN}🎵 Advanced Telegram Music Bot${NC}"
echo -e "${YELLOW}🚀 One-Click Deployment Script${NC}"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

print_header "🔍 SYSTEM REQUIREMENTS CHECK"

# Check OS and set package manager
print_step "Detecting operating system..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_success "Linux detected"
    
    # Detect distribution
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        print_status "Distribution: $OS $VER"
    fi
    
    if command -v apt &> /dev/null; then
        PKG_MANAGER="apt"
        UPDATE_CMD="sudo apt update && sudo apt upgrade -y"
        INSTALL_CMD="sudo apt install -y"
        print_status "Package manager: APT (Debian/Ubuntu)"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
        UPDATE_CMD="sudo yum update -y"
        INSTALL_CMD="sudo yum install -y"
        print_status "Package manager: YUM (CentOS/RHEL)"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
        UPDATE_CMD="sudo dnf update -y"
        INSTALL_CMD="sudo dnf install -y"
        print_status "Package manager: DNF (Fedora)"
    elif command -v pacman &> /dev/null; then
        PKG_MANAGER="pacman"
        UPDATE_CMD="sudo pacman -Syu --noconfirm"
        INSTALL_CMD="sudo pacman -S --noconfirm"
        print_status "Package manager: Pacman (Arch Linux)"
    else
        print_error "Unsupported package manager. Please install dependencies manually."
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_success "macOS detected"
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    PKG_MANAGER="brew"
    UPDATE_CMD="brew update && brew upgrade"
    INSTALL_CMD="brew install"
    print_status "Package manager: Homebrew"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

# Check system resources
print_step "Checking system resources..."
TOTAL_RAM=$(free -m 2>/dev/null | awk 'NR==2{printf "%.0f", $2/1024}' || echo "Unknown")
AVAILABLE_SPACE=$(df -h . 2>/dev/null | awk 'NR==2{print $4}' || echo "Unknown")
CPU_CORES=$(nproc 2>/dev/null || echo "Unknown")

print_status "RAM: ${TOTAL_RAM}GB"
print_status "Available space: $AVAILABLE_SPACE"
print_status "CPU cores: $CPU_CORES"

if [[ "$TOTAL_RAM" != "Unknown" ]] && [[ $TOTAL_RAM -lt 1 ]]; then
    print_warning "Low RAM detected. Bot may run slowly."
fi

print_header "📦 INSTALLING SYSTEM DEPENDENCIES"

print_step "Updating system packages..."
eval $UPDATE_CMD

print_step "Installing required packages..."
if [[ "$PKG_MANAGER" == "apt" ]]; then
    $INSTALL_CMD python3 python3-pip python3-dev python3-venv git ffmpeg curl wget unzip build-essential libffi-dev libssl-dev
elif [[ "$PKG_MANAGER" == "yum" ]] || [[ "$PKG_MANAGER" == "dnf" ]]; then
    $INSTALL_CMD python3 python3-pip python3-devel git ffmpeg curl wget unzip gcc openssl-devel libffi-devel
elif [[ "$PKG_MANAGER" == "pacman" ]]; then
    $INSTALL_CMD python python-pip git ffmpeg curl wget unzip base-devel
elif [[ "$PKG_MANAGER" == "brew" ]]; then
    $INSTALL_CMD python3 git ffmpeg curl wget
fi

print_success "System dependencies installed"

print_header "🐍 PYTHON ENVIRONMENT SETUP"

# Check Python version
print_step "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python version: $PYTHON_VERSION"
    
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_success "Python version is compatible"
    else
        print_error "Python $PYTHON_VERSION is not compatible. Python 3.8+ required."
        exit 1
    fi
else
    print_error "Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Create virtual environment
print_step "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_step "Upgrading pip..."
pip install --upgrade pip setuptools wheel

print_header "📚 INSTALLING PYTHON DEPENDENCIES"

# Install Python dependencies
print_step "Installing Python packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

print_header "📁 CREATING PROJECT STRUCTURE"

# Create necessary directories
print_step "Creating directories..."
mkdir -p downloads cache raw_files logs backups
print_success "Project directories created"

# Set proper permissions
print_step "Setting permissions..."
chmod 755 downloads cache raw_files logs backups
print_success "Permissions set"

print_header "⚙️ CONFIGURATION SETUP"

# Copy environment file
print_step "Setting up configuration files..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Environment file created from example"
    else
        print_warning ".env.example not found, creating basic .env file"
        cat > .env << 'EOF'
# Bot Configuration
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Assistant Configuration
STRING_SESSION=your_string_session

# Database Configuration
MONGO_DB_URI=your_mongodb_uri

# Admin Configuration
OWNER_ID=your_user_id
LOG_GROUP_ID=your_log_group_id

# Support Configuration
SUPPORT_CHAT=https://t.me/JhoomMusicSupport
SUPPORT_CHANNEL=https://t.me/JhoomMusicChannel
EOF
    fi
else
    print_warning ".env file already exists"
fi

print_header "🔧 CREATING MANAGEMENT SCRIPTS"

# Create start script
print_step "Creating start script..."
cat > start.sh << 'EOF'
#!/bin/bash

# JhoomMusic Bot Start Script

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🎵 Starting JhoomMusic Bot...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found. Please run setup.sh first.${NC}"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found. Please configure your bot first.${NC}"
    exit 1
fi

# Check if configuration is complete
if grep -q "your_api_id\|your_api_hash\|your_bot_token" .env; then
    echo -e "${YELLOW}⚠️  Please configure your .env file with proper values${NC}"
    echo -e "${YELLOW}   Edit .env file and replace placeholder values${NC}"
    exit 1
fi

# Create log file if it doesn't exist
touch log.txt

# Start the bot
echo -e "${GREEN}🚀 Bot starting...${NC}"
python main.py
EOF

chmod +x start.sh
print_success "Start script created"

# Create stop script
print_step "Creating stop script..."
cat > stop.sh << 'EOF'
#!/bin/bash

# JhoomMusic Bot Stop Script

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🛑 Stopping JhoomMusic Bot...${NC}"

# Find and kill bot processes
BOT_PID=$(pgrep -f "python main.py" | head -1)

if [ ! -z "$BOT_PID" ]; then
    kill $BOT_PID
    echo -e "${GREEN}✅ Bot stopped (PID: $BOT_PID)${NC}"
else
    echo -e "${RED}❌ Bot is not running${NC}"
fi

# Also stop systemd service if running
if systemctl is-active --quiet jhoommusic 2>/dev/null; then
    sudo systemctl stop jhoommusic
    echo -e "${GREEN}✅ Systemd service stopped${NC}"
fi
EOF

chmod +x stop.sh
print_success "Stop script created"

# Create update script
print_step "Creating update script..."
cat > update.sh << 'EOF'
#!/bin/bash

# JhoomMusic Bot Update Script

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔄 Updating JhoomMusic Bot...${NC}"

# Stop bot if running
echo -e "${YELLOW}🛑 Stopping bot...${NC}"
./stop.sh

# Backup current configuration
echo -e "${YELLOW}💾 Creating backup...${NC}"
mkdir -p backups
cp .env backups/.env.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# Pull latest changes
echo -e "${YELLOW}📥 Pulling latest changes...${NC}"
if [ -d ".git" ]; then
    git stash push -m "Auto-stash before update $(date)"
    git pull origin main
    git stash pop 2>/dev/null || true
else
    echo -e "${RED}❌ Not a git repository. Please clone the repository properly.${NC}"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${RED}❌ Virtual environment not found${NC}"
    exit 1
fi

# Update dependencies
echo -e "${YELLOW}📦 Updating dependencies...${NC}"
pip install -r requirements.txt --upgrade

# Create new directories if needed
mkdir -p downloads cache raw_files logs backups

echo -e "${GREEN}✅ Update completed!${NC}"
echo -e "${YELLOW}🚀 Starting bot...${NC}"
./start.sh
EOF

chmod +x update.sh
print_success "Update script created"

# Create status script
print_step "Creating status script..."
cat > status.sh << 'EOF'
#!/bin/bash

# JhoomMusic Bot Status Script

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📊 JhoomMusic Bot Status${NC}"
echo "================================"

# Check if bot process is running
BOT_PID=$(pgrep -f "python main.py" | head -1)
if [ ! -z "$BOT_PID" ]; then
    echo -e "${GREEN}✅ Bot Status: RUNNING (PID: $BOT_PID)${NC}"
    
    # Get process info
    CPU_USAGE=$(ps -p $BOT_PID -o %cpu --no-headers 2>/dev/null | tr -d ' ')
    MEM_USAGE=$(ps -p $BOT_PID -o %mem --no-headers 2>/dev/null | tr -d ' ')
    START_TIME=$(ps -p $BOT_PID -o lstart --no-headers 2>/dev/null)
    
    echo -e "${BLUE}📈 CPU Usage: ${CPU_USAGE}%${NC}"
    echo -e "${BLUE}💾 Memory Usage: ${MEM_USAGE}%${NC}"
    echo -e "${BLUE}⏰ Started: ${START_TIME}${NC}"
else
    echo -e "${RED}❌ Bot Status: NOT RUNNING${NC}"
fi

# Check systemd service
if systemctl is-active --quiet jhoommusic 2>/dev/null; then
    echo -e "${GREEN}✅ Systemd Service: ACTIVE${NC}"
elif systemctl list-unit-files | grep -q jhoommusic 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Systemd Service: INACTIVE${NC}"
else
    echo -e "${BLUE}ℹ️  Systemd Service: NOT INSTALLED${NC}"
fi

# Check log file
if [ -f "log.txt" ]; then
    LOG_SIZE=$(du -h log.txt | cut -f1)
    LOG_LINES=$(wc -l < log.txt)
    echo -e "${BLUE}📝 Log File: ${LOG_SIZE} (${LOG_LINES} lines)${NC}"
else
    echo -e "${YELLOW}⚠️  Log File: NOT FOUND${NC}"
fi

# Check configuration
if [ -f ".env" ]; then
    if grep -q "your_api_id\|your_api_hash\|your_bot_token" .env; then
        echo -e "${RED}❌ Configuration: INCOMPLETE${NC}"
    else
        echo -e "${GREEN}✅ Configuration: COMPLETE${NC}"
    fi
else
    echo -e "${RED}❌ Configuration: NOT FOUND${NC}"
fi

# System resources
echo ""
echo -e "${BLUE}💻 System Resources:${NC}"
echo "================================"
free -h | grep -E "Mem|Swap"
df -h . | tail -1 | awk '{print "Disk: " $3 " used, " $4 " available (" $5 " used)"}'
uptime | awk '{print "Uptime: " $3 " " $4}' | sed 's/,//'
EOF

chmod +x status.sh
print_success "Status script created"

print_header "🔧 SYSTEMD SERVICE SETUP"

# Create systemd service file
print_step "Creating systemd service..."
SERVICE_FILE="jhoommusic.service"
cat > $SERVICE_FILE << EOF
[Unit]
Description=JhoomMusic Telegram Bot
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python main.py
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
Environment=PATH=$(pwd)/venv/bin
Environment=PYTHONPATH=$(pwd)
StandardOutput=append:$(pwd)/logs/bot.log
StandardError=append:$(pwd)/logs/bot.error.log

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$(pwd)

[Install]
WantedBy=multi-user.target
EOF

print_success "Systemd service file created: $SERVICE_FILE"

# Create service management script
print_step "Creating service management script..."
cat > service.sh << 'EOF'
#!/bin/bash

# JhoomMusic Bot Service Management Script

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SERVICE_NAME="jhoommusic"
SERVICE_FILE="jhoommusic.service"

case "$1" in
    install)
        echo -e "${BLUE}📦 Installing systemd service...${NC}"
        sudo cp $SERVICE_FILE /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable $SERVICE_NAME
        echo -e "${GREEN}✅ Service installed and enabled${NC}"
        ;;
    uninstall)
        echo -e "${YELLOW}🗑️  Uninstalling systemd service...${NC}"
        sudo systemctl stop $SERVICE_NAME 2>/dev/null || true
        sudo systemctl disable $SERVICE_NAME 2>/dev/null || true
        sudo rm -f /etc/systemd/system/$SERVICE_FILE
        sudo systemctl daemon-reload
        echo -e "${GREEN}✅ Service uninstalled${NC}"
        ;;
    start)
        echo -e "${GREEN}🚀 Starting service...${NC}"
        sudo systemctl start $SERVICE_NAME
        ;;
    stop)
        echo -e "${YELLOW}🛑 Stopping service...${NC}"
        sudo systemctl stop $SERVICE_NAME
        ;;
    restart)
        echo -e "${BLUE}🔄 Restarting service...${NC}"
        sudo systemctl restart $SERVICE_NAME
        ;;
    status)
        sudo systemctl status $SERVICE_NAME
        ;;
    logs)
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    *)
        echo "Usage: $0 {install|uninstall|start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  install   - Install and enable systemd service"
        echo "  uninstall - Remove systemd service"
        echo "  start     - Start the service"
        echo "  stop      - Stop the service"
        echo "  restart   - Restart the service"
        echo "  status    - Show service status"
        echo "  logs      - Show service logs"
        exit 1
        ;;
esac
EOF

chmod +x service.sh
print_success "Service management script created"

print_header "🔐 SECURITY SETUP"

# Create .gitignore if it doesn't exist
print_step "Creating .gitignore..."
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Environment files
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environment
venv/
env/
ENV/

# Bot files
*.session
*.session-journal
log.txt
logs/
cache/
raw_files/
backups/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
    print_success ".gitignore created"
else
    print_warning ".gitignore already exists"
fi

# Set secure permissions
print_step "Setting secure permissions..."
chmod 600 .env 2>/dev/null || true
chmod 755 *.sh
print_success "Permissions secured"

print_header "✅ DEPLOYMENT COMPLETED"

echo ""
print_success "JhoomMusic Bot has been successfully deployed!"
echo ""
echo -e "${CYAN}📋 NEXT STEPS:${NC}"
echo "1. Configure your bot:"
echo "   ${YELLOW}nano .env${NC}"
echo ""
echo "2. Generate session string:"
echo "   ${YELLOW}python3 generate_session.py${NC}"
echo ""
echo "3. Start the bot:"
echo "   ${YELLOW}./start.sh${NC}"
echo ""
echo -e "${CYAN}🛠️  MANAGEMENT COMMANDS:${NC}"
echo "• Start bot:           ${GREEN}./start.sh${NC}"
echo "• Stop bot:            ${GREEN}./stop.sh${NC}"
echo "• Update bot:          ${GREEN}./update.sh${NC}"
echo "• Check status:        ${GREEN}./status.sh${NC}"
echo "• Install service:     ${GREEN}./service.sh install${NC}"
echo "• Start service:       ${GREEN}./service.sh start${NC}"
echo "• Check service:       ${GREEN}./service.sh status${NC}"
echo "• View logs:           ${GREEN}./service.sh logs${NC}"
echo ""
echo -e "${CYAN}📁 IMPORTANT FILES:${NC}"
echo "• Configuration:       ${YELLOW}.env${NC}"
echo "• Logs:               ${YELLOW}log.txt${NC}"
echo "• Service file:       ${YELLOW}jhoommusic.service${NC}"
echo ""
echo -e "${CYAN}🔗 USEFUL LINKS:${NC}"
echo "• Get API credentials: ${BLUE}https://my.telegram.org/apps${NC}"
echo "• Create bot:         ${BLUE}https://t.me/BotFather${NC}"
echo "• MongoDB Atlas:      ${BLUE}https://cloud.mongodb.
    if mongodb else None # com${NC}"
echo ""
print_warning "⚠️  Don't forget to:"
echo "   • Configure your .env file with real values"
echo "   • Generate session string for assistant"
echo "   • Add bot to your log group as admin"
echo "   • Test the bot before deploying to production"
echo ""
print_success "🎉 Happy botting with JhoomMusic!"