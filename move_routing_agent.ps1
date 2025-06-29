# PowerShell script to move routing_agent to agents folder
# Run this script when the routing_agent is not in use

Write-Host "Moving routing_agent to agents folder..." -ForegroundColor Green

try {
    # Check if routing_agent exists in the current directory
    if (Test-Path "routing_agent") {
        # Move routing_agent to agents folder
        Move-Item "routing_agent" "agents/"
        Write-Host "✅ Successfully moved routing_agent to agents folder" -ForegroundColor Green
        Write-Host "📁 New location: agents/routing_agent" -ForegroundColor Cyan
    } else {
        Write-Host "❌ routing_agent directory not found in current location" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error moving routing_agent: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure the routing_agent is not currently in use" -ForegroundColor Yellow
}

Write-Host "`n📁 Current agents folder structure:" -ForegroundColor Cyan
Get-ChildItem "agents" | ForEach-Object {
    Write-Host "  📂 $($_.Name)" -ForegroundColor White
} 