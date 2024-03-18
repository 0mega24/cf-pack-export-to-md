"""
This module provides a function to build a Chrome webdriver instance with specific options.

It uses the Selenium library and the selenium_stealth package to create a headless Chrome webdriver
with various options to enhance stealth and performance.

Example usage:
    driver = build_driver()
    driver.get("https://www.example.com")

"""

from selenium import webdriver
from selenium_stealth import stealth

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-extensions")
options.add_argument("disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-logging"])


def build_driver() -> webdriver.Chrome:
    """
    Builds and returns a Chrome webdriver instance with the specified options.

    Returns:
        webdriver.Chrome: The built Chrome webdriver instance.
    """
    driver = webdriver.Chrome(options=options)
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver
