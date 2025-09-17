from bs4 import BeautifulSoup
import pandas as pd
import requests
import cloudscraper

# %%
pre_url = "https://electionstudies.org/wp-content/uploads/2008/03/anes_timeseries_2008_codebook_pre.txt"
post_url = "https://electionstudies.org/wp-content/uploads/2008/03/anes_timeseries_2008_codebook_post.txt"

post = requests.get(post_url).text
pre = requests.get(pre_url).text

pre_soup = BeautifulSoup(pre, "html.parser")
post_soup = BeautifulSoup(post, "html.parser")

url = "https://electionstudies.org/wp-content/uploads/2008/03/anes_timeseries_2008_codebook_pre.txt"
scraper = cloudscraper.create_scraper()
resp = scraper.get(url)

print(resp.status_code)
print(resp.text[:500])

with open("anes_2008_pre_codebook.txt", "w", encoding="utf-8") as f:
    f.write(resp.text)

print("Saved codebook to anes_2008_pre_codebook.txt")

# %%