from os import path
from base64 import b64decode
from time import sleep
from pytest import fixture, hookimpl
from appium.webdriver.appium_service import AppiumService
from appium.webdriver import Remote
from appium.options.android import UiAutomator2Options as Options
from selenium.common.exceptions import NoSuchElementException
from utils import utils


APPIUM_SERVER_HOST = 'localhost'
APPIUM_SERVER_PORT = '4723'
APPIUM_SERVER_URL = f'http://{APPIUM_SERVER_HOST}:{APPIUM_SERVER_PORT}'
APPIUM_SERVER_PARAMS = ['--relaxed-security']


CHROME_PARAMS = '--disable-fre --no-default-browser-check --no-first-run'
CHROME_PARAMS_PATH = '/data/local/tmp/chrome-command-line'


def stop_recording(driver: Remote):
    payload = driver.execute_script('mobile: stopMediaProjectionRecording')
    p = path.join(utils.RECORDINGS_PATH,
                  utils.current_browser, utils.current_scenario)
    with open(p, 'wb') as rec:
        rec.write(b64decode(payload))


def start_recording(driver: Remote):
    driver.execute_script('mobile: startMediaProjectionRecording', {
        'filename': utils.current_scenario
    })


def skip_chrome_welcome_screen(driver: Remote):
    driver.execute_script(utils.MOBILE_SHELL, {
        'command': 'am',
        'args': ['force-stop', utils.CHROME_PACKAGE],
        'includeStderr': True
    })
    driver.execute_script(utils.MOBILE_SHELL, {
        'command': 'pm',
        'args': ['clear', utils.CHROME_PACKAGE],
        'includeStderr': True
    })
    driver.execute_script(utils.MOBILE_SHELL, {
        'command': 'am',
        'args': ['set-debug-app', '--persistent', utils.CHROME_PACKAGE],
        'includeStderr': True
    })
    driver.execute_script(utils.MOBILE_SHELL, {
        'command': 'echo',
        'args': f'"chrome {CHROME_PARAMS}" > {CHROME_PARAMS_PATH}',
        'includeStderr': True
    })
    driver.execute_script(utils.MOBILE_SHELL, {
        'command': 'am',
        'args': ['start', '-n', f'{utils.CHROME_PACKAGE}/{utils.CHROME_ACTIVITY}'],
        'includeStderr': True
    })
    sleep(10)
    while True:
        try:
            utils.no_thanks_click(driver)
            break
        except NoSuchElementException:
            pass
    sleep(2)


@hookimpl
def pytest_bdd_before_scenario(scenario):
    utils.current_scenario = scenario.name.replace(' ', '_') + '.mp4'


@fixture
def driver(appium_service):
    appium_service.start(args=APPIUM_SERVER_PARAMS)
    driver = Remote(APPIUM_SERVER_URL,
                    options=Options().load_capabilities(utils.get_caps()))
    utils.close_alerts_if_exists(driver)
    if utils.is_chrome():
        skip_chrome_welcome_screen(driver)
    yield driver
    driver.quit()


@fixture(scope='session')
def appium_service():
    service = AppiumService()
    yield service
    service.stop()
