import random
import secrets

ANZAHL_PUNKTE = 2000


# 1. Linearer Kongruenzgenerator (LCG)
lcg_zahlen = []
zustand = 42  # Beliebiger Startwert (Seed)
a = 21
c = 1
m = 65536

for _ in range(ANZAHL_PUNKTE + 1):
    zustand = (a * zustand + c) % m
    # Durch m teilen, damit die Zahl als Kommazahl zwischen 0 und 1 liegt:
    lcg_zahlen.append(zustand / m)


# 2. Mersenne Twister (über das random-Modul)

mt_zahlen = []

random.seed(42)
for _ in range(ANZAHL_PUNKTE + 1):
    mt_zahlen.append(random.random())

# 3. ChaCha20 / CSPRNG (über das secrets-Modul)

chacha_zahlen = []
for _ in range(ANZAHL_PUNKTE + 1):
    # secrets.SystemRandom() holt kryptographisch sichere Zufallszahlen:
    chacha_zahlen.append(secrets.SystemRandom().random())


# Speichern der Zahlen in Textdateien 
with open("lcg.txt", "w") as f:
    f.write("\n".join(str(z) for z in lcg_zahlen))

with open("mersenne.txt", "w") as f:
    f.write("\n".join(str(z) for z in mt_zahlen))

with open("chacha20.txt", "w") as f:
    f.write("\n".join(str(z) for z in chacha_zahlen))

print("Fertig! Die Dateien lcg.txt, mersenne.txt und chacha20.txt wurden erstellt.")
