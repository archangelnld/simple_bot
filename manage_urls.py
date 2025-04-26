import json
import os

# Bestanden en configuratie
URLS_FILE = "/home/archangel/projects/simple_bot/urls.json"
CHAT_LOG = "/home/archangel/projects/simple_bot/logs/bot_logs/chat_log.txt"
TRIGGER_WORDS_FILE = "/home/archangel/projects/simple_bot/trigger_woorden.txt"

def load_urls():
    """Laad de opgeslagen URLs uit het JSON-bestand."""
    return json.load(open(URLS_FILE)) if os.path.exists(URLS_FILE) else []

def save_urls(urls):
    """Sla de bijgewerkte lijst met URLs op in JSON."""
    json.dump(urls, open(URLS_FILE, "w"), indent=2)

def add_url():
    """Voeg een nieuwe URL toe aan de lijst."""
    url = input("Voer een nieuwe URL in: ")
    urls = load_urls()
    if url not in urls:
        urls.append(url)
        save_urls(urls)
        print(f"✅ URL toegevoegd: {url}")
    else:
        print("⚠️ URL bestaat al!")

def remove_url():
    """Verwijder een URL uit de lijst."""
    urls = load_urls()
    if not urls:
        print("⚠️ Geen URLs opgeslagen!")
        return
    
    print("📜 Opgeslagen URLs:")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
    
    try:
        index = int(input("Voer het nummer van de te verwijderen URL in: ")) - 1
        if 0 <= index < len(urls):
            removed = urls.pop(index)
            save_urls(urls)
            print(f"❌ URL verwijderd: {removed}")
        else:
            print("⚠️ Ongeldig nummer!")
    except ValueError:
        print("⚠️ Voer een geldig getal in!")

def list_urls():
    """Geef een overzicht van de opgeslagen URLs."""
    urls = load_urls()
    if urls:
        print("📜 Opgeslagen URLs:")
        for url in urls:
            print(f"- {url}")
    else:
        print("⚠️ Geen opgeslagen URLs!")

def load_trigger_words():
    """Laad de triggerwoorden uit het tekstbestand."""
    if os.path.exists(TRIGGER_WORDS_FILE):
        with open(TRIGGER_WORDS_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def check_chat_log():
    """Controleer de chatlog op een van de triggerwoorden en voer actie uit indien gevonden."""
    trigger_words = load_trigger_words()

    if not os.path.exists(CHAT_LOG):
        print("⚠️ Chatlog bestand niet gevonden!")
        return

    with open(CHAT_LOG, "r") as f:
        logs = f.readlines()

    for line in logs:
        for word in trigger_words:
            if word in line:
                print(f"🔹 Triggerwoord '{word}' gevonden! Regel: {line.strip()}")
                list_urls()
                return

# Interactief menu
while True:
    print("\n=== URL Beheer Menu ===")
    print("1. Toon opgeslagen URLs")
    print("2. Voeg een URL toe")
    print("3. Verwijder een URL")
    print("4. Controleer chatlog op triggerwoorden")
    print("5. Terug naar hoofdmenu")
    
    keuze = input("Maak een keuze: ")
    if keuze == "1":
        list_urls()
    elif keuze == "2":
        add_url()
    elif keuze == "3":
        remove_url()
    elif keuze == "4":
        check_chat_log()
    elif keuze == "5":
        break
    else:
        print("⚠️ Ongeldige keuze!")
