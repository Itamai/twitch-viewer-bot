import csv
import time
import sys

if __name__ == "__main__":
    from utils import test_proxy, validate_ip
else:
    from .utils import test_proxy, validate_ip

# export list from https://hidemy.name/en/proxy-list as csv
FILENAME = "hideme_proxy_export.csv"


def start_hideme_thread(callback):
    get_new = _init_proxies(FILENAME)
    while True:
        try:
            proxy = get_new()
            if proxy == None:
                raise "no proxy found"
        except Exception as e:
            print("hideme error", e)
            sys.exit(0)

        if test_proxy(proxy):
            callback(proxy)


def _init_proxies(filename):
    proxies = []

    with open(filename, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")

        for line, row in enumerate(csv_reader):
            if line == 0:
                continue

            proxies.append(row)

    print(f"loaded {len(proxies)} hideme proxies")
    counter = 0

    def get_new():
        nonlocal counter

        if counter >= len(proxies):
            return None

        row = proxies[counter]

        scheme = None
        if row["http"] == "1":
            scheme = "http"

        if row["ssl"] == "1":
            scheme = "https"

        if row["socks4"] == "1":
            scheme = "socks4"

        if row["socks5"] == "1":
            scheme = "socks5"

        proxy = f"{scheme}://{row['ip']}:{row['port']}"
        counter += 1
        return proxy

    return get_new


if __name__ == "__main__":
    # extract working proxies for test here
    get_new = _init_proxies(FILENAME)
    while True:
        try:
            proxy = get_new()
            if proxy == None:
                print("no more proxies left")
                break
        except Exception as e:
            print("hideme error", e)
            sys.exit(0)

        if test_proxy(proxy, 3):
            with open("working_hideme.txt", "a") as file:
                file.write(proxy + "\n")
