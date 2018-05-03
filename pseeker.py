#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : Spx

from urllib2 import Request, urlopen, URLError, HTTPError , os
from time import sleep

from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Back, Style

import sys
import requests
import psutil
from stem import Signal
from stem.control import Controller
import socks, socket


init(convert=True,autoreset=True)

TOR_FLAG = False
TOR_PROXY_DEFAULT = True

def now():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
def checkL():
	my_file = Path(os.path.dirname(os.path.abspath(__file__)) +  "\\pseek_res.ps3k")
	sys.stdout.write(Fore.GREEN + Style.BRIGHT + '\n[*]')
	sys.stdout.write(" Validating files ...")
	if my_file.is_file():
		sys.stdout.write(Fore.GREEN + Style.BRIGHT + '\n[+]')
		sys.stdout.write(" Loaded 'pseek_res.ps3k' file successfully!")
	else:
		sys.stdout.write(Fore.RED + Style.BRIGHT +  '[-]')
		sys.stdout.write(" Error : 'pseek_res.ps3k' file is missing! \n")
		sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
		sys.exit(1)
	
	
def InM():
	os.system("cls")
	lines = ["\n--[ Ps33ker","--[ Author : Spx"]
	for line in lines:          # for each line of text (or each message)
		for c in line:          # for each character in each line
			sys.stdout.write(c)
			sys.stdout.flush()  # flush the buffer
			sleep(0.05)          # wait a little to make the effect look good.
		print('')  
	checkL()
	

def DisplayLogInfo(log):
	sys.stdout.write(Fore.GREEN + '[%s] [INFO] %s' %( now(),log))
def DisplayBackInfo(log):
	sys.stdout.write(Style.DIM + Style.BRIGHT + Fore.GREEN +"[%s] [INFO] Found access page : '%s'\n" %( now(),log))	
	
def findAdmin():
	global TOR_FLAG, TOR_PROXY_DEFAULT, Pport, Pip
	dirname , exe_file = os.path.split(os.path.abspath(__file__))			
	link = dirname + "\pseek_res.ps3k"
	
	f = open(link,"r");
	
	sys.stdout.write(Fore.BLUE + Style.BRIGHT + '\n\n[?]')
	link =	raw_input (" Enter the website name (www.example.com) : ")
	if link == "":
		sys.stdout.write(Fore.RED + Style.BRIGHT +  '[-]')
		sys.stdout.write(" Error : website link is empty! \n")
		sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
		sys.exit(1)
		
	sys.stdout.write(Fore.BLUE + Style.BRIGHT + '[?]')
	torc =	raw_input (" Using Tor proxy? [Y/n] ")
	if torc == "Y":
		
		for pid in psutil.pids():
			p = psutil.Process(pid)
			if p.name() == "tor.exe":
				TOR_FLAG = True
				break
		if TOR_FLAG == False:
			sys.stdout.write(Fore.RED + Style.BRIGHT +  '[-]')
			sys.stdout.write(" Error : Tor is not running, be sure to start it before running pseeker! \n")
			sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
			sys.exit(1)
		else:
			sys.stdout.write(Fore.BLUE + Style.BRIGHT + '[?]')
			torcd =	raw_input (" Using default Tor proxy settings (127.0.0.1:9150) ? [Y/n] ")
			if torcd == "Y":
				pass
			else:
				TOR_PROXY_DEFAULT = False
				sys.stdout.write(Fore.BLUE + Style.BRIGHT + '[?]')
				torcip = raw_input (" Enter your proxy ip : ")
				if torcip == "":
					sys.stdout.write(Fore.RED + Style.BRIGHT +  '[-]')
					sys.stdout.write(" Error : Tor proxy ip is empty! \n")
					sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
					sys.exit(1)
				else:
					Pip = torcip
				sys.stdout.write(Fore.BLUE + Style.BRIGHT + '[?]')
				torcport =	raw_input (" Enter your proxy port : ")
				if torcport == "":
					sys.stdout.write(Fore.RED + Style.BRIGHT +  '[-]')
					sys.stdout.write(" Error : Tor proxy port is empty! \n")
					sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
					sys.exit(1)
				else:
					Pport = int(torcport)
			sys.stdout.write("\n" + Fore.YELLOW + "[" + now() + '] [WARNING] Using pseeker through Tor could take more time to perform the requests.')
	
		
	sys.stdout.write( '\n\n[*] start seeking at %s\n\n' % now())
		
	
	VALID = []
	REQ_FAIL_FLAG = False
	REW_PING = False
	
	while True:
		
		try:
			sub_link = f.readline()
			
			if REW_PING == True:
				if not sub_link:
					break
				if link.startswith("http://"):
					req_link = link+"/"+sub_link
				else:
					req_link = "http://"+link+"/"+sub_link
			else:
				req_link = link
				
			if TOR_FLAG == True:
				try:
					if TOR_PROXY_DEFAULT == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, '127.0.0.1', 9150, True)
					else:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, Pip , Pport, True)
					socket.socket = socks.socksocket
					req = Request(req_link)
					
					# Ping website before proceeding
					if REW_PING == False:
						sys.stdout.write(Fore.GREEN + "[%s] [INFO] Pinging website to make sure it's online\n" % now())
						REW_PING = True
						response = urlopen(req).getcode()
						if response == 200:
							sys.stdout.write(Fore.GREEN + "[%s] [INFO] Website online and ready\n" % now())
							continue
						else:
							sys.stdout.write("\n" + Fore.RED + Style.BRIGHT +  '[-]')
							sys.stdout.write(" Error : The website is offline! \n")
							sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
							sys.exit(1)
					
					DisplayLogInfo("Trying /%s" % sub_link)
					import time
					start = time.clock()
					response = urlopen(req)
					request_time = time.clock() - start

					if request_time >= 30: # For tor request , the time it's bigger
						sys.stdout.write(Fore.YELLOW + "[" + now() + "] [WARNING] Possibile lag detected in the connection ( latency {0:.0f}ms)\n".format(request_time))

						
				except HTTPError as e:
					continue
				except URLError as e:
					continue
				
			
				else:
					DisplayBackInfo(req_link.rstrip())
					VALID.append(req_link)

			else:							
				req = Request(req_link)
				
				if REW_PING == False:
						sys.stdout.write(Fore.GREEN + "[%s] [INFO] Pinging website to make sure it's online\n" % now())
						REW_PING = True
						response = urlopen(req).getcode()
						if response == 200:
							sys.stdout.write(Fore.GREEN + "[%s] [INFO] Website online and ready\n" % now())
							continue
						else:
							sys.stdout.write("\n" + Fore.RED + Style.BRIGHT +  '[-]')
							sys.stdout.write(" Error : The website is offline! \n")
							sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
							sys.exit(1)
				try:
					DisplayLogInfo("Trying /%s" % sub_link)
					import time
					start = time.clock()
					response = urlopen(req)
					request_time = time.clock() - start

					if request_time >= 15:
						sys.stdout.write(Fore.YELLOW + "[" + now() + "] [WARNING] Possibile lag detected in the connection ( latency {0:.0f}ms)\n".format(request_time))

				except HTTPError as e:
					continue
				except URLError as e:
					continue
				else:
					DisplayBackInfo(req_link.rstrip())
					VALID.append(req_link)
		except KeyboardInterrupt:
			sys.stdout.write("\n" + Fore.RED + Style.BRIGHT +  '[-]')
			sys.stdout.write(" Error : User interrupted operation! \n")
			sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
			sys.exit(1)
		
	print "\n"
	sys.stdout.write("Access pages found [%s]:\n" % len(VALID))
	for validated in VALID:
		sys.stdout.write(Fore.GREEN + Style.BRIGHT + '[*]')
		sys.stdout.write(" %s" % validated)
	sys.stdout.write('\n\n[*] shutting down at %s\n\n' % now())
InM()
findAdmin()
