from time import sleep
from os import path
from utils import utils
from appium.webdriver import Remote
from appium.webdriver.common.appiumby import AppiumBy
from pytest_bdd import scenarios, parsers, given, when, then


SUGGESSION_INPUT_XPATH = f'{utils.WEBVIEW_CLASS_XPATH}//*[@class="android.widget.EditText"]'
DROPDOWN_XPATH = '//*[@class="android.view.View" and @index=2]' + \
    '//*[@class="android.view.View" and @index=1 and not(child::*)]'
HAMBURGER_SELECTOR = '.navbar-toggler'
ALERT_INPUT_SELECTOR = '#name'
ALERT_BUTTON_XPATH = '//*[@id="alertbtn"]'
ALERT_MSG_XPATH = '//*[@class="android.widget.TextView" and @index="1"]'
COURSES_SELECTOR = 'table[name] tbody > tr'


scenarios(path.join(utils.FEATURES_PATH, 'automation_practice.feature'))


@then(parsers.parse('the user can see in the iFrame this text:\n{text}'))
def _(driver: Remote, text):
    utils.switch_to_webview_context(driver)
    driver.switch_to.frame(driver.find_element(
        AppiumBy.XPATH, '//*[@id="courses-iframe"]'))
    current_text = driver.find_element(
        AppiumBy.XPATH, '(//*[@class="price-title"]//li[2])[2]').text
    inline_text = text.replace('\n', '')
    assert text == current_text or inline_text == current_text


@then(parsers.parse('the user can see the names of the people with the {position:w} position'))
def _(driver: Remote, position):
    utils.switch_to_webview_context(driver)
    xpath = f'//*[@class="tableFixHead"]//td[text()="{position}"]/parent::*/td[1]'
    names = driver.find_elements(AppiumBy.XPATH, xpath)
    if len(names) > 0:
        print(
            f'\n\t Here is the list of the names with people with the {position} position')
        for n in names:
            print(f'\t name = {n.text}')
    else:
        print(f'\n\t There is no person with the {position} position')


@then('the user can see its names')
def _(courses: dict):
    if len(courses['names']) > 0:
        print('\n\t Here is the list of the names')
        for n in courses['names']:
            print(f'\t name = {n}')
    else:
        print(f'\n\t There is no course that costs ${courses["price"]}')


@when(parsers.parse('the user sees how many courses cost ${price:d}'), target_fixture='courses')
def courses(driver: Remote, price):
    utils.switch_to_webview_context(driver)
    elements = driver.find_elements(
        AppiumBy.CSS_SELECTOR, COURSES_SELECTOR)
    names = []
    for tr in elements:
        try:
            p = tr.find_element(AppiumBy.CSS_SELECTOR, 'td:nth-child(3)').text
            if p == str(price):
                names.append(tr.find_element(
                    AppiumBy.CSS_SELECTOR, 'td:nth-child(2)').text)
        except utils.NoSuchElementException:
            pass
    print(f'\n\n\t {len(names)} courses cost ${price}')
    return {'price': price, 'names': names}


@then(parsers.parse('the user can see an alert with this message {msg}'))
def _(driver: Remote, msg):
    current_msg = driver.find_element(AppiumBy.XPATH, ALERT_MSG_XPATH).text
    assert current_msg == msg


@when(parsers.parse('the user types {entry} in the {element:w}'))
def _(driver: Remote, entry, element):
    if element == 'alert_box':
        utils.switch_to_webview_context(driver)
        utils.type_into_element(
            driver, entry, AppiumBy.CSS_SELECTOR, ALERT_INPUT_SELECTOR)
        utils.switch_back_to_native_context(driver)


@then('the user switches to the previous tab')
def _(driver: Remote):
    driver.switch_to.window(driver.window_handles[1])
    sleep(10)


@then('the user takes a screenshot')
def _(driver: Remote):
    sleep(10)
    driver.save_screenshot(path.join(utils.SCREENSHOTS_PATH, 'switch_tab.png'))


@when('the user clicks on the hamburger icon')
def _(driver: Remote):
    sleep(10)
    utils.switch_to_webview_context(driver)
    utils.click_on(driver, AppiumBy.CSS_SELECTOR, HAMBURGER_SELECTOR)


@then(parsers.parse('the user can see a message titled {title} with the following body:\n{body}'))
def _(driver: Remote, title: str, body: str):
    sleep(20)
    title = title.replace('"', '')
    inline_body = body.replace('\n', '')
    assert title in driver.page_source \
        and (body in driver.page_source
             or inline_body in driver.page_source)


@then(parsers.parse('the user clicks on the {text_button} button'))
@when(parsers.parse('the user clicks on the {text_button} button'))
def _(driver: Remote, text_button: str):
    if not text_button.startswith('"'):
        text_button = '"' + text_button
    if not text_button.endswith('"'):
        text_button = text_button + '"'
    utils.click_on(driver, AppiumBy.XPATH,
                   f'//*[@text={text_button}]')
    sleep(20)


@when(parsers.parse('the user selects the option {option:w} from the {element:w}'))
def _(driver: Remote, option: str, element):
    option = option.replace('Option', '')
    SELECTION_XPATH = '//*[@class="android.widget.CheckedTextView"' + \
        f' and @index="{option}"]'
    if element == 'dropdown':
        utils.select_from_dropdown(
            driver, AppiumBy.XPATH, DROPDOWN_XPATH, AppiumBy.XPATH, SELECTION_XPATH)


@when(parsers.parse('the user scrolls at the {direction:l} to the {element:w}'))
def _(driver: Remote, direction, element):
    if element == 'dropdown':
        utils.scroll_to_element(
            driver, direction, AppiumBy.XPATH, DROPDOWN_XPATH)


@then(parsers.parse('the user can see {option} in the {element:w}'))
def _(driver: Remote, option, element):
    current_value = ''
    if element == 'suggession_box':
        current_value = driver.find_element(
            AppiumBy.XPATH, SUGGESSION_INPUT_XPATH).text
    elif element == 'dropdown':
        current_value = driver.find_element(
            AppiumBy.XPATH, DROPDOWN_XPATH).text
    assert current_value == option


@when(parsers.parse('the user types {entry:w} and selects {option}'))
def _(driver: Remote, entry, option):
    utils.type_into_element(
        driver, entry, AppiumBy.XPATH, SUGGESSION_INPUT_XPATH)
    sleep(10)
    suggession_xpath = f'{utils.WEBVIEW_CLASS_XPATH}//*[@text="{option}"]'
    utils.click_on(driver, AppiumBy.XPATH, suggession_xpath)
    sleep(10)


@given('the user is on the automation practice page')
def _(driver: Remote):
    driver.get(utils.SUT_URL)
    sleep(120)
