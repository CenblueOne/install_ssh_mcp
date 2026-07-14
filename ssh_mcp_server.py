"""
ssh_mcp_server.py — SSH MCP Server untuk Hermes Agent

MCP server untuk mengontrol server/VPS jarak jauh via SSH (paramiko).
Open source, bisa dipakai umum — sesuaikan .env dengan server Anda.

Tools: ssh_exec, ssh_read_file, ssh_write_file, ssh_list_dir, check_hermes_services
Transport: stdio (native Hermes MCP)

Konfigurasi dibaca dari .env (lihat .env.example).
"""

import os
import stat
import paramiko
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
from fastmcp import FastMCP
from typing import Optional

# Load .env from same directory
_DIR = Path(__file__).parent
load_dotenv(_DIR / ".env", override=True)

# Nilai default placeholder — override lewat .env (jangan hardcode di sini)
VPS_HOST = os.getenv("VPS_HOST", "YOUR_VPS_HOST")
VPS_PORT = int(os.getenv("VPS_PORT", "22"))
VPS_USER = os.getenv("VPS_USER", "YOUR_VPS_USER")
VPS_KEY_PATH = os.getenv("VPS_KEY_PATH", "~/.ssh/id_rsa")
CMD_TIMEOUT = int(os.getenv("CMD_TIMEOUT", "60"))

mcp = FastMCP("ssh-remote")

# Simple connection cache
@lru_cache(maxsize=2)
def _get_pkey():
    key_path = Path(VPS_KEY_PATH)
    if not key_path.exists():
        raise RuntimeError(f"VPS_KEY_PATH tidak ditemukan: {VPS_KEY_PATH}. Jalankan chmod 600 terlebih dahulu.")
    return paramiko.RSAKey.from_private_key_file(str(key_path))

def _connect() -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pkey = _get_pkey()
    client.connect(
        VPS_HOST, port=VPS_PORT, username=VPS_USER, pkey=pkey,
        timeout=15, banner_timeout=30, auth_timeout=30
    )
    return client

@mcp.tool()
def ssh_exec(command: str) -> str:
    """Jalankan perintah di VPS (pm2, hermes, tmux, cloudflared, ss -ltnp, dll)."""
    client = _connect()
    try:
        stdin, stdout, stderr = client.exec_command(command, timeout=CMD_TIMEOUT, get_pty=False)
        out = stdout.read().decode("utf-8", errors="replace").strip()
        err = stderr.read().decode("utf-8", errors="replace").strip()
        code = stdout.channel.recv_exit_status()
        result = []
        if out: result.append(out)
        if err: result.append(f"[stderr]\n{err}")
        result.append(f"[exit:{code}]")
        return "\n".join(result) or "OK (no output)"
    finally:
        client.close()

@mcp.tool()
def ssh_read_file(path: str) -> str:
    """Baca file dari VPS."""
    client = _connect()
    try:
        sftp = client.open_sftp()
        with sftp.open(path, "r") as f:
            content = f.read().decode("utf-8", errors="replace")
        sftp.close()
        return content
    finally:
        client.close()

@mcp.tool()
def ssh_write_file(path: str, content: str) -> str:
    """Tulis/overwrite file di VPS."""
    client = _connect()
    try:
        sftp = client.open_sftp()
        with sftp.open(path, "w") as f:
            f.write(content)
        sftp.close()
        return f"OK — {path} ditulis ({len(content)} chars)"
    finally:
        client.close()

@mcp.tool()
def ssh_list_dir(path: str = "~") -> str:
    """List direktori di VPS."""
    client = _connect()
    try:
        sftp = client.open_sftp()
        entries = sftp.listdir_attr(path)
        sftp.close()
        lines = ["TYPE   SIZE  NAME", "-"*40]
        for e in sorted(entries, key=lambda x: x.filename.lower()):
            ftype = "DIR " if stat.S_ISDIR(e.st_mode) else "FILE"
            lines.append(f"{ftype:6} {e.st_size:>8}  {e.filename}")
        return "\n".join(lines)
    finally:
        client.close()

@mcp.tool()
def check_hermes_services() -> str:
    """Cek status Hermes services di VPS (dashboard, tunnel, tmux, gunicorn)."""
    commands = [
        "tmux ls",
        "cloudflared tunnel list",
        "ss -ltnp | grep -E '5010|9119|cloudflared'",
        "ps aux | grep -E 'gunicorn|hermes|cloudflared' | grep -v grep",
        "ls -la ~/.cloudflared/"
    ]
    results = []
    for cmd in commands:
        results.append(f"\n$ {cmd}\n{ssh_exec(cmd)}")
    return "\n".join(results)

if __name__ == "__main__":
    print("Hermes Biznet VPS MCP Server starting (stdio)...")
    mcp.run(transport="stdio")
