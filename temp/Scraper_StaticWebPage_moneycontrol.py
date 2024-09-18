## This is an Autoscaper which would keep on extracting news on a given page on moneycontrol.com news website
# given a url or a list of urls until the work is finished

# Import required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import timedelta
from requests.adapters import HTTPAdapter

# Create a requests session and mount HTTPAdapter
s = requests.Session()
s.mount('https://', HTTPAdapter(max_retries=2))

# Load news-section urls in a list from text document that contains the list of Moneycontrol section urls
# you want to scrape
urls = [line.rstrip('\n') for line in open('moneycontrol_urls.txt')]

# Using a header agent to imitate a browser request to the server  
headers = {
    'Referer': 'https://www.moneycontrol.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# Empty dictionary to store scraped information on news articles
news_articles = {}
news_count = 0    

# Just a counter to update the file name before saving to the disk
times_saved = 0

# Start the for loop over the list of section urls to scrape all the historical news from those
# sections one-by-one
for url in urls:

    # Page number initialized by 0 before entering the while loop for scraping articles from a single section
    p = 0
    
    # Start while loop to extract text features from the historical articles
    while True:
        
        ## Retry mechanism for network issues
        while True:
            response = None
            try:
                response = s.get(url, headers=headers, timeout=20)
                break
            except requests.exceptions.RequestException as err:
                print(f'Caught {err}... Sleeping for 80 sec and then retrying...')
                time.sleep(80)
                continue        
        
        # Parse the source page to extract html tags and content using Beautiful Soup
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        articles = soup.find_all('li', {'class': 'clearfix'})
        
        # Run for loop on all of the articles found on a given page number of a section to extract text features
        for article in articles:
            try:
                title = article.find('h2').text if article.find('h2') else 'N/A'
                link = article.find('a').get('href') if article.find('a') else 'N/A'
                date = article.find('span').text if article.find('span') else 'N/A'

            except AttributeError:
                title = 'N/A'
                link = 'N/A'
                date = 'N/A'

            # Skip if the link is invalid or 'N/A'
            if link == 'N/A':
                print("Skipping article with missing or invalid URL.")
                continue

            # Used as a count checker and input to the autosave section
            if news_count == 1:
                start_time = time.monotonic()    
            
            # Extract full news text and image by making another server request using the link of the article extracted earlier
            try:
                news_response = s.get(link, headers=headers, timeout=15)
                news_data = news_response.text
                news_soup = BeautifulSoup(news_data, 'html.parser')
                
                # Extract news content if the relevant div exists
                if news_soup.find('div', {'class': 'arti-flow'}):
                    news_text = news_soup.find('div', {'class': 'arti-flow'})

                    # Remove unnecessary tags (script, style)
                    for x in news_text.find_all("script"):
                        x.decompose()
                    for y in news_text.find_all('style'):
                        y.decompose()

                    # Remove extra elements and extract the clean news text
                    try:
                        news_text.find_all('a')[-1].decompose()
                        news = news_text.text
                    except IndexError:
                        news = news_text.text
                else:
                    news = 'N/A'

                # **Correct Image extraction logic targeting the `article_image` class**
                img_div = news_soup.find('div', {'class': 'article_image'})  # Target the div with class 'article_image'
                img_tag = img_div.find('img') if img_div else None
                if img_tag:
                    image_url = img_tag.get('data-src', img_tag.get('src', 'N/A'))  # Try data-src first, fallback to src
                else:
                    image_url = 'N/A'

            except requests.exceptions.RequestException as error:
                news = 'N/A'
                image_url = 'N/A'
                print(f'Caught {error}... Sleeping for 80 sec')
                time.sleep(80)
                        
            # Increase the count by 1 for every news scraped and appending it to the empty dictionary
            news_count += 1
            news_articles[news_count] = [title, date, news, link, image_url]

            # A counter, that prints number of articles scraped in multiples of 1000
            if news_count % 10 == 0:
                print('No. ', news_count)

            # Autosave: Save data to CSV when news_count reaches 40,000
            if news_count == 40:
                times_saved += 1
                print('Total Count', news_count)
                end_time = time.monotonic()
                print(timedelta(seconds=end_time - start_time))

                news_df = pd.DataFrame.from_dict(news_articles, orient='index', columns=['Title', 'Published', 'News', 'Link', 'Image'])
                news_df.to_csv(f'mc_{times_saved}.csv')
                news_articles = {}
                news_count = 0
    
        # Collect the next page url from the bottom of the page
        url_tag = soup.find('a', {'class': 'last'})
        
        # Max number of pages to scrape from a single section on the website restricted to 15,655
        max_pages = 15655
        
        # Exit loop if no further pages are available or maximum pages are reached
        try:
            if "void" in url_tag.get('href'):
                break
            elif url_tag.get('href') and p < max_pages:
                url = 'https://www.moneycontrol.com' + url_tag.get('href')
                print('\n', url, '\n')
                p += 1
            else:
                break
                print('\n\nNext page does not exist\n\n')
        except AttributeError:
            print('\n\nNext page does not exist\n\n')
