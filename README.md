# BGMI Warrior Bot by IBR - Premium Edition

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-Proprietary-red)

Advanced Telegram bot for BGMI players with DDoS protection capabilities and premium features. Built with modern async architecture and MongoDB integration for scalable, performant operation.

<p align="center">
  <img src="https://i.imgur.com/YourLogoHere.png" alt="BGMI Warrior Bot by IBR Logo" width="300">
</p>

## 🚀 Features

- **🎮 Multi-Mode Operation** - Manual and Auto DDoS protection modes for strategic flexibility
- **👑 Premium User System** - Tiered authorization with configurable expiration dates
- **🛡️ Rate Limiting** - Intelligent group chat protection against abuse
- **📊 Advanced Analytics** - Comprehensive usage tracking and performance metrics
- **⚙️ Dynamic Thread Management** - Self-optimizing thread allocation based on performance analysis
- **📈 Bandwidth Monitoring** - Real-time network usage monitoring to prevent system overload
- **🌐 Multi-language Support** - Full localization framework for global deployment
- **🏗️ Modern Architecture** - Async/await pattern with clean separation of concerns for maintainable codebase

## 🏗️ Project Structure
action-bot_by_IBR/
├── .env # Environment variables (sensitive data) 
├── .gitignore # Git ignore file 
├── README.md # Documentation 
├── main.py # Entry point 
├── bot.py # Bot initialization 
├── config.py # Configuration using Pydantic 
├── models.py # Data models
├── database.py # Database layer 
├── action_service.py # Action execution service
├── command_handlers.py # Command handlers
├── middlewares.py # Middleware for authentication etc.
├── utils.py # Utility functions
├── localization/ # Multi-language support
│ └── messages.py # Message templates
└── bot_logs/ # Log directory
└── warrior_bot.log # Log file


## Installation

### Prerequisites

- Python 3.9 or higher
- MongoDB database
- Telegram Bot Token from @BotFather

### Setup

1. Clone the repository:
```bash
git clone https://github.com/xxxxxxx/bgmi-warrior-bot.git
cd bgmi-warrior-bot
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
```bash
pip install -r requirements.txt
4. Setup env
# Edit .env with your configuration
5. Set up MongoDB database in .env.

6. Run the bot:

```bash
python main.py

Docker Setup
Alternatively, you can use Docker:

bash
# Build and start with docker-compose
docker-compose up -d
Configuration
Edit the .env file with your specific configuration:

BOT_TOKEN: Your Telegram bot token
MONGO_URI: MongoDB connection string
AUTHORIZED_USERS: Comma-separated admin user IDs
BLOCKED_PORTS: Comma-separated ports to block
TIMEZONE: Your preferred timezone
MAX_BANDWIDTH_MBPS: Maximum bandwidth limit
Usage
Basic Commands
/start - Initialize the bot
/help - Show help information
/auth - Request authorization
/stats - Show system statistics (admin only)
/ping - Check bot status
/setthread <value> - Set thread value for actions
/history - View your action history
/usage - Check your usage limits
DDoS Protection Commands
Manual Mode: <IP> <PORT> <DURATION> (e.g. 203.0.113.5 14567 60)
Auto Mode: <IP> <PORT> (e.g. 203.0.113.5 14567)
stop all - Stop all running actions
Admin Commands
/approve <user_id> <duration> - Approve user authorization
/reject <user_id> - Reject user authorization
/remove <user_id> - Remove user authorization
/yell <message> - Broadcast message to all users
/list_active - List all active actions
Disclaimer
This bot is designed for educational and protective purposes only. The authors do not condone any illegal use of this software. Use responsibly.

License
Copyright © 2025 IBR. All rights reserved.