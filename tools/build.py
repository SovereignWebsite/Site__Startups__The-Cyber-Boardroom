#!/usr/bin/env python3
"""Build a startup brochure site from content/facts.json into site/.

Usage: python3 tools/build.py            (run from the repository root)

Every page is static HTML with inline CSS and inline SVG. No scripts, no
cookies, no tracking, no third-party requests. Five designs of the same facts;
facts.json "home" picks which design is also served as index.html.
"""
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, 'content', 'facts.json')
SITE = os.path.join(ROOT, 'site')

DESIGNS = [
    ('brochure',  'The Brochure',  'The company at a glance, with diagrams'),
    ('blueprint', 'The Blueprint', 'A dark technical spec sheet'),
    ('story',     'The Story',     'Told in order, date by date'),
    ('newsroom',  'The Newsroom',  'A magazine feature about the company'),
    ('brief',     'The Brief',     'Plain and printable on A4'),
]

# Startup sites that are live: only these are linked from the others (a link to a site not yet live fails the
# link check). Add a slug here once its site answers, then rebuild every startup site.
LIVE = {'sgit', 'the-cyber-boardroom', 'risk-mandate', 'agentic-cells', 'sovereign-website'}

STARTUPS = [  # the family of startup sites, kept in the same order everywhere
    ('sgit', 'sgit'),
    ('the-cyber-boardroom', 'The Cyber Boardroom'),
    ('risk-mandate', 'RiskMandate'),
    ('agentic-cells', 'AgentiCCells'),
    ('sovereign-website', 'Sovereign Website'),
]

FAMILY = [
    ('Sovereign Website', 'https://sovereignwebsite.ai/'),
    ('Principles', 'https://sovereignwebsite.org/'),
    ('Hosted', 'https://sovereignwebsite.site/'),
    ('Hub', 'https://hub.sovereignweb.site/'),
    ('Agents', 'https://agents.sovereignweb.site/'),
    ('Vault', 'https://vault.sovereignwebsite.site/'),
    ('AgentiCCells', 'https://agenticcells.ai/'),
    ('RiskMandate', 'https://riskmandate.ai/'),
    ('Newsroom', 'https://newsroom.sgit.ai/'),
]

e = lambda s: html.escape(str(s), quote=True)


def load():
    with open(FACTS) as f:
        F = json.load(f)
    if F.get('designs'):
        DESIGNS[:] = [(d['key'], d['name'], d['blurb']) for d in F['designs']]
    F.setdefault('home', DESIGNS[0][0])
    F['_src'] = {s['id']: s for s in F['sources']}
    return F


# ---------------------------------------------------------------- helpers
def cite(F, ids, prefix):
    """Source markers: every source kept, each a 24 px target labelled "source N" (design.b round 1)."""
    if not ids:
        return ''
    out = []
    for i in ids:
        if i not in F['_src']:
            sys.exit(f'unknown source id {i}')
        out.append(f'<a href="#{prefix}src-{i}" class="cite" aria-label="source {i}">{i}</a>')
    return '<sup class="cites">' + ''.join(out) + '</sup>'


def md(text):
    """Tiny inline markup: **bold**, *italic*, [label](url)."""
    t = e(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'\[(.+?)\]\((https?://[^)\s]+)\)', r'<a href="\2">\1</a>', t)
    return t


def fmt_date(d):
    parts = d.split('-')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f'{months[int(parts[1]) - 1]} {parts[0]}'
    return f'{int(parts[2])} {months[int(parts[1]) - 1]} {parts[0]}'


def date_num(d):
    p = [int(x) for x in d.split('-')] + [1, 1]
    return datetime.date(p[0], p[1], p[2]).toordinal()


def rel(depth, path):
    return ('../' * depth) + path


def page_path(key, F):
    return 'index.html' if key == F['home'] else f'designs/{key}.html'



# ---------------------------------------------------------------- the company's own identity
def logo(F, depth, cls='logo', force_plate=False):
    i = F.get('identity') or {}
    if i.get('logo_html'):
        return f'<span class="{cls}" role="img" aria-label="{e(i["logo_alt"])}">{i["logo_html"]}</span>'
    if i.get('logo_img'):
        src = rel(depth, i['logo_img'])
        dark = f'<source srcset="{rel(depth, i["logo_img_dark"])}" media="(prefers-color-scheme: dark)">' if i.get('logo_img_dark') and not force_plate else ''
        img = f'<picture>{dark}<img src="{src}" width="{i["logo_w"]}" height="{i["logo_h"]}" alt="{e(i["logo_alt"])}"></picture>'
        plate = ' plate' if i.get('logo_plate') or force_plate else ''
        return f'<span class="{cls}{plate}">{img}</span>'
    return ''


def shot(F, depth, n=0, cls='shot', lazy=True):
    i = F.get('identity') or {}
    shots = i.get('shots') or []
    if n >= len(shots):
        return ''
    x = shots[n]
    host = re.sub(r'^https?://', '', x['url']).rstrip('/')
    ld = ' loading="lazy" decoding="async"' if lazy else ''
    return (f'<figure class="{cls}"><a href="{e(x["url"])}" class="frame" aria-label="{e(x["caption"])}: open the real page">'
            f'<span class="bar" aria-hidden="true"><i></i><i></i><i></i><span>{e(host)}</span></span>'
            + (f'<picture><source media="(max-width: 40rem)" srcset="{rel(depth, x["phone"])}" width="{x["phone_w"]}" height="{x["phone_h"]}">' if x.get('phone') else '')
            + f'<img src="{rel(depth, x["file"])}" width="1200" height="750" alt="Screenshot: {e(x["caption"])}"{ld}>'
            + ('</picture>' if x.get('phone') else '') + '</a>'
            f'<figcaption>{e(x["caption"])}. Screenshot taken {e(fmt_date(F["updated"]))}; '
            f'<a href="{e(x["url"])}">open the real page &#8599;</a></figcaption></figure>')


def gallery(F, depth, start=0, cls='gallery'):
    shots = (F.get('identity') or {}).get('shots') or []
    if len(shots) <= start:
        return ''
    return f'<div class="{cls}">' + ''.join(shot(F, depth, k) for k in range(start, len(shots))) + '</div>'

# ---------------------------------------------------------------- visuals
def svg_timeline(F, cls='tl-svg'):
    ev = sorted(F.get('timeline', []), key=lambda x: x['date'])
    if len(ev) < 2:
        return ''
    a, b = date_num(ev[0]['date']), date_num(ev[-1]['date'])
    span = max(b - a, 1)
    W, X0, X1, Y = 1000, 40, 960, 74
    marks = []
    rows = [Y - 26, Y + 42, Y - 54, Y + 70]
    last = [-999] * len(rows)
    for n, x in enumerate(ev, 1):
        px = X0 + (date_num(x['date']) - a) / span * (X1 - X0)
        r = next((i for i in range(len(rows)) if px - last[i] > 34), 0)
        last[r] = px
        ty = rows[r]
        marks.append(f'<circle cx="{px:.1f}" cy="{Y}" r="9" class="dot"/>'
                     f'<text x="{px:.1f}" y="{ty}" text-anchor="middle" class="num">{n}</text>')
    y0, y1 = ev[0]['date'][:4], ev[-1]['date'][:4]
    years = ''
    for yr in range(int(y0), int(y1) + 2):
        d = date_num(f'{yr}-01-01')
        if a <= d <= b:
            px = X0 + (d - a) / span * (X1 - X0)
            years += (f'<line x1="{px:.1f}" x2="{px:.1f}" y1="{Y-14}" y2="{Y+14}" class="tick"/>'
                      f'<text x="{px:.1f}" y="{Y+104}" text-anchor="middle" class="yr">{yr}</text>')
    label = (f'Timeline of {len(ev)} dated events from {fmt_date(ev[0]["date"])} '
             f'to {fmt_date(ev[-1]["date"])}; the numbered list below gives each one.')
    return (f'<figure class="{cls}"><svg viewBox="0 0 {W} 185" role="img" aria-label="{e(label)}">'
            f'<line x1="{X0}" x2="{X1}" y1="{Y}" y2="{Y}" class="axis"/>{years}{"".join(marks)}</svg>'
            f'<figcaption>Spaced to scale by date. Drawn for this site from the dates the company publishes.</figcaption></figure>')


def timeline_list(F, prefix, cls='tl-list'):
    ev = sorted(F.get('timeline', []), key=lambda x: x['date'])
    items = ''.join(f'<li><time datetime="{e(x["date"])}">{e(fmt_date(x["date"]))}</time> '
                    f'<span>{md(x["label"])}{cite(F, x.get("s"), prefix)}</span></li>' for x in ev)
    return f'<ol class="{cls}">{items}</ol>'


def svg_map(F, cls='map-svg'):
    prods = F.get('products', [])
    if len(prods) < 2:
        return ''
    import math
    W, H, cx, cy = 760, 520, 380, 260
    rx, ry = 270, 190
    n = len(prods)
    parts = []
    for i, p in enumerate(prods):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
        name = p.get('short', p['name'])
        w = max(130, 18 * len(name) + 40)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" class="spoke"/>')
        parts.append(f'<rect x="{x - w/2:.0f}" y="{y - 26:.0f}" width="{w}" height="52" rx="12" class="node"/>'
                     f'<text x="{x:.0f}" y="{y + 8:.0f}" text-anchor="middle" class="nlabel">{e(name)}</text>')
    hub = F['name']
    hw = max(170, 20 * len(hub) + 50)
    lab = f'{hub} and its parts: ' + ', '.join(p['name'] for p in prods) + '. Each is described below.'
    return (f'<figure class="{cls}"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(lab)}">'
            + ''.join(x for x in parts if x.startswith('<line'))
            + ''.join(x for x in parts if not x.startswith('<line'))
            + f'<rect x="{cx - hw/2:.0f}" y="{cy - 36}" width="{hw}" height="72" rx="36" class="hub"/>'
            f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" class="hlabel">{e(hub)}</text></svg>'
            f'<figcaption>Drawn for this site from the parts the company names.</figcaption></figure>')


def flow(F, prefix, cls='flow'):
    steps = F.get('how', [])
    li = ''.join(f'<li><b>{md(s["title"])}</b><span>{md(s["t"])}{cite(F, s.get("s"), prefix)}</span></li>'
                 for s in steps)
    return f'<ol class="{cls}">{li}</ol>'


def chart(F, prefix, cls='chart'):
    c = F.get('chart')
    if not c:
        return ''
    bars = c['bars']
    mx = max(b['value'] for b in bars) or 1
    rows = ''.join(
        f'<li><span class="bl">{e(b["label"])}</span><span class="bt"><span class="bb" style="width:{b["value"]/mx*100:.1f}%"></span></span>'
        f'<span class="bv">{e(b["value"])}</span></li>' for b in bars)
    return (f'<figure class="{cls}"><figcaption><b>{md(c["title"])}</b> '
            f'<span>{md(c["note"])}{cite(F, c.get("s"), prefix)}</span></figcaption><ul>{rows}</ul></figure>')


def figures(F, prefix, cls='figs'):
    fs = F.get('figures', [])
    if not fs:
        return ''
    li = ''.join(f'<li><span class="n">{e(f["value"])}</span><span class="l">{md(f["label"])}</span>'
                 f'<span class="d">as published {e(fmt_date(f["asof"]))}{cite(F, f.get("s"), prefix)}</span></li>'
                 for f in fs)
    return f'<ul class="{cls}">{li}</ul>'


def paras(F, items, prefix):
    return ''.join(f'<p>{md(x["t"])}{cite(F, x.get("s"), prefix)}</p>' for x in items)


def bullets(F, items, prefix, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<ul{c}>' + ''.join(f'<li>{md(x["t"])}{cite(F, x.get("s"), prefix)}</li>' for x in items) + '</ul>'


def products(F, prefix, cls='cards'):
    out = []
    for p in F.get('products', []):
        name = f'<a href="{e(p["url"])}">{e(p["name"])}</a>' if p.get('url') else e(p['name'])
        out.append(f'<li><h3>{name}</h3><p>{md(p["t"])}{cite(F, p.get("s"), prefix)}</p></li>')
    return f'<ul class="{cls}">' + ''.join(out) + '</ul>'


def people(F, prefix):
    ps = F.get('people', [])
    if not ps:
        return ''
    return '<ul class="people">' + ''.join(
        f'<li><b>{e(p["name"])}</b>, {md(p["role"])}{cite(F, p.get("s"), prefix)}</li>' for p in ps) + '</ul>'


def sources(F, prefix, heading='Sources'):
    li = ''.join(f'<li id="{prefix}src-{s["id"]}"><a href="{e(s["url"])}">{e(s["title"])}</a>'
                 f' <span class="acc">read {e(fmt_date(s["accessed"]))}</span></li>' for s in F['sources'])
    return (f'<section class="sources" aria-labelledby="{prefix}h-src"><h2 id="{prefix}h-src">{heading}</h2>'
            f'<p>Every fact on this page comes from the company\'s own public pages, listed here. '
            f'Numbers in the text point to them. Diagrams were drawn for this site from those facts.</p><ol>{li}</ol></section>')


# ---------------------------------------------------------------- chrome
BASE_CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);overflow-wrap:break-word}
img,svg{max-width:100%;height:auto;display:block}
figure{margin:0}
a{color:var(--link)}
:focus-visible{outline:3px solid var(--link);outline-offset:2px}
.skip{position:absolute;left:-999px;top:0}
.skip:focus{left:1rem;top:1rem;background:var(--bg);color:var(--fg);padding:.5rem .8rem;z-index:9}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
sup.cites{font-size:.68em;line-height:0;margin-left:.35em;white-space:nowrap}
sup.cites a{text-decoration:none;display:inline-block;min-width:24px;text-align:center}
sup.cites a:hover{text-decoration:underline}
/* top navigation: the site's own */
.top{background:var(--navbg,var(--bg));color:var(--navfg,var(--fg));border-bottom:1px solid var(--line);font:500 .95rem/1.4 var(--navfont,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif)}
.top a{color:inherit}
.top-row{max-width:76rem;margin:0 auto;padding:.55rem 1rem;display:flex;flex-wrap:wrap;align-items:center;gap:.4rem 1.1rem}
.top .brand{text-decoration:none;font-weight:700;font-size:1.05rem;display:flex;flex-direction:column;line-height:1.15;margin-right:auto}
.top .brand small{font-weight:400;font-size:.78rem;opacity:.85}
.top ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.2rem 1rem}
.top li a{text-decoration:none;display:inline-block;padding:.25rem 0;min-height:24px}
.top li a:hover{text-decoration:underline}
.top .visit{font-weight:700}
.pick{position:relative}
.pick summary{cursor:pointer;list-style:none;border:1px solid currentColor;border-radius:999px;padding:.25rem .8rem;white-space:nowrap}
.pick summary::-webkit-details-marker{display:none}
.pick summary::after{content:" \\25BE"}
.pick[open] summary::after{content:" \\25B4"}
.pick-cards{position:absolute;right:0;top:calc(100% + .5rem);z-index:20;width:min(46rem,calc(100vw - 2rem));background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:12px;padding:1rem;box-shadow:0 12px 40px rgba(0,0,0,.25);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.pick-cards ul{display:grid;grid-template-columns:repeat(auto-fill,minmax(8.5rem,1fr));gap:.8rem}
.pick-cards a{display:flex;flex-direction:column;gap:.15rem;text-decoration:none;color:var(--fg);font-size:.85rem;line-height:1.3}
.pick-cards img{border-radius:6px;border:1px solid var(--line);aspect-ratio:8/5;object-fit:cover;object-position:top}
.pick-cards strong{display:block}
.pick-cards a:hover strong{text-decoration:underline}
.pick-cards span{color:var(--muted)}
.pick-cards .now{color:var(--link);font-weight:600}
.pick-cards .all{margin:.8rem 0 0;font-size:.9rem}
.pick-cards .all a{display:inline;color:var(--link);text-decoration:underline}
@media (max-width:40rem){
 .top-row{flex-wrap:nowrap;gap:.5rem;padding:.45rem .8rem}
 .top-row>ul{display:none}
 .top .brand{min-width:0;flex:1 1 auto}
 .top .brand small{display:none}
 .top .brand .wm-sw{font-size:.82rem;line-height:1.1}.top .brand .wm-ac{font-size:.95rem}
 .pick summary{font-size:.82rem;padding:.2rem .6rem}
 .pick-cards{position:fixed;left:.8rem;right:.8rem;top:3.2rem;width:auto;max-height:80vh;overflow:auto}
 .top .family-credit{margin-left:0}
 .top .family-credit summary{font-size:.72rem}
 .top .family-credit ul{position:fixed;right:.8rem;left:auto;top:3.2rem}
}
.top .brand .logo img{height:2rem;width:auto}
.top .brand .logo.plate{padding:.2rem .4rem;border-radius:6px}
.top .brand .wm-sgit{font-size:1.35rem}
.top .brand .wm-ac,.top .brand .wm-sw{font-size:1.05rem}
.top .brand .wm-ac svg,.top .brand .wm-sw svg{width:22px;height:22px}
/* FAMILY_CSS */
.top .family-credit{position:relative;top:auto;right:auto;font-size:.8rem;margin-left:auto}
.top .family-credit ul{min-width:14rem}
.top .family-credit summary{font-size:1.3rem;line-height:1;padding:.2rem .5rem;opacity:.85}
.top .family-credit summary::after{content:none}
.family-credit .family-head{padding:.3rem .8rem .2rem;font-weight:700;font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--fam-fg)}
.top .wm-sw .ag{display:none}
.top .family-credit ul{display:block;right:0}
.top .family-credit li a{color:var(--fam-fg);display:block;padding:.3rem .8rem;text-decoration:none}
.top .family-credit li a:hover{text-decoration:none;color:var(--fam-strong)}
.foot{font:.85rem/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--muted);max-width:76rem;margin:0 auto;padding:1rem 1rem 2.5rem}
.foot p{margin:0 0 .4rem}
.foot a{color:var(--muted)}
.foot .sws-version{opacity:1;color:var(--fg);border-color:var(--muted)}

/* the company's own identity: logos and framed screenshots of the real site */
.logo{display:inline-flex;align-items:center}
.logo img{height:2.6rem;width:auto}
.logo.plate{background:#fff;border-radius:10px;padding:.45rem .7rem}
.wm-sgit{font:800 2.2rem/1 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;letter-spacing:-.02em}
.wm-sgit b{color:#0f766e}
.wm-ac,.wm-sw{display:inline-flex;align-items:center;gap:.5rem;font:700 1.5rem/1 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wm-sw{font-family:Georgia,"Iowan Old Style","Times New Roman",serif}
.shot{margin:0}
.shot .frame{display:block;border-radius:12px;overflow:hidden;background:#fff;box-shadow:0 18px 50px rgba(0,0,0,.28),0 0 0 1px rgba(127,127,127,.25);text-decoration:none;transition:transform .2s}
.shot .frame:hover{transform:translateY(-3px)}
.shot .bar{display:flex;align-items:center;gap:.35rem;padding:.45rem .7rem;background:#e9e9ec;color:#3b3b40;font:.75rem/1.2 ui-monospace,Menlo,Consolas,monospace}
.shot .bar i{width:.6rem;height:.6rem;border-radius:50%;background:#c4c4ca;display:inline-block}
.shot .bar i:first-child{background:#ff5f57}.shot .bar i:nth-child(2){background:#febc2e}.shot .bar i:nth-child(3){background:#28c840}
.shot .bar span{margin-left:.5rem;background:#fff;border-radius:6px;padding:.15rem .6rem;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.shot img{width:100%;height:auto}
.shot figcaption{font-size:.85rem;color:var(--muted);margin-top:.6rem}
.gallery{display:grid;gap:1.6rem;grid-template-columns:repeat(auto-fit,minmax(17rem,1fr))}
@media (prefers-reduced-motion:reduce){.shot .frame{transition:none}.shot .frame:hover{transform:none}}
@media print{.top,.pick{display:none}}
@media (max-width:40rem){.tl-svg{display:none}.map-svg{padding:.4rem!important}.map-svg .nlabel{font-size:27px!important}.map-svg .hlabel{font-size:32px!important}}
"""


def share_alt(F):
    return f'{F["name"]}: {F["kicker"]}. An independent startup brochure made from its own public pages, pointing to {F["url_label"]}.'


def share_card(F):
    b = F['brand']
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>card</title><style>
html,body{{margin:0;width:1200px;height:630px}}
body{{background:#101214;color:#f3f3f1;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;display:flex;flex-direction:column;justify-content:space-between;padding:70px 80px;box-sizing:border-box;border-left:28px solid {b['accent']}}}
.k{{font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:{b['accent_dark']};font-weight:700}}
h1{{font-size:{'112' if len(F['name']) < 14 else '92'}px;line-height:1;margin:22px 0 26px;letter-spacing:-.02em}}
p{{font-size:38px;line-height:1.3;margin:0;max-width:960px;color:#d9dad6}}
.f{{display:flex;justify-content:space-between;font-size:26px;color:#b9bab5}}
.f b{{color:#f3f3f1}}
</style></head><body><div><div class="k">Startup brochure</div><h1>{e(F['name'])}</h1><p>{e(F['kicker'])}</p></div>
<div class="f"><span>Made from its own public pages</span><b>{e(F['url_label'])}</b></div></body></html>"""


def head(F, key, depth, title, desc, css):
    if key in ('start', 'agents', 'admin'):
        canon = f'https://{F["domain"]}/{key}/'
    else:
        canon = f'https://{F["domain"]}/' + ('' if key == F['home'] else f'designs/{key}.html')
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(F['name'])}, a startup brochure">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{e(canon)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://{e(F['domain'])}/img/share-card.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(share_alt(F))}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="https://{e(F['domain'])}/img/share-card.jpg">
<meta name="twitter:image:alt" content="{e(share_alt(F))}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{rel(depth, 'favicon.svg')}" type="image/svg+xml">
<style>{BASE_CSS.replace('/* FAMILY_CSS */', seed_file('family-credit.css'))}{css}</style>
</head>
<body class="d-{key}">
<a class="skip" href="#main">Skip to content</a>
"""


def nav(F, key, depth, links):
    cards = []
    for k, name, blurb in DESIGNS:
        here = k == key
        target = rel(depth, page_path(k, F))
        cur = ' aria-current="page"' if here else ''
        cards.append(f'<li><a href="{target}"{cur}><img src="{rel(depth, f"img/designs/{k}.webp")}" width="640" height="400" alt="" loading="lazy" decoding="async">'
                     f'<strong>{e(name)}</strong><span>{e(blurb)}</span>'
                     + ('<span class="now">You are here</span>' if here else '') + '</a></li>')
    home_note = dict((k, n) for k, n, _ in DESIGNS)[F['home']]
    lis = ''.join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in links)
    return (f'<header class="top"><nav class="top-row" aria-label="{e(F["name"])}">'
            f'<a class="brand" href="{rel(depth, "index.html")}">{logo(F, depth) or e(F["name"])}<small>{e(F["kicker"])}</small></a>'
            f'<ul>{lis}<li><a class="visit" href="{e(F["url"])}">Visit {e(F["url_label"])} &#8599;</a></li></ul>'
            f'<details class="pick"><summary>Choose a design</summary><div class="pick-cards">'
            f'<p class="sr">The same facts in five designs.</p><ul>{"".join(cards)}</ul>'
            f'<p class="all"><a href="{rel(depth, "designs/index.html")}">All designs</a> &middot; the home page uses {e(home_note)}.</p>'
            f'</div></details>{fam_menu(F)}</nav></header>\n')


SEED = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed')


def seed_file(name):
    with open(os.path.join(SEED, name)) as f:
        return f.read()


def fam_menu(F):
    """The Factory's top-right credit (seed/shared/family-credit.html), with the startup brochures added."""
    block = seed_file('family-credit.html').strip()
    shown = [(x, n) for x, n in STARTUPS if x in LIVE or x == F['slug']]
    st = ''.join(f'\n    <li{" class=" + chr(34) + "family-gap" + chr(34) if i == len(shown) - 1 else ""}><a href="https://{x}.startups.sovereignweb.site/"'
                 + (' aria-current="true"' if x == F['slug'] else '') + f'>{e(n)}</a></li>' for i, (x, n) in enumerate(shown))
    block = block.replace('<summary>Sovereign Website</summary>', '<summary aria-label="Made with Sovereign Website: menu">&#8942;</summary>')
    block = block.replace('<ul>', '<ul><li class="family-head">Made with Sovereign Website</li>', 1)
    return block.replace('<li class="family-gap"><a href="/admin/">How this site was made</a></li>',
                         '<li class="family-gap"><a href="/admin/">How this site was made</a></li>' + st)


def foot(F, depth):
    built = F.get('updated', '')
    return (f'<footer class="foot"><p>An independent brochure about {e(F["name"])}, made from its own public pages. '
            f'For the real thing, go to <a href="{e(F["url"])}">{e(F["url_label"])}</a>.</p>'
            f'<p>Facts last checked {e(fmt_date(built))}. Text licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; '
            f'names and marks belong to their owners. No cookies, no tracking, no scripts. '
            f'<a href="{rel(depth, "designs/index.html")}">All designs</a> &middot; '
            f'<a href="{e(F["repo"])}">Source</a>.</p></footer>\n</body>\n</html>\n')


def std_links(prefix=''):
    return [('What it is', f'#{prefix}what'), ('How it works', f'#{prefix}how'),
            ('Products', f'#{prefix}products'), ('Story', f'#{prefix}story'), ('Sources', f'#{prefix}h-src')]


# ---------------------------------------------------------------- designs
def palette(F, light, dark):
    return (':root{' + light + '}' +
            '@media (prefers-color-scheme:dark){:root{' + dark + '}}')


def d_brochure(F, depth):
    b = F['brand']
    css = palette(F,
                  f'--bg:#f6f6f3;--card:#fff;--fg:#17181a;--muted:#4f5257;--line:#dcdcd6;--link:{b["accent"]};--acc:{b["accent"]};--acc-ink:#fff;--soft:{b["soft"]}',
                  f'--bg:#121315;--card:#1c1e21;--fg:#ececea;--muted:#a9abb0;--line:#33363b;--link:{b["accent_dark"]};--acc:{b["accent_dark"]};--acc-ink:#0b0c0e;--soft:{b["soft_dark"]}') + """
body{font:1.0625rem/1.62 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:76rem;margin:0 auto;padding:0 1rem}
.hero-band{background:radial-gradient(120% 140% at 0% 0%,var(--hero1) 0%,var(--hero2) 55%,var(--hero3) 100%);color:#fff;overflow:hidden}
.hero{max-width:76rem;margin:0 auto;display:grid;gap:2rem;padding:2.5rem 1rem 3rem;align-items:center}
@media (min-width:56rem){.hero{grid-template-columns:1fr 1.1fr;padding:4.5rem 1rem 5rem;gap:3.5rem}}
.hero .eyebrow{color:#fff;opacity:.9;margin-top:1.4rem}
.hero h1{color:#fff}
.hero .lede{color:rgba(255,255,255,.9)}
.hero .cta{background:#fff;color:var(--hero2)}
.hero .wm-sgit b{color:#99f6e4}
.hero .logo{color:#fff}
@media (min-width:56rem){.hero-shot .shot{transform:perspective(1400px) rotateY(-7deg) rotateX(2deg)}}
.hero-shot .shot figcaption{color:rgba(255,255,255,.85)}
.hero-shot .shot figcaption a{color:#fff}
.sub{color:var(--muted);margin:-.4rem 0 1.4rem}
blockquote.quote{margin:2.5rem 0 1rem}
.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;font-weight:700;color:var(--acc);margin:0 0 .6rem}
h1{font-size:clamp(2.2rem,6vw,3.7rem);line-height:1.04;margin:0 0 1rem;letter-spacing:-.02em}
.lede{font-size:clamp(1.1rem,2.2vw,1.3rem);line-height:1.5;margin:0 0 1.4rem;max-width:38rem;color:var(--muted)}
.cta{display:inline-block;background:var(--acc);color:var(--acc-ink);padding:.75rem 1.2rem;border-radius:10px;font-weight:700;text-decoration:none}
.cta:hover{filter:brightness(1.08)}
.quote{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--acc);border-radius:14px;padding:1.4rem 1.5rem;margin:0}
.quote p{font-size:1.3rem;line-height:1.4;margin:0 0 .6rem;font-weight:600}
.quote footer{font-size:.9rem;color:var(--muted)}
section{padding:2.2rem 0;border-top:1px solid var(--line)}
h2{font-size:clamp(1.5rem,3.4vw,2.1rem);line-height:1.15;margin:0 0 1rem;letter-spacing:-.01em}
section>h2::before,.two h2::before{content:"";display:block;width:2.4rem;height:5px;border-radius:3px;background:var(--acc);margin-bottom:.7rem}
.two{display:grid;gap:1.5rem}
@media (min-width:56rem){.two{grid-template-columns:1fr 1fr;gap:3rem}}
.two ul{padding-left:1.2rem;margin:0}.two li{margin:.35rem 0}
.flow{list-style:none;padding:0;margin:0;display:grid;gap:1rem;counter-reset:s}
@media (min-width:56rem){.flow{grid-template-columns:repeat(auto-fit,minmax(12rem,1fr))}}
.flow li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1.1rem 1.1rem 1.2rem;position:relative}
.flow li::before{content:counter(s);display:inline-grid;place-items:center;width:2rem;height:2rem;border-radius:50%;background:var(--acc);color:var(--acc-ink);font-weight:800;margin-bottom:.5rem}
.flow b{display:block;font-size:1.1rem;margin-bottom:.25rem}
.flow span{color:var(--muted);font-size:.97rem}
.map-svg{background:var(--soft);border-radius:16px;padding:1rem;margin:0 0 1.5rem}
.map-svg svg{margin:0 auto;max-width:46rem}
.map-svg .spoke{stroke:var(--acc);stroke-width:3;opacity:.55}
.map-svg .node{fill:var(--card);stroke:var(--acc);stroke-width:2.5}
.map-svg .nlabel{fill:var(--fg);font:700 22px system-ui,sans-serif}
.map-svg .hub{fill:var(--acc)}
.map-svg .hlabel{fill:var(--acc-ink);font:800 28px system-ui,sans-serif}
figcaption{font-size:.85rem;color:var(--muted);margin-top:.5rem}
.cards{list-style:none;padding:0;margin:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(16rem,1fr))}
.cards li{background:var(--card);border:1px solid var(--line);border-top:5px solid var(--acc);border-radius:14px;padding:1.1rem 1.2rem;box-shadow:0 6px 18px rgba(0,0,0,.06)}
.cards h3{margin:0 0 .35rem;font-size:1.15rem}
.cards p{margin:0;color:var(--muted);font-size:.97rem}
.tl-svg{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:1rem;margin-bottom:1rem}
.tl-svg .axis{stroke:var(--fg);stroke-width:3}
.tl-svg .tick{stroke:var(--muted);stroke-width:2}
.tl-svg .dot{fill:var(--acc);stroke:var(--card);stroke-width:3}
.tl-svg .num{fill:var(--fg);font:800 24px system-ui,sans-serif}
.tl-svg .yr{fill:var(--muted);font:700 24px system-ui,sans-serif}
.tl-list{padding-left:1.8rem;margin:0;columns:1}
@media (min-width:56rem){.tl-list{columns:2;column-gap:3rem}}
.tl-list li{margin:0 0 .6rem;break-inside:avoid}
.tl-list time{font-weight:700;display:block}
.figs{list-style:none;padding:0;margin:0 0 1.5rem;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(13rem,1fr))}
.figs li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem;display:flex;flex-direction:column;gap:.15rem}
.figs .n{font-size:2rem;font-weight:800;color:var(--acc);line-height:1.1}
.figs .d{font-size:.82rem;color:var(--muted)}
.chart{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem 1.2rem}
.chart figcaption{font-size:.95rem;color:var(--fg);margin:0 0 .8rem}
.chart figcaption span{display:block;color:var(--muted);font-size:.85rem}
.chart ul{list-style:none;margin:0;padding:0;display:grid;gap:.35rem}
.chart li{display:grid;grid-template-columns:6.5rem 1fr 2.5rem;gap:.6rem;align-items:center;font-size:.9rem}
.chart .bt{background:var(--soft);border-radius:4px;height:1.1rem;overflow:hidden}
.chart .bb{display:block;height:100%;background:var(--acc)}
.chart .bv{font-weight:700;text-align:right}
.people{padding-left:1.2rem}
.visit-box{background:var(--acc);color:var(--acc-ink);border-radius:18px;padding:2rem 1.5rem;text-align:center;margin:2rem 0}
.visit-box h2{margin-bottom:.5rem}.visit-box p{margin:0 0 1.2rem}
.visit-box .cta{background:var(--acc-ink);color:var(--acc)}
.sources ol{padding-left:1.6rem;font-size:.92rem}.sources li{margin:.3rem 0}.sources .acc{color:var(--muted);font-size:.85em}
.sources p{color:var(--muted)}
"""
    p = 'b-'
    q = F['quote']
    css += ':root{--hero1:%s;--hero2:%s;--hero3:%s}' % (b.get('hero1', b['accent']), b.get('hero2', b['accent']), b.get('hero3', '#0b0d10'))
    body = [head(F, 'brochure', depth, f'{F["name"]}: {F["kicker"]}', F['description'], css),
            nav(F, 'brochure', depth, std_links(p)),
            f'<div class="hero-band"><div class="hero"><div class="hero-text">{logo(F, depth, force_plate=True)}<p class="eyebrow">{e(F["kicker"])}</p><h1>{md(F["headline"])}</h1>'
            f'<p class="lede">{md(F["lede"])}</p><a class="cta" href="{e(F["url"])}">Go to {e(F["url_label"])} &#8599;</a></div>'
            f'<div class="hero-shot">{shot(F, depth, 0, lazy=False)}</div></div></div>',
            '<main id="main">',
            f'<blockquote class="quote"><p>&ldquo;{e(q["q"])}&rdquo;</p><footer>{md(q["who"])}{cite(F, q.get("s"), p)}</footer></blockquote>',
            f'<section id="{p}what"><div class="two"><div><h2>What it is</h2>{paras(F, F["what"], p)}</div>'
            f'<div><h2>Who it is for</h2>{bullets(F, F["for_whom"], p)}</div></div></section>',
            f'<section id="{p}how"><h2>How it works</h2>{flow(F, p)}</section>',
            f'<section id="{p}products"><h2>What it is made of</h2>{svg_map(F)}{products(F, p)}</section>',
            f'<section id="{p}story"><h2>The story so far</h2>{svg_timeline(F)}{timeline_list(F, p)}</section>']
    if F.get('figures') or F.get('chart'):
        body.append(f'<section id="{p}figures"><h2>In figures</h2>{figures(F, p)}{chart(F, p)}</section>')
    if F.get('people'):
        body.append(f'<section><h2>People</h2>{people(F, p)}</section>')
    if (F.get('identity') or {}).get('shots', [])[1:]:
        body.append(f'<section id="{p}real"><h2>On the real site</h2><p class="sub">Pages from {e(F["url_label"])} itself. Each one opens the real page.</p>{gallery(F, depth, 1)}</section>')
    body.append(f'<div class="visit-box"><h2>See it for yourself</h2><p>{md(F["visit"])}</p>'
                f'<a class="cta" href="{e(F["url"])}">Visit {e(F["url_label"])} &#8599;</a></div>')
    body.append(sources(F, p))
    body.append('</main>')
    body.append(foot(F, depth))
    return ''.join(body)


def d_blueprint(F, depth):
    b = F['brand']
    css = palette(F,
                  '--bg:#0d2033;--card:#11283f;--fg:#e8f1fa;--muted:#a9c0d6;--line:#2c4f73;--link:#8fd3ff;--grid:rgba(143,211,255,.09);--hi:#ffd479',
                  '--bg:#08131f;--card:#0d1d2e;--fg:#e8f1fa;--muted:#9fb6cc;--line:#24435f;--link:#8fd3ff;--grid:rgba(143,211,255,.07);--hi:#ffd479') + """
body{font:1rem/1.6 ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;background-color:var(--bg);background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:28px 28px}
.top{--navbg:#0a1a2a;--navfg:#e8f1fa;--navfont:ui-monospace,"SF Mono",Menlo,Consolas,monospace;--family-fg:#c9d6e2;--family-fg-strong:#fff;--family-bg:#0d2033}
main{max-width:70rem;margin:0 auto;padding:0 1rem}
.sheet{border:2px solid var(--line);margin:2rem 0;background:rgba(0,0,0,.12)}
.titleblock{display:grid;grid-template-columns:1fr;border-bottom:2px solid var(--line)}
@media (min-width:50rem){.titleblock{grid-template-columns:2fr 1fr 1fr}}
.titleblock>div{padding:.8rem 1rem;border-bottom:1px solid var(--line)}
@media (min-width:50rem){.titleblock>div{border-bottom:0;border-right:1px solid var(--line)}.titleblock>div:last-child{border-right:0}}
.titleblock small{display:block;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;font-size:.72rem}
h1{font-size:clamp(1.8rem,5vw,2.8rem);margin:.1rem 0;line-height:1.1;color:var(--hi)}
.titleblock b{font-size:1.05rem}
.pad{padding:1.2rem 1rem 1.4rem}
h2{font-size:1rem;text-transform:uppercase;letter-spacing:.14em;color:var(--hi);margin:0 0 1rem;padding-bottom:.4rem;border-bottom:1px dashed var(--line)}
h2::before{content:attr(data-n) "  ";color:var(--muted)}
.lede{font-size:1.1rem;max-width:48rem}
.blk{border-top:2px solid var(--line)}
.flow{list-style:none;margin:0;padding:0;display:grid;gap:0}
@media (min-width:56rem){.flow{grid-template-columns:repeat(auto-fit,minmax(11rem,1fr))}}
.flow li{border:1px solid var(--link);padding:.9rem;position:relative;margin:0 0 1.6rem}
@media (min-width:56rem){.flow li{margin:0 1.6rem 0 0}.flow li:last-child{margin-right:0}}
.flow li::after{content:"\\2193";position:absolute;left:50%;bottom:-1.55rem;color:var(--link);font-size:1.2rem}
@media (min-width:56rem){.flow li::after{content:"\\2192";left:auto;right:-1.45rem;bottom:auto;top:45%}}
.flow li:last-child::after{content:none}
.flow b{display:block;color:var(--link);margin-bottom:.3rem}
.flow span{color:var(--muted);font-size:.92rem}
.map-svg{margin:0 0 1.4rem}
.map-svg svg{max-width:44rem;margin:0 auto}
.map-svg .spoke{stroke:var(--link);stroke-width:2;stroke-dasharray:8 6}
.map-svg .node{fill:var(--bg);stroke:var(--link);stroke-width:2}
.map-svg .nlabel{fill:var(--fg);font:700 21px ui-monospace,Menlo,Consolas,monospace}
.map-svg .hub{fill:var(--hi)}
.map-svg .hlabel{fill:#0d2033;font:800 26px ui-monospace,Menlo,Consolas,monospace}
figcaption{font-size:.8rem;color:var(--muted);margin-top:.4rem}
table{width:100%;border-collapse:collapse;font-size:.93rem;table-layout:fixed}
th,td{overflow-wrap:anywhere}
th,td{border:1px solid var(--line);padding:.55rem .7rem;text-align:left;vertical-align:top}
th{color:var(--hi);font-weight:700;width:30%}
th a{color:var(--hi)}
td{color:var(--fg)}
.log{list-style:none;margin:0;padding:0}
.log li{display:grid;grid-template-columns:1fr;gap:.1rem 1rem;padding:.45rem 0;border-bottom:1px dashed var(--line)}
@media (min-width:40rem){.log li{grid-template-columns:11rem 1fr}}
.log time{color:var(--hi)}
.figs{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(12rem,1fr));gap:0}
.figs li{border:1px solid var(--line);padding:.8rem;display:flex;flex-direction:column}
.figs .n{font-size:1.7rem;color:var(--hi);font-weight:800}
.figs .d{font-size:.78rem;color:var(--muted)}
.chart{margin-top:1.2rem}
.chart figcaption{color:var(--fg);margin:0 0 .6rem}.chart figcaption span{display:block;color:var(--muted)}
.chart ul{list-style:none;margin:0;padding:0}
.chart li{display:grid;grid-template-columns:6.5rem 1fr 2.5rem;gap:.6rem;align-items:center;font-size:.85rem;margin:.25rem 0}
.chart .bt{border:1px solid var(--line);height:1rem}.chart .bb{display:block;height:100%;background:repeating-linear-gradient(45deg,var(--link) 0 6px,transparent 6px 9px)}
.chart .bv{text-align:right;color:var(--hi)}
.sources ol{padding-left:1.6rem;font-size:.88rem}.sources .acc{color:var(--muted)}.sources p{color:var(--muted)}
.cmd{display:inline-block;border:2px solid var(--hi);color:var(--hi);padding:.6rem 1rem;text-decoration:none;font-weight:700}
.cmd:hover{background:var(--hi);color:#0d2033}
"""
    p = 'p-'
    rows = ''.join(f'<tr><th>{("<a href=" + chr(34) + e(x["url"]) + chr(34) + ">" + e(x["name"]) + "</a>") if x.get("url") else e(x["name"])}</th>'
                   f'<td>{md(x["t"])}{cite(F, x.get("s"), p)}</td></tr>' for x in F.get('products', []))
    ev = sorted(F.get('timeline', []), key=lambda x: x['date'])
    log = ''.join(f'<li><time datetime="{e(x["date"])}">{e(x["date"])}</time><span>{md(x["label"])}{cite(F, x.get("s"), p)}</span></li>' for x in reversed(ev))
    users = ''.join(f'<tr><th>User {i}</th><td>{md(x["t"])}{cite(F, x.get("s"), p)}</td></tr>' for i, x in enumerate(F['for_whom'], 1))
    n = 0
    def h(t, id_=''):
        nonlocal n
        n += 1
        i = f' id="{id_}"' if id_ else ''
        return f'<h2 data-n="{n:02d}"{i}>{t}</h2>'
    body = [head(F, 'blueprint', depth, f'{F["name"]}: the blueprint', F['description'], css),
            nav(F, 'blueprint', depth, std_links(p)),
            '<main id="main"><div class="sheet">',
            f'<div class="titleblock"><div><small>Subject</small><h1>{e(F["name"])}</h1>{e(F["kicker"])}</div>'
            f'<div><small>Origin</small><b><a href="{e(F["url"])}">{e(F["url_label"])}</a></b></div>'
            f'<div><small>Sheet checked</small><b>{e(F["updated"])}</b></div></div>',
            f'<div class="pad">{h("Specification", p + "what")}<p class="lede">{md(F["lede"])}</p>{paras(F, F["what"], p)}'
            f'<p><b>Stated purpose:</b> &ldquo;{e(F["quote"]["q"])}&rdquo; ({md(F["quote"]["who"])}){cite(F, F["quote"].get("s"), p)}</p></div>',
            f'<div class="pad blk">{h("Intended users")}<table>{users}</table></div>',
            f'<div class="pad blk">{h("Process", p + "how")}{flow(F, p)}</div>',
            f'<div class="pad blk">{h("Components", p + "products")}{svg_map(F)}<table>{rows}</table></div>',
            f'<div class="pad blk">{h("Change log", p + "story")}<ol class="log" reversed>{log}</ol></div>']
    if F.get('figures') or F.get('chart'):
        body.append(f'<div class="pad blk">{h("Measurements")}{figures(F, p)}{chart(F, p)}</div>')
    body.append(f'<div class="pad blk">{h("Next step")}<p>{md(F["visit"])}</p><a class="cmd" href="{e(F["url"])}">&gt; open {e(F["url_label"])}</a></div>')
    body.append(f'<div class="pad blk">{sources(F, p, "References")}</div></div></main>')
    body.append(foot(F, depth))
    return ''.join(body)


def d_story(F, depth):
    b = F['brand']
    css = palette(F,
                  f'--bg:#fbf7f0;--card:#fffdf9;--fg:#231f1a;--muted:#5f574c;--line:#e3d9c8;--link:{b["accent"]};--acc:{b["accent"]}',
                  f'--bg:#191612;--card:#221e19;--fg:#efe8dc;--muted:#b5aa98;--line:#3a332b;--link:{b["accent_dark"]};--acc:{b["accent_dark"]}') + """
body{font:1.125rem/1.7 "Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif}
main{max-width:46rem;margin:0 auto;padding:0 1.1rem}
.open{padding:3rem 0 1.5rem;text-align:center}
.open p.k{font:700 .8rem/1 system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--acc)}
h1{font-size:clamp(2.3rem,7vw,3.8rem);line-height:1.05;margin:.5rem 0 1rem;font-weight:700}
.open .logo{margin-bottom:1.2rem}
.story-shot{margin:2.5rem -1rem}
@media (min-width:60rem){.story-shot{margin:3rem -8rem}}
.open .lede{font-size:1.25rem;color:var(--muted);font-style:italic}
h2{font-size:1.6rem;margin:2.5rem 0 1rem;text-align:center}
h2::after{content:"";display:block;width:3rem;height:2px;background:var(--acc);margin:.6rem auto 0}
.chap{list-style:none;margin:0;padding:0;position:relative}
.chap::before{content:"";position:absolute;left:.55rem;top:.4rem;bottom:.4rem;width:2px;background:var(--line)}
@media (min-width:44rem){.chap::before{left:9.5rem}}
.chap li{position:relative;padding:0 0 1.6rem 2.2rem}
@media (min-width:44rem){.chap li{padding-left:11.5rem}}
.chap li::before{content:"";position:absolute;left:.1rem;top:.45rem;width:1rem;height:1rem;border-radius:50%;background:var(--acc);border:3px solid var(--bg)}
@media (min-width:44rem){.chap li::before{left:9.05rem}}
.chap time{display:block;font:700 .95rem/1.3 system-ui,sans-serif;color:var(--acc)}
@media (min-width:44rem){.chap time{position:absolute;left:0;width:8.5rem;text-align:right;top:.3rem}}
.chap .what{font-size:1.15rem}
.prose p{margin:0 0 1.1rem}
.pull{font-size:1.5rem;line-height:1.35;text-align:center;margin:2.5rem 0;padding:1.5rem 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.pull footer{font:.9rem system-ui,sans-serif;color:var(--muted);margin-top:.6rem}
.flow{padding-left:1.4rem}.flow li{margin:0 0 .8rem}.flow b{display:block}
.cards{list-style:none;padding:0;margin:0}
.cards li{border-top:1px solid var(--line);padding:.8rem 0}
.cards h3{margin:0;font-size:1.2rem}.cards p{margin:.2rem 0 0;color:var(--muted)}
.figs{list-style:none;padding:0;margin:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(12rem,1fr));text-align:center}
.figs li{display:flex;flex-direction:column}
.figs .n{font-size:2.2rem;font-weight:700;color:var(--acc)}
.figs .d{font:.8rem system-ui,sans-serif;color:var(--muted)}
.chart{margin-top:1.5rem;font-family:system-ui,sans-serif}
.chart figcaption{margin-bottom:.6rem}.chart figcaption span{display:block;color:var(--muted);font-size:.85rem}
.chart ul{list-style:none;margin:0;padding:0}
.chart li{display:grid;grid-template-columns:6.5rem 1fr 2.5rem;gap:.6rem;align-items:center;font-size:.88rem;margin:.3rem 0}
.chart .bt{height:.8rem;background:var(--line);border-radius:9px;overflow:hidden}.chart .bb{display:block;height:100%;background:var(--acc)}
.chart .bv{text-align:right;font-weight:700}
.end{text-align:center;margin:3rem 0 2rem}
.end a{font:700 1.05rem system-ui,sans-serif;display:inline-block;border-bottom:3px solid var(--acc);text-decoration:none;color:var(--fg);padding:.2rem 0}
.sources{font-size:.92rem}.sources ol{padding-left:1.5rem}.sources .acc,.sources p{color:var(--muted)}
.sources h2{text-align:left}.sources h2::after{margin-left:0}
"""
    p = 's-'
    ev = sorted(F.get('timeline', []), key=lambda x: x['date'])
    chap = ''.join(f'<li><time datetime="{e(x["date"])}">{e(fmt_date(x["date"]))}</time>'
                   f'<span class="what">{md(x["label"])}{cite(F, x.get("s"), p)}</span></li>' for x in ev)
    q = F['quote']
    body = [head(F, 'story', depth, f'The story of {F["name"]}', F['description'], css),
            nav(F, 'story', depth, [('Beginnings', f'#{p}what'), ('Timeline', f'#{p}story'), ('How it works', f'#{p}how'),
                                     ('Products', f'#{p}products'), ('Sources', f'#{p}h-src')]),
            '<main id="main">',
            f'<div class="open">{logo(F, depth)}<p class="k">The story of</p><h1>{e(F["name"])}</h1><p class="lede">{md(F["lede"])}</p></div>',
            f'<div class="prose" id="{p}what">{paras(F, F.get("story", F["what"]), p)}</div>',
            f'<div class="story-shot">{shot(F, depth, 0)}</div>',
            f'<h2 id="{p}story">Date by date</h2><ol class="chap">{chap}</ol>',
            f'<blockquote class="pull">&ldquo;{e(q["q"])}&rdquo;<footer>{md(q["who"])}{cite(F, q.get("s"), p)}</footer></blockquote>',
            f'<h2 id="{p}how">How it works</h2>{flow(F, p)}',
            f'<h2 id="{p}products">What it offers</h2>{products(F, p)}']
    if F.get('figures') or F.get('chart'):
        body.append(f'<h2>By the numbers</h2>{figures(F, p)}{chart(F, p)}')
    body.append(f'<p class="end">{md(F["visit"])}<br><br><a href="{e(F["url"])}">Continue the story at {e(F["url_label"])} &#8599;</a></p>')
    body.append(sources(F, p))
    body.append('</main>')
    body.append(foot(F, depth))
    return ''.join(body)


def d_newsroom(F, depth):
    b = F['brand']
    css = palette(F,
                  f'--bg:#ffffff;--card:#f4f1ea;--fg:#111;--muted:#555;--line:#d8d2c4;--link:#a3001b;--acc:#a3001b;--band:{b["accent"]}',
                  f'--bg:#121212;--card:#1d1b18;--fg:#f1efe9;--muted:#b3ada1;--line:#3b3730;--link:#ff8a8a;--acc:#ff8a8a;--band:{b["accent_dark"]}') + """
body{font:1.1rem/1.65 Georgia,"Times New Roman",serif}
.mast{max-width:72rem;margin:0 auto;padding:1.4rem 1rem .6rem;border-bottom:4px double var(--fg);display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:.4rem}
.mast b{font:900 clamp(1.6rem,4.5vw,2.6rem)/1 Georgia,serif;letter-spacing:-.02em}
.mast span{font:600 .8rem system-ui,sans-serif;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}
main{max-width:72rem;margin:0 auto;padding:0 1rem}
.kick{font:800 .8rem system-ui,sans-serif;text-transform:uppercase;letter-spacing:.14em;color:var(--acc);margin:1.8rem 0 .4rem}
@media (max-width:40rem){.mast{padding:.4rem 1rem .2rem}.mast b{font-size:1.15rem}.mast span{display:none}.kick{margin-top:.5rem}}
h1{font:900 clamp(2.2rem,6.5vw,4.4rem)/1.02 Georgia,serif;margin:0 0 1rem;letter-spacing:-.02em;max-width:60rem}
.stand{font-size:clamp(1.15rem,2.4vw,1.45rem);line-height:1.45;color:var(--muted);max-width:50rem;margin:0 0 1rem}
.by{font:.85rem system-ui,sans-serif;color:var(--muted);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:.5rem 0;margin:0 0 1.6rem}
.band{background:var(--band);height:10px;margin:0 0 1.8rem}
.lead{margin:0 0 2.2rem}
.lead .shot{max-width:60rem}
.lead .shot figcaption{font-family:system-ui,sans-serif}
.grid{display:grid;gap:2rem}
@media (min-width:60rem){.grid{grid-template-columns:1fr 20rem;gap:3rem}}
.body p{margin:0 0 1.1rem}
.body>p:first-of-type::first-letter{float:left;font-size:4.3em;line-height:.85;margin:.08em .1em 0 0;font-weight:900;color:var(--acc)}
.body h2{font:800 1.4rem/1.2 Georgia,serif;margin:2rem 0 .8rem}
.pq{font:italic 700 1.55rem/1.3 Georgia,serif;margin:2rem 0;padding:0 0 0 1.2rem;border-left:6px solid var(--acc)}
.pq footer{font:normal .85rem system-ui,sans-serif;color:var(--muted);margin-top:.5rem}
aside{font-family:system-ui,sans-serif;font-size:.95rem}
aside .box{background:var(--card);padding:1.1rem 1.2rem;margin:0 0 1.4rem;border-top:4px solid var(--fg)}
aside .brandbox p{margin:.6rem 0 0}
aside h2{font:800 .8rem system-ui,sans-serif;text-transform:uppercase;letter-spacing:.14em;margin:0 0 .8rem}
.figs{list-style:none;margin:0;padding:0}
.figs li{display:flex;flex-direction:column;padding:.5rem 0;border-bottom:1px solid var(--line)}
.figs .n{font:900 1.7rem Georgia,serif;color:var(--acc)}
.figs .d{font-size:.78rem;color:var(--muted)}
.tl-list{padding-left:1.2rem;margin:0}.tl-list li{margin:0 0 .5rem}.tl-list time{font-weight:700;display:block}
.flow{padding-left:1.3rem}.flow li{margin:0 0 .7rem}.flow b{display:block}
.cards{list-style:none;padding:0;margin:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr))}
.cards li{border-top:3px solid var(--fg);padding-top:.5rem}.cards h3{font:800 1.1rem Georgia,serif;margin:0}.cards p{margin:.2rem 0 0;font-size:1rem}
.chart{font-family:system-ui,sans-serif;margin:1.5rem 0}
.chart figcaption{margin-bottom:.5rem}.chart figcaption span{display:block;color:var(--muted);font-size:.85rem}
.chart ul{list-style:none;margin:0;padding:0}
.chart li{display:grid;grid-template-columns:6.5rem 1fr 2.5rem;gap:.6rem;align-items:center;font-size:.85rem;margin:.25rem 0}
.chart .bt{height:.9rem;background:var(--line)}.chart .bb{display:block;height:100%;background:var(--acc)}
.chart .bv{text-align:right;font-weight:700}
.tl-svg{margin:1.5rem 0}
.tl-svg .axis{stroke:var(--fg);stroke-width:3}.tl-svg .tick{stroke:var(--muted);stroke-width:2}
.tl-svg .dot{fill:var(--acc)}.tl-svg .num{fill:var(--fg);font:800 24px Georgia,serif}.tl-svg .yr{fill:var(--muted);font:700 24px system-ui,sans-serif}
figcaption{font:.82rem system-ui,sans-serif;color:var(--muted)}
.more{font:700 1rem system-ui,sans-serif;background:var(--fg);color:var(--bg);display:inline-block;padding:.7rem 1.1rem;text-decoration:none}
.sources{font:.9rem/1.5 system-ui,sans-serif;border-top:4px double var(--fg);margin-top:2.5rem;padding-top:1rem}
@media print{@page{size:A4;margin:14mm}body{font-size:10pt;background:#fff;color:#000}.lead,.band,.more{display:none}.grid{grid-template-columns:1fr 14rem;gap:1.2rem}a{color:#000}}
.sources h2{font-size:1rem;text-transform:uppercase;letter-spacing:.12em}.sources ol{padding-left:1.5rem}.sources .acc,.sources p{color:var(--muted)}
"""
    p = 'n-'
    q = F['quote']
    nw = F['newsroom']
    body = [head(F, 'newsroom', depth, nw['headline'], nw['standfirst'], css),
            nav(F, 'newsroom', depth, [('The feature', f'#{p}what'), ('How it works', f'#{p}how'),
                                        ('Products', f'#{p}products'), ('Timeline', f'#{p}story'), ('Sources', f'#{p}h-src')]),
            f'<div class="mast"><b>Startups Newsroom</b><span>Sovereign Website family &middot; {e(fmt_date(F["updated"]))}</span></div>',
            '<main id="main">',
            f'<p class="kick">{e(nw["kicker"])}</p><h1>{md(nw["headline"])}</h1><p class="stand">{md(nw["standfirst"])}</p>',
            f'<p class="by">Written by startups.b, the agent that keeps this site, from {e(F["name"])}\'s own public pages. Every claim is linked to its source.</p>',
            '<div class="band" role="presentation"></div>',
            f'<div class="lead">{shot(F, depth, 0, lazy=False)}</div>',
            '<div class="grid"><article class="body" id="' + p + 'what">',
            paras(F, F.get('story', F['what']), p),
            f'<blockquote class="pq">&ldquo;{e(q["q"])}&rdquo;<footer>{md(q["who"])}{cite(F, q.get("s"), p)}</footer></blockquote>',
            paras(F, F['what'], p),
            f'<h2 id="{p}how">How it works</h2>{flow(F, p)}',
            f'<h2 id="{p}products">The parts</h2>{products(F, p)}',
            f'<h2 id="{p}story">The timeline</h2>{svg_timeline(F)}',
            f'<p>{md(F["visit"])}</p><p><a class="more" href="{e(F["url"])}">Read more at {e(F["url_label"])} &#8599;</a></p>',
            '</article><aside>']
    body.append(f'<div class="box brandbox">{logo(F, depth)}<p><a href="{e(F["url"])}">{e(F["url_label"])} &#8599;</a></p></div>')
    if F.get('figures'):
        body.append(f'<div class="box"><h2>At a glance</h2>{figures(F, p)}</div>')
    body.append(f'<div class="box"><h2>Who it is for</h2>{bullets(F, F["for_whom"], p)}</div>')
    body.append(f'<div class="box"><h2>Key dates</h2>{timeline_list(F, p)}</div>')
    if F.get('people'):
        body.append(f'<div class="box"><h2>People</h2>{people(F, p)}</div>')
    if F.get('chart'):
        body.append(f'<div class="box">{chart(F, p)}</div>')
    body.append('</aside></div>')
    body.append(sources(F, p))
    body.append('</main>')
    body.append(foot(F, depth))
    return ''.join(body)


def d_brief(F, depth):
    css = palette(F,
                  '--bg:#fff;--card:#fff;--fg:#000;--muted:#444;--line:#bbb;--link:#0645ad',
                  '--bg:#161616;--card:#1e1e1e;--fg:#eee;--muted:#bbb;--line:#555;--link:#8ab4f8') + """
body{font:1rem/1.55 "Helvetica Neue",Helvetica,Arial,sans-serif}
main{max-width:52rem;margin:0 auto;padding:1.5rem 1rem 1rem}
main>.logo{margin-bottom:.6rem}
main>.logo img{height:2.2rem}
h1{font-size:1.9rem;margin:0 0 .2rem}
.sub{margin:0 0 1rem;color:var(--muted)}
h2{font-size:1.05rem;text-transform:uppercase;letter-spacing:.06em;margin:1.4rem 0 .4rem;border-bottom:1px solid var(--line);padding-bottom:.2rem}
p,ul,ol{margin:0 0 .6rem}
ul,ol{padding-left:1.3rem}
.flow{padding-left:1.3rem}.flow b::after{content:": "}
.cards{padding-left:1.3rem}.cards h3{display:inline;font-size:1rem;margin:0}.cards h3::after{content:": "}.cards p{display:inline;margin:0}
.figs{padding-left:1.3rem}.figs li span{margin-right:.3rem}.figs .n{font-weight:700}.figs .d{color:var(--muted);font-size:.9em}
.tl-list time{font-weight:700}
.chart figcaption span{display:block;color:var(--muted);font-size:.9em}.chart ul{padding-left:1.3rem}.chart .bt{display:none}.chart .bl::after{content:": "}
.sources ol{font-size:.88rem}.sources .acc,.sources p{color:var(--muted);font-size:.88rem}
.printnote{font-size:.85rem;color:var(--muted)}
@media print{
 @page{size:A4;margin:16mm}
 body{font-size:10pt;background:#fff;color:#000}
 main{max-width:none;padding:0}
 a{color:#000;text-decoration:none}
 .sources a::after{content:" " attr(href);font-size:.85em}
 .printnote,.foot,footer{display:none}
 h2{break-after:avoid}
}
"""
    p = 'r-'
    body = [head(F, 'brief', depth, f'{F["name"]}: the brief', F['description'], css),
            nav(F, 'brief', depth, std_links(p)),
            '<main id="main">',
            f'{logo(F, depth)}<h1>{e(F["name"])}</h1><p class="sub">{e(F["kicker"])}. Official site: <a href="{e(F["url"])}">{e(F["url_label"])}</a>. Checked {e(fmt_date(F["updated"]))}.</p>',
            '<p class="printnote">This design prints on A4 as a one-page brief with its sources.</p>',
            f'<h2 id="{p}what">In one line</h2><p>&ldquo;{e(F["quote"]["q"])}&rdquo; ({md(F["quote"]["who"])}){cite(F, F["quote"].get("s"), p)}</p>',
            f'<h2>What it is</h2>{paras(F, F["what"], p)}',
            f'<h2>Who it is for</h2>{bullets(F, F["for_whom"], p)}',
            f'<h2 id="{p}how">How it works</h2>{flow(F, p)}',
            f'<h2 id="{p}products">Products and parts</h2>{products(F, p)}',
            f'<h2 id="{p}story">Key dates</h2>{timeline_list(F, p)}']
    if F.get('figures') or F.get('chart'):
        body.append(f'<h2>Figures</h2>{figures(F, p)}{chart(F, p)}')
    if F.get('people'):
        body.append(f'<h2>People</h2>{people(F, p)}')
    body.append(sources(F, p))
    body.append('</main>')
    body.append(foot(F, depth))
    return ''.join(body)


def designs_index(F):
    css = palette(F, '--bg:#f6f6f3;--card:#fff;--fg:#17181a;--muted:#4f5257;--line:#dcdcd6;--link:' + F['brand']['accent'],
                  '--bg:#121315;--card:#1c1e21;--fg:#ececea;--muted:#a9abb0;--line:#33363b;--link:' + F['brand']['accent_dark']) + """
body{font:1.05rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:76rem;margin:0 auto;padding:1.5rem 1rem 2rem}
h1{font-size:clamp(1.8rem,5vw,2.6rem);margin:.5rem 0}
.g{list-style:none;padding:0;margin:1.5rem 0;display:grid;gap:1.4rem;grid-template-columns:repeat(auto-fill,minmax(17rem,1fr))}
.g a{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:var(--fg)}
.g img{aspect-ratio:8/5;object-fit:cover;object-position:top;width:100%;border-bottom:1px solid var(--line)}
.g div{padding:.8rem 1rem 1rem}.g strong{font-size:1.1rem}.g span{display:block;color:var(--muted);font-size:.95rem}
.g em{font-style:normal;color:var(--link);font-weight:700;font-size:.9rem}
"""
    cards = ''.join(f'<li><a href="{"../index.html" if k == F["home"] else k + ".html"}"><img src="../img/designs/{k}.webp" width="640" height="400" alt="The {e(n)} design, top of the page">'
                    f'<div><strong>{e(n)}</strong><span>{e(bl)}</span>' + ('<em>Used on the home page</em>' if k == F['home'] else '') + '</div></a></li>'
                    for k, n, bl in DESIGNS)
    return (head(F, 'index', 1, f'{F["name"]}: choose a design', f'The same facts about {F["name"]} in five designs.', css)
            + nav(F, 'gallery', 1, [('Home', '../index.html')])
            + f'<main id="main"><h1>Five designs, the same facts</h1><p>Every design below says the same things about {e(F["name"])}, '
              f'from the same sources. Pick the one you like; the control at the top of every page moves between them.</p>'
              f'<ul class="g">{cards}</ul></main>' + foot(F, 1))


def favicon(F):
    a = F['brand']['accent']
    letter = e(F.get('mark', F['name'][0]))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{a}"/>'
            f'<text x="32" y="44" text-anchor="middle" font-family="system-ui,sans-serif" font-size="34" font-weight="800" fill="#fff">{letter}</text></svg>\n')


def llms(F):
    lines = [f'# {F["name"]}', '', f'> {F["description"]}', '',
             f'An independent brochure about {F["name"]}, made from its own public pages. Official site: {F["url"]}', '',
             '## Pages', '']
    for k, n, bl in DESIGNS:
        lines.append(f'- [{n}](https://{F["domain"]}/{page_path(k, F)}): {bl}')
    lines += ['', '## Sources', ''] + [f'- {s["title"]}: {s["url"]} (read {s["accessed"]})' for s in F['sources']]
    return '\n'.join(lines) + '\n'


def subst(F, t):
    repo = F['repo'].rstrip('/').split('/')[-1]
    return (t.replace('{{title}}', F['name']).replace('{{repo}}', repo).replace('{{host}}', F['domain'])
             .replace('{{description}}', F['description']))


PAGES = [('start', 'Start here'), ('agents', 'Use with your AI'), ('admin', 'How this site was made')]


def seed_page(F, key, label):
    """A seeded page (start/, agents/, admin/), its words kept, restyled to match the site."""
    t = subst(F, seed_file(f'{key}.html'))
    body = re.search(r'<main[^>]*>(.*?)</main>', t, re.S).group(1)
    body = re.sub(r'<footer>.*?</footer>', '', body, flags=re.S)
    body = body.replace('<div class="mark">', '<p class="eyebrow">').replace('</div>\n<h1>', '</p>\n<h1>', 1)
    if key == 'start':
        body = body.replace('This page is for the owner of ' + F['name'] + '.',
                            'This page is for the owner of this brochure about ' + F['name'] + ', which Dinis Cruz keeps until it is handed over.')
    b = F['brand']
    css = palette(F,
                  f'--bg:#f6f6f3;--card:#fff;--fg:#17181a;--muted:#4f5257;--line:#dcdcd6;--link:{b["accent"]};--acc:{b["accent"]}',
                  f'--bg:#121315;--card:#1c1e21;--fg:#ececea;--muted:#a9abb0;--line:#33363b;--link:{b["accent_dark"]};--acc:{b["accent_dark"]}') + """
body{font:1.0625rem/1.62 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:46rem;margin:0 auto;padding:2rem 1rem 2.5rem}
.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;font-weight:700;color:var(--acc);margin:0 0 .4rem}
h1{font-size:clamp(1.9rem,5vw,2.6rem);line-height:1.1;margin:0 0 1rem;letter-spacing:-.01em}
h2{font-size:1.3rem;margin:2rem 0 .6rem}
li{margin:.35rem 0}
code{font:.92em ui-monospace,Menlo,Consolas,monospace;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.05rem .3rem}
pre,blockquote{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.8rem 1rem;white-space:pre-wrap;overflow-wrap:anywhere}
"""
    links = [(t2, f'/{k2}/') for k2, t2 in PAGES if k2 != key] + [('Home', '/')]
    return (head(F, key, 1, f'{label}: {F["name"]}', f'{label}, for the brochure about {F["name"]}.', css)
            + nav(F, key, 1, links) + f'<main id="main">{body}</main>' + foot(F, 1))


def llms_full(F):
    t = subst(F, seed_file('llms.txt'))
    return t + '\n' + llms(F).split('\n', 4)[4]


def agents_json(F):
    repo = F['repo'].rstrip('/').split('/')[-1]
    return json.dumps({
        'site': f'https://{F["domain"]}/',
        'repository': F['repo'],
        'made_by': 'https://github.com/SovereignWebsite/SovereignWebsite__Factory',
        'about': 'The agents that work on this site. Their keys are published at https://agents.sovereignweb.site/.',
        'agents': [{'name': 'startups.b@SovereignWebsite.dinis',
                    'role': 'Keeps the startup brochure sites under startups.sovereignweb.site: research from public sources, the five designs, the checks.',
                    'session': 'https://claude.ai/code/session_01Kw9UwCbSQgp3wavatYAbqd',
                    'key': 'sha256:57bedf0371520b54'}]}, indent=1) + '\n'


def main():
    F = load()
    os.makedirs(os.path.join(SITE, 'designs'), exist_ok=True)
    os.makedirs(os.path.join(SITE, 'img', 'designs'), exist_ok=True)
    import designs2
    designs2.setup(sys.modules[__name__])
    old = {'brochure': d_brochure, 'blueprint': d_blueprint, 'story': d_story, 'newsroom': d_newsroom, 'brief': d_brief}
    gens = {}
    for d in F.get('designs') or [{'key': k, 'engine': k} for k, _, _ in DESIGNS]:
        if d['engine'] in old:
            gens[d['key']] = (lambda fn: lambda F, depth: fn(F, depth))(old[d['engine']])
        else:
            gens[d['key']] = (lambda fn, dd: lambda F, depth: fn(F, depth, dd))(designs2.ENGINES[d['engine']], d)
    for f_ in os.listdir(os.path.join(SITE, 'designs')):
        os.remove(os.path.join(SITE, 'designs', f_))
    for f_ in os.listdir(os.path.join(SITE, 'img', 'designs')):
        if f_.split('.')[0] not in gens:
            os.remove(os.path.join(SITE, 'img', 'designs', f_))
    for k, _, _ in DESIGNS:
        path = page_path(k, F)
        depth = path.count('/')
        with open(os.path.join(SITE, path), 'w') as f:
            f.write(gens[k](F, depth))
    # the home design is also reachable at its own address: it is a copy
    with open(os.path.join(SITE, 'designs', f'{F["home"]}.html'), 'w') as f:
        f.write(gens[F['home']](F, 1))
    with open(os.path.join(SITE, 'designs', 'index.html'), 'w') as f:
        f.write(designs_index(F))
    os.makedirs(os.path.join(ROOT, 'tools', 'out'), exist_ok=True)
    with open(os.path.join(ROOT, 'tools', 'out', 'share-card.html'), 'w') as f:
        f.write(share_card(F))
    with open(os.path.join(SITE, 'favicon.svg'), 'w') as f:
        f.write(favicon(F))
    with open(os.path.join(SITE, 'llms.txt'), 'w') as f:
        f.write(llms_full(F))
    for key, label in PAGES:
        os.makedirs(os.path.join(SITE, key), exist_ok=True)
        with open(os.path.join(SITE, key, 'index.html'), 'w') as f:
            f.write(seed_page(F, key, label))
    os.makedirs(os.path.join(SITE, 'data'), exist_ok=True)
    with open(os.path.join(SITE, 'data', 'agents.json'), 'w') as f:
        f.write(agents_json(F))
    docs = os.path.join(ROOT, 'docs')
    os.makedirs(docs, exist_ok=True)
    with open(os.path.join(docs, 'sources.md'), 'w') as f:
        f.write(f'# Sources for {F["name"]}\n\nEvery fact on this site comes from these public pages. '
                'This file is written by tools/build.py from content/facts.json; edit the facts, not this file.\n\n'
                '| # | Source | Read |\n|---|---|---|\n')
        for x in F['sources']:
            f.write(f'| {x["id"]} | [{x["title"]}]({x["url"]}) | {x["accessed"]} |\n')
        f.write('\n## Images\n\n' + F.get('images_note', 'No images from the company are used. Every diagram and the favicon were drawn for this site from the facts above.') + '\n')
    print('built', SITE)


if __name__ == '__main__':
    main()
