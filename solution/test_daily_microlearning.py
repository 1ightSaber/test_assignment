    # Scenario:
def test_user_opens_the_app(setup_server, driver, by, pass_welcome_wizard, wait_home):
    #    Given: the Headway application is installed on an Android Device
    #      And: the user is not logged in
    wait_home()
    logo = driver.find_element(by['path'], '//android.widget.ImageView[@content-desc="Hi, you!"]')
    #     When: the user checks for the Headway logo
    #     Then: the Headway logo should be shown on the screen
    assert logo.is_displayed()


    # Scenario:
def test_user_checks_the_microlearning_session_view(driver, by, locators, swipe_down, wait_home, wait_header):
    # Given: the Headway application is opened on an Android Device
    #   And: the user has skipped the welcome wizard
    #   And: the user is on the main screen

    #  When: the user scrolls down
    swipe_down()
    #  Then: the “Microlearning session” header
    #   And: the “Tap through 10 bits of knowledge in 3 min” sub-header should be visible on the screen
    wait_header()
    header = driver.find_element(by['path'], locators['header'])
    sub_header = driver.find_element(by['path'], locators['sub_header'])
    assert header.is_displayed() and sub_header.is_displayed()


    # Scenario:
def test_user_reads_insights(driver, by, wait_micro, wait_home, locators):
    # Given: the Headway application is opened on an Android Device
    #   And: the user has skipped the welcome wizard
    #   And: the user is on the main screen
    #   And: the main screen is scrolled down to the microlearning session section
    #  When: the user taps on the first insight tile of the microlearning session
    first_insight_tile = driver.find_element(by['path'], locators['first_summary'])
    first_insight_tile.click()
    wait_micro()
    #  Then: the microlearning session screen should be open
    microlearning_screen = driver.find_element(by['path'], locators['microlearning'])
    first_insight = driver.find_element(by['path'], locators['insight']).text
    assert microlearning_screen.is_displayed()

    #  When: the user taps on the close button
    back_btn = driver.find_element(by['id'], locators["back_button"])
    back_btn.click()
    #  Then: the home screen should be opened
    wait_home()
    home_screen = driver.find_element(by['path'], '//android.widget.ImageView[@content-desc="Hi, you!"]')
    assert home_screen.is_displayed()

    driver.implicitly_wait(10) # there is no valid locator to wait for it's availability
    #  When: the user on the last insight of the updated microlearning list
    last_insight_tile = driver.find_element(by['path'], locators['last_insight'])
    last_insight_tile.click()
    #  Then: the microlearning screen opens on the same insight
    wait_micro()
    microlearning_screen = driver.find_element(by['path'], locators['microlearning'])
    current_insight = driver.find_element(by['path'], locators['insight']).text
    assert microlearning_screen.is_displayed()
    assert first_insight == current_insight

    #  When: the user taps on the next button of the microlearning screen
    next_btn = driver.find_element(by['path'], locators['next_button'])
    next_btn.click()
    #  Then: the first unread insight should open
    current_insight = driver.find_element(by['path'], locators['insight']).text
    assert first_insight != current_insight

    #  When: the user taps on the next button for 9 times
    #  Then: the first opened insight should be displayed
    for _ in range(9):
        driver.implicitly_wait(2)
        next_btn = driver.find_element(by['path'], locators['next_button'])
        next_btn.click()
    driver.implicitly_wait(2)
    current_insight = driver.find_element(by['path'], locators['insight']).text
    assert current_insight == first_insight


    # Scenario:
def test_the_user_taps_share_button(driver, by, locators, size):
    # Given: the headway application is opened on an Android Device
    #   And: the user is not logged in
    #   And: the user is on the microlearning session screen
    #  When: the user taps on the share button
    share_btn = driver.find_element(by['id'], 'com.headway.books:id/btn_share')
    share_btn.click()
    #  Then: the native android's share screen is opened
    driver.implicitly_wait(5)
    android = driver.find_element(by['id'], 'android:id/contentPanel')
    assert android.is_displayed()

    #  When: the user taps on the screen ouside of the share menu
    driver.tap([(size['width'] // 2, size['height'] // 4)])
    # Then: the microlearning session screen should open
    microlearning_screen = driver.find_element(by['path'], locators['microlearning'])
    assert microlearning_screen.is_displayed()


    # Scenario:
def test_taps_on_the_summary_button(driver, by, size, locators):
    # Given: the headway application is opened on an Android Device
    #   And: the user is not logged in
    #   And: the user is on the microlearning session screen
    title = driver.find_element(by['path'], '//android.widget.TextView[@resource-id="com.headway.books:id/tv_book"]').text
    author = driver.find_element(by['path'], '//android.widget.TextView[@resource-id="com.headway.books:id/tv_author"]').text

    #  When: the user taps on the summary button
    summary_btn = driver.find_element(by['path'], '//android.widget.ImageView[@resource-id="com.headway.books:id/img_cover"]')
    summary_btn.click()
    #  Then: the summary preview screen should open
    driver.implicitly_wait(3)
    summary_title = driver.find_element(by['id'], 'com.headway.books:id/tv_title').text
    summary_author = driver.find_element(by['id'], 'com.headway.books:id/tv_author').text
    summary_screen = driver.find_element(by['id'], 'com.headway.books:id/wrapper_start_book_buttons_eng')
    assert summary_screen.is_displayed()
    assert summary_title == title and summary_author == author

    # When: the user closes the share screen
    back_btn = driver.find_element(by['id'],'com.headway.books:id/btn_close')
    back_btn.click()

    # Then: the microlearning screen is opened
    microlearning_screen = driver.find_element(by['path'], locators['microlearning'])
    assert microlearning_screen.is_displayed()


    # Scenario:
def test_user_saves_the_insight_for_repetition(driver, by, locators):
    # Given: the headway application is opened on an Android Device
    #   And: the user is not logged in
    #   And: the user is on the microlearning session screen"
    #  When: the user taps on repetition button
    insight = driver.find_element(by['path'], locators['insight']).text
    repetition_btn = driver.find_element(by['path'], '//android.widget.Button[@resource-id="com.headway.books:id/btn_repetition_add"]')
    repetition_btn.click()
    #  Then: the repetition button’s state is changed to “repetition remove”
    repetition_remove = driver.find_element(by['path'], '//android.widget.Button[@resource-id="com.headway.books:id/btn_repetition_remove"]')
    assert repetition_remove.is_displayed()

    #  When: the user navigates to the repetition tab of the library menu
    back_btn = driver.find_element(by['id'], locators['back_button'])
    back_btn.click()
    library_button = driver.find_element(by['path'], locators['library'])
    library_button.click()
    repetition_tab = driver.find_element(by['path'], '//android.widget.LinearLayout[@content-desc="Repetition 1"]')
    repetition_tab.click()
    #  Then: the repetition card is present in the menu
    repetition_card = driver.find_element(by['path'], locators['card'])
    assert repetition_card.is_displayed()

    #  When: the user taps on repetition card
    repetition_card.click()
    #  Then: the saved insight should show up on the card
    insight_card = driver.find_element(by['path'], '//android.widget.TextView[@resource-id="com.headway.books:id/tv_text_only"]').text
    assert insight == insight_card
