from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth


def build_driver() -> webdriver.Chrome:
    """
    Builds and returns a Chrome webdriver instance with the specified options.

    Returns:
        webdriver.Chrome: The built Chrome webdriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-webgl")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
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


def get_details(page):
    soup = BeautifulSoup(page, "html.parser")

    try:
        project_header = soup.find("div", class_="project-header")

        file_card = soup.find("div", class_="file-details-card")

        license_dd = soup.find("dd", id="licenseType")

        description = soup.find("meta", attrs={"name": "description"}).get(
            "content", ""
        )

        total_downloads = (
            project_header.find("li", class_="detail-downloads")
            .find("span")
            .text.strip()
        )
        img_tag = project_header.find("img")
        img_src = img_tag.get("src", "")

        file_name = (
            file_card.find("section", class_="section-file-name").find("p").text.strip()
        )
        game_version = (
            file_card.find("ul", class_="versions-group-items").find("li").text.strip()
        )

        license = license_dd.text.strip()

    except AttributeError:
        return False

    return[description, total_downloads, img_src, file_name, game_version, license]
