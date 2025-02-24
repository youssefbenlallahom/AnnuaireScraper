import scrapy
import re
from scrapy_playwright.page import PageMethod
import csv
import asyncio
from typing import Dict, Optional
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
class DepartementsSpider(scrapy.Spider):
    name = "departements"
    start_urls = [
        "https://annuaire-entreprises.data.gouv.fr/departements/index.html"
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Ouvrir un fichier texte en mode écriture
        with open("departements.txt", "w", encoding="utf-8") as file:
            for link in response.css('div.fr-container a'):
                nom = link.css('::text').get()
                lien = response.urljoin(link.attrib['href'])
                # Écrire les données dans le fichier texte
                file.write(f"Nom: {nom}, Lien: {lien}\n")
                
class DepartementsLinksSpider(scrapy.Spider):
    name = "departements_links"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        }
        
        # Ouvrir le fichier texte contenant les départements et leurs liens
        with open("departements.txt", "r", encoding="utf-8") as file:
            departements = file.readlines()

        # Itérer sur les lignes, extraire les noms et liens
        for ligne in departements:
            # Utilisation d'une expression régulière pour extraire le nom et le lien
            match = re.match(r"Nom:\s*(.*?),\s*Lien:\s*(https?://\S+)", ligne.strip())
            if match:
                nom = match.group(1)  # Nom du département
                lien = match.group(2)  # Lien

                # Faire une requête pour chaque département en utilisant le lien
                yield scrapy.Request(lien, headers=headers, callback=self.parse, meta={'nom': nom, 'lien': lien})

    def parse(self, response):
        # Récupérer le nom du département et le lien associé à partir du meta
        nom_departement = response.meta['nom']
        lien_departement = response.meta['lien']

        # Afficher le nom du département et son lien associé
        self.logger.info(f"Nom du Département: {nom_departement}")
        self.logger.info(f"Lien du Département: {lien_departement}")

        # Ouvrir un fichier texte en mode ajout
        with open("departements_links.txt", "a", encoding="utf-8") as file:
            # Extraire le div avec la classe fr-container body-wrapper
            container = response.css('div.fr-container.body-wrapper')

            # Boucle à travers tous les liens dans ce conteneur
            for link in container.css('a'):
                nom = link.css('::text').get()  # Extraire le texte (nom du département)
                href = link.attrib.get('href', '')  # Obtenir l'attribut 'href', vide si non existant
                
                # Vérifier si le texte (nom du département) et l'URL sont valides
                if nom and href:
                    # Assurez-vous que le lien commence par 'http' ou 'https'
                    if href.startswith('http') or href.startswith('https'):
                        lien = href
                    else:
                        # Si le lien est relatif, complétez-le avec l'URL de base
                        lien = response.urljoin(href)

                    # Afficher les liens associés à chaque département
                    self.logger.info(f"Lien trouvé pour {nom_departement}: {lien}")
                    
                    # Écrire les données dans le fichier texte (nom, lien)
                    file.write(f"Nom: {nom_departement}, Lien: {lien}\n")

class ActivitySpider(scrapy.Spider):
    name = "activity"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        }
        
        # Ouvrir le fichier texte contenant les départements et leurs liens
        with open("departements_links.txt", "r", encoding="utf-8") as file:
            departements = file.readlines()

        # Itérer sur les lignes, extraire les noms et liens
        for ligne in departements:
            # Utilisation d'une expression régulière pour extraire le nom et le lien
            match = re.match(r"Nom:\s*(.*?),\s*Lien:\s*(https?://\S+)", ligne.strip())
            if match:
                nom = match.group(1)  # Nom du département
                lien = match.group(2)  # Lien

                # Faire une requête pour chaque département en utilisant le lien
                yield scrapy.Request(lien, headers=headers, callback=self.parse, meta={'nom': nom, 'lien': lien})

    def parse(self, response):
        # Récupérer le nom du département et le lien associé à partir du meta
        nom_departement = response.meta['nom']
        lien_departement = response.meta['lien']

        # Afficher le nom du département et son lien associé
        self.logger.info(f"Nom du Département: {nom_departement}")
        self.logger.info(f"Lien du Département: {lien_departement}")

        # Ouvrir un fichier texte en mode ajout
        with open("activity.txt", "a", encoding="utf-8") as file:
            # Extraire le div avec la classe fr-container body-wrapper
            container = response.css('div.fr-container.body-wrapper')

            # Boucle à travers tous les liens dans ce conteneur
            for link in container.css('a'):
                # Extraire le texte complet de la balise <a>
                texte_complet = link.css('::text').get().strip()
                
                # Utiliser une expression régulière pour extraire uniquement le nom de l'activité
                match_activite = re.match(r"^(.*?)\s*-\s*\d{2}\.\d{2}[A-Z]?$", texte_complet)
                if match_activite:
                    nom_activite = match_activite.group(1).strip()  # Nom de l'activité
                    href = link.attrib.get('href', '')  # Obtenir l'attribut 'href', vide si non existant
                    
                    # Vérifier si le nom de l'activité et l'URL sont valides
                    if nom_activite and href:
                        # Assurez-vous que le lien commence par 'http' ou 'https'
                        if not href.startswith(('http', 'https')):
                            href = response.urljoin(href)  # Compléter le lien relatif

                        # Écrire le lien et le nom de l'activité dans le fichier texte
                        file.write(f"Lien: {href}, Activité: {nom_activite}\n")
                        self.logger.info(f"Lien trouvé pour {nom_departement}: {href}, Activité: {nom_activite}")
import scrapy
import re

class ActivityLinksSpider(scrapy.Spider):
    name = "activity_links"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        }
        
        # Read activity links from file
        with open("activity.txt", "r", encoding="utf-8") as file:
            activities = file.readlines()

        # Process each activity link
        for ligne in activities:
            match = re.match(r"Lien:\s*(https?://\S+),\s*Activité:\s*(.*)", ligne.strip())
            if match:
                lien = match.group(1)  # Activity URL
                activite = match.group(2).strip()  # Activity name
                yield scrapy.Request(lien, headers=headers, callback=self.parse, meta={'activite': activite})

    def parse(self, response):
        # Extract activity name from meta
        activite = response.meta['activite']

        # Extract company links
        company_links = response.css('a[href^="/entreprise/"]::attr(href)').getall()
        for link in company_links:
            full_url = response.urljoin(link)
            # Write to file with activity info
            with open("company_links.txt", "a", encoding="utf-8") as f:
                f.write(f"Lien: {full_url}, Activité: {activite}\n")

        # Handle pagination links
        pagination_links = response.css('div.pagination a::attr(href)').getall()
        for page_link in pagination_links:
            full_page_url = response.urljoin(page_link)
            yield scrapy.Request(full_page_url, callback=self.parse, meta={'activite': activite})      
                    
import scrapy
from scrapy_playwright.page import PageMethod
import csv
import asyncio
from typing import Dict, Optional
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import random
import os
class FournisseurSpider(scrapy.Spider):
    name = "fournisseur"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 2,  # Reduced from 2 to 0.5
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # Add randomization
        'CONCURRENT_REQUESTS': 1,  # Increased from 1 to 3
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 60000,  # Reduced from 60000 to 30000
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'args': [
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-setuid-sandbox',
                '--no-sandbox',
            ],
            'headless': True
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activity_links = self.read_activity_links()
        self.retry_delays = [2, 5, 10]  # Reduced retry delays
        self.start_time = datetime.now()
        self.processed_count = 0
        self.success_count = 0
        self.error_count = 0
    def save_to_csv(self, data: Dict[str, Optional[str]], filename: str = "output.csv"):
        """Save scraped data to a CSV file."""
        file_exists = os.path.isfile(filename)
        
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            
            # Write headers if file doesn't exist
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data)
        self.logger.info(f"Data saved to {filename}")

    def save_failed_url(self, url: str, activity: str, filename: str = "failed_urls.csv"):
        """Save failed URLs to a CSV file."""
        file_exists = os.path.isfile(filename)
        
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Write headers if file doesn't exist
            if not file_exists:
                writer.writerow(["URL", "Activity"])
            
            writer.writerow([url, activity])
        self.logger.info(f"Failed URL saved: {url}")
    def read_activity_links(self) -> Dict[str, str]:
        activity_links = {}
        try:
            with open("company_links.txt", "r", encoding="utf-8") as file:
                for line in file:
                    if "Lien:" in line and "Activité:" in line:
                        link = line.split("Lien: ")[1].split(", Activité: ")[0].strip()
                        activity = line.split(", Activité: ")[1].strip()
                        activity_links[link] = activity
        except Exception as e:
            self.logger.error(f"Error reading company_links.txt: {e}")
            raise
        return activity_links

    def start_requests(self):
        # Randomize the order of URLs to distribute load
        links = list(self.activity_links.items())
        random.shuffle(links)
        
        for link, activity in links:
            # Dynamic wait time between 2-4 seconds instead of fixed 5 seconds
            wait_time = random.uniform(2000, 4000)
            
            yield scrapy.Request(
                link,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "table.styleSimple_two-column-table__KG2Pf", timeout=30000),
                        PageMethod("wait_for_timeout", wait_time),
                    ],
                    "playwright_include_page": True,
                    "activity": activity,
                    "retry_count": 0,
                    "dont_retry": False
                },
                callback=self.parse,
                errback=self.handle_error,
                dont_filter=True,
                priority=random.randint(1, 100)  # Randomize priority
            )

    async def handle_error(self, failure):
        request = failure.request
        retry_count = request.meta.get('retry_count', 0)
        self.error_count += 1
        
        if retry_count < len(self.retry_delays) and not request.meta.get('dont_retry', False):
            retry_count += 1
            delay = self.retry_delays[retry_count - 1]
            
            self.logger.info(f"Retrying {request.url} (attempt {retry_count}) after {delay} seconds")
            await asyncio.sleep(delay)
            
            request.meta['retry_count'] = retry_count
            return request.copy()
        else:
            self.logger.error(f"Failed to process {request.url} after all retries: {failure.value}")
            self.save_failed_url(request.url, request.meta.get('activity', ''))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        activity = response.meta["activity"]
        self.processed_count += 1

        try:
            fields_to_extract = await self.extract_fields(response, activity)
            self.save_to_csv(fields_to_extract)
            self.success_count += 1
            
            # Log progress every 10 items
            if self.processed_count % 10 == 0:
                elapsed_time = (datetime.now() - self.start_time).total_seconds()
                speed = self.processed_count / elapsed_time
                self.logger.info(
                    f"Progress: {self.processed_count} processed, "
                    f"Success rate: {(self.success_count/self.processed_count)*100:.2f}%, "
                    f"Speed: {speed:.2f} items/second"
                )
            
        except Exception as e:
            self.logger.error(f"Error processing {response.url}: {e}")
            self.save_failed_url(response.url, activity)
            self.error_count += 1
            
        finally:
            if page:
                try:
                    await page.close()
                except Exception as e:
                    self.logger.error(f"Error closing page: {e}")

    async def extract_fields(self, response, activity: str) -> Dict[str, Optional[str]]:
        page = response.meta["playwright_page"]
        html = await page.content()
        sel = scrapy.Selector(text=html)
        
        fields_to_extract = {
            "Dénomination": None,
            "SIREN": None,
            "SIRET du siège social": None,
            "Activité principale (NAF/APE)": None,
            "Adresse postale": None,
            "Date de création": None,
            "Capital social": None,
            "Statut": "non active",
            "Activité associée": activity,
        }
        
        # Process each table that might contain data
        tables = sel.css('table.styleSimple_two-column-table__KG2Pf')
        for table in tables:
            rows = table.css('tr')
            for row in rows:
                # Try to extract the key from the dedicated label span if available
                key_text = row.xpath('.//span[contains(@class, "style_label__nkCi_")]/text()').get()
                if not key_text:
                    key_text = ''.join(row.xpath('./td[1]//text()').getall()).strip()
                value_text = ''.join(row.xpath('./td[2]//text()').getall()).strip()
                self.logger.info(f"Extracted key: {key_text}, value: {value_text}")
                
                # Use a case-insensitive substring check to update the field if it matches
                for field in fields_to_extract:
                    if field.lower() in key_text.lower():
                        fields_to_extract[field] = value_text

        # Determine status by looking for text indicating "en activité"
        activity_status = sel.xpath('//*[contains(text(), "en activité")]/text()').get()
        if activity_status and "en activité" in activity_status:
            fields_to_extract["Statut"] = "en activité"

        return fields_to_extract


    def closed(self, reason):
        # Log final statistics
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        self.logger.info(
            f"\nScraping completed!\n"
            f"Total time: {elapsed_time:.2f} seconds\n"
            f"Items processed: {self.processed_count}\n"
            f"Successful: {self.success_count}\n"
            f"Errors: {self.error_count}\n"
            f"Average speed: {self.processed_count/elapsed_time:.2f} items/second"
        )