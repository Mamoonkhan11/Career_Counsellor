# PowerShell script to run Streamlit frontend only
# Make sure Rasa is already running on port 5005

Write-Host "Starting Streamlit Frontend..." -ForegroundColor Green
Write-Host "Make sure Rasa server is running on http://localhost:5005" -ForegroundColor Yellow
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"

# Check if dependencies are installed
try {
    python -c "import streamlit" 2>$null
    Write-Host "Dependencies verified" -ForegroundColor Green
} catch {
    Write-Host "Streamlit not installed. Please run: pip install streamlit" -ForegroundColor Red
    exit 1
}

# Wait a moment to ensure Rasa is ready
Write-Host "Checking backend connection..." -ForegroundColor Blue
$backendReady = $false
for ($i = 1; $i -le 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5005/" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Host "✅ Backend is ready!" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "Waiting for backend... ($i/10)" -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }
}

if (!$backendReady) {
    Write-Host "⚠️ Backend may not be ready, but starting Streamlit anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Streamlit frontend..." -ForegroundColor Green
Write-Host "Open your browser to: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop Streamlit" -ForegroundColor Yellow

# Start Streamlit
streamlit run frontend/app.py --server.headless true --server.port 8501
