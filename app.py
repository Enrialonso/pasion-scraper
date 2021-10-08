from playwright import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.newPage()
    page.goto('https://pasion.com')
    print(page.title())
    browser.close()
