#!/usr/bin/env python3
"""Devuelve información de identificación del host GNU/Linux en JSON."""

import json
import platform
import subprocess
from pathlib import Path


def operating_system():
    path = Path("/etc/os-release")
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("PRETTY_NAME="):
                return line.split("=", 1)[1].strip().strip('"').replace(r'\"', '"')
    return platform.system()


def virtualization():
    try:
        result = subprocess.run(
            ["systemd-detect-virt"],
            capture_output=True,
            text=True,
            check=False,
            timeout=3,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else "none"


def main():
    data = {
        "host": platform.node(),
        "os": operating_system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "virtualization": virtualization(),
    }
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
