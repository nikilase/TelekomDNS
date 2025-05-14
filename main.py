import argparse
import sys

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from app.config import root_log
from app.letsencrypt import letsencrypt_telekom

log = root_log.getChild("letsencrypt")


def main():
    parser = argparse.ArgumentParser(
        description="Run tool for adding Letsencrypt entries to Telekom Homepagecenter DNS using Selenium."
    )
    parser.add_argument(
        "-e",
        "--edge",
        action="store_true",
        help="Run using Edge Browser",
    )
    parser.add_argument(
        "-c",
        "--chrome",
        action="store_true",
        help="Run using Chrome Browser",
    )
    parser.add_argument(
        "-f",
        "--firefox",
        action="store_true",
        help="Run using Firefox Browser (not tested)",
    )
    parser.add_argument(
        "-nh",
        "--no-headless",
        action="store_true",
        help="Run without headless browser (optional, still need to select a browser)",
    )

    args = parser.parse_args()

    print("―" * 20)
    no_browser = True

    if args.no_headless:
        headless = False
    else:
        headless = True

    if args.edge:
        no_browser = False
        run_edge(headless)

    if args.chrome:
        no_browser = False
        run_chrome(headless)

    if args.firefox:
        no_browser = False
        run_firefox(headless)

    if no_browser:
        browser = input(
            "No Browser selected, for more info run 'main.py -h'!\n"
            "Please select a browser.\n"
            "c - Chrome Browser\n"
            "e - Edge Browser\n"
            "f - Firefox Browser\n"
        )
        match browser:
            case "c":
                run_chrome()
            case "e":
                run_edge()
            case "f":
                run_firefox()
            case _:
                print("No Browser selected, exiting program!")
                sys.exit(1)

        print("―" * 20)

    sys.exit(0)


def run_edge(headless=True):
    options = EdgeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--edge-skip-compat-layer-relaunch")
    br = webdriver.Edge(options=options)
    letsencrypt_telekom(br)


def run_chrome(headless=True):
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument("--headless=new")
    br = webdriver.Chrome(options=options)
    letsencrypt_telekom(br)


def run_firefox(headless=True):
    options = FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    br = webdriver.Firefox(options=options)
    letsencrypt_telekom(br)


if __name__ == "__main__":
    main()
