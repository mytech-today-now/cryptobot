# Install Beads Binary Directly (Bypass npm)
# Downloads and installs the Beads binary directly from GitHub releases

param(
    [string]$InstallPath = "$env:LOCALAPPDATA\beads",
    [string]$Version = "0.49.1"
)

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         Beads Binary Installation (Direct Download)           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$downloadUrl = "https://github.com/steveyegge/beads/releases/download/v$Version/beads_${Version}_windows_amd64.zip"
$tempZip = "$env:TEMP\beads_${Version}_windows_amd64.zip"
$tempExtract = "$env:TEMP\beads_extract"

Write-Host "📋 Installation Details:" -ForegroundColor Cyan
Write-Host "   Version: $Version" -ForegroundColor White
Write-Host "   Install Path: $InstallPath" -ForegroundColor White
Write-Host "   Download URL: $downloadUrl" -ForegroundColor White
Write-Host ""

# Create installation directory
Write-Host "📁 Creating installation directory..." -ForegroundColor Yellow
if (-not (Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    Write-Host "   ✅ Created: $InstallPath" -ForegroundColor Green
} else {
    Write-Host "   ✅ Directory exists: $InstallPath" -ForegroundColor Green
}
Write-Host ""

# Download binary
Write-Host "📥 Downloading Beads binary..." -ForegroundColor Yellow
Write-Host "   This may take a moment..." -ForegroundColor Gray
Write-Host ""

try {
    # Use .NET WebClient for better progress
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($downloadUrl, $tempZip)
    Write-Host "   ✅ Downloaded successfully" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Download failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Try downloading manually:" -ForegroundColor Yellow
    Write-Host "   1. Open: https://github.com/steveyegge/beads/releases/latest" -ForegroundColor White
    Write-Host "   2. Download: beads_${Version}_windows_amd64.zip" -ForegroundColor White
    Write-Host "   3. Extract bd.exe to: $InstallPath" -ForegroundColor White
    Write-Host ""
    exit 1
}
Write-Host ""

# Extract binary
Write-Host "📦 Extracting binary..." -ForegroundColor Yellow

try {
    # Create temp extraction directory
    if (Test-Path $tempExtract) {
        Remove-Item -Path $tempExtract -Recurse -Force
    }
    New-Item -ItemType Directory -Path $tempExtract -Force | Out-Null
    
    # Extract ZIP
    Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
    
    # Find bd.exe
    $bdExe = Get-ChildItem -Path $tempExtract -Filter "bd.exe" -Recurse | Select-Object -First 1
    
    if ($bdExe) {
        # Copy to installation directory
        Copy-Item -Path $bdExe.FullName -Destination "$InstallPath\bd.exe" -Force
        Write-Host "   ✅ Extracted bd.exe to $InstallPath" -ForegroundColor Green
    } else {
        Write-Host "   ❌ bd.exe not found in archive" -ForegroundColor Red
        Write-Host ""
        Write-Host "Archive contents:" -ForegroundColor Yellow
        Get-ChildItem -Path $tempExtract -Recurse | ForEach-Object { Write-Host "   $_" }
        Write-Host ""
        exit 1
    }
} catch {
    Write-Host "   ❌ Extraction failed: $_" -ForegroundColor Red
    Write-Host ""
    exit 1
}
Write-Host ""

# Clean up temp files
Write-Host "🧹 Cleaning up temporary files..." -ForegroundColor Yellow
Remove-Item -Path $tempZip -Force -ErrorAction SilentlyContinue
Remove-Item -Path $tempExtract -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "   ✅ Cleanup complete" -ForegroundColor Green
Write-Host ""

# Add to PATH
Write-Host "🔧 Adding to PATH..." -ForegroundColor Yellow

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$InstallPath*") {
    try {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallPath", "User")
        Write-Host "   ✅ Added $InstallPath to User PATH" -ForegroundColor Green
        Write-Host "   ⚠️  You must restart PowerShell for PATH changes to take effect" -ForegroundColor Yellow
    } catch {
        Write-Host "   ⚠️  Could not automatically add to PATH: $_" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "   Please add manually:" -ForegroundColor Cyan
        Write-Host "   1. Press Win+X → System → Advanced system settings" -ForegroundColor White
        Write-Host "   2. Click 'Environment Variables'" -ForegroundColor White
        Write-Host "   3. Under 'User variables', select 'Path' → Edit" -ForegroundColor White
        Write-Host "   4. Click 'New' and add: $InstallPath" -ForegroundColor White
        Write-Host "   5. Click OK on all dialogs" -ForegroundColor White
    }
} else {
    Write-Host "   ✅ $InstallPath is already in PATH" -ForegroundColor Green
}
Write-Host ""

# Verify installation
Write-Host "🔍 Verifying installation..." -ForegroundColor Yellow

if (Test-Path "$InstallPath\bd.exe") {
    Write-Host "   ✅ bd.exe found at: $InstallPath\bd.exe" -ForegroundColor Green
    
    # Try to run bd --version (may not work until PATH is refreshed)
    $env:Path = "$env:Path;$InstallPath"
    try {
        $version = & "$InstallPath\bd.exe" --version 2>&1
        Write-Host "   ✅ Version: $version" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  Could not verify version (restart PowerShell and try 'bd --version')" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ bd.exe not found at expected location" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Final instructions
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Installation Complete!                     ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "✨ Beads binary installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Installation Location:" -ForegroundColor Cyan
Write-Host "   $InstallPath\bd.exe" -ForegroundColor White
Write-Host ""
Write-Host "🔄 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   1. RESTART PowerShell (required for PATH changes)" -ForegroundColor Yellow
Write-Host ""
Write-Host "   2. Verify installation:" -ForegroundColor White
Write-Host "      bd --version" -ForegroundColor Cyan
Write-Host ""
Write-Host "   3. Use Beads commands:" -ForegroundColor White
Write-Host "      bd list" -ForegroundColor Cyan
Write-Host "      bd list --status open" -ForegroundColor Cyan
Write-Host "      bd show bd-augext" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 If 'bd' command is not found after restarting:" -ForegroundColor Yellow
Write-Host "   Use full path: $InstallPath\bd.exe list" -ForegroundColor White
Write-Host ""

