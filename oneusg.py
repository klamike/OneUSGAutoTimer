import sys, time, requests
from selenium import webdriver
from traceback import format_exc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import MINS_TO_CLOCK, USERNAME, PASSWORD, CHROMEDRIVER_PATH, IN_PING_URL, OUT_PING_URL, FAIL_PING_URL, LOGIN_URL
SECONDS_TO_CLOCK  = MINS_TO_CLOCK * 3600
EXCEPTIONS        = (NoSuchElementException, TimeoutException)

def fprint(o, **kwargs): print(o, flush=True, **kwargs)

def ping(url, text='', data=None):
    try:
        requests.get(url, timeout=10, data=data)
        fprint(f"{text} ping success")
    except requests.RequestException as e:
        fprint(f"{text} ping failed: %s" % e)

def WDWait(browser, time, by, label, method=None, keys=None):
    assert (method == 'send_keys' and keys is not None) or (method != 'send_keys')
    element = WebDriverWait(browser, time).until(EC.element_to_be_clickable((by, label)))
    if   method ==     'click': element.click()
    elif method == 'send_keys': element.send_keys(keys)
    elif method ==        None: return

def main(browser, out_only=False):
    ## LOGIN

    browser.get(LOGIN_URL)

    WDWait(browser, 25, By.XPATH, "//*[@id='https_idp_gatech_edu_idp_shibboleth']/div/div/a/img", 'click') # click gt image

    WDWait(browser, 25, By.NAME,  "username", 'send_keys', USERNAME)
    WDWait(browser, 25, By.NAME,  "password", 'send_keys', PASSWORD)
    WDWait(browser, 25, By.NAME,  "submit",   'click') # login

    ## DUO TWO FACTOR AUTH

    fprint("Waiting for Duo Auth...", end='')

    for _ in range(24):
        try:
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.ID, "duo_form")))
            time.sleep(5)
            fprint('.', end='')
            continue
        except EXCEPTIONS:
            fprint("Exiting Duo Loop")
            time.sleep(2)
            browser.refresh() # initial page is blank, need refresh
            break
    else:
        fprint("No Duo Auth for 2 mins, exiting.")
        ping(FAIL_PING_URL, text="Duo Failure", data="NO DUO AUTH")
        browser.quit()
        exit(1)

    ## CLOCK IN
    if not out_only:
        WDWait(browser, 25, By.ID, "TL_RPTD_SFF_WK_GROUPBOX$PIMG", 'send_keys', Keys.RETURN) # clock menu

        WDWait(browser, 25, By.ID, "TL_RPTD_SFF_WK_TL_ACT_PUNCH1", 'send_keys', Keys.RETURN) # clock in
        clock_in_time = time.time()

        try: # handle double clock
            WDWait(browser, 5, By.ID, "#ICOK", 'send_keys', Keys.RETURN)
            WDWait(browser, 5, By.ID, "PT_WORK_PT_BUTTON_BACK", 'send_keys', Keys.RETURN)
            fprint("You were about to double clock, we prevented that.")
        except EXCEPTIONS:
            pass

        WebDriverWait(browser, 25).until( # verify successful clock in
            lambda browser: "In" in browser.find_element_by_id("TL_WEB_CLOCK_WK_DESCR50_1").get_attribute('innerHTML')
        )

        ping(IN_PING_URL, text="Clock In")

        ## IDLE

        min_counter, elapsed_time = 0, 0
        while elapsed_time < SECONDS_TO_CLOCK:
            elapsed_time = time.time() - clock_in_time
            time.sleep(30)
            min_counter += 0.5

            if min_counter % 15 == 0:
                browser.refresh()
                fprint(f"{round(elapsed_time / 3600, 3)}hrs, {min_counter}mins")
                try:
                    WDWait(browser, 5, By.ID, "BOR_INSTALL_VW$0_row_0", "send_keys", Keys.RETURN)
                    fprint("Timeout Prevented")
                except EXCEPTIONS:
                    pass

    ## CLOCK OUT

    WDWait(browser, 25, By.ID, "TL_RPTD_SFF_WK_GROUPBOX$PIMG", 'send_keys', Keys.RETURN) # clock menu

    WDWait(browser, 25, By.ID, "TL_RPTD_SFF_WK_TL_ACT_PUNCH3", 'send_keys', Keys.RETURN) # clock out
    clock_out_time = time.time()

    WebDriverWait(browser, 25).until( # verify successful clock out
        lambda browser: "Out" in browser.find_element_by_id("TL_WEB_CLOCK_WK_DESCR50_1").get_attribute('innerHTML') # TODO: sometimes leads to StaleElementReferenceException
    )

    browser.quit()

    fprint("Clocked out.")
    total_clock_time = (clock_out_time - clock_in_time)/3600
    fprint(f"Logged {total_clock_time}hr")

    ping(OUT_PING_URL, text="Clock Out", data=str(total_clock_time))

if __name__ == "__main__":
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless"); chrome_options.add_argument("--log-level=3")
        browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

        try:
            main(browser)
        except KeyboardInterrupt:
            fprint("Interrupted. Make sure to clock out manually!")
            ping(FAIL_PING_URL, text="Failure", data='KeyboardInterrupt')
        finally:
            browser.quit()

    except Exception as e:
        traceback = format_exc()
        fprint(traceback)
        ping(FAIL_PING_URL, text="Failure", data=traceback)