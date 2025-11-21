'''
Function to scrape all the previous years on the webpage and save them into txt files
'''
import pandas as pd
from bs4 import BeautifulSoup
import cloudscraper
from urllib.parse import urljoin
import os

OUT_DIR = "/Users/yipho/anes/cumulative_anes/data/raw/txt/prev_years/"
BASE = "https://electionstudies.org/"

def scrape_year(url):
    scraper2 = cloudscraper.create_scraper()
    html2 = scraper2.get(url).text
    soup2 = BeautifulSoup(html2, "html.parser")
    cb_link = soup2.find("h3", string=lambda s: s and "CODEBOOK" in s.upper())
    table = cb_link.find_next("table")
    link = table.select("tr")[1].find_all("td")[1]
    print(link)



scraper = cloudscraper.create_scraper()

html = scraper.get("https://electionstudies.org/data-center/").text

soup = BeautifulSoup(html, "html.parser")

study_links = soup.find('div', class_="et_pb_tab et_pb_tab_0 clearfix et_pb_active_content")
links = study_links.find_all('a')
for link in links:
    href = link.get('href')
    # print(f"Processing {href}")
    full_url = urljoin(BASE, href)
    scrape_year(full_url)




