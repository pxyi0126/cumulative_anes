'''
Function to scrape all the previous years on the webpage and save them into txt files
'''
import pandas as pd
from bs4 import BeautifulSoup
import cloudscraper
from urllib.parse import urljoin
import os

OUT_DIR = "/Users/yipho/anes/cumulative_anes/data/raw/txt/"
BASE = "https://electionstudies.org/"

def scrape_year(url, OUT_DIR=OUT_DIR):
    scraper2 = cloudscraper.create_scraper()
    html2 = scraper2.get(url).text
    soup2 = BeautifulSoup(html2, "html.parser")
    cb_link = soup2.find("h3", string=lambda s: s and "CODEBOOK" in s.upper())
    table = cb_link.find_next("table")
    checker = table.find("a", string=lambda s: s and "Variables" in s)
    if checker is not None:
        table = cb_link.find_next("table")
        txt = table.select("tr")[1].find_all("td")[2]
        if txt.find("a") is not None:
            link = txt.find("a")["href"]
            filename_split = link.split("/")[-1].split("_")[2:]
            filename = filename_split[0] + "_" + filename_split[-1]
            print(filename)
            full_txt_url = urljoin(BASE, link)
            print(full_txt_url)
            # filename = link.split("/")[-1]
            with open(os.path.join(OUT_DIR, filename), "wb") as f_out:
                resp = scraper2.get(full_txt_url)
                f_out.write(resp.content)


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




