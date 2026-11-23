"""Render the neofetch-style profile card (dark + light SVG) with live GitHub stats.

Run locally:   GITHUB_TOKEN=$(gh auth token) python scripts/card.py
In Actions:    see .github/workflows/card.yml (uses the built-in GITHUB_TOKEN)
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from html import escape

USER = os.environ.get("GH_USER", "poggymacello")

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC) { totalCount }
    repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST]) { totalCount }
    pullRequests { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions }
    }
  }
}
"""


def fetch_stats():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": "bearer " + os.environ["GITHUB_TOKEN"]},
    )
    u = json.load(urllib.request.urlopen(req))["data"]["user"]
    cc = u["contributionsCollection"]
    return {
        "created": datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00")),
        "repos": u["repositories"]["totalCount"],
        "contributed": u["repositoriesContributedTo"]["totalCount"],
        "prs": u["pullRequests"]["totalCount"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "contribs": cc["contributionCalendar"]["totalContributions"],
    }


def uptime(since):
    now = datetime.now(timezone.utc)
    months = (now.year - since.year) * 12 + now.month - since.month
    if now.day < since.day:
        months -= 1
    y, m = divmod(months, 12)
    anchor_month = since.month + months
    anchor = since.replace(year=since.year + (anchor_month - 1) // 12, month=(anchor_month - 1) % 12 + 1)
    d = (now - anchor).days
    return f"{y} years, {m} months, {d} days"


# ---- left side: a DIP chip, because EE ------------------------------------
CHIP = """
            │ │ │ │ │ │ │ │
          ┌─┴─┴─┴─┴─┴─┴─┴─┴─┐
   ○──────┤ ●               ├──────○
   ○──────┤                 ├──────○
     ┌────┤  POGGY          ├────┐
     │  ──┤  MACELLO        ├──  │
     │  ──┤  ─────────────  ├──  │
     │  ──┤  AI-SEC  0x7E9  ├──  │
     │  ──┤  rev 2026 · ITB ├──  │
     └────┤                 ├────┘
   ○──────┤                 ├──────○
   ○──────┤                 ├──────○
          └─┬─┬─┬─┬─┬─┬─┬─┬─┘
            │ │ │ │ │ │ │ │
""".strip("\n").split("\n")
CHIP_ACCENT = ("POGGY", "MACELLO")  # words drawn in the accent colour

W = 60  # characters in a right-side row


def row(key, value):
    """'Key: ······ value' with faint dot leaders to a fixed width."""
    head = f"{key}:"
    dots = W - len(head) - len(value) - 2
    return [("k", head), ("d", " " + "·" * max(dots, 1) + " "), ("v", value)]


def section(title):
    return [("t", title), ("d", " " + "─" * (W - len(title) - 1))]


def build_rows(s):
    return [
        [("k", "poggy"), ("m", "@"), ("t", "macello")],
        [("d", "─" * W)],
        row("OS", "Electrical Engineering, ITB"),
        row("Host", "Bandung, Indonesia"),
        row("Uptime", uptime(s["created"])),
        row("Kernel", "AI security · ML for cyber defense"),
        row("Shell", "Python, C/C++, Solidity, JavaScript"),
        row("Stack", "FastAPI, Docker, Kubernetes, sklearn"),
        row("Hobbies", "Hackathons, analog IC design"),
        row("Motto", "the model proposes, the rules decide"),
        [],
        section("Contact"),
        row("LinkedIn", "in/poggymacello"),
        row("Email", "gultompoggy@gmail.com"),
        [],
        section("GitHub"),
        row("Repos", f"{s['repos']} public · contributed to {s['contributed']}"),
        row("Commits", f"{s['commits']:,} this year · {s['prs']} PRs"),
        row("Contributions", f"{s['contribs']:,} in the last year"),
    ]


# Soft palette: pink keys, purple headings, low-contrast leaders.
THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", art="#6e7681", accent="#f778ba",
                 k="#f778ba", v="#e6edf3", d="#30363d", t="#bc8cff", m="#8b949e", title="#8b949e"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", art="#8c959f", accent="#bf3989",
                  k="#bf3989", v="#1f2328", d="#d8dee4", t="#8250df", m="#6e7781", title="#6e7781"),
}
BLOCKS = ["#f778ba", "#d2a8ff", "#a5d6ff", "#7ee787", "#ffa657", "#ff7b72"]


def art_line(line, c):
    out, rest = [], line
    while rest:
        hits = [(rest.find(w), w) for w in CHIP_ACCENT if w in rest]
        if not hits:
            out.append(("art", rest)); break
        i, w = min(hits)
        if i: out.append(("art", rest[:i]))
        out.append(("accent", w)); rest = rest[i + len(w):]
    return "".join(f'<tspan fill="{c[k]}">{escape(t)}</tspan>' for k, t in out)


def render(theme, rows):
    c = THEMES[theme]
    fs, lh, cw = 14, 22, 8.45
    bar_h = 36
    art_x, text_x = 34, 380
    top = bar_h + 34
    body_h = max(len(CHIP), len(rows) + 1) * lh
    height = top + body_h + 18
    width = int(text_x + W * cw + 40)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, \'SF Mono\', '
        f'Menlo, Consolas, \'Liberation Mono\', monospace" font-size="{fs}px">',
        "<style>.a{animation:f .6s ease-out both}@keyframes f{from{opacity:0;transform:translateY(3px)}"
        "to{opacity:1;transform:none}}@media (prefers-reduced-motion: reduce){.a{animation:none}}</style>",
        f'<clipPath id="r"><rect width="{width}" height="{height}" rx="12"/></clipPath>',
        f'<g clip-path="url(#r)"><rect width="{width}" height="{height}" fill="{c["bg"]}"/>',
        f'<rect width="{width}" height="{bar_h}" fill="{c["bar"]}"/>',
        f'<line x1="0" y1="{bar_h}" x2="{width}" y2="{bar_h}" stroke="{c["border"]}"/></g>',
        f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12" fill="none" stroke="{c["border"]}"/>',
    ]
    for j, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        out.append(f'<circle cx="{20 + j*20}" cy="{bar_h/2}" r="6" fill="{col}"/>')
    out.append(f'<text x="{width/2}" y="{bar_h/2 + 4.5}" text-anchor="middle" fill="{c["title"]}" '
               f'font-size="12.5px">poggy@macello: ~ — neofetch</text>')
    art_top = top + (body_h - len(CHIP) * lh) // 2
    for i, line in enumerate(CHIP):
        out.append(f'<text x="{art_x}" y="{art_top + i*lh}" xml:space="preserve">{art_line(line, c)}</text>')
    for i, parts in enumerate(rows):
        if not parts:
            continue
        spans = "".join(f'<tspan fill="{c[k]}">{escape(t)}</tspan>' for k, t in parts)
        out.append(f'<text class="a" style="animation-delay:{i*40}ms" x="{text_x}" y="{top + i*lh}" '
                   f'xml:space="preserve">{spans}</text>')
    by = top + len(rows) * lh - 6
    for j, col in enumerate(BLOCKS):
        out.append(f'<rect class="a" style="animation-delay:{len(rows)*40 + j*50}ms" x="{text_x + j*34}" '
                   f'y="{by}" width="28" height="12" rx="6" fill="{col}"/>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    stats = fetch_stats()
    rows = build_rows(stats)
    root = os.path.join(os.path.dirname(__file__), "..")
    for theme in THEMES:
        with open(os.path.join(root, f"card-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(render(theme, rows))
    print("card rendered:", stats)


if __name__ == "__main__":
    main()
