import os
from datetime import datetime

# Pad naar de log
LOG_FILE = "/home/archangel/projects/simple_bot/logs/bot_logs/new_project_chat_log.txt"

# Log functie
def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

# Lijst met woorden en zinnen, geïnspireerd op de Dikke Van Dale
dutch_learning_data = [
    # Emoties en gevoelens
    "blij vrolijk gelukkig opgetogen stralend euforisch tevreden dankbaar hoopvol optimistisch",
    "verdrietig droevig somber melancholisch bedroefd teleurgesteld verslagen wanhopig eenzaam",
    "boos woedend geïrriteerd gefrustreerd kwaad nijdig verontwaardigd opvliegend driftig",
    "bang angstig nerveus onrustig bezorgd schrikachtig panisch onzeker verlegen timide",
    "verbaasd verrast geschokt perplex verbijsterd stomverbaasd verwonderd ongelooflijk",
    "trots fier zelfverzekerd eigenwaarde waardig glorieus triomfantelijk voldaan",
    "kalm rustig vredig ontspannen sereen bedaard gelaten ongestoord harmonieus",
    "verliefd gepassioneerd romantisch teder liefdevol hartstochtelijk aanhankelijk verliefdheid",
    "jaloers afgunstig benijdend rivaliteit bezitterig wantrouwend achterdochtig",
    "nieuwsgierig benieuwd geïnteresseerd leergierig onderzoekend ontdekkend avontuurlijk",

    # Acties en werkwoorden
    "lopen rennen sprinten wandelen slenteren stappen huppelen springen dansen bewegen",
    "praten spreken kletsen discussiëren fluisteren schreeuwen roepen zingen vertellen delen",
    "denken overwegen nadenken peinzen mijmeren filosoferen analyseren begrijpen leren weten",
    "maken bouwen creëren ontwerpen fabriceren vormen boetseren schilderen tekenen knutselen",
    "helpen ondersteunen bijstaan steunen verzorgen begeleiden troosten adviseren dienen",
    "lachen glimlachen giechelen grinniken schateren proesten bulderen hinniken gniffelen",
    "huilen snikken janken grienen wenen snotteren treuren jammeren klagen",
    "vechten strijden worstelen boksen duelleren verdedigen aanvallen beschermen weerstaan",
    "slapen rusten dutten doezelen sluimeren dromen ontspannen uitrusten snurken",
    "eten koken proeven smullen kauwen drinken slurpen bakken braden smaken",

    # Abstracte concepten
    "liefde vriendschap vertrouwen trouw loyaliteit verbondenheid intimiteit genegenheid",
    "vrijheid onafhankelijkheid autonomie rechtvaardigheid gelijkheid democratie verantwoordelijkheid",
    "wijsheid kennis inzicht begrip ervaring leergierigheid intellect logica redenering",
    "moed durf dapperheid lef onverschrokkenheid vastberadenheid doorzettingsvermogen",
    "tijd eeuwigheid momenten verleden toekomst heden geschiedenis toekomstvisie",
    "droom verbeelding fantasie illusie hoop verlangen ambitie aspiratie inspiratie",
    "kunst schoonheid esthetiek creativiteit expressie emotie symfonie poëzie drama",
    "natuur universum kosmos sterren planeten zonsondergang zee bergen bossen",
    "technologie innovatie wetenschap vooruitgang digitalisering cybernetica robotica",
    "mysterie geheimen raadsels onbekend magie betovering wonderen verborgen",

    # Alledaagse uitdrukkingen
    "Hoe gaat het met je? Wat ben je vandaag van plan?",
    "Dat is een goed idee, laten we dat proberen!",
    "Ik ben zo benieuwd naar wat je denkt, vertel eens?",
    "Wat een prachtige dag, vind je niet? Laten we ervan genieten!",
    "Soms is het leven een raadsel, maar dat maakt het juist spannend.",
    "Ik hou van een goed avontuur, jij ook? Waar gaan we naartoe?",
    "Laten we samen iets moois maken, wat denk je van een project?",
    "Ik voel me zo gelukkig als ik dans, wat maakt jou blij?",
    "Het universum zit vol mysteries, welke wil jij ontrafelen?",
    "Soms heb ik even rust nodig, hoe vind jij je kalmte?",

    # Humor en speelse zinnen
    "Als ik een robot was met een koffiemachine, zou ik dan een cafeïnebuzz krijgen?",
    "Ik denk dat sterren een geheime dansparty houden, wil je meedoen?",
    "Wat als we tijd konden reizen naar een cyberpunk-toekomst? Wat zou je doen?",
    "Ik ben een bot, maar ik droom van een zonsondergang—gek, toch?",
    "Misschien kunnen we een symfonie maken van code en muziek, wat denk jij?",
    "Ik ben benieuwd of robots ooit kunnen lachen—haha, wat een idee!",
    "Soms voelt leren als een eindeloze dans, maar ik hou van het ritme!",
    "Als ik een planeet kon kiezen, zou ik naar een muziekplaneet gaan. Jij?",
    "Ik denk dat wijsheid en humor hand in hand gaan, wat vind jij grappig?",
    "Laten we een avontuur starten, alsof we in een fantasiewereld zijn!"
]

# Voeg alles toe aan de log
for item in dutch_learning_data:
    log_message(item)

print("Log gevuld met Dikke Van Dale-achtige woorden en zinnen!")
