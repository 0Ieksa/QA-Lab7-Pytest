"""Частина 1: запуск iperf-клієнта через subprocess, розбір відповіді."""
import argparse
import subprocess
import sys
from parser import parse_intervals


def client(host='127.0.0.1', port=5507):
    try:
        result = subprocess.run(
            ['iperf', '-c', host, '-p', str(port), '-t', '5', '-i', '1'],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return '', str(error), 1
    return result.stdout, result.stderr, result.returncode


def main():
    argument = argparse.ArgumentParser()
    argument.add_argument('--host', default='127.0.0.1')
    argument.add_argument('--port', type=int, default=5507)
    args = argument.parse_args()
    output, error, code = client(args.host, args.port)
    if code != 0:
        print('Помилка підключення:', error.strip() or output.strip() or f'код {code}')
        return 1
    rows = parse_intervals(output)
    if not rows:
    	print("Помилка: iperf не повернув секундних інтервалів")
    	if error.strip():
        	print("stderr:", error.strip())
    	if output.strip():
        	print("stdout:", output.strip())
    	return 1
    print('Інтервали, де Transfer > 2 Мбайт і Bitrate > 20 Мбіт/с:')
    for row in rows:
        if row['Transfer'] > 2 and row['Bitrate'] > 20:
            print(row)
    print(f'Усього інтервалів: {len(rows)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
