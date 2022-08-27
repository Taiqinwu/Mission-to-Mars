#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 10.3.3 Scrape Mars Data: The News


# In[2]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from IPython.display import Image


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
# **executable_path is unpacking the dictionary we've stored the path in – think of it as unpacking a suitcase.
browser = Browser('chrome', **executable_path, headless=False)
# headless=False means that all of the browser's actions will be displayed in a Chrome window so we can see them.


# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


# Parse the HTML
html = browser.html
news_soup = soup(html, 'html.parser')
# Question
slide_elem = news_soup.select_one('div.list_text')


# In[6]:


# Get the tittle
slide_elem.find('div', class_='content_title')


# In[7]:


news_soup.find('div', class_='content_title')


# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# get_text() will remove any of the HTML tags or elements.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


# Use the parent element to find the paragraph text
# Question, how can I find the first one or a specific one, how do I use find_all()
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[10]:


# 10.3.4 Scrape Mars Data: Featured Image


# ### Featured Images

# In[11]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[12]:


# Find and click the full image button
# hit the second 'button'
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[13]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[14]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') # .get('src') pulls the link to the image.
img_url_rel
# this is only partial link


# In[15]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[16]:


# 10.3.5 Scrape Mars Data: Mars Facts
# Using Inspector we know
# The main container is the <table /> tag. Inside the table is <tbody />, which is the body of the table—the headers, columns, and rows.
# <tr /> is the tag for each table row. Within that tag, the table data is stored in <td /> tags. This is where the columns are established.
PATH = "/Users/ziyingpan/Downloads/"
# Image(filename = PATH + "Table image.png", width=1000, height=1000)
Image(url= "https://courses.bootcampspot.com/courses/1873/files/1803035/preview", width=1000, height=1000)


# In[17]:


# Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function.
df = pd.read_html('https://galaxyfacts-mars.com/')[0] #read_html specifically searches for and returns a list of tables found in the HTML
df.columns = ['Description', 'Mars', 'Earth'] # we assign columns to the new DataFrame for additional clarity.
df.set_index('Description', inplace=True) # Set Description as index
# df
df.to_html() # Print in HTML ready code
# Question on [0]


# In[18]:


# browser.quit()


# In[19]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[20]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[21]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[22]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[23]:


slide_elem.find('div', class_='content_title')


# In[24]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[25]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[26]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[27]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[28]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[29]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[30]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[31]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[32]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[33]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[34]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[40]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# First, get a list of all of the hemispheres
links = browser.find_by_css('a.product-item img')

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css('a.product-item img')[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()
hemisphere_image_urls


# In[ ]:


# # 2. Create a list to hold the images and titles.
# hemisphere_image_urls = []
# # 3. Write code to retrieve the image urls and titles for each hemisphere.
# links = mars_soup.find_all('div', class_='item')
# image_title = {}

# for link in links:
#     title = link.find('h3').get_text()
#     image = link.find('img', class_='thumb').get('src')
#     img_url = f'https://marshemispheres.com/{image}'
#     image_title["img_url"] = img_url
#     image_title["title"] = title
#     hemisphere_image_urls.append(image_title)
# hemisphere_image_urls


# In[41]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




