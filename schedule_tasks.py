import schedule
import time
import subprocess

# Function to run the scraping script
def run_scraping():
    print("Running scraping script...")
    subprocess.run(["python3", "scraper.py"]) 

# Function to run the summarizing script
def run_summarizing():
    print("Running summarizing script...")
    subprocess.run(["python3", "summarizer.py"])

# Schedule the scraping and summarizing tasks every 12 hours
schedule.every(12).hours.do(run_scraping)
schedule.every(12).hours.do(run_summarizing)

print("Scheduling started. Scraping and summarizing every 12 hours...")

# Infinite loop to keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(1)
