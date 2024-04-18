import logging
import tomllib

import click

config_exists = False

try:
    with open("app/config/config.toml", "rb") as f:
        config = tomllib.load(f)
        config_exists = True
except FileNotFoundError:
    print("No config found! Please setup your config.toml from the template!")
    if not click.confirm(
        "You can continue, but only change one record at a time!\n"
        "Do you want to continue?",
        default=True,
    ):
        exit(1)

if config_exists:
    DEBUG = config["general"]["show_debug"]
    USERNAME = config["login"]["username"]
    PASSWORD = config["login"]["password"]
    ENTRIES = config["entries"]
else:
    DEBUG = False
    USERNAME = input("Enter your Username:")
    PASSWORD = input("Enter your Password:")
    ENTRIES = []
    enter_entry = True
    while enter_entry:
        __domain__ = input("Enter your domain:")
        __typ__ = input("Enter your typ:")
        __prefix__ = input("Enter your prefix:")
        __ttl__ = input("Enter your TTL:")
        ENTRIES.append(
            {"domain": __domain__, "typ": __typ__, "prefix": __prefix__, "ttl": __ttl__}
        )
        enter_entry = click.confirm(
            "\nDo you want to enter another entry?", default=False
        )

logging.basicConfig()
root_log = logging.getLogger("app")
if DEBUG:
    root_log.setLevel(logging.DEBUG)
else:
    root_log.setLevel(logging.INFO)
root_log.debug("Config loaded")
root_log.info("Config loaded")
