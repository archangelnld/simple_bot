from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Gebruik headless mode
options = Options()
options.add_argument("--headless")

# Start de Firefox WebDriver
driver = webdriver.Firefox(options=options)

# Open NU.nl
driver.get("https://copilot.microsoft.com/chats/HGZGHv4y4QtBMwkc8eqft")

# Wacht een paar seconden zodat de pagina volledig laadt
driver.implicitly_wait(5)

# Haal de headlines op
headlines = driver.find_elements("xpath", "//h2")

# Print de headlines
for headline in headlines:
    print(headline.text)

# Sluit de browser
driver.quit()

