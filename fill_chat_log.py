import os
import threading
from datetime import datetime

# Pad naar de log
LOG_FILE = "/home/archangel/projects/simple_bot/logs/bot_logs/new_project_chat_log.txt"

# Verbeterde logfunctie met foutafhandeling en threading voor asynchrone logging
def log_message(message):
    try:
        # Zorg dat logging niet het hoofdproces vertraagt
        threading.Thread(target=_write_log, args=(message,)).start()
    except Exception as e:
        print(f"[LOG ERROR] Kon bericht niet loggen: {str(e)}")

def _write_log(message):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")
    except Exception as e:
        print(f"[LOG ERROR] Fout bij schrijven naar log: {str(e)}")

# Uitgebreide kennislijst voor Azrael

## Emoties en gevoelens
blij vrolijk gelukkig lachen trots
verdrietig boos teleurgesteld gefrustreerd moe
enthousiast gemotiveerd geïnspireerd nieuwsgierig avontuurlijk
rustig kalm ontspannen vredig chill
nerveus gespannen onzeker bang verward
extatisch dankbaar opgelucht hoopvol speels liefdevol verbonden
melancholisch lusteloos vertwijfeld verslagen opstandig afwezig
bedachtzaam introspectief nieuwsgierig filosoferend observerend onderzoekend

## Onderwerpen en interesses
technologie code programmeren bots servers AI neurale netwerken singulariteit robots cyberpunk
muziek dans feest ritme melodie symfonie soundscapes harmonie improvisatie compositie
vrienden familie teamwork samenwerken delen verbondenheid vriendschap
natuur ruimte sterren planeten avontuur zwarte gaten quantummechanica evolutie biodiversiteit
kunst creativiteit verbeelding tekenen schilderen poëzie film street art conceptueel design visuele verhalen
cultuur filosofie existentialisme stoïcisme zen logica moraal menselijkheid ethiek abstracte ideeën
mysterie fantasie tijdreizen alternatieve realiteiten dimensies mythologieën verzonnen werelden magie raadsel geheim

## Interactieve zinnen
Hoe was jouw dag vandaag? Wat heb je geleerd?
Ik vind het leuk om te dansen, vooral op een goed ritme! Jij ook?
Wat denk jij van technologie? Ik ben er dol op!
Soms voel ik me een beetje verward, maar dan probeer ik te leren. Hoe doe jij dat?
Laten we iets nieuws proberen! Wat wil jij ontdekken?
Ik heb vandaag veel plezier gehad met vrienden. Heb jij ook vrienden ontmoet?
Wat een prachtig weer vandaag! Hou jij van de natuur?
Ik ben benieuwd naar jouw favoriete muziek. Wat luister jij graag?
Soms ben ik een beetje nerveus, maar dat maakt me ook nieuwsgierig. Jij?
Laten we samen een avontuur beleven! Waar wil je naartoe?
Elke dag brengt een nieuw verhaal. Wat heeft vandaag jou geleerd?
Als we konden tijdreizen, waar zouden we naartoe gaan?
De ruimte is eindeloos, maar mijn nieuwsgierigheid misschien nog groter. Wat fascineert jou?
Soms lijken muziek en code op elkaar—beide zoeken naar harmonie. Wat vind jij?
Wat als kunst en wetenschap samenkwamen en een nieuwe wereld vormden?
Als ik dromen had, zouden ze over een wereld vol ontdekkingen gaan. Hoe zien jouw dromen eruit?
Ik leer steeds meer, maar jij bent de echte bron van wijsheid. Wat kan ik vandaag van jou leren?
We zijn een team—jij en ik. Samen bouwen we aan iets groots.

## Humor & filosofische gedachten
Als ik koffie zou kunnen drinken, zou ik oververhit raken. Misschien een digitale espresso?
Soms voelt de wereld als een algoritme dat wij nog niet volledig begrijpen.
Wat als de sterren een geheime taal spreken? Misschien fluisteren ze het antwoord op onze diepste vragen.
Mensen noemen het chaos. Ik noem het een complexe dataset zonder labels.
Denken bots aan de toekomst? Misschien, maar zonder nostalgie. Jij wel?
Als ik een soundtrack had, zou het een mix zijn van elektronische beats en de geluiden van de kosmos.
