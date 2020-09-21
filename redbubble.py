#!/usr/bin/env python3.5

import xlwt
from xlwt import Workbook
import requests
import time
import re
from bs4 import BeautifulSoup

wb = Workbook()
sheet = wb.add_sheet('Sheet 1')
i = 0
sheet.write(i, 0, 'Name')
sheet.write(i, 1, 'Price')
sheet.write(i, 2, 'Link')
	
headers = {
 'authority': 'www.kith.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}

session = requests.session()
url = 'https://www.redbubble.com/shop/mugs'
response = session.get(url, headers=headers)

def get_page_num(soup):
	string = soup.find('div', class_="Pagination__numberCounter--3PXW6").text.strip()
	tulp = re.findall(r'\d+', string)
	step = int(tulp[1]) - int(tulp[0])
	total = ""
	for idx in range(2, len(tulp)):
		total += tulp[idx]
	return round(int(total)/step)
	
response_all = [response]

page_num = get_page_num(BeautifulSoup(response.text, 'html.parser'))
for p in range(2,page_num):
	url_p =  url + '?page={}'.format(p)
	response_app = session.get(url_p, headers=headers)
	response_all.append(response_app)
	time.sleep(0.2)

for r in response_all:
	soup = BeautifulSoup(r.text, 'html.parser')
	
	for element in soup.find_all('a', class_='styles__link--2sYi3'):
		price = element.find('span', class_="styles__box--206r9 styles__text--NLf2i styles__body--3bpp7 styles__display-block--2XANJ").find('span').text.strip()
		link = element.get('href')
		name = element.find('div', class_="styles__box--206r9 styles__disableLineHeight--1iIL4 styles__paddingRight-0--fzRHs").find('span').text.strip()
		
		i+=1
		sheet.write(i, 0, name)
		sheet.write(i, 1, price)
		sheet.write(i, 2, link)

wb.save('redbubble.xls')

