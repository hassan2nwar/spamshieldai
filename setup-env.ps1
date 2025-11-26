# PowerShell script to create .env file from template
# Run this script: .\setup-env.ps1

if (Test-Path ".env") {
    Write-Host ".env file already exists. Skipping creation." -ForegroundColor Yellow
    Write-Host "If you want to recreate it, delete .env first and run this script again." -ForegroundColor Yellow
} else {
    if (Test-Path "env.template") {
        Copy-Item "env.template" ".env"
        Write-Host ".env file created successfully from env.template!" -ForegroundColor Green
        Write-Host "You can now edit .env to customize your configuration." -ForegroundColor Green
    } else {
        Write-Host "Error: env.template file not found!" -ForegroundColor Red
        exit 1
    }
}

