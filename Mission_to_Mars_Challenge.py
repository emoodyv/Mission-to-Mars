from selenium import webdriver as wd
from bs4 import BeautifulSoup as soup
import pandas as pd

browser = wd.Chrome()

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.implicitly_wait(5)
browser.get(url)

# Convert the browser html to a soup object and then quit the browser
html = browser.page_source
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.get(url)

# Find and click the full image button
browser.find_element_by_link_text('FULL IMAGE').click()

# Find the more info button and click that
more_info_elem = browser.find_element_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]').click()

# Parse the resulting html with soup
html = browser.page_source
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")

# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)

df.to_html()

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.get(url)

# Parse the data
html = browser.page_source
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.get(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemi_names = ['[alt="Cerberus Hemisphere Enhanced thumbnail"]', '[alt="Schiaparelli Hemisphere Enhanced thumbnail"]',
             '[alt="Syrtis Major Hemisphere Enhanced thumbnail"]', '[alt="Valles Marineris Hemisphere Enhanced thumbnail"]']

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(0, len(hemi_names)):
    browser.find_element_by_tag_name(hemi_names[i]).click()
    hemisphere_image_urls.append(browser.find_element_by_link_text('Sample').get_attribute('href'))
    browser.get(url)

# 4. Print the list that holds the dictionary of each image url and title.
for i in range(0, len(hemisphere_image_urls)):
    hemisphere_image_urls[i] = {'img_url': hemisphere_image_urls[i], 'name': hemi_names[i][6:-2]}

# 5. Quit the browser
browser.quit()