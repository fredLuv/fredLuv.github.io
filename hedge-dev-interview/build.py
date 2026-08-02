#!/usr/bin/env python3
"""Build the Markdown field guide into dependency-free static HTML pages."""

from __future__ import annotations

import argparse
import html
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import markdown


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
SUMMARY = SOURCE / "SUMMARY.md"


@dataclass(frozen=True)
class NavItem:
    group: str
    title: str
    source_path: Path


def output_path(source_path: Path) -> Path:
    relative = source_path.relative_to(SOURCE)
    if relative.name == "README.md":
        return ROOT / relative.parent / "index.html"
    return ROOT / relative.with_suffix(".html")


def parse_navigation() -> list[NavItem]:
    group = "Guide"
    items: list[NavItem] = []
    for line in SUMMARY.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            group = line.removeprefix("## ").strip()
            continue
        match = re.match(r"\* \[([^]]+)]\(([^)]+)\)", line)
        if match:
            title, target = match.groups()
            items.append(NavItem(group, title, (SOURCE / target).resolve()))
    return items


def page_title(source_path: Path, text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else source_path.stem.replace("-", " ").title()


def description(text: str) -> str:
    body = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body)]
    for paragraph in paragraphs:
        if paragraph and not paragraph.startswith(("#", "|", "-", "*", ">")):
            plain = re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", paragraph)
            plain = re.sub(r"[`*_]", "", plain).replace("\n", " ")
            return plain[:155]
    return "A three-day field guide for quant developer interviews."


def relative_url(from_output: Path, to_output: Path) -> str:
    return Path(os.path.relpath(to_output, from_output.parent)).as_posix()


def rewrite_links(rendered: str, source_path: Path, page_output: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        raw = html.unescape(match.group(1))
        parts = urlsplit(raw)
        if parts.scheme or raw.startswith(("//", "mailto:")):
            return f'href="{html.escape(raw, quote=True)}" target="_blank" rel="noopener noreferrer"'
        if raw.startswith("#") or not parts.path:
            return match.group(0)
        if not parts.path.endswith(".md"):
            return match.group(0)
        target_source = (source_path.parent / parts.path).resolve()
        try:
            target_source.relative_to(SOURCE)
        except ValueError as exc:
            raise ValueError(f"link leaves source tree: {source_path}: {raw}") from exc
        target_output = output_path(target_source)
        rewritten = urlunsplit(("", "", relative_url(page_output, target_output), parts.query, parts.fragment))
        return f'href="{html.escape(rewritten, quote=True)}"'

    return re.sub(r'href="([^"]+)"', replace, rendered)


def navigation_html(items: list[NavItem], page_output: Path, current: Path) -> str:
    groups: list[str] = []
    by_group: dict[str, list[NavItem]] = {}
    for item in items:
        if item.group not in by_group:
            groups.append(item.group)
            by_group[item.group] = []
        by_group[item.group].append(item)

    sections = []
    for group in groups:
        links = []
        for item in by_group[group]:
            target = output_path(item.source_path)
            active = item.source_path == current
            links.append(
                f'<a class="nav-link{" is-active" if active else ""}" '
                f'href="{html.escape(relative_url(page_output, target), quote=True)}" '
                f'data-search="{html.escape((group + " " + item.title).lower(), quote=True)}">'
                f'<span>{html.escape(item.title)}</span></a>'
            )
        sections.append(
            f'<section class="nav-section"><h2>{html.escape(group)}</h2>'
            f'<div class="nav-items">{"".join(links)}</div></section>'
        )
    return "".join(sections)


def neighbors(items: list[NavItem], source_path: Path, page_output: Path) -> str:
    index = next((i for i, item in enumerate(items) if item.source_path == source_path), None)
    if index is None:
        return ""

    links = []
    if index > 0:
        previous = items[index - 1]
        links.append(
            f'<a class="page-turn previous" href="{relative_url(page_output, output_path(previous.source_path))}">'
            f'<small>Previous</small><strong>{html.escape(previous.title)}</strong></a>'
        )
    if index + 1 < len(items):
        following = items[index + 1]
        links.append(
            f'<a class="page-turn next" href="{relative_url(page_output, output_path(following.source_path))}">'
            f'<small>Next</small><strong>{html.escape(following.title)}</strong></a>'
        )
    return f'<nav class="page-turns" aria-label="Chapter navigation">{"".join(links)}</nav>'


def render_page(source_path: Path, items: list[NavItem]) -> None:
    text = source_path.read_text(encoding="utf-8")
    title = page_title(source_path, text)
    page_output = output_path(source_path)
    page_output.parent.mkdir(parents=True, exist_ok=True)

    engine = markdown.Markdown(
        extensions=["fenced_code", "tables", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False, "slugify": lambda value, separator: re.sub(r"[^a-z0-9]+", separator, value.lower()).strip(separator)}},
        output_format="html5",
    )
    article = rewrite_links(engine.convert(text), source_path, page_output)
    style_url = relative_url(page_output, ROOT / "styles.css")
    script_url = relative_url(page_output, ROOT / "app.js")
    home_url = relative_url(page_output, ROOT / "index.html")
    repo_url = "https://github.com/fredLuv/fredLuv.github.io/tree/main/hedge-dev-interview/source"
    current_item = next((item for item in items if item.source_path == source_path), None)
    group = current_item.group if current_item else "Reference"
    coordinate = items.index(current_item) + 1 if current_item else 0
    home_intro = ""
    body_class = ""
    if source_path == SOURCE / "README.md":
        body_class = " home-page"
        home_intro = (
            '<div class="briefing-strip" aria-label="Course summary">'
            '<span><b>03</b> focused days</span><span><b>12</b> core chapters</span>'
            '<span><b>07</b> tested Python checks</span></div>'
        )

    document = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; base-uri 'self'; object-src 'none'; form-action 'self'; img-src 'self' data: https:; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; connect-src 'self'; upgrade-insecure-requests">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="description" content="{html.escape(description(text), quote=True)}">
  <title>{html.escape(title)} | Hedge Dev Field Guide</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Newsreader:opsz,wght@6..72,500;6..72,650;6..72,750&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{style_url}">
  <script src="{script_url}" defer></script>
</head>
<body class="docs{body_class}">
  <div class="reading-progress" aria-hidden="true"><span></span></div>
  <header class="topbar">
    <button class="menu-button" type="button" aria-label="Open navigation" aria-expanded="false"><span></span><span></span></button>
    <a class="wordmark" href="{home_url}"><span>EL/</span> FIELD GUIDE</a>
    <div class="topbar-meta"><span>QRT · HK</span><span>PYTHON TRACK</span></div>
    <a class="portfolio-link" href="{relative_url(page_output, ROOT.parent / 'index.html')}">Portfolio ↗</a>
  </header>
  <aside class="sidebar" aria-label="Book navigation">
    <div class="sidebar-head">
      <p>Quant Developer Interview</p>
      <h1>Three-Day<br>Field Manual</h1>
      <label class="search-label"><span>Find a chapter</span><input id="chapter-search" type="search" placeholder="Press / to search" autocomplete="off"></label>
    </div>
    <nav class="chapter-nav">{navigation_html(items, page_output, source_path)}</nav>
    <div class="sidebar-foot"><a href="{repo_url}" target="_blank" rel="noopener noreferrer">Source on GitHub ↗</a><span>v1 · Aug 2026</span></div>
  </aside>
  <button class="nav-scrim" type="button" aria-label="Close navigation"></button>
  <main class="reading-pane">
    <div class="content-shell">
      <div class="page-coordinate"><span>{html.escape(group)}</span><span>{coordinate:02d}/{len(items):02d}</span></div>
      {home_intro}
      <article class="prose">{article}</article>
      {neighbors(items, source_path, page_output)}
      <footer class="book-footer"><span>Built as an extensible interview system.</span><a href="{home_url}">Return to index ↑</a></footer>
    </div>
  </main>
</body>
</html>
'''
    document = re.sub(r"(?m)^[ \t]+$", "", document)
    page_output.write_text(document, encoding="utf-8")


def clean_generated() -> None:
    for path in ROOT.rglob("*.html"):
        path.unlink()
    for directory in sorted((p for p in ROOT.iterdir() if p.is_dir() and p.name != "source"), reverse=True):
        if directory.name.startswith("."):
            continue
        for child in sorted(directory.rglob("*"), reverse=True):
            if child.is_dir() and not any(child.iterdir()):
                child.rmdir()


def validate(items: list[NavItem]) -> None:
    missing = [item.source_path for item in items if not item.source_path.exists()]
    if missing:
        raise FileNotFoundError(f"missing summary targets: {missing}")
    outputs = [output_path(item.source_path) for item in items]
    if len(outputs) != len(set(outputs)):
        raise ValueError("duplicate navigation output")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate inputs without building")
    args = parser.parse_args()

    items = parse_navigation()
    validate(items)
    if args.check:
        print(f"validated {len(items)} navigation entries")
        return 0

    clean_generated()
    markdown_sources = sorted(
        path for path in SOURCE.rglob("*.md") if path.name != "SUMMARY.md"
    )
    for source_path in markdown_sources:
        render_page(source_path, items)
    print(f"built {len(markdown_sources)} pages from {SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
