from selenium import webdriver as wd
from bs4 import BeautifulSoup as soup
import pandas as pd
from datetime import datetime as dt


def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.implicitly_wait(5)
    browser.get(url)

    html = browser.page_source
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.get(url)

    # Find the more info button and click that
    browser.find_element_by_link_text('FULL IMAGE').click()
    more_info_elem = browser.find_element_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]').click()

    # Parse the resulting html with soup
    html = browser.page_source
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def hemi_img(browser):
    # 1. Use browser to visit the URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.get(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    hemi_names = ['[alt="Cerberus Hemisphere Enhanced thumbnail"]',
                  '[alt="Schiaparelli Hemisphere Enhanced thumbnail"]',
                  '[alt="Syrtis Major Hemisphere Enhanced thumbnail"]',
                  '[alt="Valles Marineris Hemisphere Enhanced thumbnail"]']

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(0, len(hemi_names)):
        browser.find_element_by_tag_name(hemi_names[i]).click()
        hemisphere_image_urls.append(browser.find_element_by_link_text('Sample').get_attribute('href'))
        browser.get(url)

    # 4. Print the list that holds the dictionary of each image url and title.
    for i in range(0, len(hemisphere_image_urls)):
        hemisphere_image_urls[i] = {'img_url': hemisphere_image_urls[i], 'title': hemi_names[i][6:-2]}

    return hemisphere_image_urls


def scrape_all():
    # Initiate headless driver for deployment
    browser = wd.Chrome()

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.now(),
        "hemispheres": hemi_img(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
