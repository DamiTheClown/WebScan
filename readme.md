# WebScan
## A simple web enumeration tool | Made by Dami

WebScan is a simple enumeration tool. It is my first Python project, so it is not perfect. The main idea of the project is to detect fake 404 HTTP statuses. The project creates its own simple scoring system, which it uses to detect fake 404 HTTP responses with a certain degree of accuracy.

## Features
* [+] **Multi-threading:** Fast scanning because of ThreadPoolExecutor.
* [+] **Smart 404 Detection:** Automatic "bait scan" for response length calibration.
* [+] **URL Auto-formatting:** Automatic correction of errors in URL entry.
* [+] **Scoring System:** Evaluation of the interest of findings (LOW/MEDIUM/HIGH).

## Roadmap
* [?] Writing logs into `/scans` folder
* [?] Subdomain enumeration
* [?] Wappalyzer integration
* [?] Custom User-Agent rotation
