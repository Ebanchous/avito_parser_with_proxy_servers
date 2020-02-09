import re
import requests
from func_timeout import func_timeout, FunctionTimedOut
from urllib.parse import urlsplit
from urllib.request import urlparse, urljoin
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv
import time
import os
import colorama



def is_valid(url):
	"""
	Checks whether `url` is a valid URL.
	"""
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)

def write_csv(data, today):
#	print('trying to save CSV')
	with open(str('result') +'_' + str(today) + 'fin_1' + '.csv', 'a', newline='', encoding='cp1251', errors='replace') as f:
		try:
			writer = csv.writer(f, delimiter =';')
			writer.writerow((
						data['url'],
						data['email'],
						data['header'],
						data['time_of_completion'],
						data['file']))
#		except:
#			pass
		except Exception as err:
			print('cannot do it because of ', err.args)
			pass
#			print(f'Cannot write CSV because of {err.args}')
#		print('saved suceessfully')

def get_html(url):

	timeout = 1
	r = requests.get(url, timeout = timeout)
	return r.text

def get_emails(text):
	emails = []
	# emails = set(re.findall(r'\w+@\w+\.{1}\w+',
	# 				text, re.I))
#------------------------------------
	# regexp = re.compile(("mailto:([a-z0-9!#$%&'*+\/=?^_`{|}~-]+@[a-z0-9]+\.[a-zA-Z0-9-.]+)"))

	# emails = re.findall(regexp, text)

#--------------------------------------

	mailtos = text.select('a[href^=mailto]')
	for i in mailtos:
		href=i['href']
		try:
			str1, str2 = href.split(':')
		except ValueError:
			break
		
		emails.append(str2)

	print('emails from function:',emails)
#	time.sleep()
	return emails

def get_soup(response):
	soup = BeautifulSoup(response, 'lxml')
	return soup

def link_repair(link, url):
	if 'http' in link:
		print('link:',link)
		full_link = link
	else:
		full_link = 'http://www.'+url+link	
	href = urljoin(url, link)
	parsed_href = urlparse(full_link)
	full_link = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
	full_link = str.lower(full_link)
	return full_link

def more_urls(urls, file):
	for  url in urls:
		today = datetime.now().strftime("%d-%m-%Y")
		try:
			print('url processing', url)
			url_full = str('http://www.') + str(url)
			try:
				response = get_html(url_full)
			except Exception as err:
				response = ''
				print('cannot get html because of ', err.args)
				pass
			try:
				soup = get_soup(response)
			except Exception as err:
				print('cannot do soup because of ', err.args)
				soup = ''
				pass
			try:
				header = soup.find('head').find('title').text.strip()
			except Exception as err:
				print('cannot do header because of ', err.args , 'in', url_full)
				header = '-'
				pass			
			try:
				for each_link in soup.find_all('a'):
					link = each_link.get('href')
					full_link = link_repair(link, url)
#					print('full link: ',full_link)
					try:
						emails = func_timeout(3, get_emails, args=(soup,))#response
						if len(emails) == 0:
							emails = '-'
					except FunctionTimedOut:
						print ( 'function could not complete within 3 seconds and was terminated.\n')	
					except Exception as err:
						print('cannot extract emails because of ', err.args)
						emails = '-'
						pass
					mail = 1
					for email in emails:
						print ('site:', full_link, 'e-mail:', mail, email)
						mail += 1
						now = datetime.now()
						current_time = now. strftime("%d/%m/%Y - %H:%M:%S")
						data = {
							'url': full_link,
							'email': email,
							'header': header,
							'time_of_completion':current_time,
							'file': file,
							}
						print('writting csv')
						write_csv(data, today)
			except Exception as err:
				print('cannot last action because of ', err.args)
				header = '-'
				pass
		except:
			pass

def operate(file):
	print('start')
	df = pd.read_csv(file, delimiter = ';', encoding = 'cp1251')
	urls = df.iloc[ : , 5].values.tolist()
	more_urls(urls, file)

def main():
	path = os.path.abspath(os.getcwd())
	print('path:', path)
	folder = os.fsencode(path)
	filenames = []

	for file in os.listdir(folder):
		filename = os.fsdecode(file)
		if filename.startswith( ('final') ) and filename.endswith('csv'): # whatever file types you're using...
			filenames.append(filename)

	for each_file in filenames:
		print('processing:', each_file)
		urls = operate(each_file)
		for url in urls:
			start('Processing url:', url)
			operate(url)
		os.remove(each_file)
		print('done:', each_file)

if __name__ == '__main__':
	main()
