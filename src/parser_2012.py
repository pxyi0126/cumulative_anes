#html parser for 2012
import pandas as pd
from bs4 import BeautifulSoup
import cloudscraper

url = "https://electionstudies.org/2012-time-series-study-release-variables/"

scraper = cloudscraper.create_scraper()
html = scraper.get(url).text
soup = BeautifulSoup(html, "html.parser")

rows = []
container = soup.find("table")
# print(container.prettify()[:3000])
for trs in container.find_all("tr"):
    tds = trs.find_all("td")
    if len(tds) == 1 and tds[0].get("colspan") == "2":
        continue
    if len(tds) == 2:
        varname = tds[0].get_text(" ", strip=True)
        summary = tds[1].get_text(" ", strip=True)

        if varname and summary:
            rows.append({"varname": varname, "summary": summary})

df = pd.DataFrame(rows)
# print(df.head(10))
df.to_csv("2012_vars.csv", index=False)
print(f"Extracted {len(df)} variables")

