from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class CheckboxesPage(BasePage):
    url = "/checkboxes"
    BOXES = (By.CSS_SELECTOR, "#checkboxes input")

    def boxes(self):
        return self.find_all(self.BOXES)

    def states(self):
        return [b.is_selected() for b in self.boxes()]

    def toggle(self, index):
        self.boxes()[index].click()


class DropdownPage(BasePage):
    url = "/dropdown"
    SELECT = (By.ID, "dropdown")

    def choose(self, text):
        Select(self.find(self.SELECT)).select_by_visible_text(text)

    def selected(self):
        return Select(self.find(self.SELECT)).first_selected_option.text


class DynamicLoadingPage(BasePage):
    url = "/dynamic_loading/2"
    START = (By.CSS_SELECTOR, "#start button")
    LOADER = (By.ID, "loading")
    RESULT = (By.CSS_SELECTOR, "#finish h4")

    def start_and_get_text(self):
        self.click(self.START)
        self.wait.until(EC.invisibility_of_element_located(self.LOADER))
        return self.text_of(self.RESULT)


class AlertsPage(BasePage):
    url = "/javascript_alerts"
    RESULT = (By.ID, "result")

    def _button(self, text):
        return By.XPATH, f"//button[text()='{text}']"

    def _alert(self):
        return self.wait.until(EC.alert_is_present())

    def js_alert(self):
        self.click(self._button("Click for JS Alert"))
        alert = self._alert()
        text = alert.text
        alert.accept()
        return text

    def js_confirm(self, accept):
        self.click(self._button("Click for JS Confirm"))
        alert = self._alert()
        alert.accept() if accept else alert.dismiss()

    def js_prompt(self, value):
        self.click(self._button("Click for JS Prompt"))
        alert = self._alert()
        alert.send_keys(value)
        alert.accept()

    def result(self):
        return self.text_of(self.RESULT)


class HoversPage(BasePage):
    url = "/hovers"
    FIGURES = (By.CSS_SELECTOR, ".figure")
    CAPTION = (By.CSS_SELECTOR, ".figcaption h5")

    def hover_and_get_caption(self, index):
        figure = self.find_all(self.FIGURES)[index]
        ActionChains(self.driver).move_to_element(figure).perform()
        caption = figure.find_element(*self.CAPTION)
        self.wait.until(lambda _: caption.is_displayed())
        return caption.text


class WindowsPage(BasePage):
    url = "/windows"
    LINK = (By.LINK_TEXT, "Click Here")
    HEADER = (By.TAG_NAME, "h3")

    def open_new_window(self):
        original = self.driver.current_window_handle
        self.click(self.LINK)
        self.wait.until(EC.number_of_windows_to_be(2))
        new = next(h for h in self.driver.window_handles if h != original)
        self.driver.switch_to.window(new)
        return original

    def header(self):
        return self.text_of(self.HEADER)


class AddRemovePage(BasePage):
    url = "/add_remove_elements/"
    ADD = (By.XPATH, "//button[text()='Add Element']")
    DELETE = (By.CSS_SELECTOR, "#elements .added-manually")

    def add(self, times=1):
        for _ in range(times):
            self.click(self.ADD)

    def delete_first(self):
        self.driver.find_elements(*self.DELETE)[0].click()

    def count(self):
        return len(self.driver.find_elements(*self.DELETE))
