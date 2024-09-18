import pandas as pd
from newspaper import Article
from newspaper import Config
import time

# Set user-agent to prevent being blocked by the website
config = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# List of article URLs from The Economic Times
urls = [
    # Add the list of article URLs you want to scrape from The Economic Times
    'https://economictimes.indiatimes.com/tech/technology/apple-brings-a-major-change-in-ios-17-beta-4/articleshow/102047661.cms',
    'https://economictimes.indiatimes.com/markets/stocks/news/adani-group-stocks-rise-after-rally-in-india-stock-market/articleshow/102046962.cms',
    # Add more URLs here...
]

# Initialize an empty list to store article data
articles_data = []

# Loop through each URL and scrape the content
for url in urls:
    try:
        article = Article(url, config=config)
        article.download()
        article.parse()

        # Get article details
        title = article.title
        published_date = article.publish_date if article.publish_date else 'N/A'
        text = article.text

        # Print the article title for monitoring
        print(f'Scraped: {title}')

        # Append the data to the list
        articles_data.append([title, url, published_date, text])

        # Be nice to the server
        time.sleep(2)  # Wait 2 seconds between requests

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Convert the list into a DataFrame
df = pd.DataFrame(articles_data, columns=['Title', 'URL', 'Published Date', 'Article Text'])

# Save the data to a CSV file
df.to_csv('economic_times_articles.csv', index=False)

print('Scraping completed. Articles saved to economic_times_articles.csv')
