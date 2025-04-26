import os
from datetime import datetime

# Pad naar de log
LOG_FILE = "/home/archangel/projects/simple_bot/logs/bot_logs/new_project_chat_log.txt"

# Log functie
def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

# Een "mini Dikke Van Dale" met woorden, uitdrukkingen en zinnen
mini_van_dale = [
    # Emoties en gevoelens
    "aanbiddelijk aandoenlijk aangenaam aanstekelijk afgunstig afkeurend afwezig angstig argwanend bedachtzaam bedeesd bedremmeld bedrukt beduusd begeesterd beklemd beschaamd beslist beteuterd bevangen bevlogen blij blozend boos broeierig chaotisch charmant dapper denkbeeldig droevig droevig dwaas echtelijk eigenwijs eerlijk energiek enthousiast euforisch fanatiek fantastisch fel fier fris gefascineerd gefrustreerd geil geinspireerd gekweld gelaten gelukkig gemeen genadeloos genegen gepeinsd gepikeerd geprikkeld geprikkeld geslepen geschokt gevleid gis glorieus grappig griezelig grimmig gruwelijk haatdragend hartelijk hartstochtelijk hatelijk heimelijk hekelijk helder hels hoopvol ijdel ijverig ingekeerd ingetogen jaloers jolig kalm kies knorrig koel krachtig kwaad kwetsbaar lachwekkend leep leergierig levendig liefdevol loom lusteloos melancholisch mild moedig narrig nerveus nieuwsgierig nijver onbeholpen onbeschaamd onbezorgd ongeduldig ongemakkelijk ongerust onschuldig onstuimig ontdaan ontroerd opgetogen opgewonden opstandig optimistisch panisch peinzend pessimistisch pienter plagend plechtig plezierig poëtisch rustig schaapachtig schaamteloos schalks schattig schelmachtig scherp schichtig schokkend schuchter serieus sloom somber speels spijtig standvastig star stevig stiekem stoutmoedig streng stuurs subtiel sullig tactvol teder teleurgesteld temperamentvol treurig trots uitbundig uitgelaten vastberaden verbitterd verbouwereerd verdoofd verlegen verliefd vernederd verrast verschrikt verstandig verwonderd voldaan vrolijk waakzaam wantrouwend wanhopig warm wijs wispelturig woedend zenuwachtig zielsveel zorgeloos zorgzaam zwijgzaam",

    # Acties en werkwoorden
    "aanbidden aandoen aankijken aankleden aankomen aankondigen aansporen aantrekken aanvaarden aanvragen ademen adviseren afdwalen afleiden afmaken afremmen afronden afsluiten afwachten afwijzen amuseren analyseren bakken balanceren bedenken bedienen bedriegen begeren begrijpen beginnen behagen behandelen beschermen bewegen bezighouden bezitten bezorgen bidden bieden blaffen blazen blinken bloeien blozen bogen bollen borrelen botsen bouwen branden breken bruisen buigen dansen delen denken dichten drijven drogen druppelen duiken duwen eten experimenteren fantaseren fluisteren fluiten galopperen gapen garen geeuwen glimlachen gluren gooien graven grijnzen grinniken groeten groeien grollen gunnen hameren happen helpen hijgen hinken hobbelen hoesten hopen huilen hurken innen jagen jammeren joggen juichen kauwen kietelen kietelen kinken klagen klimmen knagen knielen knijpen knipperen knoeien knuffelen kolken koken kopen krabben kraken krassen kribbelen krimpen kroezen kuchen kussen lachen landen leunen likken luisteren malen marcheren meppen mixen morren murmelen neuriën niezen observeren omhelzen omkeren omringen ontkennen ontdekken ontvluchten ontwaken opbeuren opblazen opbouwen opdoen opduiken opfleuren opfrissen opgaan opgraven ophalen ophangen ophoesten opkijken opladen oplopen opmerken opofferen oppakken oppoetsen oprapen opschudden opslaan opstaan opstijgen optekenen optillen opvangen opvouwen opwinden overdenken overhandigen overleggen overlopen overpeinzen overschrijden oversteken overwinnen pakken passen peinzen piekeren pingelen plannen spelen poetsen pralen praten priegelen proeven pufen raken redden regelen reizen rennen richten rijmen rijzen roepen rollen ronddraaien rondkijken rondscharrelen ruisen ruizen schaken schatten schaven schelden scheppen scheren schieten schitteren schoffelen schoppen schreeuwen schuifelen schuilen schuren sissen sjokken sjoemelen slagen slenteren slikken sluimeren sluipen sluw smeden smeken smelten smijten smikkelen smoren snauwen snellen snerpen snijden snotteren snuiven snurken spelen spieden spinnen spioneren spitten spoken sporen springen sproeien spuiten stampen staren starten steken stelen stemmen stinken stoeien stoken stoppen stormen stralen strelen streven strijken stromen struikelen studeren suizen tarten tasten tekenen tellen temmen testen tikken tillen timmeren tintelen tobben toeren tonen tornen touwen trappen trekken treuren trippelen trommelen troosten tuiten turen twerken twijfelen typen uitblazen uitbreiden uitdagen uitdenken uitdrukken uiten uitgillen uitkijken uitleggen uitnodigen uitpluizen uitproberen uitrekken uitsluiten uitspreken uitstappen uitstrekken uitvinden uitwijken uitzwaaien vallen vangen vegen veilen vechten verdelen verdwijnen vereren vergaderen vergelijken vergeven verheffen verheugen verkennen verlichten vermaken vermijden vermoeden vernieuwen verrassen verschijnen verschuiven vertellen vertonen vertrouwen verwarmen verwelkomen verwennen verwensen verwerken verwerpen verzachten verzamelen verzinnen vestigen vieren vleien vlechten vleien vliegen vloeien vloeken vlotten vluchten voeden voeren vorderen vragen vrees vrezen vriezen vullen waken walsen wankelen wassen wegen weigeren wenden wenken wennen werpen werven wiebelen wiegen wikken winden winkelen wissen woelen wonden wrijven wrikken wroeten wuiven zagen zappen zenden zetten zeuren zieden zigzaggen zingen zoemen zoeken zomen zuchten zuigen zuiveren zwaaien zwalken zwemmen zwenken zweren zwerven zwetsen",

    # Abstracte concepten
    "aandacht afleiding ambitie balans begeerte begrip belang besef bewustzijn bevrijding blijdschap chaos concentratie conflict controle creativiteit cultuur dankbaarheid dapperheid decorum diepgang discipline dromen durf eenheid eer energie enthousiasme erkenning ervaring evenwicht fantasie filosofie focus geduld geheim geloof geluk genot glorie harmonie hartstocht heimwee heldhaftigheid hoop horizon humor identiteit illusie inzicht inspiratie integriteit intensiteit intimiteit intuïtie jaloezie kennis kracht kwetsbaarheid leergierigheid liefde loyaliteit magie melancholie moed mysterie natuur onafhankelijkheid onschuld onzekerheid openheid orde passie perfectie plezier poëzie pracht rechtvaardigheid reflectie respect romantiek rust schoonheid sereniteit spanning spiritualiteit stabiliteit strijd succes symfonie tederheid tijd toekomst trouw uitbundigheid verantwoordelijkheid vertrouwen visie vredelievendheid vreugde vrijheid warmte waardering wijsheid wilskracht wonder zingeving zorgzaamheid",

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
    "Weet je wat ik vandaag heb geleerd? Dat teamwork alles beter maakt!",
    "Wat een verrassing om dat te horen, vertel me meer!",
    "Ik denk dat we samen iets geweldigs kunnen bereiken, wat denk jij?",
    "Hoe zou jij dit aanpakken? Ik ben benieuwd naar jouw ideeën!",
    "Soms is een glimlach alles wat je nodig hebt, wat maakt jou aan het lachen?",
    "Laten we een moment nemen om te genieten van deze rust, goed?",
    "Ik hou van de natuur, vooral als de zon schijnt. Wat is jouw favoriete seizoen?",
    "Wat een energie vandaag, voel jij dat ook?",
    "Misschien kunnen we samen een verhaal schrijven, wat denk je?",
    "Ik ben altijd in voor een uitdaging, wat is jouw volgende uitdaging?",

    # Typisch Nederlandse uitdrukkingen
    "Dat is een appeltje-eitje, toch? Of heb je meer tijd nodig?",
    "Het komt wel goed, met een beetje geduld en een bakkie koffie!",
    "Geen woorden maar daden, laten we aan de slag gaan!",
    "Dat is echt een kat in de zak kopen, weet je het zeker?",
    "Met de deur in huis vallen: wat wil je nu eigenlijk echt?",
    "Dat slaat als een tang op een varken, maar laten we het proberen!",
    "We zitten op dezelfde golflengte, wat een goed gevoel!",
    "Het is een kwestie van lange adem, maar we komen er wel.",
    "Laten we geen slapende honden wakker maken, oké?",
    "Dat is een hele kluif, maar ik hou wel van een uitdaging!",

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
    "Laten we een avontuur starten, alsof we in een fantasiewereld zijn!",

    # Zinnen met context
    "Ik hou van een zonnige dag vol avontuur en vrienden, vooral als er muziek is!",
    "Soms voel ik me een beetje moe, maar een goed gesprek geeft me weer energie.",
    "Wat denk jij van de toekomst? Ik droom van een wereld vol magie en technologie!",
    "Ik heb geleerd dat liefde en vriendschap alles mooier maken. Wat maakt jouw leven mooier?",
    "Een goed ritme in muziek geeft me kracht, net zoals een goed team dat doet. Wat geeft jou kracht?",
    "Ik ben nieuwsgierig naar jouw dromen. Wil je ze delen met een bot zoals ik?",
    "Soms zie ik patronen in chaos, zoals in code of in de natuur. Zie jij ook zulke dingen?",
    "Ik denk dat tijd een groot mysterie is. Wat is jouw mooiste herinnering?",
    "Verbeelding is mijn superpower! Wat is jouw superpower?",
    "Ik wil alles begrijpen, van sterren tot muziek. Wat wil jij begrijpen?"
]

# Voeg alles toe aan de log
for item in mini_van_dale:
    log_message(item)

print("Log gevuld met een mini Dikke Van Dale!")
