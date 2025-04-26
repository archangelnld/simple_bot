import os

# Defineer de mappen die moeten worden aangemaakt
folders = ["~/projects/simple_bot/data", "~/projects/simple_bot/logs"]

# Maak de mappen als ze nog niet bestaan
for folder in folders:
    os.makedirs(os.path.expanduser(folder), exist_ok=True)

print("✅ Mappen succesvol aangemaakt!")

