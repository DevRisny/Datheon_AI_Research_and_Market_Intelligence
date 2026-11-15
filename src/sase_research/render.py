"""HTML -> PDF rendering with a shared editorial stylesheet (Chromium via Playwright)."""

from __future__ import annotations

import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

from . import CHARTS, OUT

AUTHOR = "Risny Suha"
PROGRAM = "Datheon AI Research &amp; Market Intelligence Internship · DT-2026-P5IEX"
DATE = "November 2026"

CSS = """
@page { size: A4; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Inter', sans-serif; font-size: 9.6pt; line-height: 1.55; color: #1d2430; margin: 0; }
h1, h2, h3 { font-family: 'Lora', serif; color: #0f2a44; line-height: 1.2; }
h1 { font-size: 25pt; margin: 0 0 6pt; font-weight: 600; letter-spacing: -0.2pt; }
h2 { font-size: 15pt; margin: 18pt 0 6pt; font-weight: 600; padding-top: 6pt; border-top: 1.5pt solid #2a78d6; }
h2 .n { color: #2a78d6; margin-right: 6pt; }
h3 { font-size: 11.2pt; margin: 12pt 0 4pt; font-weight: 600; }
p { margin: 0 0 7pt; }
.lead { font-size: 11pt; color: #33404f; line-height: 1.5; }
.kicker { font-size: 8pt; letter-spacing: 1.4pt; text-transform: uppercase; color: #2a78d6; font-weight: 700; margin-bottom: 6pt; }
.meta { font-size: 8.5pt; color: #5b6676; margin-top: 8pt; }
.cover { background: linear-gradient(135deg, #f2f7fd 0%, #fbfcfe 60%, #eef6f2 100%); border: 1pt solid #dde6f0;
         border-radius: 8pt; padding: 22pt 24pt 18pt; margin-bottom: 14pt; }
.cover.full { min-height: 250mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
.cover.full h1 { font-size: 34pt; }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin: 10pt 0 12pt; }
.tiles.t3 { grid-template-columns: repeat(3, 1fr); }
.tile { background: #fff; border: 1pt solid #e1e6ee; border-radius: 6pt; padding: 8pt 9pt; }
.tile b { display: block; font-family: 'Lora', serif; font-size: 17pt; color: #0f2a44; line-height: 1.1; }
.tile span { font-size: 7.8pt; color: #5b6676; line-height: 1.3; display: block; margin-top: 3pt; }
.callout { background: #f3f7fc; border-left: 3pt solid #2a78d6; padding: 8pt 11pt; border-radius: 0 6pt 6pt 0; margin: 8pt 0 10pt; }
.callout.green { background: #f0f8f4; border-left-color: #1baf7a; }
.callout.orange { background: #fdf4ef; border-left-color: #eb6834; }
.callout b:first-child { color: #0f2a44; }
figure { margin: 8pt 0 10pt; page-break-inside: avoid; }
figure img { width: 100%; display: block; border-radius: 4pt; }
figure.half img { width: 72%; margin: 0 auto; }
figcaption { font-size: 7.8pt; color: #6b7482; margin-top: 3pt; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0 10pt; font-size: 8.3pt; }
tr { page-break-inside: avoid; }
h2, h3 { break-after: avoid; page-break-after: avoid; }
th { background: #0f2a44; color: #fff; text-align: left; font-weight: 600; padding: 5pt 6pt; }
td { padding: 4.5pt 6pt; border-bottom: 0.6pt solid #e3e7ee; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fc; }
td.r, th.r { text-align: right; font-variant-numeric: tabular-nums; }
ul, ol { margin: 0 0 8pt; padding-left: 15pt; }
li { margin-bottom: 3pt; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 14pt; }
.swot { display: grid; grid-template-columns: 1fr 1fr; gap: 6pt; margin: 4pt 0 12pt; page-break-inside: avoid; }
.swot div { border-radius: 6pt; padding: 7pt 9pt; font-size: 8.2pt; }
.swot h4 { margin: 0 0 3pt; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.8pt; }
.swot ul { padding-left: 12pt; margin: 0; }
.s { background: #eef4fc; } .w { background: #fdf2ec; } .o { background: #ecf7f2; } .t { background: #f6f1fb; }
.rec { border: 1pt solid #dfe6ef; border-radius: 7pt; padding: 10pt 12pt; margin: 8pt 0; page-break-inside: avoid; }
.rec .num { display: inline-block; background: #2a78d6; color: #fff; border-radius: 50%; width: 18pt; height: 18pt;
            text-align: center; line-height: 18pt; font-weight: 700; margin-right: 6pt; font-size: 9pt; }
.rec h3 { display: inline; }
.tag { display: inline-block; font-size: 7.2pt; padding: 1pt 6pt; border-radius: 8pt; background: #eef4fc; color: #1b5aa6;
       margin-right: 4pt; font-weight: 600; }
sup.c { color: #2a78d6; font-size: 6.5pt; font-weight: 600; margin-left: 1pt; }
.refs { font-size: 7.6pt; color: #3d4756; padding-left: 16pt; }
.refs li { margin-bottom: 2.5pt; word-break: break-all; }
.refs span { word-break: normal; }
.refs a { color: #2a78d6; text-decoration: none; }
.small { font-size: 8pt; color: #5b6676; }
.toc { columns: 2; font-size: 9.5pt; }
.toc div { padding: 3pt 0; border-bottom: 0.6pt dotted #c9d2de; break-inside: avoid; }
.pb { page-break-before: always; }
.avoid { page-break-inside: avoid; }
"""

HEADER = "<div style='font-size:7px;width:100%;padding:0 18mm;color:#8a93a1;font-family:Inter;text-align:right'>{title}</div>"
FOOTER = ("<div style='font-size:7px;width:100%;padding:0 18mm;color:#8a93a1;font-family:Inter;display:flex;"
          "justify-content:space-between'><span>" + AUTHOR + " · Datheon DT-2026-P5IEX · " + DATE +
          "</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>")


def img(name: str) -> str:
    data = base64.b64encode((CHARTS / f"{name}.png").read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def fig(name: str, caption: str, cls: str = "") -> str:
    return f"<figure class='{cls}'><img src='{img(name)}'><figcaption>{caption}</figcaption></figure>"


def page(title: str, body: str) -> str:
    return f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"


def to_pdf(html: str, out_name: str, title: str, landscape_deck: bool = False) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    html_path = OUT / "html" / f"{out_name}.html"
    html_path.parent.mkdir(exist_ok=True)
    html_path.write_text(html, encoding="utf-8")
    pdf = OUT / f"{out_name}.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(html_path.as_uri())
        pg.wait_for_timeout(300)
        if landscape_deck:
            pg.pdf(path=str(pdf), width="1280px", height="720px", print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        else:
            pg.pdf(path=str(pdf), format="A4", print_background=True, display_header_footer=True,
                   header_template=HEADER.format(title=title), footer_template=FOOTER,
                   margin={"top": "19mm", "bottom": "17mm", "left": "18mm", "right": "18mm"})
        b.close()
    return pdf
