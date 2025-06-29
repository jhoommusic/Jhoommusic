#!/bin/bash

# JhoomMusic Bot Setup Script
# This script will install all dependencies and set up the bot

echo "🎵 JhoomMusic Bot Setup Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    echo -e "${BLUE}$1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

print_header "🔍 Checking System Requirements..."

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_status "Linux detected"
    if command -v apt &> /dev/null; then
        PKG_MANAGER="apt"
        UPDATE_CMD="sudo apt update && sudo apt upgrade -y"
        INSTALL_CMD="sudo apt install -y"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
        UPDATE_CMD="sudo yum update -y"
        INSTALL_CMD="sudo yum install -y"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
        UPDATE_CMD="sudo dnf update -y"
        INSTALL_CMD="sudo dnf install -y"
    else
        print_error "Unsupported package manager. Please install dependencies manually."
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_status "macOS detected"
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found. Please install Homebrew first."
        exit 1
    fi
    PKG_MANAGER="brew"
    UPDATE_CMD="brew update && brew upgrade"
    INSTALL_CMD="brew install"
else
    print_error "Unsupported operating system"
    exit 1
fi

print_status "Package manager: $PKG_MANAGER"

# Update system
print_header "📦 Updating System Packages..."
eval $UPDATE_CMD

# Install system dependencies
print_header "🔧 Installing System Dependencies..."

if [[ "$PKG_MANAGER" == "apt" ]]; then
    $INSTALL_CMD python3 python3-pip python3-dev python3-venv git ffmpeg curl wget unzip
elif [[ "$PKG_MANAGER" == "yum" ]] || [[ "$PKG_MANAGER" == "dnf" ]]; then
    $INSTALL_CMD python3 python3-pip python3-devel git ffmpeg curl wget unzip
elif [[ "$PKG_MANAGER" == "brew" ]]; then
    $INSTALL_CMD python3 git ffmpeg curl wget
fi

# Check Python version
print_header "🐍 Checking Python Version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python $PYTHON_VERSION is compatible"
else
    print_error "Python $PYTHON_VERSION is not compatible. Python 3.8+ required."
    exit 1
fi

# Create virtual environment
print_header "🌐 Creating Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_header "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_header "📚 Installing Python Dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Python dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Create necessary directories
print_header "📁 Creating Directories..."
mkdir -p downloads cache raw_files logs
print_status "Directories created"

# Copy environment file
print_header "⚙️ Setting up Configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_status "Environment file created from example"
        print_warning "Please edit .env file with your configuration"
    else
        print_error ".env.example not found"
    fi
else
    print_warning ".env file already exists"
fi

# Create systemd service file
print_header "🔧 Creating Systemd Service..."
SERVICE_FILE="jhoommusic.service"
cat > $SERVICE_FILE << EOF
[Unit]
Description=JhoomMusic Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python main.py
Restart=always
RestartSec=10
Environment=PATH=$(pwd)/venv/bin

[Install]
WantedBy=multi-user.target
EOF

print_status "Systemd service file created: $SERVICE_FILE"
print_warning "To install service: sudo cp $SERVICE_FILE /etc/systemd/system/"
print_warning "To enable service: sudo systemctl enable jhoommusic"
print_warning "To start service: sudo systemctl start jhoommusic"

# Create start script
print_header "🚀 Creating Start Script..."
cat > start.sh << 'EOF'
#!/bin/bash

# JhoomMusic Bot Start Script

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🎵 Starting JhoomMusic Bot...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Virtual environment not found. Please run setup.sh first.${NC}"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}.env file not found. Please configure your bot first.${NC}"
    exit 1
fi

# Start the bot
python main.py
EOF

chmod +x start.sh
print_status "Start script created: start.sh"

# Create update script
print_header "🔄 Creating Update Script..."
cat > update.sh << 'EOF'
#!/bin/bash

# JhoomMusic Bot Update Script

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔄 Updating JhoomMusic Bot...${NC}"

# Pull latest changes
echo -e "${YELLOW}Pulling latest changes...${NC}"
git pull origin main

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}Virtual environment activated${NC}"
else
    echo -e "${RED}Virtual environment not found${NC}"
    exit 1
fi

# Update dependencies
echo -e "${YELLOW}Updating dependencies...${NC}"
pip install -r requirements.txt --upgrade

echo -e "${GREEN}✅ Update completed!${NC}"
echo -e "${YELLOW}Please restart the bot to apply changes${NC}"
EOF

chmod +x update.sh
print_status "Update script created: update.sh"

# Final instructions
print_header "✅ Setup Complete!"
echo ""
print_status "Next steps:"
echo "1. Edit .env file with your bot configuration"
echo "2. Generate session string: python3 generate_session.py"
echo "3. Start the bot: ./start.sh"
echo ""
print_status "Useful commands:"
echo "• Start bot: ./start.sh"
echo "• Update bot: ./update.sh"
echo "• Install as service: sudo cp jhoommusic.service /etc/systemd/system/"
echo "• Enable service: sudo systemctl enable jhoommusic"
echo "• Start service: sudo systemctl start jhoommusic"
echo "• Check service status: sudo systemctl status jhoommusic"
echo "• View logs: sudo journalctl -u jhoommusic -f"
echo ""
print_warning "Don't forget to configure your .env file!"
print_status "Setup completed successfully! 🎉"