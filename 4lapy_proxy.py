import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import random
from datetime import datetime

def find_proxy():

	proxies_list = []
	proxies = {}
	i = True
	while i == True:
		try:
			res = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0'})
			i = False
		except Exception as err:
			print(f'while searching for proxies we failed \n because of {err.args}, \n let us try else')
			pass
	soup = BeautifulSoup(res.text,"lxml")
	random_proxy = random.randint(1,50)
	for items in soup.select("#proxylisttable tbody tr")[random_proxy:random.randint(random_proxy + 1 ,75)]:
		proxy_list = ':'.join([item.text for item in items.select("td")[:2]])
		temp = ('https://' + str(proxy_list))
		proxies={
		'https': temp
		}
	return proxies

def get_html(url, timeout, proxy):
	ua = UserAgent()
	header = {'User-Agent':str(ua.random)}
	r = requests.get(url, headers=header, timeout = timeout, proxies = proxy)	
	return r.text


def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	total_pages = 0
	try:
		pages = soup.find('div', class_='b-pagination').find('ul', class_ = 'b-pagination__list').find_all('a', class_='b-pagination__link js-pagination')[-2].get('href')	
#		print(pages)
		total_pages = pages.split('=')[-1]	
#		print(total_pages)
	except Exception as err:
		print(f'Attempt failed,because of {err.args}')
		pass
	print(f'Total pages = {total_pages}')
	return int(total_pages)

def write_csv(data):
	print('trying to save CSV')
	with open(r'C:\Users\DSimonov\Documents\scripts\avito\4_lapy.csv', 'a', newline='', encoding='cp1251', errors='replace') as f:
		try:
			writer = csv.writer(f, delimiter =';')
			writer.writerow((
		 				data['title'],
		 				data['weight'],
		 				data['price'],
		 				data['currency'],
		 				data['url'],
		 				data['time_of_completion']))
		except Exception as err:
			print(f'Cannot write CSV because of {err.args}')
		print('saved suceessfully')

def get_page_data(html):
	# title price date 
	soup = BeautifulSoup(html, 'lxml')
	print('geting_page_data')
	try:
		ads = soup.find('div', class_= 'b-common-wrapper b-common-wrapper--visible js-catalog-wrapper').find_all('div', class_= 'b-common-item  b-common-item--catalog-item js-product-item')
		print('ads found')
	except:
		ads = ''
		print('no ads found')
		
	for ad in ads:
		try:
			title = ad.find('div', class_='b-common-item__info-center-block').find('span', class_='span-strong').text.strip()		
		except:
			title = ''
		try:	
			url = 'https://4lapy.ru/' + ad.find('a', class_='b-common-item__description-wrap js-item-link').find('a').get('href')
		except:
			url = ''	
		try:	
			price = ad.find('span', class_='b-common-item__wrapper-link').find('span', class_= 'b-common-item__price js-price-block').text.strip()		
		except:
			price = ''
		try:	
			weight = ad.find('ul', class_='b-weight-container__list').find_all('li', class_='b-weight-container__item')[0].text.strip()		
		except:
			price = ''
		try:
			currency =  ad.find('span', class_='b-common-item__wrapper-link').find('span', class_= 'b-ruble').text.strip()
		except:
			currency = ''
		now = datetime.now()
		current_time = now. strftime("%H:%M:%S")	
		data = {'title': title,
				'url': url,
				'price': price,
				'currency': currency,
				'time_of_completion':current_time,
				'weight': weight}
		print('saving to csv')
		write_csv(data) 


def topic_lvl1(html):
	topics = []
	topic = None
	soup = BeautifulSoup(html, 'lxml')
	topic_lvl1_list = soup.find('div', class_= 'b-filter__wrapper').find_all('div', class_='b-accordion b-accordion--filter')#.find('ul').find_all('a')
#	print(topic_lvl1_list)
	for topic_level_1 in topic_lvl1_list:
		topic_level_2 = topic_level_1.find('div', class_='b-accordion__block js-dropdown-block').find('ul', class_='b-filter-link-list').find_all('li', class_='b-filter-link-list__item')
#		print(topic_level_2)
		for item in topic_level_2:
			topic_temp = item.find('a', class_= 'b-filter-link-list__link').get('href')
			print(topic_temp)
			topics.append(topic_temp)
	return topics


def main():
	base_url = 'https://4lapy.ru/catalog/'
	url_head = 'https://4lapy.ru'
	intermed_url = '?page='
	timeout = 20
	total_pages = None
	topics = None
	url = None
	print('start')
	attempt = 1
	while topics is None:
		try:
			proxy = find_proxy()
			print(f'Found proxy to get number of pages: {proxy}. This is {attempt} attempt.')
			topics = topic_lvl1(get_html(base_url, timeout, proxy))
		except Exception as err:
			print(f'Attempt to obtain list of links number {attempt} failed, because of {err.args}, let us try more proxies')
			attempt += 1
			pass
	for url in topics:
		total_pages = None
		attempt = 1	
		while total_pages is None:
			try:
				print(f'Looking for amount of pages (url: {url_head + url}). This is {attempt} attempt')
				total_pages = get_total_pages(get_html(url_head + url, timeout, proxy))	
			except Exception as err:	
				print(f'Attempt of counting pages {attempt} failed, because of {err.args}, let us try more proxies')
				attempt += 1
				proxy = find_proxy()
				pass
		for i in range(1,total_pages):
			url_generated = url_head + url + intermed_url + str(i)
			print('processing page: ', url_generated)
			html = None
			attempt = 1
			while html is None:
				try:
					print(f'Trying to gather page data from {url_generated}. This is {attempt} attempt.')
					html = get_html(url_generated, timeout, proxy)
					print(f'Found information in {url_generated}')
				except Exception as err:
					proxy = find_proxy()
					print(f'Attempt of getting page data {attempt} failed, because of {err.args}, let us try more proxies')
					attempt += 1
					pass
			print(f'Try to process page {url_generated} to extract data and save to CSV')
			get_page_data(html)

	print("done")
if __name__ == '__main__':
	main()

