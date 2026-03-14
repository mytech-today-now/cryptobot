# Install and Initialize Beads
# This script installs the latest version of Beads CLI and initializes it for this repository

param(
    [switch]$Force,
    [switch]$SkipInit
)

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           Beads Installation and Initialization Script        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

try {
    $nodeVersion = node --version 2>$null
    Write-Host "  ✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Node.js is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

try {
    $npmVersion = npm --version 2>$null
    Write-Host "  ✅ npm: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ npm is not installed!" -ForegroundColor Red
    Write-Host ""
    exit 1
}

Write-Host ""

# Check if bd is already installed
$bdInstalled = $false
try {
    $bdVersion = bd --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $bdInstalled = $true
        Write-Host "📦 Current Beads CLI version: $bdVersion" -ForegroundColor Cyan
        Write-Host ""
    }
} catch {
    Write-Host "📦 Beads CLI is not currently installed" -ForegroundColor Yellow
    Write-Host ""
}

# Uninstall existing version if Force flag is set or if installation is broken
if ($bdInstalled -and $Force) {
    Write-Host "🗑️  Uninstalling existing Beads CLI (--Force flag set)..." -ForegroundColor Yellow
    npm uninstall -g @beads/bd
    Write-Host "  ✅ Uninstalled" -ForegroundColor Green
    Write-Host ""
} elseif ($bdInstalled) {
    Write-Host "⚠️  Beads CLI is already installed" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  1. Continue with existing installation"
    Write-Host "  2. Reinstall (uninstall and install latest)"
    Write-Host "  3. Cancel"
    Write-Host ""
    $choice = Read-Host "Enter choice (1-3)"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "✅ Continuing with existing installation" -ForegroundColor Green
            Write-Host ""
        }
        "2" {
            Write-Host ""
            Write-Host "🗑️  Uninstalling existing Beads CLI..." -ForegroundColor Yellow
            npm uninstall -g @beads/bd
            Write-Host "  ✅ Uninstalled" -ForegroundColor Green
            Write-Host ""
            $bdInstalled = $false
        }
        "3" {
            Write-Host ""
            Write-Host "❌ Installation cancelled" -ForegroundColor Red
            Write-Host ""
            exit 0
        }
        default {
            Write-Host ""
            Write-Host "❌ Invalid choice. Exiting." -ForegroundColor Red
            Write-Host ""
            exit 1
        }
    }
}

# Install Beads CLI
if (-not $bdInstalled) {
    Write-Host "📥 Installing latest Beads CLI from npm..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  Note: If installation fails due to file locking, try:" -ForegroundColor Yellow
    Write-Host "   1. Temporarily disable antivirus/Windows Defender" -ForegroundColor Gray
    Write-Host "   2. Close any file explorer windows in npm directories" -ForegroundColor Gray
    Write-Host "   3. Run this script again" -ForegroundColor Gray
    Write-Host ""

    # Try installation with retry logic
    $maxRetries = 3
    $retryCount = 0
    $installSuccess = $false

    while ($retryCount -lt $maxRetries -and -not $installSuccess) {
        if ($retryCount -gt 0) {
            Write-Host "⏳ Retry attempt $retryCount of $($maxRetries - 1)..." -ForegroundColor Yellow
            Write-Host "   Waiting 3 seconds for file locks to release..." -ForegroundColor Gray
            Start-Sleep -Seconds 3
        }

        npm install -g @beads/bd 2>&1 | Out-Null

        if ($LASTEXITCODE -eq 0) {
            $installSuccess = $true
        } else {
            $retryCount++
        }
    }

    if (-not $installSuccess) {
        Write-Host ""
        Write-Host "❌ Failed to install Beads CLI after $maxRetries attempts" -ForegroundColor Red
        Write-Host ""
        Write-Host "💡 Alternative Installation Methods:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Manual npm installation (with verbose output):" -ForegroundColor Yellow
        Write-Host "   npm install -g @beads/bd --verbose" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Download binary directly from GitHub:" -ForegroundColor Yellow
        Write-Host "   https://github.com/steveyegge/beads/releases/latest" -ForegroundColor White
        Write-Host "   - Download beads_*_windows_amd64.zip" -ForegroundColor Gray
        Write-Host "   - Extract bd.exe to a folder in your PATH" -ForegroundColor Gray
        Write-Host ""
        Write-Host "3. Use PowerShell helper scripts (no installation needed):" -ForegroundColor Yellow
        Write-Host "   . .\scripts\beads-helpers.ps1" -ForegroundColor White
        Write-Host "   bd-list-open" -ForegroundColor White
        Write-Host ""
        Write-Host "4. Clear npm cache and retry:" -ForegroundColor Yellow
        Write-Host "   npm cache clean --force" -ForegroundColor White
        Write-Host "   .\scripts\install-beads.ps1 -Force" -ForegroundColor White
        Write-Host ""

        # Ask if user wants to use helper scripts instead
        Write-Host "Would you like to use the PowerShell helper scripts instead? (y/n)" -ForegroundColor Cyan
        $useHelpers = Read-Host

        if ($useHelpers -eq "y" -or $useHelpers -eq "Y") {
            Write-Host ""
            Write-Host "✅ Using PowerShell helper scripts" -ForegroundColor Green
            Write-Host ""
            Write-Host "To use Beads commands, run:" -ForegroundColor Cyan
            Write-Host "  . .\scripts\beads-helpers.ps1" -ForegroundColor White
            Write-Host ""
            Write-Host "Then use these commands:" -ForegroundColor Cyan
            Write-Host "  bd-list-open          # List open tasks" -ForegroundColor White
            Write-Host "  bd-show bd-augext.1   # Show task details" -ForegroundColor White
            Write-Host "  bd-list-augext        # List augext epic tasks" -ForegroundColor White
            Write-Host "  bd-help               # Show all commands" -ForegroundColor White
            Write-Host ""
            Write-Host "See BEADS-USAGE.md for complete documentation" -ForegroundColor Gray
            Write-Host ""
            exit 0
        } else {
            exit 1
        }
    }

    Write-Host ""
    Write-Host "  ✅ Beads CLI installed successfully!" -ForegroundColor Green
    Write-Host ""
}

# Verify installation
Write-Host "🔍 Verifying installation..." -ForegroundColor Yellow
Write-Host ""

try {
    $bdVersion = bd --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Beads CLI version: $bdVersion" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "  ⚠️  bd command found but returned error: $bdVersion" -ForegroundColor Yellow
        Write-Host ""
    }
} catch {
    Write-Host "  ❌ Failed to verify Beads CLI installation" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    exit 1
}

# Initialize Beads (if not skipped)
if (-not $SkipInit) {
    Write-Host "🔧 Checking Beads initialization..." -ForegroundColor Yellow
    Write-Host ""
    
    if (Test-Path ".beads/config.json") {
        Write-Host "  ✅ Beads is already initialized in this repository" -ForegroundColor Green
        Write-Host ""
        Write-Host "Configuration:" -ForegroundColor Cyan
        $config = Get-Content ".beads/config.json" | ConvertFrom-Json
        Write-Host "  • Project: $($config.project.name)" -ForegroundColor White
        Write-Host "  • Storage: $($config.storage.type)" -ForegroundColor White
        Write-Host "  • Sync Branch: $($config.sync.branch)" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "  ℹ️  Beads is not initialized in this repository" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Would you like to initialize Beads now? (y/n)" -ForegroundColor Yellow
        $initChoice = Read-Host
        
        if ($initChoice -eq "y" -or $initChoice -eq "Y") {
            Write-Host ""
            Write-Host "🚀 Initializing Beads..." -ForegroundColor Yellow
            Write-Host ""
            
            bd init
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "  ✅ Beads initialized successfully!" -ForegroundColor Green
                Write-Host ""
            } else {
                Write-Host ""
                Write-Host "  ⚠️  Beads initialization completed with warnings" -ForegroundColor Yellow
                Write-Host ""
            }
        } else {
            Write-Host ""
            Write-Host "  ⏭️  Skipping initialization" -ForegroundColor Yellow
            Write-Host ""
        }
    }
}

# Final summary
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Installation Complete!                     ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "✨ Beads is ready to use!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Quick Start Commands:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  bd list                    # List all issues" -ForegroundColor White
Write-Host "  bd list --status open      # List open issues" -ForegroundColor White
Write-Host "  bd show <id>               # Show issue details" -ForegroundColor White
Write-Host "  bd create 'title'          # Create new issue" -ForegroundColor White
Write-Host "  bd update <id> --status    # Update issue status" -ForegroundColor White
Write-Host "  bd sync                    # Sync with git remote" -ForegroundColor White
Write-Host ""
Write-Host "📖 Documentation:" -ForegroundColor Cyan
Write-Host "  • BEADS-USAGE.md - Usage guide for this repository" -ForegroundColor White
Write-Host "  • .beads/README.md - General Beads information" -ForegroundColor White
Write-Host "  • https://github.com/steveyegge/beads - Official documentation" -ForegroundColor White
Write-Host ""

