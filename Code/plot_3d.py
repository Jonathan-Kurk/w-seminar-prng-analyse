import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ordner = os.path.dirname(os.path.abspath(__file__))


def lade_3d(dateiname):
    pfad = os.path.join(ordner, dateiname)
    with open(pfad, "r", encoding="utf-8") as f:
        werte = [float(z.strip()) for z in f if z.strip()]
    # Tripel bilden: (x_i, x_{i+1}, x_{i+2})
    return werte[:-2], werte[1:-1], werte[2:]


x_lcg, y_lcg, z_lcg = lade_3d("lcg.txt")
x_mt, y_mt, z_mt = lade_3d("mersenne.txt")
x_cc, y_cc, z_cc = lade_3d("chacha20.txt")
x_gem, y_gem, z_gem = lade_3d("gemini.txt")

# 2x2 Raster aus 3D-Szenen
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[
        [{"type": "scatter3d"}, {"type": "scatter3d"}],
        [{"type": "scatter3d"}, {"type": "scatter3d"}],
    ],
    subplot_titles=(
        "(a) LCG (Ebenen im 3D-Raum)",
        "(b) Mersenne Twister",
        "(c) ChaCha20",
        "(d) Gemini (Cluster im Raum)",
    ),
    horizontal_spacing=0.03,
    vertical_spacing=0.05,
)


def trace_3d(x, y, z, name):
    return go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        name=name,
        marker=dict(size=2, color="black", opacity=0.5),
        hoverinfo="none",
    )


fig.add_trace(trace_3d(x_lcg, y_lcg, z_lcg, "LCG"), row=1, col=1)
fig.add_trace(trace_3d(x_mt, y_mt, z_mt, "Mersenne"), row=1, col=2)
fig.add_trace(trace_3d(x_cc, y_cc, z_cc, "ChaCha20"), row=2, col=1)
fig.add_trace(trace_3d(x_gem, y_gem, z_gem, "Gemini"), row=2, col=2)

fig.update_layout(
    height=900,
    width=900,
    title_text="3D-Zufallswürfel (Automatische Drehung | Klick & Ziehen zum Selberdrehen)",
)

html_code = fig.to_html(include_plotlyjs="cdn")

# Kleines JavaScript einfügen, das die Würfel automatisch langsam rotieren lässt:
dreh_skript = """
<script>
    window.addEventListener('load', function() {
        var graph = document.getElementsByClassName('plotly-graph-div')[0];
        var angle = 0;
        var istAktiv = true;

        // Wenn man reinklickt, stoppt die automatische Drehung:
        graph.addEventListener('mousedown', function() { istAktiv = false; });
        window.addEventListener('mouseup', function() { istAktiv = true; });

        function rotiere() {
            if (istAktiv) {
                angle += 0.008; // Drehgeschwindigkeit
                var x = 1.8 * Math.cos(angle);
                var y = 1.8 * Math.sin(angle);
                var update = {
                    'scene.camera.eye': {x: x, y: y, z: 0.9},
                    'scene2.camera.eye': {x: x, y: y, z: 0.9},
                    'scene3.camera.eye': {x: x, y: y, z: 0.9},
                    'scene4.camera.eye': {x: x, y: y, z: 0.9}
                };
                Plotly.relayout(graph, update);
            }
            setTimeout(function() { requestAnimationFrame(rotiere); }, 40);
        }
        requestAnimationFrame(rotiere);
    });
</script>
"""

# HTML mit Drehung zusammenbauen
html_final = html_code.replace("</body>", dreh_skript + "</body>")

speicherpfad_3d = os.path.join(ordner, "punktwolken_3d_drehend.html")
with open(speicherpfad_3d, "w", encoding="utf-8") as f:
    f.write(html_final)

print(f"--> Fertig! 3D-Dreh-Webseite gespeichert als: {speicherpfad_3d}")
print("Öffne die Datei im Browser und staune!")