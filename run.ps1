# PowerShell script to run AI Career Counsellor
# Starts both Rasa server and Streamlit frontend

Write-Host "Starting AI Career Counsellor..." -ForegroundColor Green
Write-Host "This will start two services:" -ForegroundColor Yellow
Write-Host "1. Rasa Server (Backend AI) on http://localhost:5005" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup first." -ForegroundColor Red
    Write-Host "Run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"

# Check if dependencies are installed
try {
    python -c "import rasa, streamlit, nltk, spacy" 2>$null
    Write-Host "Dependencies verified" -ForegroundColor Green
} catch {
    Write-Host "Dependencies not installed. Please run: pip install -r requirements.txt" -ForegroundColor Red
    exit 1
}

# Download spaCy model if not present
try {
    python -c "import spacy; spacy.load('en_core_web_md')" 2>$null
    Write-Host "spaCy model verified" -ForegroundColor Green
} catch {
    Write-Host "Downloading spaCy model..." -ForegroundColor Blue
    python -m spacy download en_core_web_md
}

# Check if model is trained
if (!(Test-Path "models")) {
    Write-Host "Training Rasa model (this may take a few minutes)..." -ForegroundColor Blue
    rasa train --quiet
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Green

# Start Rasa server directly (not in background)
Write-Host "Starting Rasa server..." -ForegroundColor Blue
Write-Host "Note: Rasa will run in the foreground. Use a new terminal to start Streamlit if needed." -ForegroundColor Yellow
Write-Host ""

# Check if Rasa model exists
if (!(Test-Path "models")) {
    Write-Host "Training Rasa model first (this may take a few minutes)..." -ForegroundColor Blue
    rasa train --quiet
}

Write-Host "Starting Rasa server. It will be available at http://localhost:5005" -ForegroundColor Green
Write-Host "Keep this window open. Open a new PowerShell window to start Streamlit." -ForegroundColor Cyan
Write-Host ""

# Start Rasa (this will run until stopped)
rasa run --cors "*" --enable-api
