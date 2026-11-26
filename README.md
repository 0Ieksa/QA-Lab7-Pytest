# Лабораторна №7 — Python, subprocess, pytest, iperf

Виконання у Ubuntu/WSL2 на одному комп’ютері. Тут використано **iperf2** (команда `iperf`, порт 5507), тому парсер працює з текстовим виводом iperf2. У методичці наведено приклад віддаленого підключення SSH через Paramiko; для локальної мережі його замінено запуском iperf-сервера у фікстурі через subprocess.

## Встановлення

```bash
sudo apt update
sudo apt install -y iperf python3 python3-venv
cd ~/lab7_pytest
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
```

## Частина 1 — сервер вручну та Python-клієнт

Перший термінал: `iperf -s -p 5507`

Другий термінал:

```bash
cd ~/lab7_pytest
source .venv/bin/activate
python manual_client.py
```

Для демонстрації помилки за відсутності сервера виконай `python manual_client.py --port 5597`.

## Частина 2 — фікстури та автоматичний тест

Зупини **ручний** сервер перед наступними командами, бо pytest запускає власний.

```bash
cd ~/lab7_pytest
source .venv/bin/activate
python -m pytest -s -q test_iperf.py
MIN_BITRATE_MBITS=1000000 python -m pytest -s -q test_iperf.py
```

Перший тест — перевірка реальних порогів з методички; другий — навмисний негативний тест через завищений поріг, а не несправність утиліти iperf. Після негативної перевірки знову запусти позитивний тест.

Результати й скриншоти слід фіксувати за фактичним виводом своєї Ubuntu. Для повного виконання вимог методички результати потрібно також розмістити у своєму GitHub-репозиторії.
