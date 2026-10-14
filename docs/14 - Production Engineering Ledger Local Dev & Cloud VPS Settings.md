# 14 - Production Engineering Ledger: Local Development & Cloud Linux VPS Settings

> **System Path:** `D:\projects\tensix\docs\14 - Production Engineering Ledger Local Dev & Cloud VPS Settings.md`  
> **Source Repository:** `https://github.com/hemal9102/tensix`  
> **Classification:** Systems Engineering, Kernel Tuning, TCP Socket Scaling & Docker Isolation  

---

## 🏛️ Executive Summary

Writing high-performance asynchronous software requires alignment between the application code, the operating system kernel, and physical hardware. Default operating system configurations (Windows and stock Ubuntu/Debian) are tuned for interactive desktop usage, severely throttling high-concurrency event loops, network sockets, and file descriptor throughput.

This document serves as the master production engineering configuration ledger for **TENSIX** systems, covering:
1. **Local Development Configurations** (Windows / WSL).
2. **Cloud Linux VPS Kernel & TCP Socket Optimization** (Oracle Cloud / Ubuntu).
3. **Hardened Docker Runtime & Self-Healing Systemd Daemons**.

---

## 🛠️ Part 1: Local Development Environment (Windows / WSL)

### 1.1 Python Runtime Environment Flags
Prevent buffer latency, bytecode disk clutter, and Windows console character-map crashes:

```powershell
# In PowerShell profile ($PROFILE) or project .env:
$env:PYTHONUNBUFFERED = "1"         # Instant real-time terminal log flushing
$env:PYTHONDONTWRITEBYTECODE = "1"   # Prevents __pycache__ directory litter
$env:PYTHONUTF8 = "1"               # Forces strict UTF-8 mode (fixes Windows cp1252 bugs)
```

### 1.2 Editor Optimization (`.vscode/settings.json`)
Enforce consistent line endings, trailing-whitespace stripping, and basic type-safety:

```json
{
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.eol": "\n",
  "editor.formatOnSave": true,
  "python.analysis.typeCheckingMode": "basic",
  "editor.tabSize": 4
}
```

### 1.3 Repository Hygiene (`.gitignore`)
Block memory dumps, private encryption keys, and local SQLite locks from reaching GitHub:

```gitignore
__pycache__/
*.py[cod]
.env
*.pem
*.key
*.id_rsa
*.sqlite3
*.db
.redis/
node_modules/
dist/
target/
```

---

## ⚡ Part 2: Cloud Linux VPS Kernel Optimization (Oracle Cloud / Ubuntu)

Default Linux settings cap open files at 1,024 and retain closed TCP connections in `TIME_WAIT` for 60 seconds, which rapidly triggers `OSError: [Errno 24] Too many open files` during crawl operations or webhook bursts.

### 2.1 File Descriptor & Process Scaling (`/etc/security/limits.conf`)
Append to `/etc/security/limits.conf`:

```text
* soft nofile 1048576
* hard nofile 1048576
* soft nproc 65536
* hard nproc 65536
root soft nofile 1048576
root hard nofile 1048576
```

### 2.2 Kernel TCP Socket & Memory Buffer Tuning (`/etc/sysctl.conf`)
Execute the following to apply high-throughput network tuning:

```bash
sudo bash -c 'cat >> /etc/sysctl.conf << EOF
# 1. Immediate socket reuse for outgoing connection pools
net.ipv4.tcp_tw_reuse = 1

# 2. Expand kernel socket connection backlog
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535

# 3. Maximum TCP socket read/write memory buffers (up to 16MB for 10Gbps interfaces)
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# 4. System-wide file descriptor limit
fs.file-max = 2097152

# 5. Swap discipline: keep active memory in RAM, swap only under extreme pressure
vm.swappiness = 10
EOF'

# Apply live without rebooting:
sudo sysctl -p
```

---

## 🐳 Part 3: Production Docker & Self-Healing Daemons

### 3.1 Hardened, Minimalist Production `Dockerfile`
```dockerfile
FROM python:3.11-slim

# Force unbuffered streaming and prevent cache bloat
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Cache dependencies independently from source edits
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as an unprivileged service account (Security Compliance)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "-u", "main.py"]
```

### 3.2 Autonomous Self-Healing Service (`systemd`)
Create `/etc/systemd/system/tensix-pipeline.service`:

```ini
[Unit]
Description=TENSIX Autonomous High-Throughput Pipeline Daemon
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/pipeline
ExecStart=/usr/bin/python3 -u main.py
Restart=always
RestartSec=3
LimitNOFILE=65535
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start daemon:
sudo systemctl daemon-reload
sudo systemctl enable tensix-pipeline
sudo systemctl start tensix-pipeline
```

---

## 📋 The 5 Golden In-Code Rules During Implementation

1. **Deterministic Timeouts**: Never issue a network call without an explicit timeout (`timeout=5`).
2. **Object Pre-Allocation**: Keep buffers and data structures outside tight `while` loops to avoid constant heap allocations.
3. **Structured Sockets**: Utilize connection pooling (`httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=50))`).
4. **Unbuffered Streaming**: Always execute with `python -u` to ensure logs emit immediately to Docker/systemd journals.
5. **Idempotent Retries**: Any network write must be guarded by a unique SHA-256 hash or version lock before retrying.
