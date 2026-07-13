# SSH MCP Server — KHUSUS HERMES AGENT

MCP server untuk Hermes Agent mengontrol VPS Biznet (idxbandarhunter.com) via SSH + Cloudflare Tunnel.

**Transport**: stdio (native Hermes MCP)

## Tools
- `ssh_exec(command)` — jalankan perintah (pm2, hermes, tmux, cloudflared)
- `ssh_read_file(path)` — baca file VPS
- `ssh_write_file(path, content)` — tulis file
- `ssh_list_dir(path)` — list direktori

## Setup (langsung push saja)

```bash
cd /mnt/c/Users/Administrator/OneDrive/HERMES/MCP/install_ssh_mcp
cp -f "/mnt/c/Users/Administrator/OneDrive/CLAUDE WORK/API/biznet-vps/Jember0807.pem" ~/.ssh/Jember0807.pem
chmod 600 ~/.ssh/Jember0807.pem

# Buat .env dengan path WSL
cat > .env << EOF
VPS_HOST=103.93.163.67
VPS_PORT=22
VPS_USER=J-Squad007
VPS_KEY_PATH=/home/zorro/.ssh/Jember0807.pem
CMD_TIMEOUT=60
EOF

python3 -m venv .venv --clear
.venv/bin/pip install -r requirements.txt
```

## Register ke Hermes
```bash
hermes mcp add biznet-vps --command ".venv/bin/python" --args "ssh_mcp_server.py"
hermes mcp list
```

## Jalankan test
```bash
.venv/bin/python ssh_mcp_server.py --help
hermes mcp test biznet-vps
```

**Tunnel**: Sudah terhubung via mcp.idxbandarhunter.com (Cloudflare Tunnel ID 73bf930d-2f6a-4870-9da8-28a52f1ab325).

**OneDrive pitfall**: Jangan edit file langsung di OneDrive mount. Gunakan ~/.ssh/ untuk key.

**YA LANJUT** = jalankan semua perintah di atas.

Last updated: 2026-07-08 (Hermes optimized)
