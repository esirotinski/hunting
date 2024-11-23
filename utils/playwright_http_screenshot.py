from playwright.sync_api import sync_playwright

def save_screenshot(domain):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://' + domain)
        page.screenshot(path="../logs/screenshots/" + domain + ".png", full_page=True)
        browser.close()

if __name__ == "__main__":
    save_screenshot("www.example.com")