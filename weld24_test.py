import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import random
from datetime import datetime


def get_html(url, timeout):
	ua = UserAgent()
	header = {'User-Agent':str(ua.chrome)}
	r = requests.get(url, headers=header, timeout = timeout)	
	return r.text

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = soup.find('div', class_='left_block_menu').find_all('a', class_='pagination-page')[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]
	return int(total_pages)

def write_csv(data):
	with open(r'C:\Users\DSimonov\Documents\scripts\avito\welt.csv', 'a', newline='') as f:
			writer = csv.writer(f, delimiter =';')
			# writer.writerow((
			#  				data['price'],
			#  				))

			writer.writerow((
		 				data['metro'],
		 				data['url'],
		 				data['price'],
		 				data['title'],
		 				data['time_of_completion']))

'''
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
		now = datetime.now()
		current_time = now. strftime("%H:%M:%S")	
		data = {'title': title,
				'url': url,
				'price': price,
				'metro': metro,
				'time_of_completion':current_time}
		write_csv(data) 
'''
def topic_lvl1(html):
	topic_lvl1 = []
	soup = BeautifulSoup(html, 'lxml')
	topic_lvl1_list = soup.find('div', class_= 'left_block_menu').find_all('ul')#.find_all('li', class_='lvl1')#.find_all('li')#.find('ul').find_all('li', class_= 'lvl1 ')
#	print(topic_lvl1_list)
	for topic in topic_lvl1_list:
		topic_lvl1_temp = soup.find('li', class_= 'lvl1')#.get('href')
		#topic_lvl1_temp = soup.find('ul').find('li')#.find('a', class_= 'root-item-selected').get('href')
		print(topic_lvl1_temp)
#		topic_lvl1.append(topic_lvl1_temp)
	return topic_lvl1

def main():
	base_url = 'https://24weld.ru/katalog-svarochnoe-oborudovanie/'
	timeout = 20
	for topic_lvl1_list in topic_lvl1(get_html(base_url, timeout)):
		print(topic_lvl1_list)

 
#	total_pages = None
#	total_pages = get_html(base_url, timeout)
#	attempt = 1
	#total_pages = get_total_pages(get_html(base_url, timeout))
#	print(f'found as many pages as {total_pages}')
	
	'''for i in range(1, total_pages):
					url_gen = base_url + topic + query_part + page_part + str(i)
					html = None
					attempt = 1
					print(f'Trying to process the following url: {url_gen}')
					html = get_html(url_gen, timeout)
					print(html)
					#get_page_data(html)
			'''



if __name__ == '__main__':
	main()
