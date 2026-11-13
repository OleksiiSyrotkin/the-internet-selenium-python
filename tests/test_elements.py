import pytest

from pages.internet_pages import (
    AddRemovePage,
    AlertsPage,
    CheckboxesPage,
    DropdownPage,
    DynamicLoadingPage,
    HoversPage,
    WindowsPage,
)

def test_checkboxes(driver):
    page = CheckboxesPage(driver).open()
    assert page.states() == [False, True]

    page.toggle(0)
    page.toggle(1)

    assert page.states() == [True, False]


@pytest.mark.parametrize("option", ["Option 1", "Option 2"])
def test_dropdown(driver, option):
    page = DropdownPage(driver).open()
    page.choose(option)
    assert page.selected() == option


def test_dynamic_loading(driver):
    page = DynamicLoadingPage(driver).open()
    assert page.start_and_get_text() == "Hello World!"


class TestAlerts:

    def test_alert(self, driver):
        page = AlertsPage(driver).open()
        assert page.js_alert() == "I am a JS Alert"
        assert page.result() == "You successfully clicked an alert"

    @pytest.mark.parametrize("accept, expected", [(True, "You clicked: Ok"), (False, "You clicked: Cancel")])
    def test_confirm(self, driver, accept, expected):
        page = AlertsPage(driver).open()
        page.js_confirm(accept)
        assert page.result() == expected

    def test_prompt(self, driver):
        page = AlertsPage(driver).open()
        page.js_prompt("selenium")
        assert page.result() == "You entered: selenium"


@pytest.mark.parametrize("index", [0, 1, 2])
def test_hover_shows_user(driver, index):
    page = HoversPage(driver).open()
    assert page.hover_and_get_caption(index) == f"name: user{index + 1}"


def test_new_window(driver):
    page = WindowsPage(driver).open()
    original = page.open_new_window()

    assert page.header() == "New Window"

    driver.close()
    driver.switch_to.window(original)
    assert page.header() == "Opening a new window"


def test_add_remove_elements(driver):
    page = AddRemovePage(driver).open()
    page.add(3)
    assert page.count() == 3

    page.delete_first()
    assert page.count() == 2
