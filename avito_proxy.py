import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import random


def find_proxy():

	proxies_list = []
	res = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0'})
	soup = BeautifulSoup(res.text,"lxml")
	for items in soup.select("#proxylisttable tbody tr")[50:random.randint(51,75)]:
		proxy_list = ':'.join([item.text for item in items.select("td")[:2]])
		temp = ('https://' + str(proxy_list))
		proxies={
		'https': temp
		}
	return proxies



def get_html(url, proxy, timeout):
	ua = UserAgent()
	header = {'User-Agent':str(ua.chrome)}
	#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	r = requests.get(url, headers=header, proxies = proxy, timeout = timeout)
	return r.text

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
#	print(soup)
	pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]
	return int(total_pages)

def write_csv(data):
	with open(r'C:\Users\DSimonov\Documents\scripts\avito\avito.csv', 'a') as f:
		writer = csv.writer(f, delimiter =';')
		# writer.writerow((
		#  				data['price'],
		#  				))

		writer.writerow((
		 				data['metro'],
		 				data['url'],
		 				data['price'],
		 				data['title'],
		 				))


def get_page_data(html):
	# title price date 
	soup = BeautifulSoup(html, 'lxml')
	try:
		ads = soup.find('div', class_= 'js-catalog_serp').find_all('div', class_= 'snippet-horizontal item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended')
	except:
		ads = ''
	for ad in ads:
		try:
			title = ad.find('div', class_='item_table-header').find('h3').text.strip()		
		except:
			title = ''
		try:	
			url = 'https://www.avito.ru' + ad.find('div', class_='item_table-header').find('h3').find('a').get('href')
		except:
			url = ''	
		try:	
			price = ad.find('div', class_='about').find('span', class_= 'price').text.strip()[:-1].strip()
			
		except:
			price = ''
		try:
			metro =  ad.find('div', class_='item-address').find('span', class_='item-address-georeferences-item__content').text.strip()
		except:
			metro = ''
		data = {'title': title,
				'url': url,
				'price': price,
				'metro': metro}
		write_csv(data) 

def main():
	base_url = 'https://www.avito.ru/moskva/nastolnye_kompyutery?'
	page_part = 'p='
	query_part = 'cd=1&user=1&q=pc&'
	url = 'https://www.avito.ru/moskva/nastolnye_kompyutery?cd=1&user=1&q=pc&p=1'  
	total_pages = None
	timeout = 20
	attempt = 1
	while total_pages is None:
		print()
		try:
			proxy = find_proxy()
			print(f'Found proxy to get number of pages: {proxy}')
			total_pages = get_total_pages(get_html(url, proxy, timeout))
		except Exception as err:
			print(f'Attempt {attempt} failed,because of {err.args}, let us try more proxies')
			attempt += 1
			pass
	for i in range(1, total_pages):
		url_gen = base_url + query_part + page_part + str(i)
		html = None
		attempt = 1
		while html is None:
			try:
				proxy = find_proxy()
				print(f'Found proxy to grab the info: {proxy}')
				html = get_html(url_gen, proxy, timeout)
			except Exception as err:
				print(f'Attempt {attempt} failed,because of {err.args}, let us try more proxies')
				attempt += 1
				pass
		get_page_data(html)
		print(f'Page number {i} ready')



if __name__ == '__main__':
	main()
