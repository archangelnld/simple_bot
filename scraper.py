import requests
from bs4 import BeautifulSoup
import os
import time

# Instellen van de URL die gescraped moet worden
URL = "https://example.com"  # Vervang dit met jouw doelwebsite

# Opslagmap voor logs
log_file = os.path.expanduser("~/projects/simple_bot/logs/scraping_log.txt")

def scrape_page():
    """Scrape de webpagina en sla de resultaten op."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Foutafhandeling bij slechte response

        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find("div", class_="target-data")  # Pas dit aan naar jouw doeldata

        if data:
            save_to_log(data.get_text().strip())
        else:
            print("Geen nieuwe data gevonden.")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Fout bij het scrapen: {e}")

def save_to_log(content):
    """Sla gescrapete data op als er nieuwe informatie is."""
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = f.read()
    else:
        logs = ""

    if content not in logs:  # Voorkomen van dubbele entries
        with open(log_file, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {content}\n")
        print("✅ Nieuwe data toegevoegd aan log!")
    else:
        print("⚡ Data al aanwezig, geen actie nodig.")

def start_scraping():
    """Start de scraper en check elke 5 minuten op updates."""
    print("🚀 Scraper gestart! Elke 5 minuten controleren...")
    while True:
        scrape_page()
        time.sleep(300)  # Wacht 5 minuten

if __name__ == "__main__":
    user_input = input("Wil je de scraper starten? (ja/nee): ").strip().lower()
    if user_input == "ja":
        start_scraping()
    else:
        print("❌ Scraper niet gestart.")

