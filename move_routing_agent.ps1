# PowerShell script to move routing-agent to agents folder
# Run this script when the routing-agent is not in use

Write-Host "Moving routing-agent to agents folder..." -ForegroundColor Green

try {
    # Check if routing-agent exists in the current directory
    if (Test-Path "routing-agent") {
        # Move routing-agent to agents folder
        Move-Item "routing-agent" "agents/"
        Write-Host "✅ Successfully moved routing-agent to agents folder" -ForegroundColor Green
        Write-Host "📁 New location: agents/routing-agent" -ForegroundColor Cyan
    } else {
        Write-Host "❌ routing-agent directory not found in current location" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error moving routing-agent: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure the routing-agent is not currently in use" -ForegroundColor Yellow
}

Write-Host "`n📁 Current agents folder structure:" -ForegroundColor Cyan
Get-ChildItem "agents" | ForEach-Object {
    Write-Host "  📂 $($_.Name)" -ForegroundColor White
} 