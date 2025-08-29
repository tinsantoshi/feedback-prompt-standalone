#!/usr/bin/env python3
"""
Helper script to run the Prompt Feedback Tool locally.
This script checks dependencies and launches the Streamlit app.
"""

import os
import sys
import subprocess
import webbrowser
from time import sleep

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_pip():
    """Check if pip is installed"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ pip is installed")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ pip is not installed or not working properly")
        return False

def install_requirements():
    """Install required packages"""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print("❌ requirements.txt not found")
        return False
    
    print("📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], 
                      check=True)
        print("✅ Required packages installed successfully")
        return True
    except subprocess.SubprocessError as e:
        print(f"❌ Failed to install required packages: {e}")
        return False

def check_streamlit():
    """Check if Streamlit is installed and working"""
    try:
        result = subprocess.run([sys.executable, "-m", "streamlit", "--version"], 
                               check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        version = result.stdout.decode().strip() or result.stderr.decode().strip()
        print(f"✅ Streamlit is installed: {version}")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Streamlit is not installed or not working properly")
        return False

def setup_env_file():
    """Create a .env file for environment variables if it doesn't exist"""
    env_file = ".env"
    
    if os.path.exists(env_file):
        print("ℹ️ .env file already exists")
        return
    
    print("🔑 Creating .env file for API keys...")
    with open(env_file, "w") as f:
        f.write("# OpenAI API Key\n")
        f.write("OPENAI_API_KEY=\n\n")
        f.write("# Add other environment variables below\n")
    
    print("✅ Created .env file. Please edit it to add your API keys.")

def run_app():
    """Run the Streamlit app"""
    app_file = "streamlit_app.py"
    
    if not os.path.exists(app_file):
        print("❌ streamlit_app.py not found")
        return False
    
    print("🚀 Running the Streamlit app...")
    
    # Start the Streamlit app in a new process
    process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", app_file])
    
    # Wait a moment for the server to start
    sleep(2)
    
    # Open the browser
    webbrowser.open("http://localhost:8501")
    
    print("✅ App is running at http://localhost:8501")
    print("Press Ctrl+C to stop the app")
    
    try:
        # Wait for the user to stop the app
        process.wait()
    except KeyboardInterrupt:
        print("\n👋 Stopping the app...")
        process.terminate()
    
    return True

def main():
    """Main function"""
    print("=" * 50)
    print("Prompt Feedback Tool - Local Setup")
    print("=" * 50)
    print()
    
    # Check Python version
    check_python_version()
    
    # Check pip
    if not check_pip():
        print("Please install pip and try again.")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Failed to install required packages. Please install them manually.")
        sys.exit(1)
    
    # Setup .env file
    setup_env_file()
    
    # Check Streamlit
    if not check_streamlit():
        print("Streamlit is not installed or not working properly.")
        print("Please make sure Streamlit is installed correctly.")
        sys.exit(1)
    
    # Run the app
    run_app()

if __name__ == "__main__":
    main()