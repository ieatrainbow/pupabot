# 🤖 PupaBot - Telegram Bot

A Telegram bot with UNBELIVEABLE features.

## 🚀 Quick Start

**Note**: Never commit `.env` file to Git! It's added to `.gitignore` for security.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional)
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

## 📁 Project Structure

```
pupabot/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image configuration
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── data/                       # Data directory (mounted into container, not exist in this repo)
│   ├── audio/                  # Audio files for bot
│   ├── font/                   # Font files
│   ├── gif/                    # Animated GIFs
│   ├── log/                    # Application logs
│   ├── pupaups/                # Pupa-related content
│   ├── stickers/               # Telegram stickers
│   ├── text/                   # Bot text files
│   └── video/                  # Video content
└── src/                        # Source code
    ├── main.py                 # Entry point - bot initialization and startup
    ├── ai.py                   # AI integration (not working)
    ├── config.py               # Configuration management and environment validation
    ├── handlers.py             # Telegram message handlers and command processors
    ├── services.py             # Business logic and external service integrations
    ├── utils.py                # Utility functions and helpers
    ├── helpers.py              # Helper classes and bot initialization
```

## ⚙️ Configuration

### 1. Create `.env` file
Copy the template and fill with your data:

```bash
cp .env.example .env
```

Edit the `.env` file.

### 2. Prepare data
Create necessary folders and files:

```bash
# Create folders structure if not exists
mkdir -p data/text data/log

# Create quotes file (if needed XD)
echo "First quote" > data/text/pupa_q.txt
echo "Second quote" >> data/text/pupa_q.txt
```

## 🐳 Running with Docker Compose (Recommended)

### Install Docker Compose
```bash
# Check installation
docker-compose --version
```

### Start the bot
```bash
# Build and run in background
docker-compose up -d --build

# Or run with log output
docker-compose up --build
```

### Bot management
```bash
# View logs
docker-compose logs -f

# Last 50 lines only
docker-compose logs --tail=50

# Stop the bot
docker-compose down

# Restart with updated variables
docker-compose down && docker-compose up -d

# Restart only the bot
docker-compose restart
```

## 🐋 Running with Docker Run

### Build the image
```bash
# Build image with tag 'pupabot'
docker build -t pupabot .
```

### Run container
```bash
# Run in background with .env file
docker run -d \
  --name pupabot \
  --restart unless-stopped \
  -v $(pwd)/data:/usr/src/app/data:rw \
  -e DATA_FOLDER=data \
  --env-file .env \
  pupabot
```

### Container management
```bash
# View logs
docker logs -f pupabot

# Enter container (for debugging)
docker exec -it pupabot bash

# Stop container
docker stop pupabot

# Remove container
docker rm pupabot

# Restart with new variables
docker stop pupabot && docker rm pupabot
docker run -d ... (your run command)
```

## 🐛 Debugging and Logs

### Where to find logs
- **In container**: `/usr/src/app/data/log/debug.log`
- **On host**: `./data/log/debug.log` (if folder is mounted)
- **Docker logs**: `docker-compose logs` or `docker logs pupabot`

### Health check
```bash
# Check container status
docker-compose ps
# or
docker ps | grep pupabot

### Common issues
1. **.env file not found** - ensure file is in same directory as docker-compose.yml
2. **Data folder missing** - create: `mkdir -p data/text data/log`
3. **Permission denied** - set permissions: `chmod -R 755 data/`
4. **Token not working** - verify token with @BotFather

## 🔄 Updating the Bot

### Code updates
```bash
# Stop the bot
docker-compose down

# Get new code (git pull or copy files)

# Rebuild and run
docker-compose up -d --build
```

### Environment variable updates
```bash
# Edit .env file
nano .env

# Restart containers
docker-compose down && docker-compose up -d
```

## 🗑️ Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove image
docker rmi pupabot

# Remove all unused Docker data
docker system prune -a -f --volumes

# Remove bot data (caution!)
rm -rf data/
```

## 📊 Monitoring

```bash
# Container statistics
docker stats pupabot

# Resource usage
docker-compose top

# Real-time log monitoring
docker-compose logs -f --tail=100
```

## 🤝 Development

### Local development without Docker
```bash
# Install dependencies
pip install -r requirements.txt

# Create symlink or copy .env
cp .env.example .env

# Run bot
python src/main.py
```