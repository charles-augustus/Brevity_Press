import sqlite3
from transformers import pipeline

# SQLite Database setup
conn = sqlite3.connect('news.db')
c = conn.cursor()

# Set up a summarization pipeline using the Hugging Face Transformers
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to summarize the content
def summarize_content(content):
    try:
        input_length = len(content.split())
        max_len = min(130, input_length)  # Set max_length to the shorter of 130 or the input length
        if input_length > 50:
            summary = summarizer(content, max_length=max_len, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        else:
            return content  # Short content, return as is
    except Exception as e:
        print(f"Failed to summarize content: {e}")
        return content  # Fallback to full content if summarization fails

# Fetch articles without summaries from the database
c.execute('SELECT id, content FROM articles WHERE summary IS NULL')
articles_to_summarize = c.fetchall()

# Loop through each article and summarize it
for article in articles_to_summarize:
    article_id, content = article
    summary = summarize_content(content)
    
    # Update the article record with the summary
    c.execute('UPDATE articles SET summary = ? WHERE id = ?', (summary, article_id))
    conn.commit()
    print(f"Summarized article ID: {article_id}")

# Close the connection
conn.close()

print("Summarization complete and database updated.")
