import pytest
from browser.driver_factory import get_browserstack_driver
from config.browserstack_caps import BROWSER_CAPS
from main import run_pipeline


@pytest.mark.parametrize("capabilities", BROWSER_CAPS)
def test_el_pais_browserstack(capabilities):
    driver = get_browserstack_driver(capabilities)
    try:
        run_pipeline(driver)
    finally:
        driver.quit()
