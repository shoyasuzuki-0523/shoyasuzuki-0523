#!/usr/bin/env python3
"""GitHub GraphQL API からデータを取得し、プロフィール用の SVG カードを生成する。

外部のカード生成サービスに依存しないよう、標準ライブラリのみで実装している。
使い方: GITHUB_TOKEN=... python3 generate_cards.py <username> <output_dir> [pinned repo ...]
"""
import json
import os
import sys
import urllib.request
from collections import defaultdict
from xml.sax.saxutils import escape

# tokyonight テーマ
BG = "#1a1b27"
TITLE = "#70a5fd"
TEXT = "#a9b1d6"
ACCENT = "#38bdae"
ICON = "#bf91f3"
BORDER = "#2a2e45"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif"

# 言語カードの集計から除外するもの。
# Unity / Flutter のテンプレートや自動生成コード、マークアップ言語が割合を歪めるため。
EXCLUDE_LANGS = {
    "HTML", "CSS", "SCSS", "ShaderLab", "HLSL", "GLSL", "Makefile", "CMake", "Dockerfile",
    "Objective-C", "Swift", "Kotlin", "C", "C++",
}
EXCLUDE_REPOS = {"FirstGame", "test_game"}
# 行頭に来てはいけない文字（禁則処理）
NO_LINE_START = set("、。，．・：；？！）」』】〕＞ー…,.)!?:;")

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    login
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        name
        description
        stargazerCount
        forkCount
        primaryLanguage { name color }
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]["user"]


def text_width(s: str, size: float) -> float:
    """全角文字を考慮したおおよその描画幅。"""
    return sum(size if ord(c) > 0x2E80 else size * 0.55 for c in s)


def truncate(s: str, size: float, max_width: float) -> str:
    if text_width(s, size) <= max_width:
        return s
    while s and text_width(s + "…", size) > max_width:
        s = s[:-1]
    return s + "…"


def wrap(s: str, size: float, max_width: float, max_lines: int) -> list:
    lines, cur = [], ""
    for c in s:
        if text_width(cur + c, size) > max_width and c not in NO_LINE_START:
            lines.append(cur)
            cur = c
            if len(lines) == max_lines:
                break
        else:
            cur += c
    else:
        lines.append(cur)
        return lines
    lines[-1] = truncate(lines[-1] + s, size, max_width)
    return lines[:max_lines]


def frame(width: int, height: int, title: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title, {'"': '&quot;'})}">
<style>
  .title {{ font: 600 18px {FONT}; fill: {TITLE}; }}
  .label {{ font: 600 14px {FONT}; fill: {TEXT}; }}
  .value {{ font: 700 14px {FONT}; fill: {ACCENT}; }}
  .small {{ font: 400 12px {FONT}; fill: {TEXT}; }}
  .fade {{ animation: fadeIn .6s ease-in-out backwards; }}
  @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
</style>
<rect x="0.5" y="0.5" rx="6" width="{width - 1}" height="{height - 1}" fill="{BG}" stroke="{BORDER}"/>
<text x="25" y="35" class="title">{escape(title)}</text>
{body}
</svg>
"""


def stats_card(user: dict) -> str:
    repos = user["repositories"]["nodes"]
    cc = user["contributionsCollection"]
    calendar = cc["contributionCalendar"]
    rows = [
        ("⬆", "Contributions (1y)", calendar["totalContributions"]),
        ("⇄", "Total PRs", user["pullRequests"]["totalCount"]),
        ("!", "Total Issues", user["issues"]["totalCount"]),
        ("▣", "Public Repos", user["repositories"]["totalCount"]),
        ("★", "Total Stars", sum(r["stargazerCount"] for r in repos)),
        ("♥", "Followers", user["followers"]["totalCount"]),
    ]
    body = []
    for i, (icon, label, value) in enumerate(rows):
        y = 65 + i * 22
        body.append(
            f'<g class="fade" style="animation-delay:{150 + i * 120}ms">'
            f'<text x="25" y="{y}" class="label" fill="{ICON}" style="fill:{ICON}">{escape(icon)}</text>'
            f'<text x="48" y="{y}" class="label">{escape(label)}:</text>'
            f'<text x="250" y="{y}" class="value">{value:,}</text></g>'
        )
    # 過去 1 年でコントリビューションがあった日数のリング
    days = [d for w in calendar["weeks"] for d in w["contributionDays"]]
    active = sum(1 for d in days if d["contributionCount"] > 0)
    circumference = 282.74
    offset = circumference * (1 - active / max(len(days), 1))
    body.append(
        f'<g transform="translate(375,115)" class="fade" style="animation-delay:200ms">'
        f'<circle r="45" fill="none" stroke="{BORDER}" stroke-width="6"/>'
        f'<circle r="45" fill="none" stroke="{TITLE}" stroke-width="6" stroke-linecap="round" '
        f'stroke-dasharray="{circumference}" stroke-dashoffset="{offset:.2f}" transform="rotate(-90)"/>'
        f'<text y="6" text-anchor="middle" class="title" style="fill:{ACCENT}">{active}</text>'
        f'<text y="64" text-anchor="middle" class="small">active days / 1y</text></g>'
    )
    name = user["name"] or user["login"]
    return frame(470, 205, f"{name}'s GitHub Stats", "\n".join(body))


def langs_card(user: dict, limit: int = 8) -> str:
    sizes, counts, colors = defaultdict(int), defaultdict(int), {}
    for r in user["repositories"]["nodes"]:
        if r["name"] in EXCLUDE_REPOS:
            continue
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            if name in EXCLUDE_LANGS:
                continue
            sizes[name] += e["size"]
            counts[name] += 1
            colors[name] = e["node"]["color"] or "#858585"
    # 巨大な 1 リポジトリに引っ張られないよう、サイズとリポジトリ数の幾何平均で重み付けする
    scores = {name: (sizes[name] * counts[name]) ** 0.5 for name in sizes}
    top = sorted(scores.items(), key=lambda kv: -kv[1])[:limit]
    total = sum(v for _, v in top) or 1
    body, x = [f'<clipPath id="bar"><rect x="25" y="55" width="300" height="8" rx="4"/></clipPath><g clip-path="url(#bar)">'], 25.0
    for name, size in top:
        w = 300 * size / total
        body.append(f'<rect x="{x:.2f}" y="55" width="{w:.2f}" height="8" fill="{colors[name]}"/>')
        x += w
    body.append("</g>")
    for i, (name, size) in enumerate(top):
        cx, cy = 25 + (i % 2) * 155, 90 + (i // 2) * 25
        body.append(
            f'<g class="fade" style="animation-delay:{150 + i * 120}ms">'
            f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{colors[name]}"/>'
            f'<text x="{cx + 15}" y="{cy}" class="small">{escape(name)} {100 * size / total:.1f}%</text></g>'
        )
    return frame(350, 205, "Most Used Languages", "\n".join(body))


def activity_card(user: dict, days: int = 31) -> str:
    cal = [d for w in user["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    cal = cal[-days:]
    counts = [d["contributionCount"] for d in cal]
    peak = max(-(-max(counts) // 4) * 4, 4)  # 目盛りが整数になるよう 4 の倍数に切り上げ
    W, H, L, R, T, B = 1000, 320, 60, 30, 60, 50
    pw, ph = W - L - R, H - T - B
    pts = [(L + pw * i / (len(counts) - 1), T + ph * (1 - c / peak)) for i, c in enumerate(counts)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{L},{T + ph} {line} {L + pw},{T + ph}"
    body = [
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{TITLE}" stop-opacity="0.5"/>'
        f'<stop offset="100%" stop-color="{TITLE}" stop-opacity="0"/></linearGradient></defs>'
    ]
    for i in range(5):
        y = T + ph * i / 4
        body.append(f'<line x1="{L}" x2="{L + pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="{BORDER}"/>')
        body.append(f'<text x="{L - 10}" y="{y + 4:.1f}" text-anchor="end" class="small">{round(peak * (1 - i / 4))}</text>')
    body.append(f'<polygon points="{area}" fill="url(#g)"/>')
    body.append(f'<polyline points="{line}" fill="none" stroke="{TITLE}" stroke-width="2.5" stroke-linejoin="round"/>')
    for (x, y), d in zip(pts, cal):
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{ACCENT}"><title>{d["date"]}: {d["contributionCount"]}</title></circle>')
    for i in range(0, len(cal), 5):
        x, _ = pts[i]
        body.append(f'<text x="{x:.1f}" y="{H - 20}" text-anchor="middle" class="small">{cal[i]["date"][5:].replace("-", "/")}</text>')
    name = user["name"] or user["login"]
    return frame(W, H, f"{name}'s Contribution Graph (last {days} days)", "\n".join(body))


def repo_card(repo: dict) -> str:
    desc = repo["description"] or "No description provided"
    lines = wrap(desc, 13, 350, 2)
    body = [f'<text x="25" y="{62 + i * 18}" class="small" style="font-size:13px">{escape(l)}</text>' for i, l in enumerate(lines)]
    x = 25
    lang = repo["primaryLanguage"]
    if lang:
        body.append(f'<circle cx="{x + 6}" cy="{106}" r="6" fill="{lang["color"] or "#858585"}"/>')
        body.append(f'<text x="{x + 18}" y="110" class="small">{escape(lang["name"])}</text>')
        x += 30 + text_width(lang["name"], 12)
    body.append(f'<text x="{x}" y="110" class="small">★ {repo["stargazerCount"]}</text>')
    body.append(f'<text x="{x + 50}" y="110" class="small">⑂ {repo["forkCount"]}</text>')
    return frame(400, 130, truncate(repo["name"], 18, 350), "\n".join(body))


def main() -> None:
    login, out, pinned = sys.argv[1], sys.argv[2], sys.argv[3:]
    user = fetch(login, os.environ["GITHUB_TOKEN"])
    os.makedirs(out, exist_ok=True)
    cards = {
        "stats.svg": stats_card(user),
        "top-langs.svg": langs_card(user),
        "activity-graph.svg": activity_card(user),
    }
    repos = {r["name"]: r for r in user["repositories"]["nodes"]}
    for name in pinned:
        if name in repos:
            cards[f"repo-{name}.svg"] = repo_card(repos[name])
        else:
            print(f"warning: repository not found: {name}", file=sys.stderr)
    for filename, svg in cards.items():
        with open(os.path.join(out, filename), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"generated {filename}")


if __name__ == "__main__":
    main()
