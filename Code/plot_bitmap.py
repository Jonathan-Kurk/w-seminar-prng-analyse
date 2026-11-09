import os
import matplotlib.pyplot as plt
import numpy as np

ordner = os.path.dirname(os.path.abspath(__file__))


def lade_daten(dateiname):
    pfad = os.path.join(ordner, dateiname)
    with open(pfad, "r", encoding="utf-8") as f:
        return np.array([float(z.strip()) for z in f if z.strip()])


# Wir nehmen die ersten 1600 Zahlen und formen ein 40x40 Pixel-Bild
SEITE = 40
ANZAHL = SEITE * SEITE

kandidaten = [
    ("lcg.txt", "(a) LCG"),
    ("mersenne.txt", "(b) Mersenne Twister"),
    ("chacha20.txt", "(c) ChaCha20"),
    ("gemini.txt", "(d) Gemini LLM"),
]

fig, axs = plt.subplots(1, 4, figsize=(12, 3.5))

for idx, (datei, titel) in enumerate(kandidaten):
    daten = lade_daten(datei)[:ANZAHL]
    # In Schwarz/Weiß umwandeln: < 0.5 wird 0 (schwarz), >= 0.5 wird 1 (weiß)
    pixel = (daten >= 0.5).astype(int).reshape((SEITE, SEITE))

    axs[idx].imshow(pixel, cmap="binary", interpolation="nearest")
    axs[idx].set_title(titel, fontsize=10)
    axs[idx].axis("off")  # Achsen ausblenden für reine Bildwirkung

plt.tight_layout()
speicherpfad = os.path.join(ordner, "bitmap_vergleich.png")
plt.savefig(speicherpfad, dpi=300)
print(f"--> Gespeichert als: {speicherpfad}")
plt.show()