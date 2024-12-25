from time import sleep

import click
from selenium.webdriver.remote.webdriver import WebDriver

from app.api import login, set_entry, delete_entry, logout
from app.config import USERNAME, PASSWORD, ENTRIES, root_log
from app.tools import check_dns_txt_entry

log = root_log.getChild("letsencrypt")


def letsencrypt_telekom(br: WebDriver):
    login(br, USERNAME, PASSWORD)
    log.info("Logged in")
    sleep(0.05)
    # ToDo: maybe have selection of all domains and let the user select them so that the order of them in the config is
    #  not as important.

    del_entries = []

    for entry in ENTRIES:
        domain = entry["domain"]
        typ = entry["typ"]
        prefix = entry["prefix"]
        ttl = entry["ttl"]
        content = input(f"Please enter your content for {typ} on {prefix}.{domain}:")
        try:
            set_entry(br, domain, typ, prefix, ttl, content)
        except Exception as e:
            print(f"Error while adding entry: {e}")
        while not check_dns_txt_entry(f"{prefix}.{domain}", content):
            sleep(1)
        sleep(0.05)
        del_entries.append([domain, typ, prefix, content])

    ready = False
    while not ready:
        ready = click.confirm(
            "Created the Records, please continue in letsencrypt and come back when Letsencrypt has finished.\n"
            "Has Letsencrypt finished and do you want to continue with the deletion of the records?",
            default=False,
        )

    for entry in del_entries:
        domain, typ, prefix, content = entry
        delete_entry(br, domain, typ, prefix, content)
    logout(br)
    log.info("Logged out")
