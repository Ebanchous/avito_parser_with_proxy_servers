import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv
import time



def write_csv(data, today):
#	print('trying to save CSV')
	with open(str('web') +'_' + str(today) + '_' + '.csv', 'a', newline='', encoding='cp1251', errors='replace') as f:
		try:
			writer = csv.writer(f, delimiter =';')
			writer.writerow((
						data['url'],
						data['email'],
						data['header'],
						data['time_of_completion']))
#		except:
#			pass
		except Exception as err:
#			print('cannot do it because of ', err.args)
			pass
#			print(f'Cannot write CSV because of {err.args}')
#		print('saved suceessfully')

print('start')
df = pd.read_csv('web1.csv', delimiter = '\t')
df = df.iloc[ : , 2].values.tolist()
count = 0
today = datetime.now().strftime("%d-%m-%Y")
start_time = datetime.now()
execution_limit = time.time() + 10	
for url in df:
	try:	
		current_time = datetime.now()
		time_difference = (current_time - start_time).total_seconds()
		print('current site is number', count)
		print('the name of ste site is:', url)		
		try:
			speed = '{:.2f}'.format(count / time_difference)
			print('average speed per second = ', speed)
		except Exception as err:
	#		print('cannot do it because of ', err.args)
			pass
		count += 1
		url_full = str('http://www.') + str(url)
	#		print('trying url:', url_full)
		try:
			response = requests.get(url_full, timeout = 1)
			response = response.text
		#except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
		except Exception as err:
			response = ''
	#		print('cannot do it because of ', err.args)
	#		print(f'Attempt failed, because of {err.args}')
			# ignore pages with errors and continue with next url
			pass
		try:
			soup = BeautifulSoup(response, 'lxml')
		except Exception as err:
	#		print('cannot do it because of ', err.args)
			soup = ''
			# ignore pages with errors and continue with next url
			pass
		
		try:
			header = soup.find('head').find('title').text.strip()
		except Exception as err:
	#		print('cannot do it because of ', err.args)
			header = '-'
			# ignore pages with errors and continue with next url
			pass

		try:
			emails = set(re.findall(r'\w+@\w+\.{1}\w+', 
				response, re.I)) # re.I: (ignore case)
		except Exception as err:
	#		print('cannot do it because of ', err.args)
	#		print(f'Attempt failed, because of {err.args}')
			emails = '-'
			pass
		mail = 1
		for email in emails:
			print ('site:', count - 1, 'e-mail:', mail)
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
				}
			print('writting csv')
			write_csv(data, today)

	except Exception as err:
		print('cannot do it because of ', err.args)
		pass
