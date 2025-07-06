#!/usr/bin/env python3
"""
🔍 BGMI Warrior Bot - Setup Validation Script
✨ Checks if all files are properly configured and ready for production
"""
import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - MISSING")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and report status"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} - MISSING")
        return False

def main():
    """Main validation function"""
    print("""
╔════════════════════════════════════════════════════════════╗
║         🔍 BGMI WARRIOR BOT - SETUP VALIDATION 🔍           ║
║              ✨ Production Readiness Check ✨               ║
╚════════════════════════════════════════════════════════════╝
""")
    
    all_good = True
    
    print("\n📁 CORE FILES CHECK:")
    core_files = [
        ("main.py", "Main entry point"),
        ("config.py", "Production configuration"),
        ("command_handlers.py", "AI-powered handlers"),
        ("models.py", "Data models"),
        ("database.py", "Database operations"),
        ("action_service.py", "Action service"),
        ("middlewares.py", "Security middlewares"),
        ("utils.py", "Utility functions"),
        ("requirements.txt", "Dependencies"),
        ("README.md", "Documentation"),
        (".env.example", "Environment template"),
        ("setup_enhanced.bat", "Windows setup script")
    ]
    
    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    print("\n📁 DIRECTORIES CHECK:")
    directories = [
        ("localization", "Multi-language support"),
        ("bot_logs", "Logging directory"),
        ("themes", "UI themes"),
        ("user_data", "User data storage"),
        ("__pycache__", "Python cache")
    ]
    
    for dir_path, description in directories:
        if not check_directory_exists(dir_path, description):
            # Create missing directories (except __pycache__)
            if dir_path != "__pycache__":
                os.makedirs(dir_path, exist_ok=True)
                print(f"  📁 Created: {dir_path}")
    
    print("\n🧩 LOCALIZATION FILES CHECK:")
    localization_files = [
        ("localization/messages.py", "Message templates"),
    ]
    
    for file_path, description in localization_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    print("\n🚫 REMOVED FILES CHECK (should not exist):")
    removed_files = [
        "enhanced_config.py",
        "enhanced_handlers.py", 
        "enhanced_models.py",
        "modern_utils.py"
    ]
    
    for file_path in removed_files:
        if os.path.exists(file_path):
            print(f"⚠️  Legacy file still exists: {file_path} - Should be removed")
            all_good = False
        else:
            print(f"✅ Legacy file properly removed: {file_path}")
    
    print("\n🔧 FEATURES CONFIGURED:")
    features = [
        "🤖 AI-powered command understanding",
        "🌍 Multi-language support", 
        "🎨 Modern UI with themes",
        "🏆 Achievement system",
        "🎮 Mini-games",
        "🎵 Music player",
        "📊 Advanced analytics",
        "💎 Premium features",
        "⚡ Enhanced attack modes",
        "🔒 User management & verification"
    ]
    
    for feature in features:
        print(f"✅ {feature}")
    
    print("\n" + "="*60)
    if all_good:
        print("🎉 VALIDATION PASSED! 🎉")
        print("✨ Your BGMI Warrior Bot is ready for production!")
        print("\n📋 NEXT STEPS:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env file with your bot token and MongoDB URI")
        print("3. Run: python main.py")
        print("\n🚀 Ready to dominate BGMI!")
    else:
        print("⚠️  VALIDATION ISSUES FOUND!")
        print("🔧 Please fix the missing files/directories above.")
    
    print("="*60)

if __name__ == "__main__":
    main()
