import sqlite3
import requests
from bs4 import BeautifulSoup
from newsplease import NewsPlease

# SQLite Database setup
conn = sqlite3.connect('news.db')
c = conn.cursor()

# Create a table to store articles if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        published_date TEXT,
        authors TEXT,
        content TEXT,
        summary TEXT,
        image_url TEXT,
        source TEXT
    )
''')
conn.commit()

# Function to scrape and store articles
def scrape_and_store(url, source):
    try:
        article = NewsPlease.from_url(url)
        title = article.title
        published_date = article.date_publish
        authors = ", ".join(article.authors) if article.authors else "Unknown"
        content = article.maintext
        image_url = article.image_url if article.image_url else "No image"

        # Insert article into the database with the source (leave summary blank for now)
        c.execute('''
            INSERT INTO articles (title, url, published_date, authors, content, summary, image_url, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, url, str(published_date), authors, content, None, image_url, source))
        conn.commit()

        print(f"Scraped and stored article: {title} from {source}")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Function to get article URLs from a given website homepage
def get_article_urls(website_url):
    response = requests.get(website_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article links (for example, <a> tags with href attributes)
    article_links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'article' in href and href.startswith(website_url):
            article_links.add(href)
        if len(article_links) >= 50:
            break

    return list(article_links)

# Read URLs and sources from the urls.txt file
def read_urls_from_file():
    url_source_pairs = []
    with open('urls.txt', 'r') as file:
        for line in file:
            url, source = line.strip().split(',')
            url_source_pairs.append((url, source))
    return url_source_pairs

# Get URLs from the file and scrape articles
url_source_pairs = read_urls_from_file()

for website_url, source in url_source_pairs:
    article_urls = get_article_urls(website_url)
    for url in article_urls:
        scrape_and_store(url, source)

# Close the connection
conn.close()

print("Scraping complete and data stored in the SQLite database.")
