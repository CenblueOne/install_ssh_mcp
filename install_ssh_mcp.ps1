# install_ssh_mcp.ps1 — Install dependencies untuk ssh_mcp_server.py
# Jalankan sekali sebelum pakai SSH MCP di Claude Desktop

$python = "C:\Python314\python.exe"

Write-Host "Installing fastmcp, paramiko, python-dotenv..." -ForegroundColor Cyan

& $python -m pip install --upgrade fastmcp paramiko python-dotenv

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "OK — Dependencies berhasil diinstall." -ForegroundColor Green
    Write-Host "Langkah berikutnya:" -ForegroundColor Yellow
    Write-Host "  1. Copy claude_desktop_config.json ke %APPDATA%\Claude\" -ForegroundColor Yellow
    Write-Host "  2. Restart Claude Desktop" -ForegroundColor Yellow
} else {
    Write-Host "GAGAL — Cek error di atas." -ForegroundColor Red
}

# Read-Host dihapus agar bisa dijalankan non-interaktif (CI / script)
