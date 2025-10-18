# loop.ps1 - Autonomous AI Revenue Engine
# Dusti (DroxAI) - Architect Level Execution

$ErrorActionPreference = "Stop"
$env:PROJECT_ROOT = "C:\Users\dusti\Code-AutonomyLoop"
$env:FRONTEND_PORT = "5174"
$env:BACKEND_PORT = "9333"
$env:OLLAMA_MODEL = "dolphin-mixtral"

Write-Host "`n🔁 Spinning up Autonomy Loop...`n"

# Step 1: Boot Backend API (FastAPI on 9333)
Write-Host "🚀 Starting backend API on port $env:BACKEND_PORT..."
Start-Process powershell -WindowStyle Hidden -ArgumentList "cd $env:PROJECT_ROOT\backend\app; uvicorn main:app --host 127.0.0.1 --port $env:BACKEND_PORT"

Start-Sleep -Seconds 2

# Step 2: Boot Frontend UI (Vite + React on 5174)
Write-Host "🎨 Starting frontend UI on port $env:FRONTEND_PORT..."
Start-Process powershell -WindowStyle Hidden -ArgumentList "cd $env:PROJECT_ROOT\frontend; npm run dev -- --port $env:FRONTEND_PORT"

Start-Sleep -Seconds 2

# Step 3: Trigger Market Scan + Offer Build
Write-Host "📡 Scanning market trends + generating Stripe product..."
python "$env:PROJECT_ROOT\backend\app\market_agent.py"
python "$env:PROJECT_ROOT\backend\app\offer_builder.py"

# Step 4: Fire LLM to write copy / CTA / headlines
Write-Host "🧠 Prompting local model ($env:OLLAMA_MODEL) to generate content..."
ollama run $env:OLLAMA_MODEL --prompt "$(Get-Content $env:PROJECT_ROOT\models\prompt_templates\offer_generator.txt -Raw)"

# Step 5: Log + Monitor Feedback Loop
Write-Host "📈 Activating feedback engine..."
python "$env:PROJECT_ROOT\backend\app\loop_engine.py"

# Step 6: Log completion
Write-Host "`n✅ Loop complete. Monitor UI at http://localhost:$env:FRONTEND_PORT"
Write-Host "🧠 API running at http://127.0.0.1:$env:BACKEND_PORT/docs"
Write-Host "`n📁 Root: $env:PROJECT_ROOT"