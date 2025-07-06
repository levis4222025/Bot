@echo off
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    🎮 BGMI WARRIOR BOT 🎮                       ║
echo ║                 🤖 AI-POWERED EDITION 🤖                       ║
echo ║                                                                ║
echo ║               🚀 PRODUCTION SETUP SCRIPT 🚀                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 🔧 Starting AI-powered production setup...
echo.

REM Check Python installation
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python found!

REM Check Python version
echo 🔍 Verifying Python version...
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set "python_version=%%a"
echo 📊 Python version: %python_version%

REM Create virtual environment
echo.
echo 🌟 Creating production virtual environment...
if exist "venv" (
    echo 📁 Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo ✅ Virtual environment created!
)

REM Activate virtual environment
echo.
echo ⚡ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo 📦 Upgrading pip to latest version...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo 🚀 Installing AI-powered dependencies...
echo 📋 This may take a few minutes...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo 💡 Please check your internet connection and try again
    pause
    exit /b 1
)
echo ✅ All AI dependencies installed successfully!

REM Create directories
echo.
echo 📁 Creating production directory structure...
mkdir bot_logs 2>nul
mkdir themes 2>nul
mkdir user_data 2>nul
mkdir backups 2>nul
mkdir music 2>nul
mkdir ai_models 2>nul
mkdir language_packs 2>nul
echo ✅ Directory structure created!

REM Copy configuration template
echo.
echo ⚙️ Setting up production configuration...
if not exist ".env" (
    copy ".env.example" ".env"
    echo ✅ Configuration template created as .env
    echo 🔧 Please edit .env file with your bot token and settings
) else (
    echo 📄 Configuration file already exists
)

REM Display feature summary
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                🎊 AI-POWERED SETUP COMPLETE! 🎊                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 🤖 AI-POWERED FEATURES INSTALLED:
echo   • 🧠 Intelligent Command Understanding
echo   • 🌍 Multi-Language AI Translation
echo   • 🎨 8 Dynamic Themes with AI Adaptation
echo   • ⚡ Smart Combat Modes (Auto-optimized)
echo   • 🎮 AI-Enhanced Mini-Games
echo   • 🏆 Intelligent Achievement System
echo   • 🎵 AI Music Recommendation Engine
echo   • 📊 Predictive Analytics Dashboard
echo   • 🤖 Natural Language Processing
echo   • 🔮 Smart User Behavior Analysis
echo   • �️ AI-Powered Security Detection
echo   • 🌈 Adaptive UI Based on User Preferences
echo.
echo 🔧 NEXT STEPS:
echo   1. Edit .env file with your bot token
echo   2. Configure MongoDB connection
echo   3. Set admin user IDs in .env
echo   4. Run: python main.py
echo.
echo 💡 QUICK START:
echo   python main.py
echo.
echo 📚 DOCUMENTATION:
echo   • README.md - Complete AI feature guide
echo   • .env.example - Configuration reference
echo.
echo 🤖 AI CAPABILITIES:
echo   • Natural language command understanding
echo   • Automatic language detection and translation
echo   • Intelligent user behavior adaptation
echo   • Smart recommendation system
echo.

REM Check if user wants to edit config now
echo.
set /p edit_config="🔧 Would you like to edit the configuration now? (y/n): "
if /i "%edit_config%"=="y" (
    echo 📝 Opening configuration file...
    notepad .env
)

echo.
set /p start_bot="🚀 Would you like to start the AI-powered bot now? (y/n): "
if /i "%start_bot%"=="y" (
    echo 🤖 Starting BGMI Warrior Bot - AI-Powered Edition...
    python main.py
) else (
    echo 👋 Setup complete! Run 'python main.py' when ready.
)

echo.
echo ✨ Thank you for choosing BGMI Warrior Bot - AI-Powered Edition! ✨
pause
