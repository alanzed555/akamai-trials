import subprocess, sys, random, json, time, datetime, os

def install_dependencies():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lxml'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])

try:
    import requests, lxml.html as html, selenium
except:
    install_dependencies()
    import requests, lxml.html as html, selenium

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as chromeopt

class footlockerbrowser():
    def __init__(self, link, proxy = None):
        self.session = requests.session()
        self.product = link
        if proxy!= None:
            self.session.proxies.update(proxy)
        self.start_sensor()
        self.get_abck()
        self.validate_abck()
        self.atc()
        self.update_csrf()
        self.checkout_delivery()
        self.validate_abck()
        self.update_csrf()
        self.check_delivery_validated()
        self.checkout_delivery_confirm()

    def start_sensor(self):
        file_name = os.path.dirname(os.path.abspath(__file__)) + r'\abck.html'
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = {'browser': 'ALL'}
        chromeoptions = chromeopt()
        chromeoptions.add_argument('--headless')
        self.driver = webdriver.Chrome(desired_capabilities=d, options=chromeoptions)
        self.driver.get(file_name)

    def get_abck(self):
        headers = {
            'authority': 'www.footlocker.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
        }
        self.session.get('https://www.footlocker.com/', headers=headers)

    def get_sensor(self, abckcookie):
        self.sensor_data = self.driver.execute_script('bmak.bpd(arguments[0]); return bmak.sensor_data', abckcookie)
        return self.sensor_data

    def validate_abck(self):
        headers = {
            'authority': 'www.footlocker.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'content-type': 'text/plain;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://www.footlocker.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.footlocker.com/',
            'accept-language': 'en-US,en;q=0.9',
        }
        r = self.session.post('https://www.footlocker.com/assets/c7b8a45816262992aff5b862e75c',json={'sensor_data': self.get_sensor(self.session.cookies.get('abck'))},headers=headers)
        print(self.session.cookies.get('_abck'))

    def atc(self):#product id
        headers = {
            'authority': 'www.footlocker.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json',
            'x-fl-productid': '22410354',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://www.footlocker.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.footlocker.com/product/nike-lebron-17-low-mens/D5007101.html',
            'accept-language': 'en-US,en;q=0.9',
        }  # add to cart
        params = {'timestamp': time.time()}
        data = {"productQuantity": 1, "productId": "22410354"}
        response = self.session.post('https://www.footlocker.com/api/users/carts/current/entries', headers=headers, params=params, json=data, verify=False)
        print("add to cart", response.status_code, response.text)

    def update_csrf(self):
        headers = {
            'authority': 'www.footlocker.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.footlocker.com/product/nike-lebron-17-low-mens/D5007101.html',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        }

        params ={'timestamp': time.time()}
        response = self.session.get('https://www.footlocker.com/api/v3/session', headers=headers, params=params)
        self.csrf_token = json.loads(response.text)['data']['csrfToken']
        print(self.csrf_token)

    def checkout_delivery(self):
        headers = {
            'authority': 'www.footlocker.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json',
            'x-csrf-token': self.csrf_token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://www.footlocker.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.footlocker.com/checkout',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        }

        params = {'timestamp': time.time()}
        data = '{"country":{"isocode":"US","name":"United States"},"region":{"countryIso":"US","isocode":"US-NJ","isocodeShort":"NJ","name":"New Jersey"},"line1":"7004 JFK BLVD E","line2":"38g","postalCode":"07093","town":"WEST NEW YORK"}'
        response = self.session.post('https://www.footlocker.com/api/v3/users/addresses/verification', headers=headers,params=params, data=data)
        print(response, response.text)

    def check_delivery_validated(self):
        headers = {
            'authority': 'www.footlocker.com',
            'content-length': '0',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json',
            'x-csrf-token': self.csrf_token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'origin': 'https://www.footlocker.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.footlocker.com/checkout',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        }

        params = {'timestamp': time.time()}
        response = self.session.put('https://www.footlocker.com/api/users/carts/current/email/chouerzi@gmail.com',headers=headers, params=params)

    def checkout_delivery_confirm(self):
        headers = {
            'authority': 'www.footlocker.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json',
            'x-csrf-token': self.csrf_token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://www.footlocker.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.footlocker.com/checkout',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        }

        params = {'timestamp': time.time()}
        data = '{"shippingAddress":{"setAsBilling":true,"country":{"isocode":"US","name":"United States"},"id":null,"region":{"countryIso":"US","isocode":"US-NJ","isocodeShort":"NJ","name":"New Jersey"},"phone":"6463222013","type":"default","firstName":"omar","lastName":"hu","line1":"7004 JFK BLVD E","line2":"38g","postalCode":"07093","town":"WEST NEW YORK","email":false,"regionFPO":null,"shippingAddress":true,"recordType":" "}}'
        response = self.session.post('https://www.footlocker.com/api/users/carts/current/addresses/shipping',
                                 headers=headers, params=params, data=data)
        print(response, response.text)

ftl = footlockerbrowser('')