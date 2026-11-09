import os
import matplotlib.pyplot as plt
import numpy as np

ordner = os.path.dirname(os.path.abspath(__file__))


def lade_daten(dateiname):
    pfad = os.path.join(ordner, dateiname)
    with open(pfad, "r", encoding="utf-8") as f:
        return np.array([float(z.strip()) for z in f if z.strip()])


def berechne_autokorrelation(daten, max_lag=40):
    n = len(daten)
    mittelwert = np.mean(daten)
    zentriert = daten - mittelwert
    varianz = np.sum(zentriert**2)

    lags = np.arange(1, max_lag + 1)
    korrelationen = []

    for k in lags:
        # Formel für empirische Autokorrelation:
        r_k = np.sum(zentriert[:-k] * zentriert[k:]) / varianz
        korrelationen.append(r_k)

    return lags, np.array(korrelationen), n


# 1. Daten laden
kandidaten = [
    ("lcg.txt", "(a) Linearer Kongruenzgenerator (LCG)"),
    ("mersenne.txt", "(b) Mersenne Twister (Python random)"),
    ("chacha20.txt", "(c) ChaCha20 / CSPRNG"),
    ("gemini.txt", "(d) Large Language Model (Gemini)"),
]

fig, axs = plt.subplots(2, 2, figsize=(11, 8))

for idx, (datei, titel) in enumerate(kandidaten):
    ax = axs[idx // 2, idx % 2]
    daten = lade_daten(datei)
    lags, r, n = berechne_autokorrelation(daten, max_lag=35)

    # 95%-Konfidenzintervall für echtes weißes Rauschen (+- 1.96 / sqrt(N)):
    schranke = 1.96 / np.sqrt(n)

    # Stem-Plot (Balken mit Punkten oben)
    markerline, stemlines, baseline = ax.stem(
        lags, r, linefmt="k-", markerfmt="ko", basefmt="k-"
    )
    plt.setp(markerline, markersize=3)
    plt.setp(stemlines, linewidth=1)

    # Gestrichelte Toleranzgrenzen einzeichnen
    ax.axhline(
        schranke,
        color="red",
        linestyle="--",
        linewidth=1,
        label="95% Konfidenzgrenze",
    )
    ax.axhline(-schranke, color="red", linestyle="--", linewidth=1)

    ax.set_title(titel, fontsize=11)
    ax.set_xlabel("Verschiebung $k$ (Lag)")
    ax.set_ylabel("Autokorrelation $r_k$")
    ax.set_ylim(-0.35, 0.35)
    ax.grid(True, linestyle=":", alpha=0.6)
    if idx == 0:
        ax.legend(loc="upper right", fontsize=9)

plt.tight_layout()
speicherpfad = os.path.join(ordner, "autokorrelation_vergleich.png")
plt.savefig(speicherpfad, dpi=300)
print(f"--> Fertig! Gespeichert als: {speicherpfad}")
plt.show()