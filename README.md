🚀 Web Scraping Project — Scrapy & Playwright

📑 Introduction

Welcome to the Web Scraping Project! This project is a powerful web scraper built using Scrapy and Playwright to extract company and activity data from annuaire-entreprises.data.gouv.fr. The spiders work together to gather department information, follow activity links, and scrape company details efficiently.

📦 Project Structure

hack_spider.py —> The core scraper containing four main spiders:

DepartementsSpider: Collects links for all departments.

DepartementsLinksSpider: Follows department links to gather activity URLs.

ActivitySpider: Scrapes activity names and their associated links.

FournisseurSpider: Extracts company data and saves them to CSV.

departements.txt —> Stores department names and their URLs.

departements_links.txt —> Contains activity links associated with each department.

activity.txt —> Lists activity names and links.

company_links.txt —> Holds company URLs for further scraping.

output.csv —> Final scraped data.

failed_urls.csv —> Tracks URLs that failed during scraping.

📜 How to Use

Clone the repository

git clone <repository_url>
cd <repository_folder>

Create a virtual environment and activate it

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies

pip install -r requirements.txt

Run the spiders

Step 1: Collect department links

scrapy crawl departements

Step 2: Scrape activity links

scrapy crawl departements_links

Step 3: Get activity data

scrapy crawl activity

Step 4: Extract company details

scrapy crawl fournisseur

📊 Output

output.csv — Contains fields like:

Dénomination

SIREN

SIRET du siège social

Activité principale (NAF/APE)

Adresse postale

Date de création

Capital social

Statut

Activité associée

🛡️ Error Handling

Failed URLs are logged into failed_urls.csv.

Automatic retries for failed requests (with randomized delays).

Pagination support for multi-page scraping.

🎯 Features

Concurrency: Manages request limits and delays with Scrapy's built-in settings.

Headless Browsing: Uses Playwright to load dynamic content.

Data Persistence: Saves outputs as CSV files.

Error Recovery: Implements robust retry strategies.

📈 Future Improvements

Add unit tests for data extraction methods.

Implement logging to visualize the scraping progress.

Optimize Playwright settings for better performance.

🤝 Contribution

Feel free to fork this repo, submit issues, and propose pull requests. Let’s build something amazing together! 🌟

🏷️ License

This project is licensed under the MIT License.
