---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Scraping Gab

The purpose of this document is to explore using a web scraper to collect data from Gab, a social networking site.


### Requests:

Gab is a React website, so instead of sending HTML, it sends over Javascript using React to generate and render HTML + CSS in the browser. As a result, I went on the website itself and noticed it was calling an API (https://gab.com/api/v1/), receiving a response, and generating the website based on the response. This approach does not require a parser like BeautifulSoup, though since it isn't really scraping and the Gab API is not documented, this may stop working if the people in charge of Gab change the API pathways.

```python
import requests
import json

url = 'https://gab.com/api/v1/timelines/explore?page=1&sort_by=hot'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
response = requests.get(url, headers=headers)
#Decoding the response into a Python list
posts = json.loads(response.content.decode('utf-8'))
```

```python
posts[0]
```

This approach can pull posts and a whole bunch of additional metadata. It is vulnerable to Gab changing their API though. This is a valid enough approach, though it could be worthwhile having a backup using legitimate web scraping.


### Selenium

Since gab is built with React, using the requests + BeautifulSoup combo is basically out without some kind of requests extension that allows it to run and render Javascript. And nothing I've found (eg requests-html) looks particularly appealing or functional. The usual way of doing this seems to be running Selenium. Selenium is quite slow but I'm not going to be pulling large amounts of data at a time, so it'll probably be fine.

<!-- #raw -->
#This will install the chrome webdriver in a really easy way
!pip install webdriver_manager

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
<!-- #endraw -->

```python
from selenium import webdriver
driver = webdriver.Chrome()
url = 'https://gab.com'
driver.get(url)
```
