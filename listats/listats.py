"""listat module
A simple script to read values from LiveInternet counters.
Usage:
  listats [--domains=<filename>]
Options:
  --domains=<filename>  A text file with the list of domains.
                        './domains.txt' will be used by default
"""
import os
import io
import sys
import argparse
import urllib.request
import random
import asyncio
import aiohttp

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
TOTAL_TIMEOUT = 60


async def fetch_image(session, url):
    async with session.get(url) as resp:
        return await resp.read()


async def fetch_images(domains):
    result = {}
    timeout = aiohttp.ClientTimeout(total=TOTAL_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for domain in domains:
            url = URL.format(domain, random.random())
            result[domain] = await fetch_image(session, url)
    return result


def read_digit(img, xcoord, ycoord):
    bgrnd = img.getpixel((3, 3))
    sio = io.StringIO()
    for col in COLS:
        xpos = xcoord + col
        for row in range(ROW_COUNT):
            ypos = ycoord + row
            sio.write(ONE if img.getpixel((xpos, ypos)) == bgrnd else ZERO)
    key = int(sio.getvalue(), 2)
    sio.close()
    return DIGITS.get(key)


def read_image(data):
    img = Image.open(io.BytesIO(data))
    numbers = []
    for ycoord in YCOORDS:
        space = 0
        digits = []
        for xcoord in XCOORDS:
            digit = read_digit(img, xcoord - space, ycoord)
            if digit is None:
                space += 2
                digit = read_digit(img, xcoord - space, ycoord)
                if digit is None:
                    break
            digits.append(str(digit))
        digits.reverse()
        numbers.append("".join(digits))
    return {"pageviews": dict(zip(NAMES, numbers[::2])),
            "visitors": dict(zip(NAMES, numbers[1::2]))}


def read_images(images_data):
    for domain, image_bytes in images_data.items():
        yield domain, read_image(image_bytes)


def get_domains(filename):
    with open(filename) as file_:
        for line in file_:
            yield line.strip()


def get_domain_stats(domain):
    data = download_image(domain)
    return read_image(data) if data else None


def show(data):
    splitter = 40 * "-"
    for domain, values in sorted(data):
        print("\033[1m{domain}\33[0m".format(domain=domain))
        if not values:
            continue
        print("{0:>20}{1:>14}".format("visitors", "pageviews"))
        for name in NAMES:
            print("{name:>10}: {visitors:<12} {pageviews:<12}".format(
                name=name, visitors=values["visitors"][name],
                pageviews=values["pageviews"][name]))
        print(splitter)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read values from LiveInternet counters.")
    parser.add_argument("--domains", dest="domains_file", type=str,
                        help="domains file path", default="domains.txt")
    return parser.parse_args()


def main():
    args = parse_args()
    domains = get_domains(args.domains_file)
    loop = asyncio.get_event_loop()
    images_data = loop.run_until_complete(fetch_images(domains))
    loop.close()
    show(read_images(images_data))


if __name__ == '__main__':
    main()
