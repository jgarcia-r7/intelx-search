#!/usr/bin/env python3
# IntelX Search Tool for Emails
# Usage: ./intelx-search.py -d <domain.com> -l <max-results> -o <output-file>

import requests
import sys
import os
import socks
import socket
import argparse
import time
from colorama import Fore, Style


# Define colorama colors.
GREEN = Fore.GREEN
RED = Fore.RED
WHITE = Fore.WHITE
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
PINK = Fore.MAGENTA
BRIGHT = Style.BRIGHT
DIM = Style.DIM
NORM = Style.NORMAL
RST = Style.RESET_ALL


# Error if no arguments and print example.
if len(sys.argv) <= 1:
    print(f'{RED}{BRIGHT}IntelX Search{RST}: Query the Public IntelX database for email addresses.{RST}\n')
    print(f'{RED}{BRIGHT}Error{DIM}: -d (--domain) REQUIRED{RST}')
    print(f'{PINK}{BRIGHT}Example:{RED} intelx-search.py{NORM}{WHITE} -d domain.com -o domain.com_emails.txt{RST}\n')
    print(f'{DIM}-h (--help) to see full usage and arguments.{RST}')
    print('\n')
    exit(1)


# Define parser and arguments.
parser = argparse.ArgumentParser(description=f'{RED}{BRIGHT}IntelX Search{RST}: Query the Public IntelX database for email addresses.{RST}')

parser.add_argument('-d', '--domain', help=f'Target domain {RED}{BRIGHT}REQUIRED{RST}', default=None, required=True)
parser.add_argument('-l', '--limit', help=f'Results limit {DIM}OPTIONAL (Defualt: 10000){RST}', type=int, default=10000, required=None)
parser.add_argument('-o', '--output', help=f'Output file name {DIM}OPTIONAL (Defualt: emails.txt){RST}', default='emails.txt', required=False)
parser.add_argument('-s', '--socks', help=f'Proxy requests through SOCKS5 proxy {DIM}OPTIONAL (Ex: -s 127.0.0.1){RST}', default=None, required=False)
parser.add_argument('-sp', '--socks_port', help=f'SOCKS5 proxy port {DIM}OPTIONAL (Ex: -sp 1080 | Default: 1080){RST}', default=1080, type=int, required=False)

args = parser.parse_args()


# Set variables.
domain = args.domain
output = args.output
limit = args.limit
socks_ip = args.socks
socks_port = args.socks_port
api_key = os.popen('''curl -s -H "User-Agent: Mozilla/5.0" https://phonebook.cz | grep 'var API_KEY' | awk '{print $4}' | sed "s/'//g" | sed "s/;//g"''').read().replace("\n","") # Lazy way to get latest API key.
api_url = 'public.intelx.io'
headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Origin": "https://phonebook.cz", "Referer": "https://phonebook.cz/", "Content-Type": "application/x-www-form-urlencoded"}


# Socks5 Proxy Settings
if socks_ip:
    socks.set_default_proxy(socks.SOCKS5, socks_ip, socks_port)
    socket.socket = socks.socksocket



# Display query info.
print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}API Key Retrieved: {DIM}{api_key}{RST}')
print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Querying: {DIM}public.intelx.io{RST}')
print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Domain: {DIM}{domain}{RST}')
print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Results limit: {DIM}{limit}{RST}')
if socks_ip:
    print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}SOCKS5 Proxy Enabled: {DIM}socks5://{socks_ip}:{socks_port}{RST}')
else:
    print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}SOCKS5 Proxy Disabled{RST}')    

time.sleep(2)


# Retrieve search ID from API.
key_payload = {"k":api_key}
data_payload = {"maxresults": limit, "media": 0, "target": 2, "term": domain, "terminate": [None], "timeout": 20}
r_id = requests.post(f'https://{api_url}/phonebook/search', headers=headers, params=key_payload, json=data_payload)
id = r_id.json()["id"]
print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Search ID Retrieved: {BRIGHT}{id}{RST}')

time.sleep(2)


print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Retrieving results from: {DIM}public.intelx.io{RST}')

time.sleep(2)

# Retrieve results using ID and API.
results_payload = {"k":api_key, "id":id, "limit": limit}
r_results = requests.get(f'https://{api_url}/phonebook/search/result', headers=headers, params=results_payload)
storage = r_results.json()


# Write results to file.
w = open(output, 'w+')
for each in storage["selectors"]:
    w.write(each["selectorvalue"])
    w.write("\n")
w.close()


# Count results.
emailSum = 0
with open(output) as emails:
    for email in emails:
        if email.strip():
            emailSum += 1

print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Found {BRIGHT}{emailSum}{NORM} email addresses{RST}')
print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Email addresses saved in {BRIGHT}{output}{RST}')
