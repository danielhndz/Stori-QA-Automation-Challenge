from time import sleep
from os import path
from appium.webdriver import Remote
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

BROWSER_CHROME = 'chrome'
BROWSER_FIREFOX = 'firefox'
BROWSER_OPERA = 'opera'
current_browser = BROWSER_CHROME

FEATURES_PATH = path.abspath(
    path.join(path.dirname(__file__), '..', 'tests', 'features'))
SCREENSHOTS_PATH = path.abspath(
    path.join(path.dirname(__file__), '..', 'reports', current_browser, 'screenshots'))
RECORDINGS_PATH = path.abspath(
    path.join(path.dirname(__file__), '..', 'reports', current_browser, 'recordings'))
current_scenario = ''

MOBILE_SHELL = 'mobile: shell'
TIMEOUT = 10000
APPIUM_CLIENT_PARAMS = '-wipe-data -no-snapshot-save -gpu swiftshader_indirect -no-boot-anim'  # -wipe-data

CHROME_PACKAGE = 'com.android.chrome'
CHROME_ACTIVITY = 'com.google.android.apps.chrome.Main'
FIREFOX_PACKAGE = 'org.mozilla.firefox'
FIREFOX_ACTIVITY = '.App'
FIREFOX_APK_PATH = path.abspath(
    path.join(path.dirname(__file__), '..', 'apps', "firefox.apk"))
OPERA_PACKAGE = 'com.opera.browser'
# OPERA_ACTIVITY = 'com.opera.Opera'
OPERA_APK_PATH = path.abspath(
    path.join(path.dirname(__file__), '..', 'apps', 'opera.apk'))

SUT_URL = 'https://rahulshettyacademy.com/AutomationPractice/'
WEBVIEW_CLASS_XPATH = '//*[@class="android.webkit.WebView"]'

DIRECTION_UP = 'up'
DIRECTION_DOWN = 'down'
DIRECTION_LEFT = 'left'
DIRECTION_RIGHT = 'right'

avd_name = 'Pixel_2_API_33'


def switch_back_to_native_context(driver: Remote):
    driver.switch_to.context(driver.contexts[0])


def switch_to_webview_context(driver: Remote):
    close_alerts_if_exists(driver)
    driver.switch_to.context(driver.contexts[1])
    driver.switch_to.window(driver.window_handles[0])


def select_from_dropdown(driver: Remote, by_dropdown, locator_dropdown, by_selection, locator_selection):
    close_alerts_if_exists(driver)
    driver.find_element(by_dropdown, locator_dropdown).click()
    sleep(10)
    driver.find_element(by_selection, locator_selection).click()
    sleep(10)


def scroll_to_element(driver: Remote, direction, by, locator):
    while True:
        try:
            driver.find_element(by, locator)
            sleep(10)
            break
        except NoSuchElementException:
            scroll_screen(driver, direction)


def scroll_screen(driver: Remote, direction: str):
    direction = direction.lower()
    SIZE = driver.get_window_size()
    start_x, start_y, end_x, end_y = 0, 0, 0, 0
    if direction == DIRECTION_UP:
        start_x = int(SIZE['width'] / 2)
        start_y = int(SIZE['height'] * 0.2)
        end_x = int(SIZE['width'] / 2)
        end_y = int(SIZE['height'] * 0.8)
    elif direction == DIRECTION_DOWN:
        start_x = int(SIZE['width'] / 2)
        start_y = int(SIZE['height'] * 0.8)
        end_x = int(SIZE['width'] / 2)
        end_y = int(SIZE['height'] * 0.2)
    elif direction == DIRECTION_LEFT:
        start_x = int(SIZE['width'] * 0.2)
        start_y = int(SIZE['height'] / 2)
        end_x = int(SIZE['width'] * 0.8)
        end_y = int(SIZE['height'] / 2)
    elif direction == DIRECTION_RIGHT:
        start_x = int(SIZE['width'] * 0.8)
        start_y = int(SIZE['height'] / 2)
        end_x = int(SIZE['width'] * 0.2)
        end_y = int(SIZE['height'] / 2)
    driver.swipe(start_x, start_y, end_x, end_y)
    sleep(10)


def type_into_element(driver: Remote, entry: str, by, locator):
    close_alerts_if_exists(driver)
    while True:
        try:
            e = driver.find_element(by, locator)
            e.clear()
            e.send_keys(entry)
            break
        except StaleElementReferenceException:
            pass
    sleep(10)
    driver.hide_keyboard()
    sleep(10)


def no_thanks_click(driver: Remote):
    no_thanks_xpath = '//*[name()="android.widget.Button"][1]'
    click_on(driver, AppiumBy.XPATH, no_thanks_xpath)


def click_on(driver: Remote, by, locator):
    close_alerts_if_exists(driver)
    try:
        e = driver.find_element(by, locator)
        e.click()
    except StaleElementReferenceException:
        click_on(driver, by, locator)


def close_alerts_if_exists(driver: Remote):
    while True:
        try:
            sleep(10)
            driver.find_element(
                AppiumBy.XPATH, '//*[@text="Close app"]').click()
            sleep(90)
            if is_chrome():
                driver.activate_app(CHROME_PACKAGE)
            elif is_firefox():
                driver.activate_app(FIREFOX_PACKAGE)
            else:
                driver.activate_app(OPERA_PACKAGE)
        except StaleElementReferenceException:
            sleep(10)
        except NoSuchElementException:
            break


def get_caps():
    caps = dict(
        platformName='android',
        platformVersion='13.0',
        automationName='uiautomator2',
        deviceName='avd',
        uiautomator2ServerLaunchTimeout=TIMEOUT * 10,
        uiautomator2ServerInstallTimeout=TIMEOUT * 10,
        appPackage=get_package(),
        appActivity=get_activity(),
        appWaitDuration=TIMEOUT * 10,
        androidInstallTimeout=TIMEOUT * 50,
        autoGrantPermissions='true',
        uninstallOtherPackages='io.appium.setting',
        adbExecTimeout=TIMEOUT * 50,
        avd=avd_name,
        avdLaunchTimeout=TIMEOUT * 50,
        avdReadyTimeout=TIMEOUT * 50,
        avdArgs=APPIUM_CLIENT_PARAMS,
        autoAcceptAlerts='true',
        newCommandTimeout=TIMEOUT
    )
    if is_firefox():
        caps['app'] = FIREFOX_APK_PATH
    elif is_opera():
        caps.pop('appActivity')
        caps['app'] = OPERA_APK_PATH
    return caps


def get_activity():
    if is_firefox():
        return FIREFOX_ACTIVITY
    elif is_opera():
        return ""
    else:
        return CHROME_ACTIVITY


def get_package():
    if is_firefox():
        return FIREFOX_PACKAGE
    elif is_opera():
        return OPERA_PACKAGE
    else:
        return CHROME_PACKAGE


def is_opera():
    return current_browser == BROWSER_OPERA


def is_firefox():
    return current_browser == BROWSER_FIREFOX


def is_chrome():
    return current_browser == BROWSER_CHROME
