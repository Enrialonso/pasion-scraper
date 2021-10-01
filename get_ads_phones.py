from playwright.sync_api import sync_playwright

from models.models import Advertisements
from utils.utils import create_sql_session, extract_phones


def main():
    session = create_sql_session()
    ads = session.query(Advertisements).filter(Advertisements.phone == None).all()
    # page.goto("https://www.pasion.com/")
    for ad in ads:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"https://www.pasion.com/datos-contacto/?id={ad.id_ad.replace('r', '')}")
            phones = extract_phones(page.inner_html("body"))
            print(phones, page.url)
            context.close()
            browser.close()


if __name__ == "__main__":
    main()
