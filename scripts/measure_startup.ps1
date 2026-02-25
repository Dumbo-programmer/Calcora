# Measure cold start time for Calcora Desktop
# Measures time from process start to browser launch

Write-Host "Measuring Calcora Desktop cold start time..." -ForegroundColor Cyan
Write-Host ""

$measurements = @()

for ($i = 1; $i -le 3; $i++) {
    Write-Host "Run $i/3: " -NoNewline
    
    # Start timing
    $start = Get-Date
    
    # Launch Calcora (will auto-open browser)
    $process = Start-Process -FilePath ".\dist\Calcora.exe" -PassThru -WindowStyle Normal
    
    # Wait for browser launch (look for chrome/edge/firefox process spawned)
    $timeout = 10
    $elapsed = 0
    $browserLaunched = $false
    
    while ($elapsed -lt $timeout -and -not $browserLaunched) {
        Start-Sleep -Milliseconds 100
        $elapsed += 0.1
        
        # Check if browser process was created recently
        $browsers = Get-Process chrome,msedge,firefox -ErrorAction SilentlyContinue | 
                    Where-Object { $_.StartTime -gt $start }
        
        if ($browsers) {
            $browserLaunched = $true
            $end = Get-Date
            $duration = ($end - $start).TotalSeconds
            $measurements += $duration
            Write-Host "$([math]::Round($duration, 2))s" -ForegroundColor Green
        }
    }
    
    # Kill the Calcora process
    Start-Sleep -Milliseconds 500
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    
    # Wait before next test
    if ($i -lt 3) {
        Start-Sleep -Seconds 2
    }
}

Write-Host ""
Write-Host "Results:" -ForegroundColor Cyan
Write-Host "  Average: $([math]::Round(($measurements | Measure-Object -Average).Average, 2))s"
Write-Host "  Min: $([math]::Round(($measurements | Measure-Object -Minimum).Minimum, 2))s"
Write-Host "  Max: $([math]::Round(($measurements | Measure-Object -Maximum).Maximum, 2))s"
Write-Host ""

$avg = ($measurements | Measure-Object -Average).Average
if ($avg -lt 2) {
    Write-Host "✓ Excellent (<2s)" -ForegroundColor Green
} elseif ($avg -lt 3) {
    Write-Host "✓ Good (2-3s)" -ForegroundColor Green
} elseif ($avg -lt 5) {
    Write-Host "⚠ Acceptable (3-5s)" -ForegroundColor Yellow
} else {
    Write-Host "✗ Too slow (>5s)" -ForegroundColor Red
}
