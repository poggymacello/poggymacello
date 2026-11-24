"""Render an animated chat-bubble intro (chat-light.svg / chat-dark.svg).

Messages "type" in one after another, like a messaging app. Two lines are live:
the weather in Bandung (Open-Meteo, no key needed) and the repo pushed most recently.
Idea credit: jasonlong/jasonlong (Unlicense). Code written from scratch.

Run locally:  GITHUB_TOKEN=$(gh auth token) python scripts/chat.py
"""
import json
import os
import textwrap
import urllib.request
from html import escape

USER = os.environ.get("GH_USER", "poggymacello")
LAT, LON = -6.9175, 107.6191  # Bandung

WMO = {
    0: ("☀️", "clear"), 1: ("🌤️", "mostly clear"), 2: ("⛅", "partly cloudy"), 3: ("☁️", "overcast"),
    45: ("🌫️", "foggy"), 48: ("🌫️", "foggy"),
    51: ("🌦️", "drizzling"), 53: ("🌦️", "drizzling"), 55: ("🌧️", "drizzling"),
    61: ("🌧️", "raining lightly"), 63: ("🌧️", "raining"), 65: ("🌧️", "pouring"),
    80: ("🌦️", "showery"), 81: ("🌧️", "showery"), 82: ("⛈️", "pouring"),
    95: ("⛈️", "stormy"), 96: ("⛈️", "stormy"), 99: ("⛈️", "stormy"),
}


def get_json(url, token=None):
    headers = {"User-Agent": "profile-readme"}
    if token:
        headers["Authorization"] = "bearer " + token
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20))


def weather_line():
    try:
        d = get_json(f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
                     "&current=temperature_2m,weather_code&timezone=Asia%2FJakarta")["current"]
        emoji, words = WMO.get(d["weather_code"], ("🌡️", "doing its thing"))
        return f"It's {round(d['temperature_2m'])}°C and {words} {emoji} in Bandung right now"
    except Exception:
        return "Greetings from Bandung, where it's probably raining 🌧️"


def latest_repo_line():
    try:
        repos = get_json(f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=10",
                         os.environ.get("GITHUB_TOKEN"))
        r = next(r for r in repos if not r["fork"] and r["name"].lower() != USER.lower())
        return f"Latest thing I pushed: {r['name']} 🛠️"
    except Exception:
        return "Latest thing I built: PERISAI-RESPON 🛡️"


def messages():
    return [
        "Hi, I'm Poggy 👋",
        "I study Electrical Engineering at ITB",
        "This year I interned at EY on cyber risk and ISO 27001, and at NTUST in Taiwan, hardening an O-RAN cloud with mTLS and Vault ✈️",
        "Before that: DevSecOps at AssistX, network design at XLSmart, and gas turbine controls at PLN",
        "I also led HME ITB, the EE student association. 550 members, 106 programmes 🫡",
        "These days I build AI that can't be hijacked by the data it reads",
        latest_repo_line(),
        weather_line(),
        "Say hi on LinkedIn: in/poggymacello 💬",
    ]


THEMES = {
    "light": dict(bg="#ffffff", bubble="#e9e9eb", text="#1c1c1e", dot="#8e8e93"),
    "dark": dict(bg="#0d1117", bubble="#262629", text="#f2f2f7", dot="#8e8e93"),
}

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FS, LH = 17, 23          # font size, line height
CW = 8.3                 # rough average glyph width at 17px
WRAP = 42                # characters per bubble line
PAD_X, PAD_Y, GAP = 16, 10, 10
TYPE_S, PAUSE_S = 1.1, 0.35  # typing-indicator duration, gap before next


def render(theme, msgs):
    c = THEMES[theme]
    css = [
        f"text{{font-family:{FONT};font-size:{FS}px;fill:{c['text']};letter-spacing:-0.01em}}",
        f".b{{fill:{c['bubble']}}}.d{{fill:{c['dot']}}}",
        ".m{opacity:0;transform-box:fill-box;transform-origin:0 100%;animation:pop .28s cubic-bezier(.2,.9,.3,1.3) forwards}",
        ".t{opacity:0;animation:typing var(--dur) linear}",
        ".t circle{animation:bounce .9s infinite}.t circle:nth-child(3){animation-delay:.15s}.t circle:nth-child(4){animation-delay:.3s}",
        "@keyframes pop{from{opacity:0;transform:scale(.85)}to{opacity:1;transform:scale(1)}}",
        "@keyframes typing{0%{opacity:0}12%{opacity:1}88%{opacity:1}100%{opacity:0}}",
        "@keyframes bounce{0%,60%,100%{opacity:.35}30%{opacity:1}}",
        "@media (prefers-reduced-motion: reduce){.m{animation:none;opacity:1}.t{display:none}}",
    ]
    body, y, t = [], 16, 0.4
    for msg in msgs:
        lines = textwrap.wrap(msg, WRAP)
        w = max(len(l) for l in lines) * CW + PAD_X * 2
        h = len(lines) * LH + PAD_Y * 2
        # typing indicator at the spot the message will appear
        body.append(
            f'<g class="t" style="animation-delay:{t:.2f}s;--dur:{TYPE_S}s">'
            f'<rect class="b" x="16" y="{y}" width="62" height="38" rx="19"/>'
            + "".join(f'<circle class="d" cx="{34 + i*13}" cy="{y + 19}" r="4"/>' for i in range(3))
            + "</g>")
        t += TYPE_S
        spans = "".join(
            f'<tspan x="{16 + PAD_X}" dy="{0 if i == 0 else LH}">{escape(l)}</tspan>'
            for i, l in enumerate(lines))
        body.append(
            f'<g class="m" style="animation-delay:{t:.2f}s">'
            f'<rect class="b" x="16" y="{y}" width="{w:.0f}" height="{h}" rx="19"/>'
            f'<text x="{16 + PAD_X}" y="{y + PAD_Y + FS}">{spans}</text></g>')
        t += PAUSE_S
        y += h + GAP
    width, height = 560, y + 10
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}"><style>{"".join(css)}</style>'
            f'<rect width="{width}" height="{height}" fill="{c["bg"]}"/>' + "".join(body) + "</svg>")


def main():
    msgs = messages()
    root = os.path.join(os.path.dirname(__file__), "..")
    for theme in THEMES:
        with open(os.path.join(root, f"chat-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(render(theme, msgs))
    print("\n".join(msgs).encode("ascii", "replace").decode())


if __name__ == "__main__":
    main()
