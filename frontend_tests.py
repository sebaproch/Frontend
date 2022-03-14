import time
import pytest
from selenium import webdriver
from Frontend.helpers import compare_value
from Frontend.page_objects.main_page import MainPage


@pytest.fixture()
def chrome_driver(request):
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(10)
    driver.maximize_window()

    def teardown():
        driver.close()

    request.addfinalizer(teardown)
    return driver


def test_study_directions_page(chrome_driver):
    """ Test verify elements on Study directions tab
    Steps:
    1. Click 'Studia i szkolenia' -> 'Studia I stopnia'
    2. Click Study directions tab
    3. Select checkboxes: 'Wrocław' and Studia inżynierskie'
    4. Check number of results
    5. Check if 'Save button', 'Search input' and 'Sort dropdown' are displayed on page
    """
    issues = []

    expected_data = [
        {'title': 'Informatyka',
         'cities': ['Chorzów/Katowice', 'Gdańsk', 'Gdynia', 'Poznań', 'Szczecin', 'Warszawa', 'Wrocław', 'Toruń'],
         'image': 'https://www.wsb.pl/sites/wsb/files/styles/listing/public/media/image/informatyka_2.jpg?itok=LL4Yzi4n'},
        {'title': 'Inżynieria zarządzania',
         'cities': ['Bydgoszcz', 'Chorzów/Katowice', 'Gdańsk', 'Opole', 'Poznań', 'Szczecin', 'Toruń', 'Wrocław'],
         'image': 'https://www.wsb.pl/sites/wsb/files/styles/listing/public/media/image/WYBRANE_IMG_0527_0.jpg?itok=BGc7oLba'},
        {'title': 'Logistyka',
         'cities': ['Bydgoszcz', 'Chorzów/Katowice', 'Gdańsk', 'Gdynia', 'Opole', 'Poznań', 'Szczecin', 'Warszawa',
                    'Wrocław', 'Toruń'],
         'image': 'https://www.wsb.pl/sites/wsb/files/styles/listing/public/media/image/logistyka.jpg?itok=4TXFUJB7'}
    ]

    main_page = MainPage(driver=chrome_driver)
    main_page.open()
    main_page.select_menu_option(lvl1_text='Studia i szkolenia', lvl2_text='Studia I stopnia')
    main_page.open_study_directions()
    main_page.check_checkbox(name='Wrocław')
    main_page.check_checkbox(name='Studia inżynierskie')

    time.sleep(1)
    directions = main_page.get_study_directions()
    issues += compare_value(observed=len(directions), expected=3, element='Number of study directions')
    issues += compare_value(observed=directions, expected=expected_data, element='Page results')
    issues += compare_value(observed=main_page.is_save_button_displayed(), expected=True, element='Save button')
    issues += compare_value(observed=main_page.is_search_input_displayed(), expected=True, element='Search input')
    issues += compare_value(observed=main_page.is_sort_dropdown_displayed(), expected=True, element='Sort dropdown')

    assert not issues, f'Some issues was found testing page elements. Issues: {issues}'
