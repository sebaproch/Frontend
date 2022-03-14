from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class MainPage:
    POPUP = (By.ID, 'popup-text')
    POPUP_ACCEPT_BUTTON = (By.XPATH, '//button[contains(@class, "agree-button")]')

    BREADCRUMB = (By.XPATH, '//ul[@class="breadcrumbs"]/li/a/span')
    HONE_XPATH = "//h1[@class='title' and contains(normalize-space(text()), '%s')]"

    TABS_XPATH = "//div[@id='block-wsbpl-tabsblock']/nav/ul/li/a[contains(normalize-space(text()), '%s')]"
    TAB_STUDY_DIRECTIONS = (By.XPATH, '//div[@class="study-directions"]')

    CHECKBOX_XPATH = "//div[@class='filters']/div[@class='options']//label/span[contains(normalize-space(text()), '%s')]"

    MENU_LEVEL_1_XPATH = "//nav[@class='main-menu']//ul//li//span[contains(normalize-space(text()), '%s')]"
    MENU_LEVEL_2 = (By.XPATH, '//div[@class="menu level-2"]')
    MENU_LEVEL_2_XPATH = "//div[@class='menu level-2']//a/span[contains(normalize-space(text()), '%s')]"

    SAVE_BUTTON = (
    By.XPATH, '//section[@id="header-page-title"]//a[contains(normalize-space(text()), "Zapisz się online")]')
    SEARCH_INPUT = (By.XPATH, '//input[@id="listing-search"]')
    SORTING_DROPDOWN = (By.XPATH, '//select[@id="sort"]')

    STUDY_DIRECTION_RESULTS = (By.XPATH, '//div[@class="study-directions"]//div[@class="direction"]')

    URL = 'https://www.wsb.pl/'
    TITLE = 'Strona główna | wsb.pl | Wyższe Szkoły Bankowe'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):
        self.driver.get(self.URL)
        if self.is_popup_displayed():
            button = self.driver.find_element(*self.POPUP_ACCEPT_BUTTON)
            button.click()
            self.wait.until(ec.invisibility_of_element_located(self.POPUP_ACCEPT_BUTTON))

    def click_tab(self, name: str):
        locator = (By.XPATH, self.TABS_XPATH % name)
        tab = self.driver.find_element(*locator)
        tab.click()

    def check_checkbox(self, name: str):
        locator = (By.XPATH, self.CHECKBOX_XPATH % name)
        checkbox = self.driver.find_element(*locator)
        checkbox.click()

    def open_study_directions(self):
        self.click_tab(name='Kierunki i specjalności')
        self.wait.until(ec.visibility_of_element_located(self.TAB_STUDY_DIRECTIONS))

    def select_menu_option(self, lvl1_text: str, lvl2_text: str):
        lvl1_locator = (By.XPATH, self.MENU_LEVEL_1_XPATH % lvl1_text)
        lvl1 = self.driver.find_element(*lvl1_locator)
        lvl1.click()
        menu = self.wait.until(ec.visibility_of_element_located(self.MENU_LEVEL_2))
        ActionChains(self.driver).move_to_element(menu).perform()
        lvl2_locator = (By.XPATH, self.MENU_LEVEL_2_XPATH % lvl2_text)
        lvl2 = self.driver.find_element(*lvl2_locator)
        lvl2.click()
        page_locator = (By.XPATH, self.HONE_XPATH % lvl2_text)
        self.wait.until(ec.visibility_of_element_located(page_locator))

    def get_breadcrumb(self):
        response = []
        breadcrumb = self.driver.find_elements(*self.BREADCRUMB)
        for element in breadcrumb:
            response.append(element.text)
        return response

    def get_study_directions(self):
        response = []
        directions = self.driver.find_elements(*self.STUDY_DIRECTION_RESULTS)
        for element in directions:
            title = element.find_element_by_xpath('.//div[@class="direction-title"]/span').text
            cities = element.find_element_by_xpath('.//div[@class="cities"]').text.split()
            image = element.find_element_by_xpath('.//div[@class="direction-img"]/img').get_attribute("src")
            response.append({
                'title': title,
                'cities': cities,
                'image': image
            })
        return response

    def is_element_displayed(self, element):
        try:
            self.driver.find_element(*element)
            return True
        except:
            return False

    def is_popup_displayed(self):
        return self.is_element_displayed(element=self.POPUP)

    def is_save_button_displayed(self):
        return self.is_element_displayed(element=self.SAVE_BUTTON)

    def is_search_input_displayed(self):
        return self.is_element_displayed(element=self.SEARCH_INPUT)

    def is_sort_dropdown_displayed(self):
        return self.is_element_displayed(element=self.SORTING_DROPDOWN)
