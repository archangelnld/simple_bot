#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from azrael_manager.stack_manager import StackManager
import os
from datetime import datetime

def scrape_url(url):
    """Scrape een URL en retourneer de tekstinhoud."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        if not text:
            return False, "No content found on the page"
        return True, text
    except requests.exceptions.RequestException as e:
        return False, f"Failed to scrape URL: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error during scraping: {str(e)}"

def save_scraped_content(content, filename):
    """Sla de gescrapte inhoud op in een lokaal bestand."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"Saved to {filename}"
    except Exception as e:
        return False, f"Failed to save content: {str(e)}"

def main():
    print("\n=== Stack Storage Connection Test ===")
    print("\nTesting stack connection...")
    try:
        stack = StackManager()
    except Exception as e:
        print(f"Failed to initialize StackManager: {str(e)}")
        return

    success, status = stack.check_stack_connection()
    print(f"Connection status: {'Success' if success else 'Failed'}")
    if not success:
        print(f"Error details: {status}")
        return

    print("\nSyncing logs to stack...")
    success, result = stack.sync_logs_to_stack()
    print(f"Log sync: {'Success' if success else 'Failed'}")
    if not success:
        print(f"Error: {result}")

    print("\nSyncing backups to stack...")
    success, result = stack.sync_backups_to_stack()
    print(f"Backup sync: {'Success' if success else 'Failed'}")
    if not success:
        print(f"Error: {result}")

    # Optie 11: URL Scraping
    print("\n=== URL Scraping (Option 11) ===")
    # Tijdelijk een standaard-URL gebruiken om invoer over te slaan
    url = "https://example.com"  # Automatisch ingesteld
    print(f"Scraping URL: {url}")
    success, content = scrape_url(url)
    if not success:
        print(f"Scraping failed: {content}")
        return

    # Maak een bestandsnaam met timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"scraped_content_{timestamp}.txt"
    local_path = os.path.join("backups", filename)

    # Sla de gescrapte inhoud lokaal op
    success, result = save_scraped_content(content, local_path)
    print(result)
    if not success:
        return

    # Upload naar SFTP
    print(f"Uploading {filename} to stack...")
    success, result = stack.sync_backups_to_stack()
    print(f"Upload: {'Success' if success else 'Failed'}")
    if not success:
        print(f"Error: {result}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
