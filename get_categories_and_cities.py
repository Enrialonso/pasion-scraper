from playwright.sync_api import Playwright, sync_playwright

from models.models import Categories, Cities
from utils.utils import clean_text, create_sql_session


def run(playwright: Playwright) -> None:
    session = create_sql_session()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pasion.com/")
    page.click("text=Contactos hombres")
    page.click("text=ENTRAR")

    categories = page.query_selector("//*[@id='ca2']")
    print("search Categories")
    for category in categories.query_selector_all("option"):
        value, name = category.get_attribute("value"), clean_text(category.inner_text())
        check_category = session.query(Categories).filter(Categories.value == value).count()
        if not check_category:
            cat = Categories(name=name, value=value)
            session.add(cat)
            session.commit()
            print(value, name)

    cities = page.query_selector("//*[@id='protmp']")
    print("search Cities")
    for city in cities.query_selector_all("option"):
        value, name = city.get_attribute("value"), clean_text(city.inner_text())
        check_city = session.query(Cities).filter(Cities.value == value).count()
        if not check_city:
            cit = Cities(name=name, value=value)
            session.add(cit)
            session.commit()
            print(value, name)

    context.close()
    browser.close()


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
