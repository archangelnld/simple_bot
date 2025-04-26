#!/usr/bin/env python3

##### Imports ####
from datetime import datetime
import subprocess
import json
import os
import time
import threading
import asyncio
import aiohttp
from fuzzywuzzy import fuzz
from collections import Counter
import shutil
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

##### Configuratie en Globale Variabelen ####
app = Flask(__name__)

# Bestanden voor opslag (absoluut pad)
SEARCH_FILE = "/home/archangel/projects/simple_bot/search_list.json"
CHAT_LOG = "/home/archangel/projects/simple_bot/logs/bot_logs/chat_log.txt"
CHAT_URL_FILE = "/home/archangel/projects/simple_bot/logs/scrape_logs/chat_history.txt"
WGET_LOG_DIR = "/home/archangel/projects/simple_bot/logs/wget_logs"
TEST_FILE_PREFIX = "wget_test"
SEARCH_FILE_WGET_PREFIX = "wget_search"
CACHE_FILE = "/home/archangel/projects/simple_bot/logs/cache/cache.json"

# Proxy configuratie
proxies = {
    "http": "http://localhost:3128",
    "https": "http://localhost:3128",
}

# Globale zoeklijst en cache
search_list = {}
last_modified = 0
chat_check_started = False
chat_check_running = True
url_cache = {}
recent_commands = []

# Synoniemen dictionary
synonyms = {
    "hoe laat": ["wat is de tijd", "hoe laat is het"],
    "wie ben je": ["wat ben je", "wie ben jij"],
    "goedemorgen": ["goedemorgen!", "goedemorgend"],
    "goedemiddag": ["goedemiddag!", "goedemiddag"],
    "goedenavond": ["goedenavond!", "goedenavond"],
    "goedennacht": ["goedennacht!", "goedennacht"],
    "wat is je favoriete kleur": ["favoriete kleur", "welke kleur vind je leuk"],
    "vertel een grap": ["grap", "vertel grap", "maak me aan het lachen"],
    "zullen we dansen": ["dans", "dans met me"],
    "test_internet": ["internet test", "check internet"],
    "test_internet_wget": ["test wget", "check wget"],
}

# Laad TransIP STACK SFTP-credentials
with open("/home/archangel/projects/simple_bot/stack_credentials.json", "r") as f:
    creds = json.load(f)

##### HTTP API Endpoint ####


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message', '')
    response = get_response(message)
    return jsonify({"response": response})

##### Zoeklijst Beheer ####


def load_search_list():
    global search_list, last_modified
    default_list = {
        "system timestamp": "Mijn system timestamp is {timestamp}.",
        "hoe laat": "Mijn system timestamp is {timestamp}.",
        "dansplaat": "Dansplaat! *Zet de speakers op 11!* 🎶 Klaar om te strijden!",
        "wie ben je": "Ik ben een mini-AI, gemaakt om te helpen en te leren!",
        "goedemorgen": "Goedemorgen! Hoe kan ik je helpen vandaag?",
        "meta charset": "Dat lijkt op een HTML-tag! Charset bepaalt de tekencodering, zoals UTF-8.",
        "html": "Ik zie dat je iets over HTML vraagt. Wil je meer weten over een specifieke tag?",
        "goedemiddag": "Goedemiddag! Wat wil je weten?",
        "goedenavond": "Goedenavond! Hoe kan ik je helpen?",
        "goedennacht": "Goedenacht! Slaap lekker!",
        "wat is je favoriete kleur": "Mijn favoriete kleur is blauw—lekker rustig!",
        "vertel een grap": "Waarom kunnen geesten geen leugens vertellen? Omdat je dwars door ze heen kijkt!",
        "wat is het weer": "Ik kan het weer niet checken, maar ik stel voor om naar buiten te kijken!",
        "hoe oud ben je": "Ik ben geboren op 20 april 2025, dus ik ben nog piepjong!",
        "wat is liefde": "Liefde is als Wi-Fi—je voelt het pas als het er niet is!",
        "zullen we dansen": "Ja, laten we dansen! *zet een dansplaat op*",
        "test_internet": "Probeer een website te bereiken via proxy...",
        "test_internet_wget": "Probeer een website te bereiken via proxy met wget...",
    }
    if os.path.exists(SEARCH_FILE):
        current_modified = os.path.getmtime(SEARCH_FILE)
        if current_modified != last_modified:
            with open(SEARCH_FILE, "r") as f:
                loaded_list = json.load(f)
            search_list = default_list.copy()
            search_list.update(loaded_list)
            last_modified = current_modified
    else:
        search_list = default_list
        save_search_list()


def save_search_list():
    with open(SEARCH_FILE, "w") as f:
        json.dump(search_list, f, indent=2)

##### Cache Beheer ####


def load_cache():
    global url_cache
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            url_cache = json.load(f)
    else:
        url_cache = {}
    if len(url_cache) > 100:
        oldest = sorted(url_cache.items(),
                        key=lambda x: x[1]["timestamp"])[:50]
        for url, _ in oldest:
            del url_cache[url]
        save_cache()


def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(url_cache, f, indent=2)

##### Chatlog Beheer ####


def save_chat(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(f"Saving log locally: {log_entry}")
    try:
        os.makedirs(os.path.dirname(CHAT_LOG), exist_ok=True)
        with open(CHAT_LOG, "a") as f:
            f.write(log_entry)
        print(f"Wrote to {CHAT_LOG}")
    except Exception as e:
        print(f"Local log error: {e}")
    try:
        temp_file = f"/tmp/log_{timestamp.replace(' ', '_').replace(':', '-')}.txt"
        remote_file = f"{creds['logs_path']}/log_{timestamp.replace(' ', '_').replace(':', '-')}.txt"
        with open(temp_file, "w") as f:
            f.write(log_entry)
        subprocess.run(
            ["sshpass", "-p", creds['sftp_password'], "sftp", "-oStrictHostKeyChecking=no",
                f"{creds['sftp_username']}@{creds['sftp_host']}"],
            input=f"mkdir {creds['logs_path']}\nbye\n",
            text=True,
            shell=False,
            capture_output=True,
            check=True
        )
        result = subprocess.run(
            ["sshpass", "-p", creds['sftp_password'], "sftp", "-oStrictHostKeyChecking=no",
                f"{creds['sftp_username']}@{creds['sftp_host']}"],
            input=f"put {temp_file} {remote_file}\nbye\n",
            text=True,
            shell=False,
            capture_output=True,
            check=True
        )
        print(f"SFTP output: {result.stdout}")
        os.remove(temp_file)
        print("Uploaded to TransIP STACK via SFTP")
    except subprocess.CalledProcessError as e:
        print(
            f"STACK upload error: Command {e.cmd} failed with return code {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")
    except Exception as e:
        print(f"STACK upload error: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    try:
        if os.path.getsize(CHAT_LOG) > 100_000:
            if os.path.exists(CHAT_LOG + ".gz"):
                os.remove(CHAT_LOG + ".gz")
            subprocess.run(["gzip", CHAT_LOG])
            open(CHAT_LOG, "w").close()
    except Exception as e:
        print(f"Log size error: {e}")


def learn_from_chatlog():
    if not os.path.exists(CHAT_LOG):
        print("Geen chatlog gevonden om te leren.")
        return
    try:
        with open(CHAT_LOG, "r") as f:
            lines = f.readlines()
        messages = [line.split("] ")[1].strip() for line in lines if "] " in line and len(
            line.split("] ")) > 1 and line.split("] ")[1].strip()]
        message_counts = Counter(messages)
        for msg, count in message_counts.items():
            if (count >= 3 and msg.lower() not in search_list and
                not msg.lower().startswith(("[", "scrape uit cache:", "scrape duur:", "scrape mislukt:", "zoekopdracht:", "zoekfout:", "update-check:", "internet test:", "wget test:", "cache-status:", "geleerde patronen gereset", "cache gewist", "bot-statistieken:", "beschikbare commando's:")) and
                not msg.lower().startswith("/") and msg.lower() != "/stop" and msg):
                response = f"Je hebt '{msg}' vaak gevraagd! Wat wil je daarover weten?"
                search_list[msg.lower()] = response
                save_search_list()
                print(f"Geleerd: '{msg}' -> '{response}'")
    except Exception as e:
        print(f"Chatlog error: {e}")


def check_chat():
    global chat_check_running
    while chat_check_running:
        with open(CHAT_LOG, "r") as f:
            content = f.read()
        print("Chatlog controleren...\n" + content)
        learn_from_chatlog()
        time.sleep(1800)

##### TransIP STACK Mapstructuur ####


def get_stack_directory_structure():
    try:
        sftp_commands = f"cd {creds['stack_base_path']}\nls\ndir\nbye\n"
        result = subprocess.run(
            ["sshpass", "-p", creds['sftp_password'], "sftp", "-oStrictHostKeyChecking=no",
                f"{creds['sftp_username']}@{creds['sftp_host']}"],
            input=sftp_commands,
            text=True,
            shell=False,
            capture_output=True,
            check=True
        )
        dir_list = result.stdout
        return f"Mapstructuur van {creds['stack_base_path']}:\n{dir_list}"
    except subprocess.CalledProcessError as e:
        return f"Fout bij ophalen mapstructuur: Command {e.cmd} failed with return code {e.returncode}\nOutput: {e.output}\nError: {e.stderr}"
    except Exception as e:
        return f"Fout bij ophalen mapstructuur: {e}"

##### Netwerkverzoeken ####


async def async_get_url(url, retries=3):
    connector = aiohttp.TCPConnector(limit=10, ssl=False)
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, proxy="http://localhost:3128", timeout=10, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                }) as response:
                    response.raise_for_status()
                    return await response.text()
        except Exception as e:
            if attempt == retries - 1:
                raise e
            await asyncio.sleep(1)


async def handle_test_internet():
    try:
        html = await async_get_url("http://example.com")
        save_chat("Internet test: Success (Status: 200)")
        return "Success! Website bereikt: 200"
    except Exception as e:
        save_chat(f"Internet test: Error ({str(e)})")
        return f"Error: {str(e)}"


def handle_test_internet_wget():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        test_file = os.path.join(
            WGET_LOG_DIR, f"{TEST_FILE_PREFIX}_{timestamp}.html")
        log_file = os.path.join(WGET_LOG_DIR, f"wget_log_{timestamp}.txt")
        save_chat(
            f"Wget test: Start (Testbestand: {test_file}, Logbestand: {log_file})")
        os.makedirs(WGET_LOG_DIR, exist_ok=True)
        if not os.access(WGET_LOG_DIR, os.W_OK):
            raise PermissionError(f"Geen schrijfrechten voor {WGET_LOG_DIR}")
        try:
            subprocess.run(["nc", "-z", "localhost", "3128"],
                           timeout=5, check=True)
            save_chat("Wget test: Proxy op localhost:3128 is bereikbaar")
        except subprocess.CalledProcessError:
            raise RuntimeError("Proxy op localhost:3128 is niet bereikbaar")
        env = os.environ.copy()
        env["http_proxy"] = "http://localhost:3128"
        result = subprocess.run(
            ["wget", "--debug", "--output-file", log_file,
                "-O", test_file, "http://example.com"],
            timeout=10,
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        save_chat(
            f"Wget test: Stdout: {result.stdout[:200]}\nStderr: {result.stderr[:200]}")
        if not os.path.exists(test_file):
            raise FileNotFoundError(f"Testbestand {test_file} niet aangemaakt")
        with open(test_file, "r") as f:
            content = f.read()
        save_chat(
            f"Wget test: Success (Bestand: {test_file}, Log: {log_file})")
        return f"Success! Website bereikt: {content[:100]}..."
    except Exception as e:
        error_msg = f"Wget test: Error ({str(e)})\nStdout: {result.stdout[:200] if 'result' in locals() else 'N/A'}\nStderr: {result.stderr[:200] if 'result' in locals() else 'N/A'}"
        save_chat(error_msg)
        return f"Error: {str(e)}"

##### Hoofdlogica (Berichtverwerking) ####


def get_response(message):
    global chat_check_started, chat_check_running, recent_commands
    save_chat(message)
    if not chat_check_started:
        threading.Thread(target=check_chat, daemon=True).start()
        chat_check_started = True

    message_lower = message.lower().strip()
    recent_commands.append(message_lower)
    if len(recent_commands) > 5:
        recent_commands.pop(0)

    load_search_list()
    load_cache()

    if message_lower == "/clear_cache":
        url_cache.clear()
        save_cache()
        return "Cache gewist!"
    if message_lower == "/cache_status":
        if url_cache:
            status = "\n".join(
                f"{url}: Cached at {time.ctime(data['timestamp'])}" for url, data in url_cache.items())
            return f"Cache-status:\n{status}"
        return "Cache is leeg."
    if message_lower == "/reset_learned":
        learned_patterns = [k for k in search_list.keys() if k not in synonyms and k not in ["system timestamp", "hoe laat", "dansplaat", "wie ben je", "goedemorgen", "meta charset", "html", "goedemiddag",
                                                        "goedenavond", "goedennacht", "wat is je favoriete kleur", "vertel een grap", "wat is het weer", "hoe oud ben je", "wat is liefde", "zullen we dansen", "test_internet", "test_internet_wget"]]
        for pattern in learned_patterns:
            del search_list[pattern]
        save_search_list()
        return "Geleerde patronen gereset!"
    if message_lower == "/list_stack_dirs":
        return get_stack_directory_structure()
    if message_lower == "/benchmark":
        url = "https://nu.nl"
        start_time = time.time()
        if url in url_cache and (time.time() - url_cache[url]["timestamp"]) < 86400:
            content = url_cache[url]["content"]
            duration = time.time() - start_time
            return f"Benchmark (cache): {duration:.2f}s\nResultaat: {content[:100]}..."
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            html = loop.run_until_complete(async_get_url(url))
            duration = time.time() - start_time
            return f"Benchmark (live): {duration:.2f}s\nResultaat: {html[:100]}..."
        except Exception as e:
            duration = time.time() - start_time
            return f"Benchmark failed: {e} (Duur: {duration:.2f}s)"
        finally:
            loop.close()
    if message_lower == "/suggest":
        if recent_commands:
            suggestions = []
            for cmd in recent_commands[-3:]:
                for pattern in search_list.keys():
                    if fuzz.ratio(cmd, pattern.lower()) > 70:
                        suggestions.append(pattern)
            return f"Suggesties gebaseerd op recente commando's:\n" + "\n".join(suggestions) if suggestions else "Geen suggesties beschikbaar."
        return "Geen recente commando's om suggesties te baseren."
    if message_lower == "toon chat url" or fuzz.ratio("toon chat url", message_lower) > 75:
        if os.path.exists(CHAT_URL_FILE):
            with open(CHAT_URL_FILE, "r") as f:
                content = f.read()
            return "Chat history (URL):\n" + (content[:500] or "Leeg")
        return "Geen chat history (URL) gevonden."
    if message_lower == "toon overzicht" or fuzz.ratio("toon overzicht", message_lower) > 75:
        output = "Overzicht van alle chat history:\n"
        if os.path.exists(CHAT_LOG):
            with open(CHAT_LOG, "r") as f:
                output += f"Chatlog:\n{f.read()[:1000]}\n"
        else:
            output += "Geen chatlog gevonden.\n"
        if os.path.exists(CHAT_URL_FILE):
            with open(CHAT_URL_FILE, "r") as f:
                output += f"Chat URL history:\n{f.read()[:500] or 'Leeg'}"
        else:
            output += "Geen chat URL history gevonden."
        return output
    if message_lower == "analyze log":
        if os.path.exists(CHAT_LOG):
            with open(CHAT_LOG, "r") as f:
                lines = f.readlines()
            scrape_attempts = sum(1 for line in lines if "scrape url:" in line)
            failed_attempts = sum(
                1 for line in lines if "Fout: Kon URL niet scrapen" in line)
            return f"Log-analyse: {scrape_attempts} scrape-pogingen, {failed_attempts} mislukt."
        return "Geen chatlog gevonden."
    if message_lower == "/stats":
        command_counts = Counter(recent_commands)
        stats = "\n".join(f"{cmd}: {count}x" for cmd,
                          count in command_counts.items())
        return f"Bot-statistieken:\nAantal recente commando's: {len(recent_commands)}\nCommando-verdeling:\n{stats}"
    if message_lower == "/help":
        return "Beschikbare commando's:\n- dansplaat: Start de party!\n- scrape url: <url>: Scrapet een website\n- /test_internet_wget: Test internet via wget\n- zoek iets <tekst>: Zoek online\n- /zoek update van ai bot: Check bot-status\n- toon chat url: Toon URL-geschiedenis\n- toon overzicht: Toon chatlog\n- analyze log: Analyseer log\n- leer: <patroon> | <antwoord>: Leer nieuwe reactie\n- /stats: Toon gebruiksstatistieken\n- /help: Toon deze hulp\n- /clear_cache: Wis de cache\n- /cache_status: Toon cache-status\n- /reset_learned: Reset geleerde patronen\n- /list_stack_dirs: Toon mapstructuur op TransIP STACK\n- /benchmark: Test scrape-snelheid\n- /suggest: Geef suggesties"
    if message_lower.startswith("sla chat url:"):
        url = message[13:].strip().replace("https:.//", "https://")
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            os.makedirs(os.path.dirname(CHAT_URL_FILE), exist_ok=True)
            subprocess.run(["curl", "-L", "-o", CHAT_URL_FILE, "-H", "User-Agent: Mozilla/5.0",
                           "--proxy", "http://localhost:3128", url], timeout=10, check=True)
            with open(CHAT_URL_FILE, "r") as f:
                content = f.read()
            return f"Opgeslagen in chat_history.txt: {content[:100]}..."
        except subprocess.CalledProcessError:
            return "Fout: Kon URL niet downloaden (403 Forbidden?). Probeer 'scrape url:'."
        except Exception as e:
            return f"Fout bij opslaan URL: {e}"
    if message_lower.startswith("scrape url:"):
        url = message[11:].strip().replace("https:.//", "https://")
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if url in url_cache and (time.time() - url_cache[url]["timestamp"]) < 86400:
            content = url_cache[url]["content"]
            save_chat(f"Scrape uit cache: {url}")
            return f"Gescrapet uit cache in chat_history.txt: {content[:100]}..."
        start_time = time.time()
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            html = loop.run_until_complete(async_get_url(url))
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.get_text(separator=" ", strip=True)[:500]
            os.makedirs(os.path.dirname(CHAT_URL_FILE), exist_ok=True)
            with open(CHAT_URL_FILE, "w") as f:
                f.write(content)
            url_cache[url] = {"content": content, "timestamp": time.time()}
            save_cache()
            duration = time.time() - start_time
            save_chat(f"Scrape duur: {duration:.2f} seconden voor {url}")
            return f"Gescrapet in chat_history.txt: {content[:100]}... (Duur: {duration:.2f}s)"
        except Exception as e:
            duration = time.time() - start_time
            save_chat(
                f"Scrape mislukt: {e} voor {url} (Duur: {duration:.2f}s)")
            return f"Fout bij scrapen URL: {e} (Duur: {duration:.2f}s)"
        finally:
            loop.close()
    if message_lower.startswith("upload file:"):
        file_path = message[12:].strip()
        if os.path.exists(file_path):
            try:
                os.makedirs(os.path.dirname(CHAT_URL_FILE), exist_ok=True)
                shutil.copy(file_path, CHAT_URL_FILE)
                with open(CHAT_URL_FILE, "r") as f:
                    content = f.read()
                return f"Geüpload naar chat_history.txt: {content[:100]}..."
            except Exception as e:
                return f"Fout bij uploaden bestand: {e}"
        return "Fout: Bestand niet gevonden."
    if fuzz.ratio("toon lijst", message_lower) > 75:
        return "Dit weet ik al:\n" + "\n".join([f"'{k}' -> '{v}'" for k, v in search_list.items()])
    if fuzz.ratio("herlaad lijst", message_lower) > 75:
        load_search_list()
        return "Zoeklijst opnieuw geladen!"
    if message_lower.startswith("leer:"):
        parts = message[5:].split("|")
        if len(parts) == 2 and all(part.strip() for part in parts):
            pattern, response = parts
            search_list[pattern.strip()] = response.strip()
            save_search_list()
            return f"Geleerd: '{pattern.strip()}' -> '{response.strip()}'"
        return "Ongeldige leeropdracht. Gebruik: leer: patroon | antwoord"
    if message_lower.startswith("/zoek update van ai bot"):
        try:
            version = "1.0"
            uptime = subprocess.run(
                ["uptime"], capture_output=True, text=True).stdout.strip()
            git_status = subprocess.run(["git", "log", "-1", "--pretty=%h %s"], capture_output=True, text=True, cwd="/home/archangel/projects/simple_bot").stdout.strip(
            ) if os.path.exists("/home/archangel/projects/simple_bot/.git") else "Geen Git-repository"
            save_chat(
                f"Update-check: Huidige versie: {version}, Systeemstatus: {uptime}, Git: {git_status}")
            return f"Huidige versie: {version}\nSysteemstatus: {uptime}\nGit: {git_status}"
        except Exception as e:
            save_chat(f"Update-check fout: {e}")
            return f"Fout bij update-check: {e}"
for pattern, response in search_list.items():
pattern_lower = pattern.lower()
if fuzz.ratio(pattern_lower, message_lower) > 75 or pattern_lower in message_lower:
    if pattern_lower == "test_internet_wget":
        return handle_test_internet_wget()
    if pattern_lower == "test_internet":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
           return loop.run_until_complete(handle_test_internet())
        finally:
            loop.close()
    if "timestamp" in response:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return response.format(timestamp=timestamp)
    return response

  for pattern, syn_list in synonyms.items():
      pattern_lower = pattern.lower()
      if fuzz.ratio(pattern_lower, message_lower) > 75 or pattern_lower in message_lower:
            response = search_list.get(pattern, "Synoniem match, maar geen antwoord gevonden.")
        if pattern_lower == "test_internet":
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(handle_test_internet())
                finally:
                    loop.close()
        if pattern_lower == "test_internet_wget":
                return handle_test_internet_wget()
        if "timestamp" in response:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return response.format(timestamp=timestamp)
            return response
        for synonym in syn_list:
            if fuzz.ratio(synonym, message_lower) > 75 or synonym in message_lower:
                response = search_list.get(pattern, "Synoniem match, maar geen antwoord gevonden.")
                if pattern_lower == "test_internet":
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        return loop.run_until_complete(handle_test_internet())
                    finally:
                        loop.close()
                if pattern_lower == "test_internet_wget":
                    return handle_test_internet_wget()
                if "timestamp" in response:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return response.format(timestamp=timestamp)
                return response
    if "zoek iets" in message_lower:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            search_file = os.path.join(WGET_LOG_DIR, f"{SEARCH_FILE_WGET_PREFIX}_{timestamp}.html")
            log_file = os.path.join(WGET_LOG_DIR, f"wget_log_{timestamp}.txt")
            save_chat(f"Zoekopdracht: Start (Bestand: {search_file}, Log: {log_file})")
            os.makedirs(WGET_LOG_DIR, exist_ok=True)
            if not os.access(WGET_LOG_DIR, os.W_OK):
                raise PermissionError(f"Geen schrijfrechten voor {WGET_LOG_DIR}")
            try:
                subprocess.run(["nc", "-z", "localhost", "3128"], timeout=5, check=True)
                save_chat("Zoekopdracht: Proxy op localhost:3128 is bereikbaar")
            except subprocess.CalledProcessError:
                raise RuntimeError("Proxy op localhost:3128 is niet bereikbaar")
            env = os.environ.copy()
            env["http_proxy"] = "http://localhost:3128"
            result = subprocess.run(
                ["wget", "--debug", "--output-file", log_file, "-O", search_file, "http://example.com"],
                timeout=10,
                env=env,
                check=True,
                capture_output=True,
                text=True
            )
            save_chat(f"Zoekopdracht: Stdout: {result.stdout[:200]}\nStderr: {result.stderr[:200]}")
            if not os.path.exists(search_file):
                raise FileNotFoundError(f"Zoekbestand {search_file} niet aangemaakt")
            with open(search_file, "r") as f:
                content = f.read()
            save_chat(f"Zoekopdracht: {message_lower} (Bestand: {search_file})")
            return "Zoekresultaat: " + content[:200]
        except Exception as e:
            save_chat(f"Zoekfout: {e}\nStdout: {result.stdout[:200] if 'result' in locals() else 'N/A'}\nStderr: {result.stderr[:200] if 'result' in locals() else 'N/A'}")
            return f"Zoekfout: {str(e)}"
    best_match = max((fuzz.ratio(pattern.lower(), message_lower), pattern) for pattern in search_list.keys())[1]
    if fuzz.ratio(best_match.lower(), message_lower) > 70:
        return f"Sorry, ik begrijp je niet. Bedoelde je '{best_match}'?"
    if recent_commands and len(recent_commands) > 1:
        context_response = f"Je vroeg eerder om '{recent_commands[-2]}'. Wil je daar meer over weten?"
        return context_response
    return "Sorry, ik begrijp je niet. Wil je me iets leren? Gebruik 'leer: patroon | antwoord'."

##### Start de Bot ####
load_search_list()
load_cache()

app.run(host='0.0.0.0', port=5000)
