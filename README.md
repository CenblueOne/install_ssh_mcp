# SSH MCP Server (Universal — Semua AI Client)

MCP server yang memungkinkan **client AI apa pun yang mendukung MCP stdio**
mengontrol server/VPS jarak jauh via SSH (paramiko). Cocok untuk automation:
jalankan perintah, baca/tulis file, dan kelola proses di remote host.

> Open source, bisa dipakai umum. Sesuaikan `.env` dengan server Anda sendiri.
> Bekerja dengan Claude Desktop, Hermes Agent, Cursor, VS Code, dan client MCP lainnya.

## Fitur / Tools
- `ssh_exec(command)` — jalankan perintah di remote (pm2, docker, tmux, dll)
- `ssh_read_file(path)` — baca file remote
- `ssh_write_file(path, content)` — tulis file remote
- `ssh_list_dir(path)` — list isi direktori remote

## Prasyarat
- Python 3.11+
- Akses SSH ke target host (user + private key)
- Client AI yang mendukung MCP stdio (Claude Desktop, Hermes Agent, Cursor, VS Code, dll)

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

## Semua AI Client (Model-Agnostic)

Server ini menggunakan **MCP stdio transport** — artinya bisa dipakai oleh
**semua model AI / client yang mendukung MCP**, bukan hanya satu vendor.
Contoh konfigurasi ada di [`mcp-config.example.json`](mcp-config.example.json)
(ganti `PATH_KE_FOLDER_ANDA` dengan lokasi folder Anda):

| Client | Cara daftar |
|--------|-------------|
| **Claude Desktop** | Tambahkan isi `mcp-config.example.json` ke `claude_desktop_config.json` (`%APPDATA%\Claude\`) |
| **Hermes Agent** | `hermes mcp add ssh-remote --command python --args ssh_mcp_server.py` |
| **Cursor / VS Code** | Masukkan ke `mcp.json` / MCP settings dengan command `python ssh_mcp_server.py` |
| **Lainnya** | Bila client mendukung MCP stdio, arahkan ke `ssh_mcp_server.py` |

Semua client memanggil **tool yang sama** (`ssh_exec`, `ssh_read_file`, dll).
Tidak ada hardcode ke model tertentu.

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
├── main.py             # helper/launch
├── install_ssh_mcp.ps1 # installer PowerShell (Windows)
├── mcp-config.example.json # contoh config multi-client (Claude/Hermes/Cursor)
├── requirements.txt
├── .env.example        # template konfigurasi
├── LICENSE             # MIT
├── SECURITY.md         # kebijakan keamanan
└── README.md
```

## Lisensi
Lihat file [`LICENSE`](LICENSE) — **MIT**. Bebas digunakan & dimodifikasi.
Untuk kebijakan keamanan, lihat [`SECURITY.md`](SECURITY.md).
