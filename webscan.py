########################
# --- Made by Dami --- #
#   My first project   #
########################

from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import http.client
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

print("\n")
score = 0.0

# --- Output file setup --- #
date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"/scans/scan_{date}.txt"
if not os.path.exists("/scans"):
    os.mkdir("/scans")
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

scanned_count = 0
progress_lock = Lock()

# --- Bait scan --- #
def bait_scan():
    bait_wordlist = ["x9QvM2Lr8ZpA7DkW4HjC", "H7WkP9rCqLZ8x2A4DVMj", "Z4C8xqH9D7PjAMrWLVk2", "rWZx9M4P2C7DqHkA8VLj", "A8ZqH9r4Wk2P7DVMCLxj"]
    bait_lengths = []
    
    for bait in bait_wordlist:
        try:
            bait_url = f"{formatted_url}/{bait}"
            response = requests.get(bait_url, timeout=5)
            bait_lengths.append(len(response.content))
        except Exception as e:
            print(f"[-] Bait scan error for {bait}: {e}")
    
    unique_lengths = set(bait_lengths)
    if len(unique_lengths) == 1:
        print(f"[+] Server isn't probbably dynamic, using bait length: {bait_lengths[0]}")
        return bait_lengths[0]
    else:
        print(f"[-] Warning: Server might be dynamic ! Detected {len(unique_lengths)} different content lengths.")
        return sum(bait_lengths) / len(bait_lengths)

bait_score = bait_scan()

    
def score_system(length):
    percentage = abs(length - bait_score) / bait_score * 100
    if percentage < 2:
        return "LOW"
    elif percentage < 20:
        return "MEDIUM"
    else:
        return "HIGH"
    

# --- Url enumeration --- #
def scan_word(word):
    global scanned_count
    scan_url = f"{formatted_url}/{word}"
    status_code = "ERR"
    score = "N/A"
    try:
        response = requests.get(scan_url, timeout=5)
        status_code = response.status_code
        length = len(response.content)
        score = score_system(length)
    except requests.RequestException:
        pass
    finally:
        with progress_lock:
            scanned_count += 1
            print(
                f"\r[+] Scanned: {scanned_count}/{total_words} | Word: {word} | Status: {status_code} | Score: {score}",
                end="",
                flush=True,
            )

with ThreadPoolExecutor() as executor:
    executor.map(scan_word, words)

print("\n[+] Scan complete.")

#TODO Ukládání do txt
#TODO Předělání score systému
#TODO Načítání z wordlistu
#TODO Upravit status kody s významama tzv: 200 = OK, 403 = Forbidden, 404 = Not Found, 500 = Server Error