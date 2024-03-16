import pytest, time, json, os

import selenium.common.exceptions

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService

DEVICE_NAME = '' # Insert your device name


@pytest.fixture(scope='session')
def setup_server():
    appium_service = AppiumService()
    appium_service.start()

    yield appium_service

    appium_service.stop()


@pytest.fixture(scope='session')
def driver():
    appium_server_url = 'http://127.0.0.1:4723'
    desired_caps = dict(
        platformName='Android',
        udid=f'{DEVICE_NAME}',
        automationName='UiAutomator2',
        appPackage="com.headway.books",
        appActivity="app.Launcher"
    )
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(desired_caps))
    yield driver

    driver.quit()


@pytest.fixture(scope='module')
def by():
    return {'path': AppiumBy.XPATH, 'id': AppiumBy.ID}


@pytest.fixture(scope='module')
def pass_welcome_wizard(driver):

    buttons = ("com.headway.books:id/btn_next",
               "com.headway.books:id/btn_continue",
               "com.headway.books:id/btn_cta",
               "com.headway.books:id/btn_yes",
               "com.android.permissioncontroller:id/permission_allow_button")

    while True:
        for button in buttons:
            try:
                to_click = driver.find_element(AppiumBy.ID, button)
                to_click.click()
            except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.WebDriverException):
                continue
        try:
            logo = driver.find_element(AppiumBy.ID, "com.headway.books:id/iv_toolbar_home_headline_logo")
            if logo.is_displayed():
                break
        except selenium.common.exceptions.NoSuchElementException:
            continue


@pytest.fixture(scope='module')
def locators():
    locators = {
        "header": '//android.widget.TextView[@resource-id="com.headway.books:id/tv_section_title_title" and @text="Daily microlearning session"]',
        "sub_header": '//android.widget.TextView[@resource-id="com.headway.books:id/tv_section_title_subtitle" and @text="Tap through 10 bits of knowledge in 3 min"]',
        "first_summary": '(//android.widget.ImageView[@resource-id="com.headway.books:id/iv_item_insight_book_cover"])[1]',
        "microlearning": '//android.widget.LinearLayout[@resource-id="com.headway.books:id/wrapper_insight"]',
        "insight":'//android.widget.TextView[@resource-id="com.headway.books:id/tv_content"]',
        "last_insight": '(//android.widget.ImageView[@resource-id="com.headway.books:id/iv_item_insight_book_cover"])[5]',
        "next_button": '//android.view.View[@resource-id="com.headway.books:id/btn_next"]',
        "back_button": 'com.headway.books:id/btn_back',
        "card": '//android.widget.GridView[@resource-id="com.headway.books:id/rv_to_repeat"]/android.widget.LinearLayout[2]/android.widget.FrameLayout/androidx.cardview.widget.CardView[2]',
        "library": '//android.widget.TextView[@resource-id="com.headway.books:id/tv_layout_bottom_navigation_view_library"]'
    }
    return locators


@pytest.fixture
def wait_home(driver, by):
    def _wait():
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                element = driver.find_element(by['path'],
                                              '//android.widget.TextView[@resource-id="com.headway.books:id/tv_section_title_title" and @text="Today for you"]')
                if element:
                    break
            except selenium.common.NoSuchElementException:
                pass
            time.sleep(1)
    return _wait


@pytest.fixture
def wait_micro(driver, by):
    def _wait():
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                element = driver.find_element(by['path'],
                                              '//android.widget.LinearLayout[@resource-id="com.headway.books:id/wrapper_insight"]')
                if element:
                    break
            except selenium.common.NoSuchElementException:
                pass
            time.sleep(1)
    return _wait



@pytest.fixture
def wait_header(driver, by):
    def _wait():
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                element = driver.find_element(by['path'],
                                              '//android.widget.TextView[@resource-id="com.headway.books:id/tv_section_title_title" and @text="Daily microlearning session"]')
                if element:
                    break
            except selenium.common.NoSuchElementException:
                pass
            time.sleep(1)
    return _wait


@pytest.fixture
def wait_content(driver, by):
    def _wait():
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                element = driver.find_element(by['path'], '//android.widget.TextView[@resource-id="com.headway.books:id/tv_content"]')
                if element:
                    break
            except selenium.common.NoSuchElementException:
                pass
            time.sleep(1)
    return _wait


@pytest.fixture(scope='module')
def size(driver):
    size = driver.get_window_size()
    return size


@pytest.fixture
def swipe_down(driver, size):
    def _swp_d():
        driver.swipe(start_x=size['width'] // 2, start_y=size['height'] * 0.5,
                     end_x=size['width'] // 2, end_y=size['height'] // 4)
    return _swp_d
