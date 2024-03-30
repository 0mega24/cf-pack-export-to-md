from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from typing import List, Union


def build_driver() -> webdriver.Chrome:
    options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-webgl")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver: webdriver.Chrome = webdriver.Chrome(options=options)
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


def get_details(page: str) -> Union[bool, List[str]]:
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")

    try:
        description: str = soup.find("meta", attrs={"name": "description"}).get(
            "content", ""
        )

        project_header: BeautifulSoup = soup.find("div", class_="project-header")
        total_downloads: str = (
            project_header.find("li", class_="detail-downloads")
            .find("span")
            .text.strip()
        )
        img_src: str = project_header.find("img").get("src", "")

        file_card: BeautifulSoup = soup.find("div", class_="file-details-card")
        file_name: str = (
            file_card.find("section", class_="section-file-name").find("p").text.strip()
        )
        game_version: str = (
            file_card.find("ul", class_="versions-group-items").find("li").text.strip()
        )

        license: str = soup.find("dd", id="licenseType").text.strip()

    except AttributeError:
        return False

    return [description, total_downloads, img_src, file_name, game_version, license]
