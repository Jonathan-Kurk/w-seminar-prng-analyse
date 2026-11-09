import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ordner = os.path.dirname(os.path.abspath(__file__))


def lade_punkte(dateiname):
    pfad = os.path.join(ordner, dateiname)
    with open(pfad, "r", encoding="utf-8") as f:
        werte = [float(z.strip()) for z in f if z.strip()]
    return werte[:-1], werte[1:]


# Daten laden
x_lcg, y_lcg = lade_punkte("lcg.txt")
x_mt, y_mt = lade_punkte("mersenne.txt")
x_cc, y_cc = lade_punkte("chacha20.txt")
x_gem, y_gem = lade_punkte("gemini.txt")

# 2x2 Raster erstellen (Achsen unabhängig voneinander!)
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "(a) LCG (21 Linien)",
        "(b) Mersenne Twister",
        "(c) ChaCha20 (CSPRNG)",
        "(d) Gemini LLM (Cluster & Hohlraum)",
    ),
    horizontal_spacing=0.1,
    vertical_spacing=0.1,
)


def punkt_trace(x, y, name):
    return go.Scatter(
        x=x,
        y=y,
        mode="markers",
        name=name,
        marker=dict(size=4, color="black", opacity=0.6),
        hoverinfo="none",  # Spart Rechenleistung beim Zoomen
    )


fig.add_trace(punkt_trace(x_lcg, y_lcg, "LCG"), row=1, col=1)
fig.add_trace(punkt_trace(x_mt, y_mt, "Mersenne Twister"), row=1, col=2)
fig.add_trace(punkt_trace(x_cc, y_cc, "ChaCha20"), row=2, col=1)
fig.add_trace(punkt_trace(x_gem, y_gem, "Gemini"), row=2, col=2)

# Startbereiche festlegen
for i in range(1, 5):
    fig.update_xaxes(range=[0, 1], row=(i - 1) // 2 + 1, col=(i - 1) % 2 + 1)
    fig.update_yaxes(range=[0, 1], row=(i - 1) // 2 + 1, col=(i - 1) % 2 + 1)

fig.update_layout(
    height=850,
    width=850,
    title_text="2D-Phasenraum (Mausrad-Zoom in jedem Feld aktiv, Doppelklick zum Zurücksetzen)",
    dragmode="pan",  # Mit Klick & Ziehen kann man den Ausschnitt verschieben
)

speicherpfad = os.path.join(ordner, "punktwolken_2d_zoombahr.html")

# HIER ist die Magie: scrollZoom=True schaltet das Mausrad frei!
fig.write_html(
    speicherpfad,
    config={
        "scrollZoom": True,
        "displayModeBar": True,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    },
)

print(f"--> Fertig! Gespeichert als: {speicherpfad}")
print("Doppelklicke auf die Datei, um sie im Browser zu öffnen.")