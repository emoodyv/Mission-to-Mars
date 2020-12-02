from selenium import webdriver as wd
from bs4 import BeautifulSoup as soup
import pandas as pd

browser = wd.Chrome()
url = 'https://mars.nasa.gov/news/'
browser.implicitly_wait(5)
browser.get(url)

html = browser.page_source
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.get(url)

# Find the more info button and click that
browser.find_element_by_link_text('FULL IMAGE').click()
more_info_elem = browser.find_element_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]').click()

# Parse the resulting html with soup
html = browser.page_source
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)

df.to_html()

browser.quit()