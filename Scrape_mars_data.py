#import dependecies 
import time 
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_broswer():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    
    broswer = init_broswer()
    mars_data = {}
    
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    #beaututiful soup to HTML
    html = browser.html
    soup = bs(html,"html.parser")
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_p}")
    
    featured_url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_url_image)

    browser.click_link_by_partial_text("FULL IMAGE")

    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()

    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = f'https://www.jpl.nasa.gov{img_url}'
    print(full_img_url)
    
    #scrape Mars weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    tweets = soup.find('ol', class_='stream-items')
    mars_weather = tweets.find("p", class_="tweet-text").text
    print(mars_weather)

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    mars_html = browser.html
    mars_soup = bs(mars_html, 'html.parser')

    mars_table = mars_soup.find('table', class_='tablepress tablepress-id-mars')
    column1 = mars_table.findAll('td', class_='column-1')
    column2 = mars_table.findAll('td', class_='column-2')

    Categories = []
    Values = []

    for row in column1:
        Category = row.text.strip()
        Categories.append(Category)
    
    for row in columns2:
        Value = row.text.strip()
        Values.append(value)

    mars_facts = pd.DataFrame({"Category":Categories,
                          "Value":Values})

    mars_facts_html = mars_facts.to_html(header=False, index=False)
    print(mars_facts)
    
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
    
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
    
        hemi_img_soup = bs(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        print(hemi_name)
        hemi_dict['title'] = hemi_name.strip()
    
        print(hemi_img_path)
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)
    
mars_data["hemisphere_imgs"] = hemi_dicts
        
browser.quit()
        
return mars_data
