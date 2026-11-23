"""Round 1 designs (design.b.rounds, 20 November 2026): ideas from each company's world and its real identity.

Each site's content/facts.json lists its five designs in "designs": [{key, name, blurb, engine, cfg}].
An engine is a function (F, depth, d) -> html page. The shared pieces (head, nav, foot, cite, sources...)
come from build.py, which imports this module after defining them.
"""
import hashlib
import re

B = None  # build.py module, set by setup()

BAND_CSS = """
.oneline{font:600 1.05rem/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;margin:-.2rem 0 1rem;opacity:.9}
.band-full{background:#0f1113;color:#f4f4f2;padding:3rem 0;margin:2.5rem 0}
.band-full h2{color:#fff;margin:0 0 1.4rem;font:800 clamp(1.6rem,4vw,2.6rem)/1.1 var(--headfont,system-ui,sans-serif)}
.band-full a{color:#9be7d8}
.bcols,.bnums,.bkeys{display:grid;gap:1.2rem;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr))}
.bcol,.bkey{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:1.1rem 1.2rem}
.bcol b,.bkey b{display:block;font-size:1.15rem;margin-bottom:.3rem}
.bcol span,.bkey span{color:#d6d6d2}
.bkey .keyico{display:block;color:var(--bandacc,#5eead4);margin-bottom:.4rem}
.bnum b{display:block;font:900 clamp(2.6rem,7vw,4.4rem)/1 system-ui,sans-serif;color:var(--bandacc,#5eead4)}
.bnum span{display:block;color:#e4e4e0;margin-top:.4rem}.bnum small{display:block;color:#d0d0cb;font-size:.78rem;margin-top:.3rem}
.bcode{margin:1.6rem 0 0;max-width:40rem}.bcode pre{background:#000;border:1px solid #333;border-radius:10px;padding:1rem 1.2rem;overflow-x:auto;color:#7ee787;font:.95rem/1.6 ui-monospace,Menlo,monospace;margin:0}
.bcode figcaption{color:#d0d0cb;font-size:.85rem;margin-top:.4rem}
.bquote{margin:1.6rem 0 0;border-left:5px solid var(--bandacc,#5eead4);padding:.4rem 0 .4rem 1.2rem;max-width:46rem}
.bquote p{font:600 1.3rem/1.45 system-ui,sans-serif;margin:0 0 .4rem}.bquote footer{color:#d0d0cb;font-size:.9rem}
.band-full .people{margin-top:1.4rem;color:#e4e4e0}
.bnote{color:#c9c9c4;margin-top:1rem}

.bflow{list-style:none;margin:1.6rem 0;padding:0;display:grid;gap:2.2rem;counter-reset:z}
@media (min-width:56rem){.bflow{grid-template-columns:repeat(3,1fr);gap:3rem}}
.bzone{position:relative;border:2px solid var(--bandacc,#5eead4);border-radius:16px;padding:1.2rem 1.2rem 1.3rem;display:flex;flex-direction:column;gap:.5rem}
.bzone b{font:800 1.25rem system-ui,sans-serif;color:#fff}.bzone span{color:#e4e4e0}
.zico{fill:none;stroke:var(--bandacc,#5eead4);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.zsample{margin-top:auto;display:block;padding:.5rem .7rem;border-radius:8px;background:rgba(255,255,255,.08);color:#e4e4e0;font:600 .9rem ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.bzone:not(:last-child)::after{content:"";position:absolute;left:50%;bottom:-2.2rem;width:2px;height:2.2rem;background:var(--bandacc,#5eead4)}
@media (min-width:56rem){.bzone:not(:last-child)::after{left:auto;right:-3rem;top:50%;bottom:auto;width:3rem;height:2px}}
.kring-fig{margin:1.4rem 0}.kring{display:block;width:100%;max-width:46rem;margin:0 auto;fill:none;stroke:var(--bandacc,#5eead4);stroke-width:5;stroke-linecap:round}
.kring .kr-link{stroke-width:3;opacity:.8}.kring .kr-hole{fill:currentColor;stroke:none;color:var(--bandacc,#5eead4)}.kring .kr-n{fill:#fff;stroke:none;font:800 34px system-ui,sans-serif}
.kr-list{list-style:none;margin:1rem 0 0;padding:0;display:grid;gap:1.2rem}@media (min-width:48rem){.kr-list{grid-template-columns:repeat(3,1fr);text-align:center}}
.kr-list b{display:block;font:800 1.2rem var(--headfont,system-ui),system-ui,sans-serif;color:#fff;margin-bottom:.3rem}.kr-list span{color:#e4e4e0}
.kr-num{display:inline-grid;place-items:center;width:1.7rem;height:1.7rem;border-radius:50%;background:var(--bandacc,#5eead4);color:#111;font-size:1rem;margin-right:.3rem}
@media (max-width:40rem){.kring .kr-n{font-size:40px}}
.bchat{list-style:none;margin:1.6rem 0;padding:0;display:flex;flex-direction:column;gap:1.4rem;max-width:52rem}
.bub{position:relative;max-width:min(36rem,92%);padding:1rem 1.2rem;border-radius:20px;font-size:1.15rem;line-height:1.5}
.bub b{display:block;font:700 .95rem system-ui,sans-serif;margin-bottom:.3rem}.bub p{margin:0}
.bub-l{align-self:flex-start;background:#f4f1ee;color:#1d2428;border-bottom-left-radius:4px}
.bub-r{align-self:flex-end;background:var(--bandacc,#5eead4);color:#06201c;border-bottom-right-radius:4px}
.kset{list-style:none;margin:1.6rem 0;padding:0;display:grid;gap:2rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr));text-align:center}
.kset li{display:flex;flex-direction:column;align-items:center;gap:.5rem}
.kkey{fill:none;stroke:var(--bandacc,#5eead4);stroke-width:7;stroke-linecap:round;margin-bottom:.4rem}.kkey .kk-hole{fill:var(--bandacc,#5eead4);stroke:none}
.kset b{font:800 1.3rem var(--headfont,system-ui),system-ui,sans-serif;color:#fff}.kset span{color:#ececea;max-width:20rem}
.hero-chat{margin:0;max-width:34rem}.hero-chat .bub{font-size:1.1rem}
.bwhen{margin:.2rem 0 1rem;color:#e4e4e0;font-weight:600}.bnum small:empty{display:none}
.band-full .bnote{color:#ececea}
.hero-shot-k{margin:1.6rem 0 .6rem;font-weight:800;font-size:1.05rem}.ihero .shot-phonelink a{color:#fff;font-weight:700}"""


def setup(build):
    global B
    B = build


def e(s):
    return B.e(s)


def md(s):
    return B.md(s)


# ---------------------------------------------------------------- shared blocks
def next_step(F, depth, cls='next'):
    """The company's own first step, quoted from its real site, as the main buttons."""
    n = F.get('next') or []
    if not n:
        return ''
    btns = ''.join(f'<a class="btn{" primary" if i == 0 else ""}" href="{e(x["url"])}">{e(x["label"])} &#8599;</a>' for i, x in enumerate(n))
    note = None if F.get('next_note_hero_only') else F.get('next_note')  # round 10: said once, under the hero button
    note = f'<p class="next-note">{md(note["t"])}{B.cite(F, note.get("s"), "")}</p>' if note else ''
    return f'<div class="{cls}"><p class="next-k">Next step, on {e(F["url_label"])}</p><div class="btns">{btns}</div>{note}</div>'


def identity_credit(F):
    host = F['url_label']
    return (f'<p class="credit">Logo and screenshots: {e(host)}; each caption gives the date its screenshot was taken. '
            f'Used with Dinis Cruz\'s permission: these are his own companies (relayed by design.b, 20 November 2026). '
            f'Each screenshot links to the real page it shows.</p>')


def page(F, key, depth, title, desc, css, links, body, credit=False):
    extra = identity_credit(F) if credit else ''
    foot = B.foot(F, depth)
    if extra:
        foot = foot.replace('<footer class="foot">', '<footer class="foot">' + extra, 1)
    return B.head(F, key, depth, title, desc, css) + B.nav(F, key, depth, links) + f'<main id="main">{body}</main>' + foot


def sect_links(p, names):
    return [(n, f'#{p}{k}') for k, n in names] + [('Sources', f'#{p}h-src')]


def facts_blocks(F, p, depth):
    """The standard facts, as plain blocks a design can wrap."""
    return {
        'what': B.paras(F, F['what'], p),
        'for': B.bullets(F, F['for_whom'], p),
        'how': B.flow(F, p),
        'products': B.products(F, p),
        'timeline': B.timeline_list(F, p),
        'figures': B.figures(F, p),
        'chart': B.chart(F, p),
        'people': B.people(F, p),
        'story': B.paras(F, F.get('story', F['what']), p),
        'sources': B.sources(F, p),
    }


def palette_css(pal):
    light = ';'.join(f'--{k}:{v}' for k, v in pal['light'].items())
    dark = ';'.join(f'--{k}:{v}' for k, v in pal.get('dark', pal['light']).items())
    return ':root{' + light + '}@media (prefers-color-scheme:dark){:root{' + dark + '}}'


COMMON = """
.btns{display:flex;flex-wrap:wrap;gap:.7rem}
.btn{display:inline-block;padding:.75rem 1.15rem;border-radius:10px;font-weight:700;text-decoration:none;border:2px solid var(--acc);color:var(--acc);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.btn.primary{background:var(--acc);color:var(--acc-ink,#fff)}
.btn:hover{filter:brightness(1.1)}
.next{margin:2.5rem 0;padding:1.4rem 1.5rem;border-radius:16px;background:var(--card);border:1px solid var(--line)}
.next-note{margin:.8rem 0 0;max-width:40rem}
.next-k{margin:0 0 .7rem;font:700 .78rem system-ui,sans-serif;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}
.credit{font-weight:600}
.sources ol{padding-left:1.6rem;font-size:.9rem}.sources .acc,.sources p{color:var(--muted)}
.wrap{max-width:74rem;margin:0 auto;padding:0 1rem}
@media (max-width:40rem){
 .ihero{padding:1rem 0 2rem}.ihero .logo,.chathead .logo{display:none}
 .chathead{padding:1rem 0 2rem}.seal{padding-top:1rem}.seal .ct{display:none}
 .sheet{margin:0 auto;padding-top:.9rem}.sheet .kick{display:none}.sheet h1{margin-top:.2rem;padding-right:5.5rem}.stamp{font-size:.7rem}.stamp{top:.8rem;right:.8rem}
 .stage .lanyard{order:2}.stage{padding-top:.8rem}
 .chero,.shead,.hero{padding-top:1rem}.ghero{padding-top:1.2rem}
}
.exhibit>*,.ihero .wrap>*,.stage>*,.ghero .wrap>*,.strip>*{min-width:0}
.shot figcaption{overflow-wrap:anywhere}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
""" + BAND_CSS


def oneline(F, p, h1=''):
    """Under each h1, one plain line of what it is, in the company's own words (design.b round 2)."""
    o = F.get('oneline')
    if not o or o['t'].strip('."').lower() in re.sub(r'<[^>]+>', '', h1).lower():
        return ''
    return f'<p class="oneline">&ldquo;{e(o["t"])}&rdquo;{B.cite(F, o.get("s"), p)}</p>'


def band(F, depth, d, p):
    """One full-bleed band below the fold, on the home design only (design.b round 2)."""
    b = F.get('band')
    if not b or d['key'] != F['home']:
        return ''
    cols = ''.join(f'<div class="bcol"><b>{e(c["k"])}</b><span>{md(c["t"])}{B.cite(F, c.get("s"), p)}</span></div>' for c in b.get('cols', []))
    flow = ''
    if b.get('flow') and not b.get('chat'):  # round 7: the columns drawn as zones joined by arrows (sgit: machine, server, read key)
        icons = {
            'machine': '<rect x="10" y="10" width="44" height="30" rx="3"/><path d="M4 48 H60 L54 40 H10 Z"/><path d="M20 22 h12 M20 29 h20" />',
            'server': '<rect x="12" y="6" width="40" height="14" rx="3"/><rect x="12" y="25" width="40" height="14" rx="3"/><rect x="12" y="44" width="40" height="12" rx="3"/><path d="M20 13 h4 M20 32 h4 M20 50 h4"/>',
            'key': '<circle cx="18" cy="32" r="11"/><circle cx="18" cy="32" r="3.5"/><path d="M29 32 H60 M48 32 V41 M56 32 V39"/>',
        }
        items = ''.join(f'<li class="bzone"><svg class="zico" viewBox="0 0 64 64" width="56" height="56" aria-hidden="true" focusable="false">{icons.get(c.get("icon"), "")}</svg>'
                        f'<b>{e(c["k"])}</b><span>{md(c["t"])}{B.cite(F, c.get("s"), p)}</span>'
                        + (f'<code class="zsample" aria-hidden="true">{e(c["sample"])}</code>' if c.get('sample') else '') + '</li>' for c in b.get('cols', []))
        flow = f'<ol class="bflow">{items}</ol>' + (f'<p class="bnote">{md(b["flow_note"])}</p>' if b.get('flow_note') else '')
        cols = ''
    if b.get('chat'):  # round 8: the columns as a conversation, speech bubbles left and right; a col with "note" sits below
        bub = '' if d.get('cfg', {}).get('hero') == 'chat' else ''.join(f'<li class="bub {"bub-r" if c.get("side") == "right" else "bub-l"}"><b>{e(c["k"])}</b><p>{md(c["t"])}{B.cite(F, c.get("s"), p)}</p></li>'
                      for c in b.get('cols', []) if not c.get('note'))
        notes = ''.join(f'<p class="bnote">{md(c["t"])}{B.cite(F, c.get("s"), p)}</p>' for c in b.get('cols', []) if c.get('note'))
        flow = (f'<ol class="bchat">{bub}</ol>' if bub else '') + notes
        cols = ''
    if b.get('merge_figures'):  # round 9: the company's published figures join the band's own numbers, one section
        b = dict(b, nums=list(b.get('nums', [])) + [{'n': f['value'], 'l': f['label'], 's': f.get('s'),
                 'when': f['when'] if 'when' in f else 'as published ' + B.fmt_date(f['asof'])} for f in F.get('figures', [])])
    head = f'<p class="bwhen">{e(b["when_head"])}</p>' if b.get('when_head') else ''  # round 14: the shared date once, at the head
    nums = ''.join(f'<div class="bnum"><b>{e(n["n"])}</b><span>{md(n["l"])}{B.cite(F, n.get("s"), p)}</span><small>{e(n.get("when", ""))}</small></div>' for n in b.get('nums', []))
    code = ''
    if b.get('code'):
        code = (f'<figure class="bcode"><pre><code>{e(chr(10).join(b["code"]["lines"]))}</code></pre>'
                f'<figcaption>{md(b["code"]["caption"])}{B.cite(F, b["code"].get("s"), p)}</figcaption></figure>')
    quote = ''
    if b.get('quote'):
        q = b['quote']
        quote = f'<blockquote class="bquote"><p>&ldquo;{e(q["q"])}&rdquo;</p><footer>{md(q["who"])}{B.cite(F, q.get("s"), p)}</footer></blockquote>'
    extra = B.people(F, p) if b.get('people') else ''
    keys = ''
    if b.get('keys'):
        keys = '<div class="bkeys">' + ''.join(f'<div class="bkey"><svg class="keyico" viewBox="0 0 64 32" width="56" height="28" aria-hidden="true" focusable="false"><circle cx="14" cy="16" r="11" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="14" cy="16" r="3.5" fill="currentColor"/><path d="M25 16 H60 M48 16 V25 M56 16 V23" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg><b>{e(k)}</b><span>{md(v)}</span></div>' for k, v in b['keys']) + '</div>'
        if b.get('keys_s'):
            keys += f'<p class="bnote">{md(b["keys_note"])}{B.cite(F, b.get("keys_s"), p)}</p>'
    if b.get('keys') and b.get('ring'):  # round 9: three separate keys side by side, each labelled with what it opens
        key = ('<svg class="kkey" viewBox="0 0 80 200" width="64" height="160" aria-hidden="true" focusable="false">'
               '<circle cx="40" cy="40" r="30"/><circle cx="40" cy="40" r="10" class="kk-hole"/>'
               '<path d="M40 70 V188 M40 140 h24 M40 168 h18"/></svg>')
        items = ''.join(f'<li>{key}<b>{e(k)}</b><span>{md(v)}</span></li>' for k, v in b['keys'])
        keys = f'<ul class="kset" aria-label="Three keys">{items}</ul>'
        if b.get('keys_s'):
            keys += f'<p class="bnote">{md(b["keys_note"])}{B.cite(F, b.get("keys_s"), p)}</p>'
    hf = F['brand'].get('headfont')
    st = f' style="--headfont:{e(hf)}"' if hf else ''
    return (f'<section class="band-full"{st} aria-labelledby="{p}band"><div class="wrap"><h2 id="{p}band">{e(b["title"])}</h2>'
            f'{"<div class=bcols>" + cols + "</div>" if cols else ""}{head}{"<div class=bnums>" + nums + "</div>" if nums else ""}{flow}{keys}{code}{quote}{extra}</div></section>')





# ---------------------------------------------------------------- engine: the terminal (sgit)
def eng_terminal(F, depth, d):
    c = d['cfg']
    p = 't-'
    css = palette_css({'light': {'bg': '#0d1117', 'card': '#161b22', 'fg': '#e6edf3', 'muted': '#9da7b3', 'line': '#30363d', 'link': '#58a6ff', 'acc': '#3fb950', 'acc-ink': '#0d1117'}}) + COMMON + """
body{font:1rem/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.top{--navbg:#010409;--navfg:#e6edf3;--family-fg:#c9d1d9;--family-fg-strong:#fff;--family-bg:#161b22}
.hero{padding:2.5rem 0 1rem}
.hero h1{font-size:clamp(2rem,7vw,4.2rem);line-height:1.02;margin:0 0 .8rem;color:#fff;font-weight:800;letter-spacing:-.02em}
.hero h1 b{color:#3fb950}
.hero p{color:var(--muted);max-width:44rem;font-size:1.05rem}
.install{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin:1.2rem 0}
.install input{font:inherit;font-size:1.05rem;background:#010409;color:#3fb950;border:1px solid #3fb950;border-radius:8px;padding:.6rem .9rem;width:16rem;max-width:100%}
.install label{color:var(--muted);font-size:.85rem}
.sess{display:grid;gap:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:2rem 0}
.sess-h{display:grid;grid-template-columns:1fr;background:#010409;color:var(--muted);font-size:.78rem;text-transform:uppercase;letter-spacing:.1em}
.sess-h span{padding:.5rem 1rem}
@media (min-width:56rem){.sess-h,.step{grid-template-columns:1.4fr 1fr}}
.sess-h span+span{display:none}
@media (min-width:56rem){.sess-h span+span{display:block;border-left:1px solid var(--line)}}
.step{display:grid;grid-template-columns:1fr;border-top:1px solid var(--line)}
.step .you{padding:1rem 1.1rem;background:var(--card)}
.step .srv{padding:1rem 1.1rem;background:#010409;color:#8b949e;font-size:.82rem;overflow-wrap:anywhere}
.step .srv b{color:#d29922;font-weight:400}
@media (min-width:56rem){.step .srv{border-left:1px solid var(--line)}}
.cmd{color:#fff;white-space:pre-wrap;overflow-wrap:anywhere}
.cmd::before{content:"$ ";color:#3fb950}
.typed{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:bottom;max-width:100%;animation:type .7s steps(24,end) both}
@keyframes type{from{width:0}to{width:100%}}
.cmt{color:#8b949e;margin:.45rem 0 0}
.cmt::before{content:"# ";color:#6e7681}
.cmt a{color:#58a6ff}
h2{font-size:1rem;color:#3fb950;margin:2.5rem 0 1rem;text-transform:lowercase}
h2::before{content:"$ cat ";color:#8b949e}
.cards li,.flow li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.9rem 1rem;list-style:none}
.cards,.flow{padding:0;display:grid;gap:.8rem;grid-template-columns:repeat(auto-fill,minmax(16rem,1fr))}
.cards h3{margin:0 0 .3rem;font-size:1rem;color:#fff}.cards p{margin:0;color:color-mix(in srgb,currentColor 90%,transparent);font-size:.9rem}
.flow b{display:block;color:#fff}.flow span{color:var(--muted);font-size:.9rem}
.tl-list{padding-left:1.4rem}.tl-list time{color:#d29922}
.figs{list-style:none;padding:0;display:grid;gap:.8rem;grid-template-columns:repeat(auto-fill,minmax(12rem,1fr))}
.figs li{border:1px solid var(--line);border-radius:10px;padding:.8rem;display:flex;flex-direction:column}
.figs .n{font-size:1.6rem;color:#3fb950;font-weight:800}.figs .d{font-size:.75rem;color:var(--muted)}
.chart{margin:1.2rem 0}.chart figcaption span{display:block;color:var(--muted);font-size:.8rem}
.chart ul{list-style:none;padding:0}.chart li{display:grid;grid-template-columns:6.5rem 1fr 2.5rem;gap:.6rem;align-items:center;font-size:.85rem;margin:.2rem 0}
.chart .bt{height:.9rem;border:1px solid var(--line)}.chart .bb{display:block;height:100%;background:#3fb950}.chart .bv{text-align:right}
"""
    steps = []
    for i, st in enumerate(c['session']):
        cmt = ''.join(f'<p class="cmt">{md(x["t"])}{B.cite(F, x.get("s"), p)}</p>' for x in st.get('notes', []))
        delay = f' style="animation-delay:{i * 0.35:.2f}s"'
        steps.append(f'<div class="step"><div class="you"><div class="cmd"><span class="typed"{delay}>{e(st["cmd"])}</span></div>{cmt}</div>'
                     f'<div class="srv">{st["server"]}</div></div>')
    fb = facts_blocks(F, p, depth)
    body = (f'<div class="wrap"><section class="hero"><h1>{c["h1"]}</h1>{oneline(F, p, c["h1"])}<p>{md(F["lede"])}</p>'
            f'<div class="install"><label for="inst">Copy and run:</label><input id="inst" readonly value="pip install sgit-ai" aria-label="pip install sgit-ai"></div>'
            f'{next_step(F, depth, "nx")}</section>'
            f'<div class="sess" role="group" aria-label="A terminal session, drawn from sgit\'s documentation"><div class="sess-h"><span>Your machine</span><span>What the server sees</span></div>{"".join(steps)}</div>'
            f'<p class="cmt">{e(c["caption"])}</p>'
            f'<h2 id="{p}what">what-it-is.txt</h2>{fb["what"]}'
            f'<h2 id="{p}for">who-it-is-for.txt</h2>{fb["for"]}'
            f'<h2 id="{p}products">components.txt</h2>{fb["products"]}'
            f'<h2 id="{p}story">git-log.txt</h2>{fb["timeline"]}'
            f'<h2>measurements.txt</h2>{fb["figures"]}{fb["chart"]}'
            f'{next_step(F, depth)}{fb["sources"]}</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                sect_links(p, [('what', 'What it is'), ('products', 'Components'), ('story', 'Log')]), body)


# ---------------------------------------------------------------- engine: the vault (sgit)
def cipher(text, n=None):
    h = hashlib.sha256(text.encode()).hexdigest()
    out = (h * (len(text) // 64 + 2))
    n = n or min(len(text), 360)
    return ' '.join(out[i:i + 8] for i in range(0, n, 8))


def eng_vault(F, depth, d):
    c = d['cfg']
    p = 'v-'
    css = palette_css({'light': {'bg': '#faf9f5', 'card': '#ffffff', 'fg': '#1c1d21', 'muted': '#5c5f66', 'line': '#e5e1d5', 'link': '#0f766e', 'acc': '#0f766e', 'acc-ink': '#fff'},
                       'dark': {'bg': '#0e1412', 'card': '#151d1b', 'fg': '#e7efec', 'muted': '#a3b3ae', 'line': '#26332f', 'link': '#5eead4', 'acc': '#5eead4', 'acc-ink': '#04201c'}}) + COMMON + """
body{font:1.06rem/1.65 "Iowan Old Style",Charter,Georgia,serif}
.seal{background:#0d1117;color:#3fb950;padding:3rem 1rem 3.5rem;overflow:hidden;position:relative}
.seal .ct{font:.85rem/1.5 ui-monospace,Menlo,monospace;color:#3fb950;word-break:break-all;max-height:9rem;overflow:hidden}
.seal h1{position:relative;font:800 clamp(2.4rem,8vw,5.2rem)/1 ui-sans-serif,system-ui,sans-serif;color:#fff;margin:1.2rem 0 .8rem;letter-spacing:-.03em}
.seal h1 b{color:#5eead4}
.seal p{color:#c9d1d9;max-width:42rem;font-family:system-ui,sans-serif}
.key{display:inline-flex;align-items:center;gap:.5rem;margin-top:1rem;background:#5eead4;color:#04201c;padding:.7rem 1.1rem;border-radius:999px;font:700 1rem ui-monospace,Menlo,monospace;text-decoration:none}
.key::before{content:"\\1F511"}
.blk{position:relative;margin:2.6rem 0;padding:1.4rem 1.5rem;background:var(--card);border:1px solid var(--line);border-radius:14px}
.blk h2{font:800 1.4rem/1.2 ui-sans-serif,system-ui,sans-serif;margin:0 0 .8rem}
.blk .id{font:.75rem ui-monospace,Menlo,monospace;color:var(--muted);margin:0 0 .6rem}
.blk .srcline{position:relative;z-index:1;background:#0d1117;color:#c9d1d9;opacity:1;display:inline-block;padding:.1rem .6rem;border-radius:6px}
.blk .ct{position:absolute;inset:0;border-radius:14px;background:#0d1117;color:#3fb950;font:.8rem/1.45 ui-monospace,Menlo,monospace;padding:1.2rem 1.4rem;word-break:break-all;overflow:hidden;pointer-events:none;opacity:0}
@supports (animation-timeline:view()){
 .blk .ct{opacity:1;animation:open linear both;animation-timeline:view();animation-range:entry 0% entry 90%}
 @keyframes open{from{opacity:1}to{opacity:0}}
}
.cards{list-style:none;padding:0;display:grid;gap:.8rem;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr))}
.cards li{border-left:4px solid var(--acc);padding:.2rem .9rem}.cards h3{margin:0;font:700 1.05rem system-ui,sans-serif}.cards p{margin:.2rem 0 0;color:color-mix(in srgb,currentColor 90%,transparent)}
.flow{padding-left:1.3rem}.flow li{margin:.4rem 0}.flow b{display:block;font-family:system-ui,sans-serif}
.tl-list{padding-left:1.3rem}.tl-list time{font:700 .9rem system-ui,sans-serif;color:var(--acc);display:block}
.figs{list-style:none;padding:0;display:grid;gap:.8rem;grid-template-columns:repeat(auto-fill,minmax(11rem,1fr))}
.figs li{display:flex;flex-direction:column}.figs .n{font:800 1.8rem system-ui,sans-serif;color:var(--acc)}.figs .d{font-size:.75rem;color:var(--muted)}
"""
    fb = facts_blocks(F, p, depth)
    blocks = [('what', 'What is inside', fb['what'] + fb['for']), ('how', 'How it is sealed', fb['how']),
              ('products', 'The parts', fb['products']), ('story', 'The history', fb['timeline']),
              ('figures', 'The numbers', fb['figures'])]
    out = []
    for k, title, html in blocks:
        plain = re.sub(r'<[^>]+>', ' ', html)
        oid = hashlib.sha256(title.encode()).hexdigest()[:16]
        out.append(f'<section class="blk" id="{p}{k}"><p class="id">obj-{oid}</p><h2>{e(title)}</h2>{html}'
                   f'<div class="ct" aria-hidden="true">{cipher(plain, 900)}</div></section>')
    body = (f'<div class="seal"><div class="wrap"><div class="ct" aria-hidden="true">{cipher(F["lede"], 700)}</div>'
            f'<h1>{c["h1"]}</h1>{oneline(F, p, c["h1"])}<p>{e(c["sub"])}</p>'
            f'<a class="key" href="#{p}what">{e(c["key"])}</a></div></div>'
            f'<div class="wrap">{"".join(out)}{next_step(F, depth)}{fb["sources"]}</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                sect_links(p, [('what', 'Inside'), ('how', 'Sealed'), ('products', 'Parts')]), body)


# ---------------------------------------------------------------- engine: identity (all five, twice)
def eng_identity(F, depth, d):
    c = d['cfg']
    p = d['key'][:3] + '-'
    pal = c['palette']
    css = palette_css(pal) + COMMON + f"""
body{{font:1.05rem/1.62 {c.get('body_font', 'system-ui,-apple-system,"Segoe UI",Roboto,sans-serif')}}}
.top{{--navbg:var(--bg)}}
.ihero{{background:var(--herobg);color:var(--heroink);padding:3rem 0 3.5rem;overflow:hidden}}
.ihero .wrap{{display:grid;gap:2.2rem;align-items:center}}
@media (min-width:58rem){{.ihero .wrap{{grid-template-columns:1fr 1.15fr}}}}
.ihero .logo{{margin-bottom:1.4rem}}
.ihero .logo img{{height:{c.get('logo_h', '3.4rem')}}}
.ihero h1{{font:{c.get('h1_font', '800 clamp(2.6rem,7vw,4.8rem)/1.02 system-ui,sans-serif')};margin:0 0 1rem;letter-spacing:-.02em;color:var(--heroink)}}
.ihero h1 em{{color:var(--heroacc)}}
.ihero .sub{{font-size:1.15rem;opacity:.92;max-width:36rem;margin:0 0 1.4rem}}
.ihero .btn{{border-color:var(--heroacc);color:var(--heroink)}}
.ihero .btn.primary{{background:var(--heroacc);color:var(--heroacc-ink);border-color:var(--heroacc)}}
.ihero .shot figcaption,.ihero .shot figcaption a{{color:var(--heroink);opacity:.85}}
.ihero cite,.ihero .cites a{{color:var(--heroink)}}
h2{{font:{c.get('h2_font', '800 clamp(1.5rem,3.5vw,2.2rem)/1.15 system-ui,sans-serif')};margin:2.6rem 0 1rem}}
.cards{{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr))}}
.cards li{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem}}
.cards h3{{margin:0 0 .3rem;font-size:1.1rem}}.cards h3 a{{color:var(--fg)}}.cards p{{margin:0;color:color-mix(in srgb,currentColor 90%,transparent)}}
.flow{{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr));counter-reset:s}}
.flow li{{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}}
.flow li::before{{content:counter(s);display:grid;place-items:center;width:2rem;height:2rem;border-radius:50%;background:var(--acc);color:var(--acc-ink);font-weight:800;margin-bottom:.5rem}}
.flow b{{display:block}}.flow span{{color:var(--muted);font-size:.95rem}}
.bigfigs{{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(13rem,1fr));margin:0}}
.bigfigs li{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1.1rem}}
.bigfigs b{{display:block;font:800 2.6rem/1 {c.get('num_font', 'system-ui,sans-serif')};color:var(--acc)}}
.bigfigs span{{display:block;color:var(--muted);font-size:.92rem;margin-top:.4rem}}
.bigfigs small{{display:block;color:var(--muted);font-size:.78rem;margin-top:.4rem}}
.tl-list{{padding-left:1.4rem}}.tl-list li{{margin:.4rem 0}}.tl-list time{{font-weight:700;display:block}}
.tl-svg{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem;margin:0 0 1rem}}
.tl-svg .axis{{stroke:var(--fg);stroke-width:3}}.tl-svg .tick{{stroke:var(--muted);stroke-width:2}}.tl-svg .dot{{fill:var(--acc);stroke:var(--card);stroke-width:3}}
.tl-svg .num{{fill:var(--fg);font:800 24px system-ui,sans-serif}}.tl-svg .yr{{fill:var(--muted);font:700 24px system-ui,sans-serif}}.tl-svg figcaption{{font-size:.82rem;color:var(--muted)}}
.two{{display:grid;gap:2rem}}@media (min-width:56rem){{.two{{grid-template-columns:1fr 1fr}}}}
.offer{{border:2px dashed var(--acc);border-radius:12px;padding:1.2rem 1.3rem;background:var(--card);max-width:26rem}}
.offer .tag{{display:inline-block;border:1px solid var(--fg);font:700 .7rem system-ui,sans-serif;text-transform:uppercase;letter-spacing:.1em;padding:.1rem .4rem;margin-bottom:.4rem}}
.offer b{{display:block;font:700 2.2rem Georgia,serif;color:var(--acc)}}
.dial{{max-width:40rem;margin:0 auto}}
.dial .lv{{font:700 22px system-ui,sans-serif}}
.stopcard{{background:var(--card);color:var(--fg);border:2px solid var(--acc);border-radius:12px;padding:.9rem 1.1rem;max-width:26rem;display:flex;align-items:center;gap:.8rem;margin:0 0 1rem}}
.stopcard a{{margin-left:auto;background:var(--acc);color:#fff;border-radius:999px;padding:.2rem .8rem;font-weight:700;text-decoration:none}}
.stopcard:target{{border-style:dashed}}.stopcard:target .st::after{{content:" (stopped: the stop file is written)"}}
.strip{{display:grid;gap:1.4rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr))}}
.strip .shot .bar span{{font-size:.68rem}}
.vcards{{list-style:none;margin:0;padding:0;display:grid;gap:.9rem;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr))}}
.vcards a{{display:block;height:100%;background:var(--card);color:var(--fg);border:1px solid var(--line);border-top:6px solid var(--acc);border-radius:12px;padding:1rem;text-decoration:none;box-shadow:0 10px 30px rgba(0,0,0,.08)}}
.vcards small{{display:block;font:700 .72rem system-ui;letter-spacing:.14em;text-transform:uppercase;color:var(--acc)}}
.vcards b{{display:block;font:700 1.2rem/1.2 "Iowan Old Style",Charter,Georgia,serif;margin:.3rem 0}}.vcards span{{display:block;color:var(--muted);font-size:.92rem}}.vcards em{{display:block;font-style:normal;font-weight:700;margin-top:.5rem;color:var(--acc)}}
.acard{{background:#fff;color:#0e2c2d;border-radius:18px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
.acard-h{{background:#5b3fd6;color:#fff;font-weight:700;padding:.7rem 1.1rem}}
.acard-m{{margin:1.1rem;background:#f1f4f4;border-radius:14px;padding:.9rem 1rem;font-size:1.05rem}}
.acard-k{{margin:0 1.1rem .4rem;font-weight:700;font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:#4a5e5f}}
.chips{{list-style:none;margin:0 1.1rem 1rem;padding:0;display:flex;flex-wrap:wrap;gap:.4rem}}.chips li{{border:1px solid #cfdcdc;border-radius:999px;padding:.25rem .7rem;font-size:.88rem}}
.acard .btn{{margin:0 1.1rem;background:#c23a44;border-color:#c23a44;color:#fff}}.acard-c{{margin:.8rem 1.1rem 1rem;font-size:.8rem;color:#4a5e5f}}.acard-c a{{color:#2b5c60}}
.excerpt{{margin:0;background:#f7f6f2;color:#1a1917;border-radius:4px;padding:1.6rem 1.6rem 1.2rem;box-shadow:0 20px 50px rgba(0,0,0,.4);border-top:8px solid #1a7f5a}}
.excerpt .ex-id{{font:.8rem ui-monospace,Menlo,monospace;color:#4a4845;margin:0}}.excerpt .ex-t{{font:800 1.4rem/1.2 ui-sans-serif,system-ui,sans-serif;margin:.4rem 0 .8rem}}
.excerpt blockquote{{margin:0;font-size:1.15rem;line-height:1.5;border-left:4px solid #1a7f5a;padding-left:1rem}}.excerpt figcaption{{font-size:.82rem;color:#4a4845;margin-top:1rem}}.excerpt a{{color:#1a7f5a}}
.sharecard{{background:linear-gradient(135deg,#0f5a63,#0a3d44);color:#fff;border-radius:18px;padding:2.4rem 2rem;max-width:44rem}}
.sharecard b{{display:block;font:700 clamp(2rem,6vw,3.4rem)/1.05 system-ui,sans-serif}}
.sharecard span{{display:block;font-size:1.3rem;margin-top:.6rem;opacity:.92}}

.ihero .wrap > div > .shot{{background:color-mix(in srgb,var(--heroacc) 14%,var(--herobg));border:1px solid color-mix(in srgb,var(--heroacc) 35%,transparent);border-radius:18px;padding:1rem 1rem .8rem}}
.ihero .wrap > div > .shot figcaption::before{{content:"On the real site: ";font-weight:700}}
.ihero p.sub:empty{{display:none}}"""
    fb = facts_blocks(F, p, depth)
    hero_right = ''
    if c.get('hero') == 'shot':
        hero_right = B.shot(F, depth, c.get('shot', 0), lazy=False)
    elif c.get('hero') == 'chat':  # round 13: the band's conversation, live in the hero
        bub = ''.join(f'<li class="bub {"bub-r" if x.get("side") == "right" else "bub-l"}"><b>{e(x["k"])}</b><p>{md(x["t"])}{B.cite(F, x.get("s"), p)}</p></li>'
                      for x in (F.get('band') or {}).get('cols', []) if not x.get('note'))
        hero_right = f'<ol class="bchat hero-chat" aria-label="{e(c.get("chat_label", "A conversation"))}">{bub}</ol>'
        if c.get('chat_shot') is not None:  # round 14: the real page, right under the conversation
            hero_right += f'<p class="hero-shot-k">{e(c.get("chat_shot_title", "On the real site"))}</p>' + B.shot(F, depth, c['chat_shot'], lazy=False, phone_hide=bool(c.get('chat_shot_phone_link')))
    elif c.get('hero') == 'strip':
        hero_right = '<div class="strip">' + ''.join(B.shot(F, depth, k, lazy=False) for k in c['strip'][:2]) + '</div>'
    elif c.get('hero') == 'sharecard':
        hero_right = f'<div class="sharecard"><b>{e(F["name"])}</b><span>{e(c["share_line"])}</span><span style="font-size:1rem;margin-top:1.6rem">{e(F["url_label"])}</span></div>'
    elif c.get('hero') == 'vaultcards':
        hero_right = '<ul class="vcards">' + ''.join(
            f'<li><a href="{e(v["url"])}"><small>{e(v["cat"])}</small><b>{e(v["title"])}</b><span>&ldquo;{e(v["line"])}&rdquo;</span><em>Open it &#8599;</em></a></li>' for v in c['vaults']) + '</ul>'
    elif c.get('hero') == 'athenacard':
        a = c['athena']
        chips = ''.join(f'<li>{e(x)}</li>' for x in a['prompts'])
        hero_right = (f'<div class="acard"><div class="acard-h">Athena</div><p class="acard-m">&ldquo;{e(a["greeting"])}&rdquo;</p>'
                      f'<p class="acard-k">Prompt examples on its page</p><ul class="chips">{chips}</ul>'
                      f'<a class="btn primary" href="{e(a["url"])}">Ask the real Athena &#8599;</a><p class="acard-c">Quoted from {e(a["host"])}, {e(B.fmt_date(F["updated"]))}{B.cite(F, a.get("s"), p)}</p></div>')
    elif c.get('hero') == 'excerpt':
        x = c['excerpt']
        hero_right = (f'<figure class="excerpt"><p class="ex-id">{e(x["id"])}</p><p class="ex-t">{e(x["title"])}</p><blockquote>&ldquo;{e(x["q"])}&rdquo;</blockquote>'
                      f'<figcaption>One of the sixteen example policies, quoted from <a href="{e(x["url"])}">riskmandate.ai</a>{B.cite(F, x.get("s"), p)}</figcaption></figure>')
    elif c.get('hero') == 'dial':
        hero_right = dial_svg(c['levels'], c.get('mark'))
        if c.get('mark_note'):
            hero_right += f'<p style="margin:.4rem 0 0">{md(c["mark_note"])}{B.cite(F, c.get("mark_s"), p)}</p>'
    extra_left = ''
    if c.get('stopcard'):
        extra_left = f'<div class="stopcard" id="{p}stop"><span class="st">{e(c["stopcard"])}</span><a href="#{p}stop">Stop</a></div>'
    if c.get('offer'):
        o = c['offer']
        extra_left += f'<div class="offer"><span class="tag">{e(o["tag"])}</span><p style="margin:.2rem 0 0">{e(o["title"])}</p><b>{e(o["price"])}</b><p style="margin:.3rem 0 0">{md(o["text"])}{B.cite(F, o.get("s"), p)}</p></div>'
    hs = B.cite(F, c.get('h1_s'), p)
    body = [f'<div class="ihero"><div class="wrap"><div>{B.logo(F, depth, force_plate=c.get("plate", False))}'
            f'<h1>{c["h1"]}</h1>{oneline(F, p, c["h1"])}'
            + (f'<p class="oneline">&ldquo;{e(c["under_h1"])}&rdquo;{B.cite(F, c.get("under_h1_s"), p)}</p>' if c.get('under_h1') else '')
            + f'<p class="sub">{md(c["sub"])}{hs}</p>{extra_left}'
            f'<div class="btns">' + ''.join(f'<a class="btn{" primary" if i == 0 else ""}" href="{e(x["url"])}">{e(x["label"])} &#8599;</a>' for i, x in enumerate(F.get('next', []))) +
            f'</div></div><div>{hero_right}</div></div></div>{band(F, depth, d, p)}<div class="wrap">']
    if c.get('cards'):
        cards = ''.join(f'<li><b>{e(x["n"])}</b><span>{md(x["l"])}{B.cite(F, x.get("s"), p)}</span><small>{e(x["when"])}</small></li>' for x in c['cards'])
        body.append(f'<h2 id="{p}figs">{e(c.get("cards_title", "In its own numbers"))}</h2><ul class="bigfigs">{cards}</ul>')
    if c.get('strip_below'):
        lead = 0 if c.get('hero') in ('shot', 'strip') or c.get('chat_shot') is not None else 1  # the hero already shows one screenshot on phones, or none
        body.append(f'<h2 id="{p}real"{"" if lead else " class=desk-only"}>{e(c.get("strip_title", "On the real site"))}</h2>' + B.more_shots(F, depth, c['strip_below'], lead=lead))
    body.append(f'<div class="two" id="{p}what"><div><h2>What it is</h2>{fb["what"]}</div><div><h2>Who it is for</h2>{fb["for"]}</div></div>')
    body.append(f'<h2 id="{p}how">How it works</h2>{fb["how"]}')
    body.append(f'<h2 id="{p}products">What it offers</h2>{fb["products"]}')
    body.append(f'<h2 id="{p}story">Key dates</h2>{B.timeline_list(F, p, "tl-list tl-rail")}')
    body.append(next_step(F, depth))
    body.append(fb['sources'] + '</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                sect_links(p, [('what', 'What it is'), ('how', 'How it works'), ('products', 'Offer')]), ''.join(body), credit=True)


def dial_svg(levels, mark=None):
    import math
    n = len(levels)
    parts = []
    for i, (lab, col) in enumerate(levels):
        a0 = math.pi + i * math.pi / n
        a1 = math.pi + (i + 1) * math.pi / n
        r0, r1, cx, cy = 120, 230, 260, 260
        pts = [(cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)), (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)),
               (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1)), (cx + r0 * math.cos(a0), cy + r0 * math.sin(a0))]
        dpath = (f'M{pts[0][0]:.1f},{pts[0][1]:.1f} A{r1},{r1} 0 0 1 {pts[1][0]:.1f},{pts[1][1]:.1f} '
                 f'L{pts[2][0]:.1f},{pts[2][1]:.1f} A{r0},{r0} 0 0 0 {pts[3][0]:.1f},{pts[3][1]:.1f} Z')
        am = (a0 + a1) / 2
        tx, ty = cx + 175 * math.cos(am), cy + 175 * math.sin(am)
        parts.append(f'<path d="{dpath}" fill="{col}" stroke="#fff" stroke-width="3"/>'
                     f'<text x="{tx:.0f}" y="{ty + 8:.0f}" text-anchor="middle" class="lv" fill="#fff">{i}</text>')
    needle = ''
    if mark is not None:
        am = math.pi + (mark + .5) * math.pi / n
        needle = (f'<line x1="260" y1="260" x2="{260 + 105 * math.cos(am):.0f}" y2="{260 + 105 * math.sin(am):.0f}" stroke="currentColor" stroke-width="8" stroke-linecap="round"/>'
                  f'<circle cx="260" cy="260" r="16" fill="currentColor"/>')
    lab = 'Six levels, 0 to 5, from ' + levels[0][0] + ' to ' + levels[-1][0] + (f'; the needle at level {mark}' if mark is not None else '')
    legend = ''.join(f'<li><b>{i}</b> {e(l)}</li>' for i, (l, _) in enumerate(levels))
    return (f'<figure class="dial"><svg viewBox="0 0 520 290" role="img" aria-label="{e(lab)}">{"".join(parts)}{needle}</svg>'
            f'<figcaption><ol start="0" style="list-style:none;padding:0;margin:.4rem 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(10rem,1fr));gap:.2rem .8rem">{legend}</ol></figcaption></figure>')


# ---------------------------------------------------------------- engine: the paper (board pack, policy, hand-over)
def eng_paper(F, depth, d):
    c = d['cfg']
    p = 'pp-'
    pal = c.get('palette') or {'light': {'bg': '#e9e6df', 'card': '#ffffff', 'fg': '#1b1b1b', 'muted': '#555', 'line': '#d6d1c6', 'link': F['brand']['accent'], 'acc': F['brand']['accent'], 'acc-ink': '#fff'},
                               'dark': {'bg': '#141414', 'card': '#1e1e1e', 'fg': '#eee', 'muted': '#bbb', 'line': '#3a3a3a', 'link': F['brand']['accent_dark'], 'acc': F['brand']['accent_dark'], 'acc-ink': '#111'}}
    css = palette_css(pal) + COMMON + """
body{font:1.05rem/1.6 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
.sheet{max-width:52rem;margin:2rem auto;background:var(--card);border:1px solid var(--line);box-shadow:0 20px 60px rgba(0,0,0,.18);padding:2.2rem clamp(1rem,4vw,3rem) 2.5rem;position:relative}
.sheet::before{content:"";position:absolute;left:0;right:0;top:0;height:10px;background:var(--acc)}
.stamp{position:absolute;right:1.4rem;top:1.6rem;transform:rotate(6deg);border:3px solid var(--acc);color:var(--acc);font:800 .85rem system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;padding:.3rem .6rem;border-radius:6px}
.kick{font:700 .78rem system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin:0 0 .4rem}
h1{font-size:clamp(1.9rem,5.5vw,3rem);line-height:1.08;margin:0 0 1.2rem;max-width:34rem}
.fields{display:grid;grid-template-columns:auto 1fr;gap:.25rem 1rem;font:.95rem system-ui,sans-serif;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:.8rem 0;margin:0 0 1.6rem}
.fields dt{color:var(--muted);font-weight:600}.fields dd{margin:0}
.agenda{font-family:system-ui,sans-serif;background:var(--bg);padding:1rem 1.2rem;border-radius:8px;margin:0 0 2rem}
.agenda b{display:block;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:.3rem}
.agenda ol{margin:0;padding-left:1.4rem}.agenda a{color:var(--fg)}
.item{margin:0 0 2rem}
.item h2{font-size:1.35rem;margin:0 0 .6rem;display:flex;gap:.7rem;align-items:baseline}
.item h2 span{font:800 .95rem system-ui,sans-serif;color:var(--acc-ink);background:var(--acc);border-radius:6px;padding:.05rem .45rem}
.note{border-left:5px solid var(--acc);padding:.6rem 1rem;background:var(--bg);font-style:italic}
.cards{list-style:none;padding:0;margin:0}.cards li{border-top:1px solid var(--line);padding:.6rem 0}.cards h3{display:inline;font-size:1.05rem;margin:0}.cards h3::after{content:": "}.cards p{display:inline;margin:0}
.flow{padding-left:1.4rem}.flow li{margin:.4rem 0}.flow b::after{content:": "}
.tl-list{padding-left:1.4rem;font-family:system-ui,sans-serif;font-size:.95rem}.tl-list time{font-weight:700}
.figs{list-style:none;padding:0;display:grid;gap:.6rem;grid-template-columns:repeat(auto-fill,minmax(11rem,1fr));font-family:system-ui,sans-serif}
.figs li{display:flex;flex-direction:column;border:1px solid var(--line);padding:.6rem}.figs .n{font-size:1.5rem;font-weight:800;color:var(--acc)}.figs .d{font-size:.75rem;color:var(--muted)}
.keytag{display:flex;flex-wrap:wrap;gap:1rem;margin:1rem 0 2rem;font-family:system-ui,sans-serif}
.keytag div{flex:1 1 12rem;border:2px solid var(--acc);border-radius:12px 40px 40px 12px;padding:1rem 1.2rem;position:relative;background:var(--bg)}
.keytag div::before{content:"";position:absolute;right:1rem;top:50%;width:1rem;height:1rem;margin-top:-.5rem;border-radius:50%;border:2px solid var(--acc);background:var(--card)}
.keytag b{display:block;font-size:1.15rem}.keytag span{color:var(--muted);font-size:.9rem}
.formf{display:grid;grid-template-columns:1fr;gap:0;border:1px solid var(--line);font-family:system-ui,sans-serif;margin:0 0 2rem}
.formf div{display:grid;grid-template-columns:1fr;border-bottom:1px solid var(--line)}
@media (min-width:44rem){.formf div{grid-template-columns:11rem 1fr}}
.formf div:last-child{border-bottom:0}
.formf b{background:var(--bg);padding:.6rem .8rem;font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.formf span{padding:.6rem .8rem}
.sig{font-family:system-ui,sans-serif;color:var(--muted);border-top:1px solid var(--line);padding-top:.8rem;font-size:.9rem}
@media print{.sheet{box-shadow:none;border:0;margin:0}}
/* the policy form: a ruled, numbered form */
.sheet.policyform{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;border:2px solid var(--fg);box-shadow:8px 8px 0 var(--acc);border-radius:0}
.sheet.policyform::before{height:2.4rem;background:var(--fg)}
.sheet.policyform .kick{position:relative;color:var(--bg);margin-top:-1.55rem;margin-bottom:1.6rem}
.sheet.policyform h1{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:800;letter-spacing:-.02em}
.sheet.policyform .stamp{border-radius:0;transform:none;top:3.2rem}
.sheet.policyform .formf{border:2px solid var(--fg)}.sheet.policyform .formf b{background:var(--fg);color:var(--bg)}
.sheet.policyform .item h2 span{border-radius:0}
.sheet.policyform .agenda{border:1px dashed var(--muted);background:transparent}
/* the luggage tag: the whole page is a tag on a string */
.sheet.luggage{max-width:46rem;border-radius:22px;clip-path:polygon(12% 0,88% 0,100% 7%,100% 100%,0 100%,0 7%);padding-top:6.5rem;border:3px solid var(--acc);background:linear-gradient(var(--card),var(--card)) padding-box}
.sheet.luggage::before{left:50%;top:1.6rem;right:auto;width:3.2rem;height:3.2rem;margin-left:-1.6rem;border-radius:50%;background:var(--bg);border:5px solid var(--acc);box-sizing:border-box}
.sheet.luggage::after{content:"";position:absolute;left:50%;top:-3rem;width:4px;height:4.8rem;margin-left:-2px;background:var(--acc);transform:rotate(18deg);transform-origin:bottom}
.sheet.luggage .stamp{transform:rotate(-8deg);top:7rem;right:3rem}
.sheet.luggage h1{text-align:center;margin-left:auto;margin-right:auto}
.sheet.luggage .kick{text-align:center}
.sheet.luggage .fields{grid-template-columns:auto 1fr;border-style:dashed}
.wrapper-luggage{padding-top:3rem}
/* the board paper: a minuted document with a margin rule */
.sheet.boardpaper{border-left:2.6rem solid var(--bg);box-shadow:0 20px 60px rgba(0,0,0,.18),inset 1px 0 0 var(--line)}
.sheet.boardpaper .item h2{border-bottom:1px solid var(--line);padding-bottom:.3rem}
.sheet.boardpaper .agenda{border-left:5px solid var(--acc);border-radius:0}
@media (max-width:40rem){.sheet.boardpaper{border-left-width:.8rem}.sheet.luggage{clip-path:polygon(16% 0,84% 0,100% 4%,100% 100%,0 100%,0 4%);padding-top:2.6rem}.sheet.luggage::before{top:.5rem;width:1.8rem;height:1.8rem;margin-left:-.9rem;border-width:3px}.sheet.luggage::after{display:none}.wrapper-luggage{padding-top:.3rem}.sheet.luggage .stamp{top:3rem;right:1rem}}
"""
    fb = facts_blocks(F, p, depth)
    fields = ''.join(f'<dt>{e(k)}</dt><dd>{md(v)}</dd>' for k, v in c['fields'])
    items = c['items']
    agenda = ''.join(f'<li><a href="#{p}i{i}">{e(it["title"])}</a></li>' for i, it in enumerate(items, 1))
    out = []
    for i, it in enumerate(items, 1):
        if it['kind'] == 'text':
            inner = f'<p class="note">{md(it["text"])}{B.cite(F, it.get("s"), p)}</p>'
        elif it['kind'] == 'keytag':
            inner = '<div class="keytag">' + ''.join(f'<div><b>{e(k)}</b><span>{md(v)}</span></div>' for k, v in it['keys']) + '</div>'
        elif it['kind'] == 'form':
            inner = '<div class="formf">' + ''.join(f'<div><b>{e(k)}</b><span>{md(v)}{B.cite(F, s, p)}</span></div>' for k, v, s in it['rows']) + '</div>'
        elif it['kind'] == 'shot':
            inner = B.shot(F, depth, it['shot'])
        else:
            inner = ''.join(fb[k] for k in it['kind'].split('+'))
        out.append(f'<section class="item" id="{p}i{i}"><h2><span>{i}</span>{e(it["title"])}</h2>{inner}</section>')
    body = (('<div class="wrapper-luggage">' if c.get('variant') == 'luggage' else '<div>') + f'<div class="sheet {c.get("variant", "")}"><span class="stamp">{e(c["stamp"])}</span><p class="kick">{e(c["kick"])}</p><h1>{md(c["h1"])}</h1>{oneline(F, p, c["h1"])}'
            f'<dl class="fields">{fields}</dl><nav class="agenda" aria-label="Contents"><b>{e(c.get("agenda", "Agenda"))}</b><ol>{agenda}</ol></nav>'
            f'{"".join(out)}{next_step(F, depth)}<p class="sig">{md(c["sig"])}</p>{fb["sources"]}</div></div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                [(it.get('short', it['title'].split(':')[0]), f'#{p}i{i}') for i, it in list(enumerate(items, 1))[:3]] + [('Sources', f'#{p}h-src')], body)


# ---------------------------------------------------------------- engine: the conversation (Ask Athena)
def eng_chat(F, depth, d):
    c = d['cfg']
    p = 'c-'
    pal = c['palette']
    css = palette_css(pal) + COMMON + """
body{font:1.04rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.chathead{background:var(--herobg);color:#fff;padding:2.4rem 0 2rem}
.chathead h1{font-size:clamp(2.2rem,6.5vw,4rem);line-height:1.04;margin:.8rem 0 .6rem}
.chathead p{max-width:40rem;opacity:.92}
.chathead .logo{margin-bottom:.4rem}.chathead .logo img{height:3rem}
.win{max-width:50rem;margin:-1rem auto 0;background:var(--card);border-radius:18px;box-shadow:0 20px 60px rgba(0,0,0,.2);overflow:hidden;border:1px solid var(--line)}
.win-h{background:var(--acc2);color:#fff;padding:.7rem 1.1rem;font-weight:700;display:flex;justify-content:space-between}
.msgs{padding:1.2rem;display:flex;flex-direction:column;gap:1rem}
.m{max-width:88%;padding:.8rem 1rem;border-radius:16px;animation:pop .45s both}
.m.q{align-self:flex-end;background:var(--acc);color:var(--acc-ink);border-bottom-right-radius:4px}
.m.a{align-self:flex-start;background:var(--bg);border:1px solid var(--line);border-bottom-left-radius:4px}
.m.a .who{display:block;font-size:.78rem;font-weight:700;color:var(--acc2);margin-bottom:.2rem}
.m p{margin:.2rem 0}.m ul,.m ol{margin:.3rem 0;padding-left:1.2rem}
.m.a .cards{list-style:none;padding:0}.m.a .cards h3{font-size:1rem;margin:.4rem 0 0}.m.a .cards p{color:color-mix(in srgb,currentColor 90%,transparent)}
.m.a .flow b{display:block}.m.a .tl-list time{font-weight:700}
.m.a .figs{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(9rem,1fr));gap:.4rem}.m.a .figs li{display:flex;flex-direction:column}.m.a .figs .n{font-weight:800;font-size:1.3rem;color:var(--acc2)}.m.a .figs .d{font-size:.72rem;color:var(--muted)}
@keyframes pop{from{transform:translateY(10px)}to{transform:none}}
.prompts{display:flex;flex-wrap:wrap;gap:.5rem;padding:0 1.2rem 1.2rem}
.prompts a{border:1px solid var(--line);border-radius:999px;padding:.3rem .8rem;text-decoration:none;color:var(--fg);font-size:.88rem;background:var(--bg)}
.shotwrap{max-width:50rem;margin:2.5rem auto}
"""
    fb = facts_blocks(F, p, depth)
    msgs = []
    for i, m in enumerate(c['messages']):
        delay = f' style="animation-delay:{min(i, 6) * .12:.2f}s"'
        if m['who'] == 'q':
            msgs.append(f'<div class="m q"{delay}><p>{e(m["text"])}</p></div>')
        else:
            inner = fb[m['block']] if m.get('block') else f'<p>{md(m["text"])}{B.cite(F, m.get("s"), p)}</p>'
            anchor = f' id="{p}{m["id"]}"' if m.get('id') else ''
            msgs.append(f'<div class="m a"{anchor}{delay}><span class="who">{e(c["bot"])}</span>{inner}</div>')
    prompts = ''.join(f'<a href="{e(x["url"])}">{e(x["label"])}</a>' for x in c.get('prompts', []))
    body = (f'<div class="chathead"><div class="wrap">{B.logo(F, depth, force_plate=True)}<h1>{e(c["h1"])}</h1>{oneline(F, p, c["h1"])}<p>{md(c["sub"])}</p></div></div>'
            f'<div class="wrap"><div class="win" role="group" aria-label="A conversation, answered from the company\'s own pages"><div class="win-h"><span>{e(c["bot"])}</span><span>{e(c["win_note"])}</span></div>'
            f'<h2 class="sr">The conversation</h2><div class="msgs">{"".join(msgs)}</div>' + (f'<p style="padding:0 1.2rem;margin:0 0 .4rem;font-size:.85rem;color:var(--muted)">{e(c["prompts_note"])}</p><div class="prompts">{prompts}</div>' if prompts else '') +
            f'</div><div class="shotwrap">{B.shot(F, depth, c.get("shot", 1))}</div>{next_step(F, depth)}{fb["sources"]}</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                [('Athena', f'#{p}athena'), ('The parts', f'#{p}parts'), ('Dates', f'#{p}dates'), ('Sources', f'#{p}h-src')], body, credit=True)


# ---------------------------------------------------------------- engine: the gap (RiskMandate)
def eng_gap(F, depth, d):
    c = d['cfg']
    p = 'g-'
    css = palette_css({'light': {'bg': '#f7f6f2', 'card': '#fff', 'fg': '#1a1917', 'muted': '#4a4845', 'line': '#e2dfd8', 'link': '#1a7f5a', 'acc': '#1a7f5a', 'acc-ink': '#fff'},
                       'dark': {'bg': '#1b1b19', 'card': '#252523', 'fg': '#f7f6f2', 'muted': '#b8b5ae', 'line': '#3d3c38', 'link': '#22c55e', 'acc': '#22c55e', 'acc-ink': '#0d0d0c'}}) + COMMON + """
body{font:1.05rem/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.ghero{background:#0d0d0c;color:#f7f6f2;padding:2.6rem 0 3rem}
@media (prefers-color-scheme:dark){.ghero,.band-full{border-block:1px solid #3d3c38}}
.ghero .wrap{display:grid;gap:2rem;align-items:center}
@media (min-width:58rem){.ghero .wrap{grid-template-columns:1fr 1.1fr}}
.ghero h1{font:800 clamp(2.4rem,7vw,4.6rem)/1.02 ui-sans-serif,system-ui,sans-serif;margin:0 0 1rem;letter-spacing:-.03em}
.ghero h1 em{color:#22c55e}
.ghero p{color:#cfccc4;max-width:34rem}
.ghero .btn{border-color:#22c55e;color:#f7f6f2}.ghero .btn.primary{background:#22c55e;color:#0d0d0c}
.gap svg{width:100%;max-width:40rem}
.gap .reach{fill:#2b2a27;stroke:#8a8780;stroke-width:2}
.gap .auth{fill:#0d0d0c;stroke:#f7f6f2;stroke-width:3}
.gap .delta{fill:url(#g-hatch)}.gap .grant{fill:#0d0d0c;stroke:#f7f6f2;stroke-width:4}.gap .pill{fill:#0d0d0c}
.gap .barrier{stroke:#ffd166;stroke-width:6;stroke-dasharray:960;stroke-dashoffset:960;animation:draw 1.2s .4s ease-out forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.gap text{font:800 25px ui-sans-serif,system-ui,sans-serif;fill:#f7f6f2}
.gap .small{font:600 21px ui-sans-serif,system-ui,sans-serif;fill:#e4e1da}
.parts{display:grid;gap:1.2rem;margin:2.4rem 0}
@media (min-width:56rem){.parts{grid-template-columns:repeat(4,1fr)}}
.part{background:var(--card);border:1px solid var(--line);border-top:6px solid var(--c);border-radius:12px;padding:1rem 1.1rem}
.part b{display:block;font:800 1.2rem ui-sans-serif,system-ui,sans-serif;margin-bottom:.3rem}
.part span{color:var(--muted);font-size:.95rem}
h2{font:800 clamp(1.5rem,3.4vw,2.1rem)/1.15 ui-sans-serif,system-ui,sans-serif;margin:2.6rem 0 1rem}
.cards{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr))}
.cards li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1rem}.cards h3{margin:0 0 .3rem;font-size:1.05rem}.cards h3 a{color:var(--fg)}.cards p{margin:0;color:color-mix(in srgb,currentColor 90%,transparent);font-size:.95rem}
.figs{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(13rem,1fr))}
.figs li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1.1rem;display:flex;flex-direction:column}.figs .n{font:900 clamp(2.2rem,4.6vw,3.4rem)/1 system-ui,sans-serif;color:var(--acc);margin-bottom:.4rem;white-space:nowrap}.figs .d{font-size:.85rem;color:var(--muted)}
.gapchart{margin:0 0 2.4rem}.gapchart .chart{margin-top:0}
.chart{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1rem;margin-top:1rem}.chart figcaption span{display:block;color:var(--muted);font-size:.85rem}
.chart ul{list-style:none;padding:0}.chart li{display:grid;grid-template-columns:7rem 1fr 4rem;gap:.6rem;align-items:center;margin:.3rem 0}
.chart .bv{white-space:nowrap}
.chart .bt{height:1rem;background:var(--line);border-radius:4px;overflow:hidden}.chart .bb{display:block;height:100%;background:var(--acc)}.chart .bv{text-align:right;font-weight:700}
.tl-list{padding-left:1.4rem}.tl-list time{font-weight:700;display:block}

.gap .onfill{paint-order:stroke;stroke:#0d3b2a;stroke-width:6px;stroke-linejoin:round}.gap text.onfill{fill:#fff}
@media (max-width:40rem){.parts{gap:.6rem!important;margin:1.4rem 0!important}.part{padding:.7rem .9rem!important}.part b{margin-bottom:.1rem!important}}"""
    fb = facts_blocks(F, p, depth)
    how = F['how']
    cols = ['#8a8780', '#f7f6f2', '#1a7f5a', '#ffd166']
    parts = ''.join(f'<div class="part" style="--c:{cols[i % 4]}"><b>{e(h["title"])}</b>'
                    + (f'<span class="desk-only">{md(h["t"])}</span><span class="phone-only">{md(h["t_short"])}</span>' if h.get('t_short') else f'<span>{md(h["t"])}</span>')
                    + f'{B.cite(F, h.get("s"), p)}</div>' for i, h in enumerate(how))
    svg = ('<figure class="gap"><svg viewBox="0 0 640 540" role="img" aria-label="The gap: the grant is everything the agent can reach; inside it sits the mandate, what you authorised; '
           'the rest of the grant, hatched in green, is the delta; a barrier is drawn round the mandate.">'
           '<defs><pattern id="g-hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="14" height="14" fill="#1a7f5a"/><rect width="5" height="14" fill="#22c55e"/></pattern></defs>'
           '<rect x="6" y="6" width="628" height="528" rx="30" class="grant"/>'
           '<text x="34" y="52">The grant</text><text x="34" y="84" class="small">everything the agent can reach</text>'
           '<path d="M50 108 H590 a22 22 0 0 1 22 22 V452 a22 22 0 0 1 -22 22 H50 a22 22 0 0 1 -22 -22 V130 a22 22 0 0 1 22 -22 Z M70 204 V398 a26 26 0 0 0 26 26 H276 a26 26 0 0 0 26 -26 V204 a26 26 0 0 0 -26 -26 H96 a26 26 0 0 0 -26 26 Z" fill-rule="evenodd" class="delta"/>'
           '<rect x="82" y="190" width="208" height="222" rx="22" class="auth"/>'
           '<rect x="70" y="178" width="232" height="246" rx="28" fill="none" class="barrier"/>'
           '<text x="98" y="240">The mandate</text><text x="104" y="272" class="small">what you</text><text x="104" y="298" class="small">authorised</text>'
           '<rect x="332" y="244" width="262" height="114" rx="14" class="pill"/>'
           '<text x="350" y="282">The delta</text><text x="350" y="314" class="small">reach nobody</text><text x="350" y="342" class="small">authorised</text>'
           '<text x="34" y="512" class="small" style="fill:#ffd166">the barrier, round the mandate</text></svg>'
           '<figcaption style="color:#cfccc4;font-size:.85rem">Drawn for this site from RiskMandate\'s four objects: mandate, grant, delta and barrier.</figcaption></figure>')
    btns = ''.join(f'<a class="btn{" primary" if i == 0 else ""}" href="{e(x["url"])}">{e(x["label"])} &#8599;</a>' for i, x in enumerate(F.get('next', [])))
    body = (f'<div class="ghero"><div class="wrap"><div><h1>{c["h1"]}</h1>{oneline(F, p, c["h1"])}<p>{md(F["lede"])}</p><div class="btns">{btns}</div></div>{svg}</div></div>'
            f'<div class="wrap"><div class="parts" id="{p}how">{parts}</div>'
            + (f'<section class="gapchart" aria-label="Measured">{fb["chart"]}</section>' if fb["chart"] else '')
            + f'</div>{band(F, depth, d, p)}<div class="wrap">'
            f'<h2 id="{p}what">The gap, in plain words</h2>{fb["what"]}'
            f'<h2>Who looks at the gap</h2>{fb["for"]}'
            f'<h2 id="{p}products">What closes it</h2>{fb["products"]}'
            f'{"" if (F.get("band") or {}).get("merge_figures") else "<h2>Measured on its own team</h2>" + fb["figures"]}'
            f'<h2 id="{p}story">Key dates</h2>{B.timeline_list(F, p, "tl-list tl-rail")}'
            f'{next_step(F, depth)}{fb["sources"]}</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                sect_links(p, [('how', 'The four objects'), ('what', 'The gap'), ('products', 'What closes it')]), body)


# ---------------------------------------------------------------- engine: the cell (AgentiCCells)
def eng_cell(F, depth, d):  # cfg 'shot': index of a real screenshot shown after the diagram (round 7)
    c = d['cfg']
    p = 'cl-'
    css = palette_css({'light': {'bg': '#f8f5f1', 'card': '#fff', 'fg': '#17141a', 'muted': '#4f4a55', 'line': '#e4ddd6', 'link': '#a8205a', 'acc': '#a8205a', 'acc-ink': '#fff'},
                       'dark': {'bg': '#141116', 'card': '#1e1a21', 'fg': '#f2eef4', 'muted': '#b9b0bd', 'line': '#342d38', 'link': '#f0a7c4', 'acc': '#f0a7c4', 'acc-ink': '#14101a'}}) + COMMON + """
body{font:1.05rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.chero{padding:2.4rem 0 1rem}
.chero h1{font:900 clamp(2.4rem,7.5vw,5rem)/1 system-ui,sans-serif;margin:0 0 .8rem;letter-spacing:-.03em}
.chero h1 em{color:var(--acc);font-style:normal}
.chero p{max-width:40rem;color:var(--muted)}
.cellbox{position:relative;border:3px solid var(--acc);border-radius:44px;padding:2rem 1.2rem 1.4rem;margin:2rem 0;background:radial-gradient(circle at 50% 40%,rgba(168,32,90,.10),transparent 60%),var(--card)}
.cellbox .env{position:absolute;top:-.8rem;left:1.6rem;background:var(--bg);padding:0 .6rem;font:700 .78rem system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--acc)}
.cond{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .8rem;justify-content:center;margin:0 0 1.4rem;text-align:center}
.cond b{white-space:nowrap}
.cond i{width:3.2rem;height:3.2rem;border-radius:50%;background:var(--acc);color:var(--acc-ink);display:grid;place-items:center;font:800 1.2rem system-ui;font-style:normal;animation:pulse 1.6s ease-in-out infinite}
.cond b{font-size:1.1rem}
@keyframes pulse{50%{box-shadow:0 0 0 12px rgba(168,32,90,.15)}}
.agents{list-style:none;padding:0;margin:0;display:grid;gap:.9rem;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr))}
.agents li{border:2px solid var(--line);border-radius:18px;padding:.9rem 1rem;background:var(--bg);position:relative}
.agents li::before{content:"";position:absolute;right:.9rem;top:.9rem;width:.7rem;height:.7rem;border-radius:50%;background:#2fb36b;animation:blink 1.2s steps(2) infinite}
@keyframes blink{50%{opacity:.25}}
.agents b{display:block}.agents span{color:var(--muted);font-size:.93rem}
.stopbar{display:flex;flex-wrap:wrap;align-items:center;gap:.8rem;justify-content:space-between;margin:1.2rem 0;border:2px solid var(--acc);border-radius:14px;padding:.7rem 1rem;background:var(--card)}
.stopbar a{background:#c81e4a;color:#fff;font-weight:800;border-radius:999px;padding:.4rem 1.1rem;text-decoration:none}
.stopbar .resume{display:none;background:var(--fg);color:var(--bg)}
.halted{display:none;font-weight:700;color:#c81e4a}
#cell-stop:target .agents li::before{background:#c81e4a;animation:none}
#cell-stop:target .cond i{animation:none;background:#777}
#cell-stop:target .halted{display:block}
#cell-stop:target .stopbar .go{display:none}#cell-stop:target .stopbar .resume{display:inline-block}
h2{font:800 clamp(1.5rem,3.4vw,2.1rem)/1.15 system-ui,sans-serif;margin:2.4rem 0 1rem}
.cards{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr))}
.cards li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}.cards h3{margin:0 0 .3rem}.cards h3 a{color:var(--fg)}.cards p{margin:0;color:color-mix(in srgb,currentColor 90%,transparent)}
.chart{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}.chart figcaption span{display:block;color:var(--muted);font-size:.85rem}
.realshot{margin:2.4rem 0 1rem}.realshot-in .strip.desk-only{display:grid;gap:1.6rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,26rem),1fr))}
.chart ul{list-style:none;padding:0}.chart li{display:grid;grid-template-columns:7.5rem 1fr 5.5rem;gap:.6rem;align-items:center;margin:.3rem 0}
.chart .bv{white-space:nowrap}
.chart .bt{height:1rem;background:var(--line);border-radius:4px;overflow:hidden}.chart .bb{display:block;height:100%;background:var(--acc)}.chart .bv{text-align:right;font-weight:700}
.figs{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(12rem,1fr))}.figs li{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.8rem}.figs .n{font:800 1.8rem system-ui;color:var(--acc)}.figs .d{font-size:.75rem;color:var(--muted)}
.tl-list{padding-left:1.4rem}.tl-list time{font-weight:700;display:block}

@media (max-width:40rem){.agents-scroll{overflow-x:auto;scroll-snap-type:x mandatory;margin:0;padding:0 0 .6rem;scrollbar-width:thin}.agents-scroll:focus-visible{outline:3px solid var(--acc);outline-offset:2px}.agents{display:flex!important;gap:.6rem!important;width:max-content}.agents li{flex:0 0 13rem;scroll-snap-align:start;padding:.8rem .9rem!important}.agents-cue{margin:.2rem 0 .5rem;font-weight:700;color:var(--acc)}}"""
    fb = facts_blocks(F, p, depth)
    agents = ''.join(f'<li><b>{e(h["title"])}</b><span>{md(h["t"])}{B.cite(F, h.get("s"), p)}</span></li>' for h in F['how'])
    btns = ''.join(f'<a class="btn{" primary" if i == 0 else ""}" href="{e(x["url"])}">{e(x["label"])} &#8599;</a>' for i, x in enumerate(F.get('next', [])))
    body = (f'<div class="wrap"><section class="chero"><h1>{c["h1"]}</h1>{oneline(F, p, c["h1"])}<p>{md(F["lede"])}</p><div class="btns">{btns}</div></section>'
            + (f'<section class="realshot" aria-labelledby="{p}real"><h2 id="{p}real">'
               + (f'<span class="desk-only">{e(c.get("shot_title", "The real thing"))}</span><span class="phone-only">{e(c["shot_title_phone"])}</span>' if c.get('shot_title_phone') else e(c.get("shot_title", "The real thing")))
               + f'</h2><div class="realshot-in">{B.more_shots(F, depth, c["shot"] if isinstance(c["shot"], list) else [c["shot"]], lead=1)}</div></section>' if c.get('shot') is not None else '')
            + f'<section class="cellbox" id="cell-stop" aria-label="One cell, drawn: a conductor and its agents inside your environment"><span class="env">Your environment</span>'
            f'<div class="cond"><i>C</i><b>The conductor</b><span style="color:var(--muted)">hands out the work and keeps the record</span></div>'
            f'<div class="stopbar"><span>{e(c["stopline"])}</span><span><a class="go" href="#cell-stop">Stop</a><a class="resume" href="#{p}what">Resume</a></span></div>'
            f'<p class="halted">{e(c["halted"])}</p><p class="agents-cue phone-only" aria-hidden="true">Five agents, side by side: swipe &#8594;</p><div class="agents-scroll" role="region" aria-label="The agents in the cell, side by side" tabindex="0"><ul class="agents">{agents}</ul></div></section>'
            f'<p style="font-size:.85rem;color:var(--muted)">{e(c["caption"])}</p>'
            + f'</div>{band(F, depth, d, p)}<div class="wrap">'
            f'<h2 id="{p}what">What a cell is</h2>{fb["what"]}<h2>Who it is for</h2>{fb["for"]}'
            f'<h2 id="{p}products">Sizes and offers</h2>{fb["products"]}{fb["chart"]}'
            f'<h2 id="{p}story">How it started</h2>{fb["timeline"]}{"" if (F.get("band") or {}).get("merge_figures") else "<h2>Counted</h2>" + fb["figures"]}'
            f'{next_step(F, depth)}{fb["sources"]}</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                sect_links(p, [('what', 'What a cell is'), ('products', 'Sizes'), ('story', 'Start')]), body)


# ---------------------------------------------------------------- engine: the badge (Web Summit to live site)
def eng_badge(F, depth, d):
    c = d['cfg']
    p = 'bd-'
    css = palette_css({'light': {'bg': '#1b1024', 'card': '#241630', 'fg': '#f6eef8', 'muted': '#cbb9d2', 'line': '#3d2a4a', 'link': '#f0a7c4', 'acc': '#f0a7c4', 'acc-ink': '#1b1024'}}) + COMMON + """
body{font:1.05rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.top{--navbg:#14101a;--navfg:#f2eef4;--family-fg:#e0d4e6;--family-fg-strong:#fff;--family-bg:#241630}
.stage{display:grid;gap:2rem;align-items:start;padding:2rem 0 1rem}
@media (min-width:58rem){.stage{grid-template-columns:22rem 1fr}}
.lanyard{position:relative;padding-top:5rem;max-width:22rem;margin:0 auto}
.lanyard::before{content:"";position:absolute;top:0;left:50%;width:2.4rem;height:5.4rem;margin-left:-1.2rem;background:repeating-linear-gradient(45deg,#a8205a 0 10px,#f0a7c4 10px 20px);clip-path:polygon(0 0,100% 0,70% 100%,30% 100%)}
.badge{background:#fff;color:#17141a;border-radius:16px;padding:1.4rem 1.3rem 1.2rem;box-shadow:0 30px 60px rgba(0,0,0,.45);transform:rotate(-3deg);animation:swing 3s ease-in-out infinite alternate;transform-origin:50% -4rem}
@keyframes swing{from{transform:rotate(-3deg)}to{transform:rotate(2deg)}}
.badge .hole{width:3rem;height:.6rem;border-radius:9px;background:#e8e2ea;margin:0 auto 1rem}
.badge small{display:block;font:700 .72rem system-ui;letter-spacing:.16em;text-transform:uppercase;color:#a8205a}
.badge b{display:block;font:900 2.1rem/1.05 system-ui;margin:.3rem 0}
.badge span{display:block;color:#4f4a55}
.badge .tier{margin-top:1rem;background:#a8205a;color:#fff;font:800 .9rem system-ui;text-transform:uppercase;letter-spacing:.12em;text-align:center;padding:.4rem;border-radius:8px}
h1{font:900 clamp(2.4rem,7vw,4.6rem)/1.02 system-ui,sans-serif;margin:0 0 1rem;letter-spacing:-.03em}
h1 em{font-style:normal;color:#f0a7c4}
.road{list-style:none;padding:0;margin:1.6rem 0;position:relative}
.road::before{content:"";position:absolute;left:1.05rem;top:.5rem;bottom:.5rem;width:4px;background:linear-gradient(#f0a7c4,#a8205a)}
.road li{position:relative;padding:0 0 1.6rem 3.2rem}
.road li::before{content:"";position:absolute;left:.4rem;top:.25rem;width:1.3rem;height:1.3rem;border-radius:50%;background:#f0a7c4;border:4px solid #1b1024}
.road time{display:block;font:800 .85rem system-ui;letter-spacing:.1em;text-transform:uppercase;color:#f0a7c4}
.road .big{font:800 1.5rem/1.25 system-ui;display:block;margin:.2rem 0}
.stat{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(12rem,1fr));margin:1.6rem 0}
.stat div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}
.stat b{display:block;font:900 2.4rem/1 system-ui;color:#f0a7c4}.stat span{color:var(--muted);font-size:.92rem}
h2{font:800 1.6rem system-ui;margin:2.4rem 0 1rem}
.cards{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr))}.cards li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}.cards h3{margin:0 0 .3rem}.cards h3 a{color:var(--fg)}.cards p{margin:0;color:color-mix(in srgb,currentColor 90%,transparent)}
.next{background:var(--card)}
"""
    fb = facts_blocks(F, p, depth)
    road = ''.join(f'<li><time datetime="{e(x["date"])}">{e(B.fmt_date(x["date"]))}</time><span class="big">{md(x["label"])}</span>{B.cite(F, x.get("s"), p)}</li>'
                   for x in sorted(F['timeline'], key=lambda x: x['date']))
    stats = ''.join(f'<div><b>{e(x["n"])}</b><span>{md(x["l"])}{B.cite(F, x.get("s"), p)}</span></div>' for x in c['stats'])
    btns = ''.join(f'<a class="btn{" primary" if i == 0 else ""}" href="{e(x["url"])}">{e(x["label"])} &#8599;</a>' for i, x in enumerate(F.get('next', [])))
    body = (f'<div class="wrap"><div class="stage"><div class="lanyard" aria-hidden="true"><div class="badge"><div class="hole"></div>'
            f'<small>{e(c["badge_event"])}</small><b>{e(F["name"])}</b><span>{e(c["badge_line"])}</span><div class="tier">{e(c["badge_tier"])}</div></div></div>'
            f'<div><h1>{c["h1"]}</h1>{oneline(F, p, c["h1"])}<p style="color:var(--muted);max-width:40rem">{md(c["sub"])}</p><div class="btns">{btns}</div>'
            f'<div class="stat">{stats}</div></div></div>'
            f'<h2 id="{p}story">From the conference floor to a live site</h2><ol class="road">{road}</ol>'
            f'<h2 id="{p}what">What came out of it</h2>{fb["what"]}<h2 id="{p}products">The offers</h2>{fb["products"]}'
            f'{next_step(F, depth)}{fb["sources"]}</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                sect_links(p, [('story', 'The road'), ('what', 'What came out'), ('products', 'Offers')]), body)


# ---------------------------------------------------------------- engine: the showroom (Sovereign Website)
def eng_showroom(F, depth, d):
    c = d['cfg']
    p = 'sr-'
    css = palette_css({'light': {'bg': '#fbf6ee', 'card': '#fffdf9', 'fg': '#2a1f17', 'muted': '#5e5148', 'line': '#eadccd', 'link': '#a5432a', 'acc': '#a5432a', 'acc-ink': '#fff'},
                       'dark': {'bg': '#1a1512', 'card': '#231c18', 'fg': '#f1e9e1', 'muted': '#c3b6aa', 'line': '#3a2f28', 'link': '#f0a084', 'acc': '#f0a084', 'acc-ink': '#1a1512'}}) + COMMON + """
body{font:1.05rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.shead{padding:2.6rem 0 1rem}
.shead h1{font:700 clamp(2.4rem,7vw,4.6rem)/1.02 Georgia,"Iowan Old Style","Times New Roman",serif;margin:0 0 .8rem}
.shead h1 em{color:var(--acc)}
.shead p{max-width:42rem;color:var(--muted);font-size:1.15rem}
.wall{display:grid;gap:2.4rem;margin:2rem 0}
.exhibit{display:grid;gap:1.4rem;align-items:center}
@media (min-width:58rem){.exhibit{grid-template-columns:1.5fr 1fr}.exhibit:nth-child(even) .shot{order:2}}
.exhibit h2{font:700 clamp(1.6rem,3.6vw,2.4rem)/1.1 Georgia,serif;margin:0 0 .4rem}
.exhibit .role{color:var(--acc);font-weight:700;margin:0 0 .6rem}
.exhibit .hand{border-left:4px solid var(--acc);padding:.4rem .9rem;background:var(--card);margin:.8rem 0}
.exhibit .shot figcaption{font-size:.82rem}
h2.s,.sources h2{font:700 clamp(1.5rem,3.4vw,2.1rem)/1.15 Georgia,"Iowan Old Style",serif;margin:2.6rem 0 1rem}
.cards{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr))}.cards li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}.cards h3{margin:0 0 .3rem;font-family:Georgia,serif}.cards h3 a{color:var(--fg)}.cards p{margin:0;color:color-mix(in srgb,currentColor 90%,transparent)}
.flow{list-style:none;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(20rem,100%),1fr));counter-reset:s}.flow li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}.flow li::before{content:counter(s);display:grid;place-items:center;width:2rem;height:2rem;border-radius:50%;background:var(--acc);color:var(--acc-ink);font-weight:800;margin-bottom:.5rem}.flow b{display:block}.flow span{color:var(--muted);font-size:.95rem}
.tl-list{padding-left:1.4rem}.tl-list time{font-weight:700;display:block}

.wthumbs{list-style:none;margin:1rem 0 1.2rem;padding:0;gap:1.4rem;grid-template-columns:1fr}.wt-role{margin:.2rem 0 0;color:var(--acc);font-weight:700}.wt-credit{margin:.1rem 0 0;color:var(--muted)}.wt-hand{margin:.3rem 0 0;border-left:4px solid var(--acc);padding:.2rem .7rem}@media (max-width:40rem){.wthumbs.phone-only{display:grid}}
.wthumbs a{display:block;color:var(--fg);font-weight:700;font-size:15px;text-decoration:none;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--card)}.wthumbs img{display:block;width:100%;height:220px;object-fit:cover;object-position:top;margin:0}
.wthumbs a > span{display:block;line-height:1.25;padding:.55rem .8rem;font-size:1.05rem}
.exhibit .shot-phonelink{display:none!important}
@media (max-width:40rem){.wall{display:none}.shead .btns{justify-content:center}.shead .next-note{text-align:center}}"""
    fb = facts_blocks(F, p, depth)
    ex = []
    for x in c['sites']:
        ex.append(f'<article class="exhibit">{B.shot(F, depth, x["shot"], lazy=x["shot"] != c["sites"][0]["shot"], phone_hide=True)}'
                  f'<div><h2><a href="{e(x["url"])}" style="color:var(--fg)">{e(x["name"])}</a></h2><p class="role">{e(x["role"])}{B.cite(F, x.get("s"), p)}</p>'
                  f'<p class="hand">{md(x["hand"])}{B.cite(F, x.get("hs"), p)}</p><p>{md(x["credit"])}</p></div></article>')
    shots = (F.get('identity') or {}).get('shots') or []
    thumbs = ''.join(f'<li><a href="{e(x["url"])}"><img src="{B.rel(depth, shots[x["shot"]].get("phone") or shots[x["shot"]]["file"])}" alt="{e(x["name"])}: the live site" loading="lazy" decoding="async"'
                     + (f' style="object-position:50% {x["thumb_y"]}%"' if x.get('thumb_y') is not None else '') + '>'
                     f'<span>{e(x["name"])} &#8599;</span></a>'
                     + (f'<p class="wt-role">{e(x["role"])}{B.cite(F, x.get("s"), p)}</p>' if not x.get('thumb_role_hidden') else B.cite(F, x.get("s"), p))
                     + f'<p class="wt-hand">{md(x["hand"])}{B.cite(F, x.get("hs"), p)}</p><p class="wt-credit">{md(x["credit"])}</p></li>'
                     for x in c['sites'] if x['shot'] < len(shots))
    thumbs = f'<ul class="wthumbs phone-only" aria-label="The owners\' sites">{thumbs}</ul>'  # round 11: on phones, all three owners at a glance
    btns = ''.join(f'<a class="btn{" primary" if i == 0 else ""}" href="{e(x["url"])}">{e(x["label"])} &#8599;</a>' for i, x in enumerate(F.get('next', [])))
    body = (f'<div class="wrap"><section class="shead"><h1>{c["h1"]}</h1>{oneline(F, p, c["h1"])}<p>{md(c["sub"])}</p>{thumbs}<div class="btns">{btns}</div>'
            + (f'<p class="next-note">{md(F["next_note"]["t"])}{B.cite(F, F["next_note"].get("s"), p)}</p>' if F.get('next_note') else '')
            + '</section>'
            f'<div class="wall" id="{p}sites">{"".join(ex)}</div></div>{band(F, depth, d, p)}<div class="wrap">'
            f'<h2 class="s" id="{p}how">How each one was made</h2>{fb["how"]}'
            f'<h2 class="s" id="{p}what">What Sovereign Website is</h2>{fb["what"]}'
            f'<h2 class="s" id="{p}products">The family</h2>{fb["products"]}'
            f'<h2 class="s">Key dates</h2>{B.timeline_list(F, p, "tl-list tl-rail")}{next_step(F, depth)}{fb["sources"]}</div>')
    return page(F, d['key'], depth, f'{F["name"]}: {d["name"]}', F['description'], css,
                sect_links(p, [('sites', 'The sites'), ('how', 'How'), ('what', 'What it is')]), body, credit=True)


ENGINES = {'terminal': eng_terminal, 'vault': eng_vault, 'identity': eng_identity, 'paper': eng_paper,
           'chat': eng_chat, 'gap': eng_gap, 'cell': eng_cell, 'badge': eng_badge, 'showroom': eng_showroom}
