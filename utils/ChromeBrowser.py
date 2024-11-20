from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from utils.mime_types import (expected_mime_types, extensions)


class ChromeBrowser:
    @staticmethod
    def response_interceptor(request, response):

        if response.headers['WWW-Authenticate']:
            del response.headers['WWW-Authenticate']

        if str(response.headers['Content-Type']).split(';')[0] not in expected_mime_types:
            request.abort()

    @staticmethod
    def request_interceptor(request):

        if request.path.endswith(extensions):
            request.abort()

        request.headers['X-Bug-Bounty-Hunter'] = 'sumbru'

    @property
    def selenium_wire_options(self):
        return {
            'verify_ssl': False,
            'suppress_connection_errors': True,
            # 'ignore_http_methods': [],
            # 'exclude_hosts': ['google.com'],
            # 'disable_encoding': True
        }

    @property
    def chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--disable-infobars')
        return chrome_options

    @property
    def browser(self):
        browser = webdriver.Chrome(chrome_options=self.chrome_options, seleniumwire_options=self.selenium_wire_options)
        browser.request_interceptor = self.request_interceptor
        browser.response_interceptor = self.response_interceptor
        browser.set_page_load_timeout(15)
        return browser
