"""Розбір секундних інтервалів текстового виводу iperf2."""
import re

ROW = re.compile(
    r'^\[\s*\d+\]\s*'
    r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s+sec\s+'
    r'(\d+(?:\.\d+)?)\s+([KMGT]?Bytes)\s+'
    r'(\d+(?:\.\d+)?)\s+([KMGT]?bits/sec)',
    re.IGNORECASE,
)


def parse_intervals(output):
    """Повертає [{Interval, Transfer, Bitrate}] у Мбайт і Мбіт/с.

    Підсумкові рядки 0–5 с пропускаються: перевіряємо саме ~1-секундні інтервали.
    """
    bytes_scale = {'': 1, 'k': 1024, 'm': 1024**2, 'g': 1024**3, 't': 1024**4}
    bits_scale = {'': 1, 'k': 1000, 'm': 1000**2, 'g': 1000**3, 't': 1000**4}
    result = []
    for line in output.splitlines():
        match = ROW.search(line.strip())
        if not match:
            continue
        start, end, transfer, transfer_unit, bitrate, bitrate_unit = match.groups()
        start, end = float(start), float(end)
        if not 0.8 <= end - start <= 1.2:
            continue
        transfer_mbytes = float(transfer) * bytes_scale[transfer_unit[:-5].lower()] / 1024**2
        bitrate_mbits = float(bitrate) * bits_scale[bitrate_unit[:-8].lower()] / 1000**2
        result.append({
            'Interval': f'{start:.2f}-{end:.2f}',
            'Transfer': round(transfer_mbytes, 3),
            'Bitrate': round(bitrate_mbits, 3),
        })
    return result