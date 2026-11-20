"""Generate the profile banner and section headers in the jssabater.online style.

Usage (from the repo root):
    pip install fonttools
    python scripts/build_assets.py

Edit the tagline, pill text or SECTIONS below, run it, and commit assets/.
"""
import math
import os
import random
import sys

from textpath import fraunces, onest

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

THEMES = {
    "light": dict(paper="#FFFFFF", ink="#121417", ink2="#4B5059", muted="#73787F",
                  line="#E4E6EA", indigo="#3730E8", sun="#FFC53D",
                  pill="#121417", pill_text="#FFFFFF"),
    "dark": dict(paper="#121417", ink="#FFFFFF", ink2="#B9BDC4", muted="#8B9098",
                 line="#262A31", indigo="#8A85FF", sun="#FFC53D",
                 pill="#FFFFFF", pill_text="#121417"),
}


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)


def waveform(x0, y_mid, width, color, n=120, seed=7):
    """Bars like the portfolio's voice waveform: thin, rounded, uneven heights."""
    rnd = random.Random(seed)
    step = width / n
    bars = []
    for i in range(n):
        t = i / n
        env = 0.35 + 0.65 * abs(math.sin(t * math.pi * 3.1 + 0.6)) * (0.6 + 0.4 * math.sin(t * 9.0))
        h = max(6, (10 + rnd.random() * 46) * env)
        x = x0 + i * step
        delay = (i % 12) * 0.12
        bars.append(
            f'<rect class="b" style="animation-delay:{delay:.2f}s" x="{x:.1f}" y="{y_mid - h / 2:.1f}" '
            f'width="2.4" height="{h:.1f}" rx="1.2" fill="{color}"/>'
        )
    return "\n    ".join(bars)


def banner(theme):
    c = THEMES[theme]
    W, H = 1200, 400
    name_d, name_w = fraunces("Joms", 150, 72, 190)
    l1, _ = onest("Software Engineer in Manila. I build full-stack web apps", 22, 76, 244)
    l2, _ = onest("and speech AI, and ship them to production.", 22, 76, 276)

    pill_label = "open to full-time roles"
    pill_d, pill_w = onest(pill_label, 15, 0, 0, weight=500)
    px, py, ph = 76, 300, 40
    pw = 22 + 10 + 10 + pill_w + 22
    pill_d, _ = onest(pill_label, 15, px + 22 + 10 + 10, py + 25.5, weight=500)
    num_d, _ = onest("~/jomzxc", 14, 0, 0, weight=500)
    handle_d, handle_w = onest("github.com/jomzxc", 14, 0, 0, weight=500)
    handle_d, _ = onest("github.com/jomzxc", 14, W - 76 - handle_w, 64, weight=500)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Joms. Software Engineer in Manila. I build full-stack web apps and speech AI, and ship them to production. Open to full-time roles.">
  <style>
    .b {{ transform-box: fill-box; transform-origin: center; animation: pulse 1.8s ease-in-out infinite alternate; }}
    @keyframes pulse {{ from {{ transform: scaleY(1); }} to {{ transform: scaleY(0.45); }} }}
    .dot {{ animation: blink 2.4s ease-in-out infinite; }}
    @keyframes blink {{ 50% {{ opacity: .35; }} }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="24" fill="{c['paper']}" stroke="{c['line']}"/>
  <path d="{handle_d}" fill="{c['muted']}"/>
  <path d="{name_d}" fill="{c['ink']}"/>
  <circle cx="{72 + name_w + 14:.1f}" cy="178" r="9" fill="{c['sun']}"/>
  <path d="{l1}" fill="{c['ink2']}"/>
  <path d="{l2}" fill="{c['ink2']}"/>
  <rect x="{px}" y="{py}" width="{pw:.1f}" height="{ph}" rx="{ph / 2}" fill="{c['pill']}"/>
  <circle class="dot" cx="{px + 22 + 5}" cy="{py + ph / 2}" r="5" fill="{c['sun']}"/>
  <path d="{pill_d}" fill="{c['pill_text']}"/>
  <g>
    {waveform(640, 190, 484, c['indigo'], n=96)}
  </g>
</svg>
'''


def header(num, label, theme):
    c = THEMES[theme]
    H = 84
    num_d, num_w = onest(num, 18, 2, 30, weight=600)
    title_d, title_w = fraunces(label, 48, 0, 74, tracking_em=-0.035)
    W = int(max(title_w, num_w) + 8)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{num} {label}">
  <path d="{num_d}" fill="{c['indigo']}"/>
  <path d="{title_d}" fill="{c['ink']}"/>
</svg>
'''


SECTIONS = [("01", "About"), ("02", "Projects"), ("03", "Tech stack"),
            ("04", "Stats"), ("05", "Recent"), ("06", "Activity")]

for theme in THEMES:
    write(f"banner-{theme}.svg", banner(theme))
    for num, label in SECTIONS:
        write(f"h{num}-{theme}.svg", header(num, label, theme))

print("ok", sorted(os.listdir(OUT)))
