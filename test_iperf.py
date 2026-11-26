"""Автоматична перевірка порогів Transfer та Bitrate із методички."""
import os
from parser import parse_intervals


def test_iperf_transfer_and_bitrate(client):
    assert client.returncode == 0, f'Помилка iperf: {client.stderr.strip()}'
    values = parse_intervals(client.stdout)
    assert values, 'Не вдалося прочитати секундні інтервали iperf'

    minimum_transfer = float(os.getenv('MIN_TRANSFER_MBYTES', '2'))
    minimum_bitrate = float(os.getenv('MIN_BITRATE_MBITS', '20'))
    print(f'Перевіряю {len(values)} інтервалів: Transfer > {minimum_transfer} Мбайт, '
          f'Bitrate > {minimum_bitrate} Мбіт/с')
    for row in values:
        print(row)
        assert row['Transfer'] > minimum_transfer, f'Замало даних: {row}'
        assert row['Bitrate'] > minimum_bitrate, f'Замала швидкість: {row}'