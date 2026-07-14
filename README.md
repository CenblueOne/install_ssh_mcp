# SSH MCP Server untuk Hermes Agent

MCP server yang memungkinkan **Hermes Agent** mengontrol server/VPS jarak jauh
via SSH (paramiko, transport stdio). Cocok untuk automation: jalankan perintah,
baca/tulis file, dan kelola proses di remote host.

> Open source, bisa dipakai umum. Sesuaikan `.env` dengan server Anda sendiri.

## Fitur / Tools
- `ssh_exec(command)` — jalankan perintah di remote (pm2, docker, tmux, dll)
- `ssh_read_file(path)` — baca file remote
- `ssh_write_file(path, content)` — tulis file remote
- `ssh_list_dir(path)` — list isi direktori remote

## Prasyarat
- Python 3.11+
- Akses SSH ke target host (user + private key)
- Hermes Agent (untuk register sebagai MCP)

## Instalasi

```bash
# 1. Siapkan SSH key (jangan commit key ke repo)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
# letakkan private key Anda di sini, mis. ~/.ssh/id_rsa

# 2. Buat .env dari template
cp .env.example .env
# edit .env: isi VPS_HOST, VPS_USER, VPS_KEY_PATH, dst.

# 3. Virtualenv + dependencies
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # Linux/macOS
# atau: .venv\Scripts\pip install -r requirements.txt  (Windows)
```

Isi `.env`:
```
VPS_HOST=203.0.113.10          # ganti IP/host server Anda
VPS_PORT=22
VPS_USER=ubuntu                # ganti user SSH Anda
VPS_KEY_PATH=~/.ssh/id_rsa     # path ke private key
CMD_TIMEOUT=60                 # timeout perintah (detik)
```

## Register ke Hermes Agent

```bash
hermes mcp add ssh-remote \
  --command ".venv/bin/python" \
  --args "ssh_mcp_server.py"
hermes mcp list
```

## Test

```bash
.venv/bin/python ssh_mcp_server.py --help
hermes mcp test ssh-remote
```

## Keamanan
- **Jangan commit** `.env` atau private key (`*.pem`, `*.key`). Sudah di-ignore
  oleh `.gitignore`.
- Berikan permission key seminimal mungkin di server target.
- MCP ini memberi akses penuh shell ke remote host — gunakan hanya pada
  server yang Anda kuasai / berwenang.

## Struktur
```
install_ssh_mcp/
├── ssh_mcp_server.py   # entrypoint MCP (stdio)
├── main.py             # helper/launch (jika ada)
├── install_ssh_mcp.ps1 # installer PowerShell (Windows)
├── requirements.txt
├── .env.example        # template konfigurasi
└── README.md
```

## Lisensi
MIT — bebas digunakan & dimodifikasi.
