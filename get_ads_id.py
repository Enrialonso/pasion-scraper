import os
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from datetime import datetime as dt

from playwright.sync_api import Playwright, sync_playwright, TimeoutError

from models.models import Categories, Cities
from utils.utils import create_sql_session, get_and_save_ad_id

scraping_date = dt.now()


def run(playwright: Playwright, config) -> None:
    test_script = os.getenv("TEST_SCRIPT", "NO")
    print(f"TEST_SCRIPT = {test_script}")
    session = create_sql_session()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pasion.com/")
    page.click("text=Contactos hombres")
    page.click("text=ENTRAR")

    print(f"Select category: {config['category']}, city: {config['city']}")
    categories_select = page.query_selector("//*[@id='ca2']")
    categories_select.select_option(value=config["category"])
    page.wait_for_timeout(500)

    city_select = page.query_selector("//*[@id='protmp']")
    city_select.select_option(value=config["city"])
    page.query_selector("//*[@id='vamos']/div").click()
    page.wait_for_timeout(1000)

    index = 0
    while True:
        get_and_save_ad_id(page, session, config["category"], config["city"], scraping_date)
        try:
            button = page.wait_for_selector("td >> div >> a:text('Siguiente')", timeout=500)
            button.click()
        except TimeoutError:
            break
        index += 1
        if index == 2 and test_script == "YES":
            break

    context.close()
    browser.close()


def worker(config):
    with sync_playwright() as playwright:
        run(playwright, config)


def main():
    config_workers, count_workers = [], int(float(os.getenv("COUNT_WORKERS", 2)))
    print(f"COUNT_WORKERS = {count_workers}")
    session = create_sql_session()
    data = session.query(Categories).all()

    for category in data:
        for city in session.query(Cities).all():
            if category.value and city.value:
                config_workers.append({"category": category.value, "city": city.value})

    with PoolExecutor(max_workers=count_workers) as executor:
        for _ in executor.map(worker, config_workers):
            pass


if __name__ == "__main__":
    main()
