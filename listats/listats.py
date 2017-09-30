"""listat module
A simple script to read values from LiveInternet counters.
Usage:
  listats [--domains=<filename>]
Options:
  --domains=<filename>  A text file with the list of domains.
                        './domains.txt' will be used by default
"""
import io
import os
import sys
import argparse
import urllib.request

from pprint import pprint
from random import random
from PIL import Image


DIGITS = {
    448:   "0",
    31774: "1",
    8514:  "2",
    14656: "3",
    3936:  "4",
    2376:  "5",
    328:   "6",
    15840: "7",
    320:   "8",
    2368:  "9"
}
COLS = (0, 2, 3)
ROW_COUNT = 5
URL = "http://counter.yadro.ru/hit?t28.1;r;s1600*900*24;uhttp%3A//{}/;{}"
XCOORDS = (78, 73, 68, 61, 56, 51, 44, 39, 34, 29, 24)
YCOORDS = (27, 34, 46, 53, 65, 72, 84, 91, 103, 110)
NAMES = ("month", "week", "24-hours", "today", "online")
ONE = "1"
ZERO = "0"


def _get_url(domain):
    """Return formatted counter URL"""
    return URL.format(domain, random())


def _get_image_data(domain):
    """Load data and return bytes"""
    url = _get_url(domain)
    return io.BytesIO(urllib.request.urlopen(url).read())


def _read_digit(img, xcoord, ycoord) -> tuple:
    """Read a single digit at the given coords"""
    bgrnd = img.getpixel((3, 3))
    sio = io.StringIO()
    for col in COLS:
        xpos = xcoord + col
        for row in range(ROW_COUNT):
            ypos = ycoord + row
            sio.write(ONE if img.getpixel((xpos, ypos)) == bgrnd
                      else ZERO)
    key = int(sio.getvalue(), 2)
    sio.close()
    return key in DIGITS, DIGITS.get(key, None)


def _get_domain_stats(domain) -> dict:
    """Read digits from the counter image"""
    data = _get_image_data(domain)
    img = Image.open(data)
    numbers = []
    for ycoord in YCOORDS:
        space = 0
        digits = []
        for xcoord in XCOORDS:
            result, digit = _read_digit(img, xcoord - space, ycoord)
            if result is False:
                space += 2
                result, digit = _read_digit(img, xcoord - space, ycoord)
                if result is False:
                    break
            digits.append(str(digit))
        digits.reverse()
        numbers.append("".join(digits))
    return {"visitors": dict(zip(NAMES, numbers[::2])),
            "pageviews": dict(zip(NAMES, numbers[1::2]))}


def get_stats(domains) -> dict:
    """Return a dict object with users and hits info"""
    stats = {}
    for domain in domains:
        stats[domain] = _get_domain_stats(domain)
    return stats


def get_domains(filename):
    """Load domains list from the file"""
    if not os.path.exists(filename):
        print("File not found: %s" % os.path.realpath(filename))
        sys.exit(1)
    with open(filename) as file_:
        for line in file_:
            yield line.strip()


def main():
    """Get data and print it"""
    parser = argparse.ArgumentParser(
        description="Read values from LiveInternet counters.")
    parser.add_argument("--domains", metavar="domains", type=str,
                        help="domains file path")
    args = parser.parse_args()
    filename = args.domains if args.domains else "domains.txt"
    pprint(get_stats(get_domains(filename)))


if __name__ == '__main__':
    main()
