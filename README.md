# the-internet-selenium-python

[![tests](https://github.com/OleksiiSyrotkin/the-internet-selenium-python/actions/workflows/tests.yml/badge.svg)](https://github.com/OleksiiSyrotkin/the-internet-selenium-python/actions/workflows/tests.yml)

Selenium + pytest tests for [the-internet.herokuapp.com](https://the-internet.herokuapp.com) - a set of pages with elements that are usually tricky to automate.

Allure report from the latest run on `main`: https://oleksiisyrotkin.github.io/the-internet-selenium-python/

## What is tested

| Page | What the test does | Selenium feature |
|---|---|---|
| Checkboxes | checks initial state, toggles both boxes | `is_selected()` |
| Dropdown | selects each option | `Select` |
| Dynamic Loading | starts loading and waits for the result text | explicit wait for loader to disappear |
| JavaScript Alerts | alert, confirm (OK / Cancel), prompt with text | `switch_to.alert`, `alert_is_present` |
| Hovers | hovers each avatar and reads the hidden caption | `ActionChains.move_to_element` |
| Multiple Windows | opens new window, checks it, closes and returns back | `window_handles`, `switch_to.window` |
| Add/Remove Elements | adds 3 elements, deletes one | dynamic elements |

## Stack

- Python 3.12, Selenium 4, pytest
- pytest-xdist, pytest-rerunfailures
- Allure
- GitHub Actions (Chrome + Firefox) and GitHub Pages for the report

## Project structure

```
pages/
  base_page.py         common actions with explicit waits
  internet_pages.py    one page object per tested page
tests/
  test_elements.py
config.py              base url and timeout
conftest.py            driver fixture, --browser and --headless options, screenshot on failure
```

## Approach

- Page Object Model: locators and Selenium calls live in page classes, tests only call methods and assert.
- No `time.sleep`, only `WebDriverWait` with expected conditions.
- Parametrized tests for dropdown options, confirm OK/Cancel and hover over each user.
- Fresh browser for each test, so tests can run in parallel.
- Screenshot and URL are attached to Allure when a test fails.

## How to run

```bash
git clone https://github.com/OleksiiSyrotkin/the-internet-selenium-python.git
cd the-internet-selenium-python

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

```bash
pytest                          # Chrome
pytest --browser=firefox
pytest --headless
pytest -n 4                     # parallel
pytest -k alert                 # only alert tests
allure serve allure-results     # report (needs Allure CLI)
```

## CI

`.github/workflows/tests.yml` runs tests in Chrome and Firefox, merges Allure results and publishes the report to GitHub Pages. Runs on push to `main`, on pull requests, manually and every Monday.
