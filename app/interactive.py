from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver

from app.config import root_log

log = root_log.getChild("interactive")


def login(br: WebDriver, username: str, password: str):
    # Login on the Webportal and go to the main page of the Homepagecenter
    log.info(f"Logging in to {username}")
    br.implicitly_wait(5)
    br.get(
        "https://accounts.login.idm.telekom.com/oauth2/auth?scope=openid&response_type=code&approval_prompt=auto&redirect_uri=https%3A%2F%2Fhomepagecenter.telekom.de%2Ftypo3conf%2Fext%2Fcidaas%2Fcallback.php&client_id=10LIVESAM30000004901HOSTING0000000000000"
    )
    log.debug(1)
    user = br.find_element(By.ID, "username")
    user.send_keys(username)
    log.debug(2)
    user_accept = br.find_element(By.ID, "pw_submit")
    user_accept.click()
    log.debug(3)
    pw = br.find_element(By.ID, "pw_pwd")
    pw.send_keys(password)
    log.debug(4)
    pw_accept = br.find_element(By.ID, "pw_submit")
    pw_accept.click()
    log.debug(5)
    br.get("https://homepagecenter.telekom.de/index.php")
    log.debug(6)


def logout(br: WebDriver):
    br.get("https://homepagecenter.telekom.de/startseite?logintype=logout")


def set_entry(
    br: WebDriver, domain: str, typ: str, prefix: str, ttl: str, content: str
):
    br.get("https://homepagecenter.telekom.de/domains/uebersicht")
    log.debug(7)
    buttons = br.find_elements(By.CLASS_NAME, "edit-domain")
    for button in buttons:
        if button.get_attribute("data-domnname") == domain:
            button.click()
            sleep(1)

    dropdown = br.find_element(By.CLASS_NAME, "dnsSelfcare")
    dropdown.click()

    new = br.find_element(By.NAME, "tx_hpcdomain_dnsselfcarelist[addrr]")
    new.click()

    sleep(1)

    select_typ = Select(br.find_element(By.NAME, "tx_hpcdomain_dnsselfcarelist[type]"))
    select_typ.select_by_value(typ)

    new = br.find_element(By.NAME, "tx_hpcdomain_dnsselfcarelist[prefix]")
    new.send_keys(prefix)

    new = br.find_element(By.NAME, "tx_hpcdomain_dnsselfcarelist[ttl]")
    new.clear()
    new.send_keys(ttl)

    new = br.find_element(By.NAME, "tx_hpcdomain_dnsselfcarelist[content]")
    new.send_keys(content)

    saves = br.find_elements(By.NAME, "tx_hpcdomain_dnsselfcarelist[addrr]")
    for save in saves:
        if save.accessible_name == "Übernehmen":
            save.click()
            sleep(1)

    commit = br.find_element(By.CLASS_NAME, "icon-confirm")
    commit.click()
    log.info(f"Created entry {prefix}.{domain} - {typ} - {content}")
    log.debug(8)


def delete_entry(br: WebDriver, domain: str, typ: str, prefix: str, content: str):
    br.get("https://homepagecenter.telekom.de/domains/uebersicht")
    log.debug(7)
    buttons = br.find_elements(By.CLASS_NAME, "edit-domain")
    for button in buttons:
        if button.get_attribute("data-domnname") == domain:
            button.click()
            sleep(1)
            break

    dropdown = br.find_element(By.CLASS_NAME, "dnsSelfcare")
    dropdown.click()

    entries = br.find_elements(By.XPATH, "//table/tbody/tr")

    for entry in entries:
        e_name = None
        e_content = None
        e_typ = None

        for td in entry.find_elements(By.CSS_SELECTOR, f"td>span"):
            if td.get_property("id").startswith("fld-dnsname-"):
                e_name = td.text
            elif td.get_property("id").startswith("fld-dnscontent-"):
                e_content = td.text
            elif td.get_property("id").startswith("fld-dnstype-"):
                e_typ = td.text
            else:
                pass

        if e_name == f"{prefix}.{domain}" and content == e_content and e_typ == typ:
            log.debug("Found it")
            edit = entry.find_element(By.CLASS_NAME, f"icon-delete")
            edit.click()
            sleep(1)
            delete = br.find_element(By.ID, "delrr-btnok")
            delete.click()
            sleep(1)
            commit = br.find_element(By.CLASS_NAME, "icon-confirm")
            commit.click()
            log.info(f"Deleted entry {prefix}.{domain} - {typ} - {content}")
            break

    log.debug(8)
