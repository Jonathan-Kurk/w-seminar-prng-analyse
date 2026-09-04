import os
import matplotlib.pyplot as plt

ordner = os.path.dirname(os.path.abspath(__file__))


def lade_punkte(dateiname):
    pfad = os.path.join(ordner, dateiname)
    with open(pfad, "r", encoding="utf-8") as f:
        
        werte = [float(zeile.strip()) for zeile in f if zeile.strip()]

    
    x = werte[:-1]  
    y = werte[1:]  
    return x, y


# 1. Daten aller vier Kandidaten laden
x_lcg, y_lcg = lade_punkte("lcg.txt")
x_mt, y_mt = lade_punkte("mersenne.txt")
x_cc, y_cc = lade_punkte("chacha20.txt")
x_gem, y_gem = lade_punkte("gemini.txt")

# 2. Grafik mit 4 Teilbildern (2x2 Raster) erstellen
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Einstellungen für die Punkte (Größe und leichte Transparenz)
punkt_einstellungen = {
    "s": 4,
    "color": "black",
    "alpha": 0.6,
    "marker": "o",
    "linewidths": 0,
}

# Subplot 1: LCG
axs[0, 0].scatter(x_lcg, y_lcg, **punkt_einstellungen)
axs[0, 0].set_title("(a) Linearer Kongruenzgenerator (LCG)", fontsize=11)
axs[0, 0].set_xlim(0, 1)
axs[0, 0].set_ylim(0, 1)
axs[0, 0].set_xlabel("$x_i$")
axs[0, 0].set_ylabel("$x_{i+1}$")
axs[0, 0].set_aspect("equal")

# Subplot 2: Mersenne Twister
axs[0, 1].scatter(x_mt, y_mt, **punkt_einstellungen)
axs[0, 1].set_title("(b) Mersenne Twister (Python random)", fontsize=11)
axs[0, 1].set_xlim(0, 1)
axs[0, 1].set_ylim(0, 1)
axs[0, 1].set_xlabel("$x_i$")
axs[0, 1].set_ylabel("$x_{i+1}$")
axs[0, 1].set_aspect("equal")

# Subplot 3: ChaCha20
axs[1, 0].scatter(x_cc, y_cc, **punkt_einstellungen)
axs[1, 0].set_title("(c) ChaCha20 / CSPRNG (Python secrets)", fontsize=11)
axs[1, 0].set_xlim(0, 1)
axs[1, 0].set_ylim(0, 1)
axs[1, 0].set_xlabel("$x_i$")
axs[1, 0].set_ylabel("$x_{i+1}$")
axs[1, 0].set_aspect("equal")

# Subplot 4: Gemini (LLM)
axs[1, 1].scatter(x_gem, y_gem, **punkt_einstellungen)
axs[1, 1].set_title("(d) Large Language Model (Gemini)", fontsize=11)
axs[1, 1].set_xlim(0, 1)
axs[1, 1].set_ylim(0, 1)
axs[1, 1].set_xlabel("$x_i$")
axs[1, 1].set_ylabel("$x_{i+1}$")
axs[1, 1].set_aspect("equal")

# Layout optimieren und speichern
plt.tight_layout()
speicherpfad = os.path.join(ordner, "punktwolken_vergleich.png")
plt.savefig(speicherpfad, dpi=300)

print("--> Erfolg! Das Diagramm wurde gespeichert als:")
print(speicherpfad)
plt.show()
