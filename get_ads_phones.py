from playwright.sync_api import sync_playwright

from models.models import Advertisements
from utils.utils import create_sql_session, extract_phones

all_proxy = [{"http": "3.250.108.95:8888", "https": "3.250.108.95:8888"}]


def main():
    session = create_sql_session()
    ads = session.query(Advertisements).filter(Advertisements.phone == None)
    for ad in ads:
        with sync_playwright() as playwright:
            # browser = playwright.chromium.launch(headless=False, proxy={"server": "http://3.250.108.95:8888"})
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"https://www.pasion.com/email/enviar_a_un_amigo.php?id={ad.id_ad.replace('r', '')}")
            # page.goto(f"https://www.pasion.com/datos-contacto/?id={ad.id_ad.replace('r', '')}")
            page.fill("//*[@id='nombre']", "546270451")
            page.fill("//*[@id='email']", "enrifood@gmail.com")
            page.fill("//*[@id='remitente']", "test email 546270451")
            page.fill("//*[@id='mensaje']", "test email 546270451")
            page.query_selector("//html/body/div/div/form/div[5]/input").click()
            page.wait_for_timeout(1000)
            # phones = extract_phones(page.inner_html("body"))
            # print(phones, page.url)
            # page.wait_for_timeout(5000)
            context.close()
            browser.close()


if __name__ == "__main__":
    main()

# with sync_playwright() as playwright:
#     # browser = playwright.chromium.launch(headless=False, proxy={"server": "http://3.250.108.95:8888"})
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(f"https://www.pasion.com/email/enviar_a_un_amigo.php?id=546270451")
#     # page.goto(f"https://www.pasion.com/datos-contacto/?id={ad.id_ad.replace('r', '')}")
#     phones = extract_phones(page.inner_html("body"))
#     print(phones, page.url)
#     page.wait_for_timeout(5000)
#     context.close()
#     browser.close()
