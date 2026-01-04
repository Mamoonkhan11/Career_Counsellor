#!/usr/bin/env python3
"""
AI Career Counsellor Setup Script
Automated setup for development and production environments
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"[WORKING] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} completed")
        return True
        return True
    except subprocess.CalledProcessError as e:
        print(f" {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print(" Python 3.10 or higher is required")
        return False
    print(f"Python {sys.version.split()[0]} detected")
    return True

def create_virtual_environment():
    """Create Python virtual environment"""
    if os.path.exists("venv"):
        print("Virtual environment already exists")
        return True

    return run_command("python -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install Python dependencies"""
    # Activate virtual environment
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"

    # Install requirements
    return run_command(f"{pip_cmd} install -r ./requirements.txt", "Installing dependencies")

def download_spacy_model():
    """Download spaCy language model"""
    # Activate virtual environment and download model
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"

    # Check if model is already downloaded
    try:
        result = subprocess.run(f'{python_cmd} -c "import spacy; spacy.load(\'en_core_web_md\')"',
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("spaCy model already downloaded")
            return True
    except:
        pass

    return run_command(f"{python_cmd} -m spacy download en_core_web_md", "Downloading spaCy model")

def train_rasa_model():
    """Train the Rasa model"""
    if os.path.exists("models"):
        print("Rasa model already trained")
        return True

    # Activate virtual environment
    if platform.system() == "Windows":
        rasa_cmd = "venv\\Scripts\\rasa"
    else:
        rasa_cmd = "venv/bin/rasa"

    return run_command(f"{rasa_cmd} train --quiet", "Training Rasa model")

def create_data_directories():
    """Create necessary data directories"""
    directories = ["data", "models", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("Data directories created")
    return True

def main():
    """Main setup function"""
    print("AI Career Counsellor Setup")
    print("=" * 50)

    # Check Python version
    if not check_python_version():
        return False

    # Create data directories
    if not create_data_directories():
        return False

    # Create virtual environment
    if not create_virtual_environment():
        return False

    # Install dependencies
    if not install_dependencies():
        return False

    # Download spaCy model
    if not download_spacy_model():
        return False

    # Train Rasa model
    if not train_rasa_model():
        return False

    print("")
    print("Setup completed successfully!")
    print("")
    print("To start the application:")
    if platform.system() == "Windows":
        print("   Run: .\\run.ps1")
    else:
        print("   Run: ./run.sh")
    print("")
    print(" Or start services manually:")
    print("   1. Rasa server: rasa run --cors \"*\" --enable-api")
    print("   2. Frontend: streamlit run frontend/app.py")
    print("")
    print("Then open: http://localhost:8501")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
