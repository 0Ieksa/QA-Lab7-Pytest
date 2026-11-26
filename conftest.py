"""Частина 2: фікстури pytest для локального iperf2-сервера та клієнта."""
import socket
import subprocess
import time
import pytest

PORT = 5507


@pytest.fixture(scope='function')
def server():
    # Весь тест виконується у локальній Ubuntu: SSH/Paramiko тут не потрібний.
    process = subprocess.Popen(
        ['iperf', '-s', '-p', str(PORT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(30):
            if process.poll() is not None:
                pytest.fail('Не вдалося запустити iperf-сервер')
            try:
                with socket.create_connection(('127.0.0.1', PORT), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.1)
        else:
            pytest.fail('iperf-сервер не відкрив порт 5507')
        yield PORT
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)


@pytest.fixture(scope='function')
def client(server):
    return subprocess.run(
        ['iperf', '-c', '127.0.0.1', '-p', str(server), '-i', '1', '-t', '5'],
        capture_output=True, text=True, timeout=15, check=False,
    )
