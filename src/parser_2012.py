#JSON parser for 2012
import pandas as pd
import requests

url = "https://electionstudies.org/2012-time-series-study-release-variables/"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}
response = requests.get(url, headers=headers)
data = response.json()
df = pd.json_normalize(data)
df2012 = df[['title', 'field_variable_name', 'field_question_text']]
df2012.columns = ['index', 'variable', 'question']
df2012.to_csv("parsed_2012.csv", index=False)
