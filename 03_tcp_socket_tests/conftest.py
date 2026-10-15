# conftest.py

import subprocess
import sys
import time
import os
import socket
import pytest


def is_port_open(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        sock.close()
        return False


@pytest.fixture(scope="session", autouse=True)
def start_signal_service():
    PORT = 2001
    HOST = "127.0.0.1"

    if is_port_open(HOST, PORT):
        print(f"\n[INFO] Порт {PORT} уже слушается — используем существующий сервис")
        yield None
        return

    script_path = os.path.join(os.path.dirname(__file__), "signal_service.py")
    print(f"\n[INFO] Запускаю сервис: {script_path}")

    process = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",      # ← фикс для Windows
        errors="replace",      # ← не падать на неизвестных символах
        cwd=os.path.dirname(script_path),
    )

    for attempt in range(20):
        time.sleep(0.5)

        if process.poll() is not None:
            output, _ = process.communicate()
            print(f"[ERROR] Сервис упал! Код: {process.returncode}")
            print(f"[ERROR] Вывод:\n{output}")
            pytest.fail(f"Сервис не запустился:\n{output}")

        if is_port_open(HOST, PORT):
            print(f"[OK] Сервис готов (PID: {process.pid})")
            break
    else:
        process.terminate()
        pytest.fail(
            f"[ERROR] Сервис не запустился за 10 секунд.\n"
            f"Проверь вручную: python {script_path}"
        )

    yield process

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    print("\n[STOP] Сервис остановлен")