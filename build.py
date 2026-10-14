#!/usr/bin/env python3
"""Rakentaa index.html:n news.json-tiedostosta. Käyttö: python3 build.py"""
import json, html, os
from datetime import datetime
D = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(D, "news.json"), encoding="utf-8"))
SECTIONS = [("auto", "FSD, TAD ja autonomia"), ("tuote", "Tuotteet – Roadster"),
            ("eurooppa", "Eurooppa ja Suomi"), ("yritys", "Yritys ja osake")]
def fmt(s):
    d = datetime.fromisoformat(s[:16]); return f"{d.day}.{d.month}.{d.year} klo {d:%H.%M}"
def card(i):
    e = html.escape
    flag = f'<span class="flag">{e(i["flag"])}</span>' if i.get("flag") else ""
    return (f'<article><div class="meta">{e(i["source"])} · {fmt(i["date"])} {flag}</div>'
            f'<h3><a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["title"])}</a></h3>'
            f'<p>{e(i["summary"])}</p></article>')
body = ""
for key, name in SECTIONS:
    its = sorted([i for i in data["items"] if i["cat"] == key], key=lambda i: i["date"], reverse=True)
    if its:
        cls = " top" if key == "auto" else ""
        body += f'<section class="sec{cls}"><h2>{name} <small>({len(its)})</small></h2>' + "".join(map(card, its)) + "</section>"
upd = fmt(data["updated"])
page = f"""<!doctype html><html lang="fi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Tesla-uutiset</title>
<style>
:root{{--bg:#0b0b0c;--card:#17181a;--txt:#e8e8e8;--mut:#9a9ca0;--red:#e82127}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--txt);font:16px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
header{{padding:28px 18px 10px;max-width:860px;margin:auto;border-bottom:1px solid #222}}
h1{{margin:0;font-weight:600;letter-spacing:.18em;text-transform:uppercase;font-size:1.5rem}}
h1 span{{color:var(--red)}}.upd{{color:var(--mut);font-size:.85rem;margin-top:6px}}
main{{max-width:860px;margin:auto;padding:0 14px 40px}}
h2{{font-weight:500;font-size:1.15rem;margin:28px 0 12px;padding-left:10px;border-left:3px solid #555}}
.top h2{{border-color:var(--red)}}h2 small{{color:var(--mut);font-weight:400}}
article{{background:var(--card);border-radius:10px;padding:14px 16px;margin:10px 0;border:1px solid #222}}
.top article{{border-color:#3a1517}}
h3{{margin:4px 0 6px;font-size:1.05rem;font-weight:600}}h3 a{{color:var(--txt);text-decoration:none}}h3 a:hover{{color:var(--red)}}
p{{margin:0;color:#c9cacc;font-size:.95rem}}.meta{{color:var(--mut);font-size:.8rem}}
.flag{{background:#5a3b00;color:#ffcc66;border-radius:4px;padding:1px 6px;margin-left:6px;font-size:.72rem}}
footer{{color:var(--mut);font-size:.8rem;text-align:center;padding:20px}}
</style></head><body><header><h1>T<span>E</span>SLA-uutiset</h1>
<div class="upd">Päivitetty {upd} (Helsingin aikaa) · {len(data["items"])} uutista</div></header>
<main>{body}</main><footer>Kooste alkuperäislähteistä. Ajat Helsingin aikaa; kellonaika voi olla likimääräinen.</footer></body></html>"""
open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(page)
print("OK", len(data["items"]))
