########################
# --- Made by Dami --- #
#   My first project   #
########################

from concurrent.futures import ThreadPoolExecutor
import datetime
import requests
import time
import sys
import os

print(r"""
 __      __      ___.     _________                     
/  \    /  \ ____\_ |__  /   _____/ ____ _____    ____  
\   \/\/   // __ \| __ \ \_____  \_/ ___\\__  \  /    \ 
 \        /\  ___/| \_\ \/        \  \___ / __ \|   |  \
  \__/\  /  \___  >___  /_______  /\___  >____  /___|  /
       \/       \/    \/        \/     \/     \/     \/ 
      """)

print("[!] WebScan - A simple web enumeration tool | Made by Dami\n")

# --- User inputs --- #
url = input("[?] Enter target URL: ")
wordlist = input("[?] Enter the path to your wordlist: ")


date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # date and time for output file naming
if not os.path.exists("scans"):
    os.makedirs("scans")
    print("[+] Created 'scans' directory.")


# -- URL formatting --- #
def format_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = 'http://' + url
    if url.endswith('/'):
        url = url[:-1]
    return url
formatted_url = format_url(url)

# --- Read the wordlist file --- #
try:
    with open(wordlist, "r", encoding="utf-8") as file:
        words = file.read().splitlines()
        total_words = len(words)
        print(f"[+] Loaded {total_words} words from the wordlist.")
except FileNotFoundError:
    print("[-] Wordlist file not found.")
    sys.exit()

# --- Bait scan --- #
def bait_scan():
    bait_url = f"{formatted_url}/idkwhattowriteherebruh"
    response = requests.get(bait_url)
    print(f"[+] Bait scan completed. Content length: {len(response.content)}")
    return len(response.content)
bait_score = bait_scan()

# --- Scoring algorithm --- #
def score_scan(length):
    if length <= bait_score:
        return "LOW"
    elif length <= bait_score * 1.5:
        return "MEDIUM"
    else:
        return "HIGH"

# --- Url enumeration --- #
def scan_word(word):
    scan_url = f"{formatted_url}/{word}"
    response = requests.get(scan_url)
    length = len(response.content)
    score = score_scan(length)
    print(f"[+] Scanning: {scan_url} | Status Code: {response.status_code} | Content Length: {length} | Score: {score}")

with ThreadPoolExecutor() as executor:
    executor.map(scan_word, words)

