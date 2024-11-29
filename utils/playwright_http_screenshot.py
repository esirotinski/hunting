from playwright.sync_api import sync_playwright

def save_screenshot(domain):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--ignore-certificate-errors", "--ignore-certificate-errors-spki-list"]
        )
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://' + domain, wait_until='networkidle')
        page.screenshot(path="../logs/screenshots/" + domain + ".png", full_page=True)
        browser.close()

if __name__ == "__main__":
    save_screenshot("www.example.com")