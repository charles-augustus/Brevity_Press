# News Aggregator & Summarization Platform

This project is a web-based platform that scrapes news from various sources, summarizes the content, and displays it on a simple website. The goal is to provide users with concise and relevant news updates from multiple sources in one place.

## Current Status

### What's Working
- **Web Scraper**: We have implemented a basic web scraper that collects news articles from specified sources.
- **Basic Website**: The scraped news articles are displayed on a simple website, which is currently in a very basic form.
- **Information Printing**: The scraper successfully prints the collected news articles on the website.

## To-Do List

### Immediate Tasks
- **Improve the Website UI**: Enhance the look and feel of the website to make it more user-friendly and visually appealing.
- **Add More News Sources**: Expand the number of news sources from which the scraper collects data.
- **Error Handling**: Implement better error handling to manage cases where scraping fails or sources are unavailable.
- **Automate Scraping**: Set up a scheduler to run the scraper periodically, ensuring the news on the website is always up-to-date.

### AI & Advanced Features
- **News Summarization**: Integrate an AI-based summarization tool (like GPT) to automatically generate summaries of the news articles.
- **Category Sorting**: Organize news articles by categories such as politics, technology, sports, etc.
- **Personalized Feeds**: Allow users to customize their news feed based on their preferences.
- **Notifications**: Implement a system to notify users of breaking news or important updates.
- **Search Functionality**: Add a search bar to allow users to find news articles quickly.
  
## Setup Instructions

### Prerequisites

Before running the application, ensure that Python and pip are installed on your Windows system. If not, follow these steps:

1. **Install Python**:
   - Download the latest version of Python from the [official website](https://www.python.org/downloads/).
   - Run the installer and make sure to check the option "Add Python to PATH" before installing.

2. **Install pip**:
   - pip is usually installed by default with Python. To confirm, open Command Prompt and type:
     ```sh
     pip --version
     ```
   - If pip is not installed, follow [this guide](https://pip.pypa.io/en/stable/installation/) to install it.

### Install Dependencies

Once Python and pip are installed, navigate to the project directory and install the required packages by running:

```sh
pip install -r requirements.txt
```

### Running the application 

To start the application, run the following command in your command prompt:

```sh
python newspaper_feedparser.py
```
