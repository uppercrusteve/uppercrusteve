"""Render assets/stats.svg from live GitHub data.

Reads the repository list, public metadata and the latest CI conclusion, then
writes one SVG. No third-party badge services: the card is generated here so it
keeps working when external endpoints are slow or blocked.
"""
from __future__ import annotations

import json
import os
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "uppercrusteve"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"

INK = "#F2EAD8"
MUTED = "#7E8894"
DIM = "#4E5762"
GREEN = "#5FA97C"
RED = "#C25A6A"
BG = "#0E1116"

try:
    import certifi

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()
LINE = "#1E242C"


def get(path: str) -> dict:
    request = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "portfolio-stats",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
        return json.loads(response.read().decode())


def latest_ci(repo: str) -> str:
    try:
        data = get(f"/repos/{OWNER}/{repo}/actions/runs?per_page=1")
        runs = data.get("workflow_runs") or []
        if not runs:
            return "none"
        return str(runs[0].get("conclusion") or runs[0].get("status") or "unknown")
    except Exception:
        return "unknown"


def main() -> int:
    projects = json.loads((ROOT / "_data/projects.json").read_text(encoding="utf-8"))
    rows = []
    stars_total = 0
    green = 0
    for item in projects:
        repo = item["repo"]
        meta = get(f"/repos/{OWNER}/{repo}")
        stars = int(meta.get("stargazers_count", 0))
        stars_total += stars
        ci = latest_ci(repo)
        if ci == "success":
            green += 1
        pushed = datetime.fromisoformat(meta["pushed_at"].replace("Z", "+00:00"))
        days = max(0, (datetime.now(timezone.utc) - pushed).days)
        rows.append((repo, item["blurb"], item["tests"], stars, ci, days))

    tests_total = sum(item["tests"] for item in projects)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    height = 140 + len(rows) * 34 + 38
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-label="Portfolio data: {len(rows)} repositories, {tests_total} tests, {green} green builds">',
        f'<rect width="1280" height="{height}" rx="10" fill="{BG}"/>',
        f'<rect x="0.5" y="0.5" width="1279" height="{height - 1}" rx="10" fill="none" stroke="{LINE}"/>',
        f'<text x="36" y="44" font-family="\'Microsoft YaHei\',sans-serif" font-size="15" fill="{INK}">仓库数据 · 由 Actions 每天生成，不手改</text>',
        f'<text x="36" y="66" font-family="\'Microsoft YaHei\',sans-serif" font-size="12" fill="{MUTED}">最近更新 {stamp}</text>',
    ]

    stats = [
        (str(len(rows)) + " 个仓库", "全部公开"),
        (str(tests_total) + " 项测试", "pytest + vitest"),
        (f"{green}/{len(rows)} CI 通过", "main 分支最近一次"),
        (str(stars_total) + " stars", "实时"),
    ]
    for index, (value, label) in enumerate(stats):
        x = 36 + index * 300
        parts.append(f'<text x="{x}" y="104" font-family="\'Microsoft YaHei\',sans-serif" font-size="19" font-weight="700" fill="{INK}">{value}</text>')
        parts.append(f'<text x="{x}" y="{120}" font-family="\'Microsoft YaHei\',sans-serif" font-size="11" fill="{MUTED}">{label}</text>')

    top = 158
    for index, (repo, blurb, tests, stars, ci, days) in enumerate(rows):
        y = top + index * 34
        if index % 2 == 0:
            parts.append(f'<rect x="28" y="{y - 21}" width="1224" height="30" rx="5" fill="#131820"/>')
        mark, color = {
            "success": ("✓", GREEN),
            "failure": ("✗", RED),
            "none": ("–", DIM),
        }.get(ci, ("·", DIM))
        parts.append(f'<text x="40" y="{y}" font-family="\'Microsoft YaHei\',sans-serif" font-size="13" font-weight="700" fill="{INK}">{repo}</text>')
        parts.append(f'<text x="238" y="{y}" font-family="\'Microsoft YaHei\',sans-serif" font-size="12" fill="{MUTED}">{blurb}</text>')
        parts.append(f'<text x="1010" y="{y}" font-family="\'Microsoft YaHei\',sans-serif" font-size="12" fill="{MUTED}" text-anchor="end">{tests} tests</text>')
        parts.append(f'<text x="1090" y="{y}" font-family="\'Microsoft YaHei\',sans-serif" font-size="12" fill="{MUTED}" text-anchor="end">{stars} ★</text>')
        parts.append(f'<text x="1128" y="{y}" font-family="sans-serif" font-size="13" fill="{color}">{mark}</text>')
        pushed = "今天" if days == 0 else f"{days} 天前"
        parts.append(f'<text x="1224" y="{y}" font-family="\'Microsoft YaHei\',sans-serif" font-size="11" fill="{DIM}" text-anchor="end">{pushed}</text>')

    parts.append(f'<text x="36" y="{height - 16}" font-family="\'Microsoft YaHei\',sans-serif" font-size="11" fill="{DIM}">测试数取自各仓库测试文件，CI 状态取自最近一次工作流运行；星标与推送时间为 GitHub API 实时值。</text>')
    parts.append("</svg>")

    out = ROOT / "assets" / "stats.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {out} ({len(parts)} nodes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
