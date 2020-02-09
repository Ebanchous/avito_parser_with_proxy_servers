import re
import requests
from func_timeout import func_timeout, FunctionTimedOut
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv
import time
import os

def write_csv(data, today):
#	print('trying to save CSV')
	with open(str('result') +'_' + str(today) + '_1' + '.csv', 'a', newline='', encoding='cp1251', errors='replace') as f:
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
#	print('emails function', text)
	emails = []
	emails = set(re.findall(r'\w+@\w+\.{1}\w+',
					text, re.I))
	return emails

def get_soup(response):
	soup = BeautifulSoup(response, 'lxml')
	return soup


def operate(file):
	print('start')
	df = pd.read_csv(file, delimiter = '\t')
	df = df.iloc[ : , 2].values.tolist()
	count = 0
	today = datetime.now().strftime("%d-%m-%Y")
	start_time = datetime.now()
	for url in df:
		execution_limit = time.time() + 1
#		while time.time() < execution_limit:
		try:
			current_time = datetime.now()
			time_difference = (current_time - start_time).total_seconds()
#			print('current site is number', count)
#				print('the name of ste site is:', url)
			try:
				speed = '{:.2f}'.format(count / time_difference)
				print('average urls per second = ', speed)
			except Exception as err:
#				print('cannot do it because of ', err.args)
				pass
			count += 1
			url_full = str('http://www.') + str(url)#+ str('7karapuzov.ru')#+ str(url)
#			print('trying url:', url_full)
			try:
#				print('trying')
				response = func_timeout(3, get_html, args=(url_full, ))
#				print('done response')
			except FunctionTimedOut:
				print ( 'function could not complete within 3 seconds and was terminated.\n')
#				print('response', response)
			#except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
			except Exception as err:
				response = ''
				print('cannot do it because of ', err.args)
#				print(f'Attempt failed, because of {err.args}')
				# ignore pages with errors and continue with next url
				pass
			try:
#				print('doing soup')
				soup = func_timeout(3, get_soup, args=(response, ))
#				print('done soup')
			except FunctionTimedOut:
				print ( 'function could not complete within 3 seconds and was terminated.\n')
			except Exception as err:
		#		print('cannot do it because of ', err.args)
				soup = ''
				# ignore pages with errors and continue with next url
				pass
			try:
#				print('trying header')
				header = soup.find('head').find('title').text.strip()
#				print('done header')
			except Exception as err:
		#		print('cannot do it because of ', err.args)
				header = '-'
				# ignore pages with errors and continue with next url
				pass
			try:
#				print('trying emails')
#				emails = func_timeout(1, get_emails, args=(response,))
				emails = '-'
#				print('emails',emails)
				if len(emails) == 0:
					emails = '-'
#				print('done emails', emails)
			except FunctionTimedOut:
				print ( 'function could not complete within 3 seconds and was terminated.\n')	
				# if time.time() > execution_limit:
				# 	stop_event.set()
			except Exception as err:
		#		print('cannot do it because of ', err.args)
		#		print(f'Attempt failed, because of {err.args}')
				emails = '-'
				pass
			mail = 1
			for email in emails:
				print ('site:', count - 1, url_full, 'e-mail:', mail, email)
				mail += 1
		#		print('header:', header)
		#		print('email:', email)
				now = datetime.now()
				current_time = now. strftime("%d/%m/%Y - %H:%M:%S")
				data = {
					'url': url_full,
					'email': email,
					'header': header,
					'time_of_completion':current_time,
					'file': file,
					}
#					print('writting csv')
				write_csv(data, today)

		except Exception as err:
			print('cannot do it because of ', err.args)
			pass

def main():
	path = os.path.abspath(os.getcwd())
	print('path:', path)
	folder = os.fsencode(path)
	filenames = []

	for file in os.listdir(folder):
		filename = os.fsdecode(file)
		if filename.startswith( ('out') ) and filename.endswith('csv'): # whatever file types you're using...
			filenames.append(filename)

	for each_file in filenames:
		print('processing:', each_file)
		operate(each_file)
		os.remove(each_file)
		print('done:', each_file)

if __name__ == '__main__':
	main()
