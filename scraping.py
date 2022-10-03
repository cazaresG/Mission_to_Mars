# Dependencies
#from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager #-----
from splinter import Browser #---
import pandas as pd
import datetime as dt

def scrape_all():
# Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()} #------
    browser = Browser('chrome', **executable_path, headless=True)#--------
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemisphere_image(browser)
    }
     # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
        # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
            # Convert html into a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
            # Add try/except for error handling---------------------------------------------------update
    try:
        slide_elem = news_soup.select_one('div.list_text')
            # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
            # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None
    return news_title, news_p  #-------------------------------------------------------update


def featured_image(browser):#-----------------------------------------------------update
     #Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:  #----------------------------------------------------------------------------update
       # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
#img_url

    return img_url  #----------------------------------------------------------------update


def mars_facts():#-----------------------------------------------------------------update
    
# ## Mars Facts:
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere_image(browser):
    #Visit URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2 create an empty list to hold the .jpg image URL string and title for each hemisphere image.
    hemisphere_image_urls = []

    # 3. write code to retrieve the full-resolution image URL and title for each hemisphere image. 
         #The full-resolution image will have the .jpg extension.
    hemisphere_image_html = browser.html
    # Convert html into a soup object
    hemisphere_image_soup = soup(hemisphere_image_html,'html.parser')

    # Scrape href tags
    hemisphere_image_href = hemisphere_image_soup.find_all('a', class_='itemLink product-item')
    # Scrape html relative address, concatenate with site url
    hemisphere_image_href = [url + entry['href'] for entry in hemisphere_image_href if entry['href'].find('.html')] 


    for image_urls in hemisphere_image_urls:
        browser.visit(image_urls)
        image_url_html = browser.html
        
        # Convert into soup objects
        image_url_soup = soup(url_html,'html.parser')
        image_url_href = url_soup.select('li > a')
        image_url = url + url_image_href[0]['href']
        # Identify and return title 
        url_title = url_soup.find('h3').text    
        
        
        # Create a holding dictionary 
        hemisphere_dict = {
            'img_url' : image_url,
            'title' : url_title
        }
        hemisphere_image_urls.append(hemispheres)
        
        
        browser.goBack()
        # Return the dictionary 
    return hemisphere_image_urls

        # 5. Quit the browser
#browser.quit()