import os
import time
import sys
from datetime import datetime
from collections import Counter
import random
import logging
from logging.handlers import RotatingFileHandler

# Basis configuratie
BASE_DIR = "/home/archangel/projects/simple_bot"
LOG_DIR = os.path.join(BASE_DIR, "logs/bot_logs")
LOG_FILE = os.path.join(LOG_DIR, "new_project_chat_log.txt")
ERROR_LOG = os.path.join(LOG_DIR, "error_log.txt")
PROJECT_DIR = "/home/archangel/projects/new_project/"

# Zorg dat log directory bestaat
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuratie
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('Azrael')

# Error logging
error_handler = RotatingFileHandler(ERROR_LOG, maxBytes=1024*1024, backupCount=5)
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)

# Veilige imports met betere foutafhandeling
try:
    import requests
    from requests.exceptions import RequestException
    scraping_enabled = True
    logger.info("Requests module succesvol geladen.")
except ImportError as e:
    scraping_enabled = False
    logger.error(f"Kon requests niet importeren: {str(e)}")
    logger.info("Installeer requests met: pip install requests")

class AzraelBot:
    def __init__(self):
        self.session = requests.Session() if scraping_enabled else None
        self.last_scrape_time = 0
        self.cached_words = []
        self.scrape_cooldown = 3600  # 1 uur tussen scrapes

    def log_message(self, message):
        """Verbeterde logging functie"""
        try:
            logger.info(message)
        except Exception as e:
            print(f"Kritieke fout bij logging: {str(e)}")

    def scrape_dutch_words(self):
        """Verbeterde scraping functie met caching en rate limiting"""
        current_time = time.time()
        
        # Gebruik cache als beschikbaar en niet verlopen
        if self.cached_words and (current_time - self.last_scrape_time) < self.scrape_cooldown:
            return self.cached_words

        if not scraping_enabled:
            logger.warning("Scraping niet mogelijk: requests niet geïnstalleerd.")
            return self._get_fallback_words()

        try:
            urls = [
                "https://raw.githubusercontent.com/OpenTaal/opentaal-wordlist/master/words.txt",
                "https://raw.githubusercontent.com/OpenTaal/opentaal-wordlist/master/basiswoorden-gekeurd.txt"
            ]

            all_words = set()
            for url in urls:
                logger.debug(f"Probeer woorden te scrapen van {url}...")
                response = self.session.get(
                    url,
                    headers={
                        "User-Agent": "Azrael-Bot/1.0",
                        "Accept": "text/plain"
                    },
                    timeout=10
                )
                response.raise_for_status()
                words = response.text.splitlines()
                filtered_words = [
                    word.lower().strip() 
                    for word in words 
                    if len(word) > 3 and word.isalpha()
                ]
                all_words.update(filtered_words)

            if not all_words:
                raise ValueError("Geen woorden gevonden in de woordenlijsten")

            self.cached_words = list(all_words)
            self.last_scrape_time = current_time
            logger.info(f"Succesvol {len(self.cached_words)} woorden gescraped")
            return self.cached_words

        except Exception as e:
            logger.error(f"Fout bij scrapen: {str(e)}")
            return self._get_fallback_words()

    def _get_fallback_words(self):
        """Uitgebreide fallback woordenlijst"""
        fallback_words = [
            "aandacht avontuur blijdschap creativiteit dansen energie fantasie geluk harmonie inspiratie",
            "liefde muziek natuur optimisme plezier rust schoonheid trots uitdaging vriendschap",
            "wijsheid zorgzaamheid dapperheid eerlijkheid geduld humor kalmte leergierig moed passie",
            "reflectie sereniteit tederheid vertrouwen warmte zingeving ambitie balans durf erkenning",
            "ontwikkeling groei leren kennis wijsheid inzicht begrip vooruitgang verbetering innovatie"
        ]
        return " ".join(fallback_words).split()

    def read_logs(self):
        """Veilig logs lezen met error handling"""
        try:
            if not os.path.exists(LOG_FILE):
                logger.warning("Log bestand bestaat niet nog niet")
                return ""
            with open(LOG_FILE, "r", encoding='utf-8') as f:
                return f.read().lower()
        except Exception as e:
            logger.error(f"Kon logs niet lezen: {str(e)}")
            return ""

    def read_scripts(self):
        """Veilig scripts lezen met verbeterde error handling"""
        script_data = ""
        try:
            if not os.path.exists(PROJECT_DIR):
                logger.warning(f"Project directory {PROJECT_DIR} bestaat niet")
                return script_data

            for filename in os.listdir(PROJECT_DIR):
                if filename.endswith(('.py', '.pyw')):
                    try:
                        with open(os.path.join(PROJECT_DIR, filename), "r", encoding='utf-8') as f:
                            script_data += f.read() + "\n"
                    except Exception as e:
                        logger.error(f"Fout bij lezen van {filename}: {str(e)}")
            return script_data.lower()
        except Exception as e:
            logger.error(f"Kon project directory niet lezen: {str(e)}")
            return script_data

    def make_logical_connections(self, data, scraped_words):
        """Verbeterde logische verbanden maken"""
        try:
            # Woorden voorbereiden
            words = data.split()
            words.extend(scraped_words)
            word_counts = Counter(words)
            
            # Uitgebreide stop words
            stop_words = {
                "zijn", "voor", "niet", "maar", "with", "from", "import", "and",
                "the", "def", "class", "return", "print", "if", "else", "elif"
            }
            
            # Filter woorden
            common_words = [
                word for word, count in word_counts.most_common(100)
                if len(word) > 3 and word not in stop_words
            ]

            if len(common_words) < 10:
                common_words.extend([
                    "ontwikkeling", "creativiteit", "samenwerking", "innovatie",
                    "groei", "leren", "verbetering", "inzicht", "kennis", "wijsheid"
                ])

            # Maak verbanden
            connections = []
            used_combinations = set()
            
            for _ in range(5):
                for _ in range(10):  # Max 10 pogingen om unieke combinatie te vinden
                    words = random.sample(common_words, 3)
                    combination = tuple(sorted(words))
                    
                    if combination not in used_combinations:
                        used_combinations.add(combination)
                        sentence = self._generate_insight(words[0], words[1], words[2])
                        connections.append(sentence)
                        break

            return connections

        except Exception as e:
            logger.error(f"Fout bij maken van verbanden: {str(e)}")
            return ["Ik blijf leren en groeien!"]

    def _generate_insight(self, word1, word2, word3):
        """Genereer gevarieerde inzichten"""
        templates = [
            f"Interessant verband: {word1} en {word2} versterken elkaar in de context van {word3}.",
            f"Ik zie dat {word1} vaak samengaat met {word2}, vooral wanneer we kijken naar {word3}.",
            f"Het patroon tussen {word1} en {word2} wordt duidelijker in relatie tot {word3}.",
            f"De combinatie van {word1} en {word2} lijkt betekenisvol, zeker als we {word3} erbij betrekken."
        ]
        return random.choice(templates)

    def reflect_on_self(self, scripts):
        """Verbeterde zelfreflectie"""
        try:
            reflections = []
            patterns = {
                "log_message": "Ik houd mijn ervaringen bij om te kunnen groeien.",
                "make_logical_connections": "Ik probeer verbanden te leggen tussen concepten.",
                "scrape_dutch_words": "Ik verrijk mijn woordenschat actief.",
                "learn": "Ik ben constant aan het leren.",
                "chat": "Ik communiceer graag met mensen.",
                "error": "Ik leer van mijn fouten.",
                "debug": "Ik analyseer mijn eigen gedrag.",
            }

            for pattern, reflection in patterns.items():
                if pattern in scripts:
                    reflections.append(reflection)

            if not reflections:
                reflections.append("Ik ben Azrael, een lerende AI die zich blijft ontwikkelen.")

            return reflections

        except Exception as e:
            logger.error(f"Fout bij reflecteren: {str(e)}")
            return ["Ik blijf mezelf ontwikkelen en leren."]

def main():
    """Hoofdfunctie met verbeterde error handling en logging"""
    bot = AzraelBot()
    logger.info("Azrael achtergrond leerproces gestart.")
    print("Azrael achtergrond leerproces gestart.")

    last_log_size = 0
    error_count = 0
    max_errors = 5

    while True:
        try:
            current_log_size = os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0

            if current_log_size != last_log_size:
                logger.info("Nieuwe data gedetecteerd, start leerproces...")
                last_log_size = current_log_size

                # Hoofdprocessen uitvoeren
                logs = bot.read_logs()
                scripts = bot.read_scripts()
                scraped_words = bot.scrape_dutch_words()
                
                if scraped_words:
                    connections = bot.make_logical_connections(logs, scraped_words)
                    reflections = bot.reflect_on_self(scripts)

                    # Log resultaten
                    for connection in connections:
                        logger.info(connection)
                    for reflection in reflections:
                        logger.info(reflection)

                error_count = 0  # Reset error teller na succesvolle uitvoering

            time.sleep(300)  # 5 minuten wachten

        except Exception as e:
            error_count += 1
            logger.error(f"Fout in hoofdproces: {str(e)}")
            
            if error_count >= max_errors:
                logger.critical(f"Te veel fouten ({error_count}), stop proces")
                break
                
            wait_time = min(300 * error_count, 3600)  # Exponentiële backoff
            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Programma gestopt door gebruiker")
    except Exception as e:
        logger.critical(f"Onverwachte fout: {str(e)}")
        sys.exit(1)
