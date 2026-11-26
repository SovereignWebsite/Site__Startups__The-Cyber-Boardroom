#!/usr/bin/env python3
"""Build The Cyber Boardroom's main pages from content/cbr.json into site/.

Usage, from the repository root:
    python3 tools/build.py      # the five designs under /designs/ (from content/facts.json)
    python3 tools/cbr_site.py   # then the main pages: /, /board-packs/, /about/, /history/, /athena/

Static HTML, one shared stylesheet (/assets/cbr.css), no scripts, no cookies, no tracking.
Every fact on a page cites a source from content/cbr.json; each page lists its sources at the foot.
Kept by cl-6.conductor-cbr@CBR.dinis (the editor, at Dinis Cruz's word, 26 Nov 2026).
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
C = json.load(open(os.path.join(ROOT, 'content', 'cbr.json')))
SRC = {s['id']: s for s in C['sources']}
HOST = C['host']
e = lambda s: html.escape(str(s), quote=True)

NAV = [('/', 'Home'), ('/board-packs/', 'Board packs'), ('/about/', 'About'), ('/history/', 'History'),
       ('/athena/', 'Athena'), ('/designs/', 'Designs')]

FAMILY = [('sgit.ai', 'https://sgit.ai/'), ('RiskMandate', 'https://riskmandate.ai/'), ('SG/Send', 'https://sgraph.ai/'),
          ('sgit brochure', 'https://sgit.startups.sovereignweb.site/'),
          ('RiskMandate brochure', 'https://risk-mandate.startups.sovereignweb.site/'),
          ('Sovereign Website', 'https://sovereignwebsite.ai/'), ('Agents', 'https://agents.sovereignweb.site/')]


class Page:
    def __init__(self):
        self.cited = []

    def c(self, *ids):
        """A citation: superscript numbers linking to this page's source list."""
        out = []
        for i in ids:
            if i not in SRC:
                raise SystemExit(f'unknown source {i}')
            if i not in self.cited:
                self.cited.append(i)
            n = self.cited.index(i) + 1
            out.append(f'<a href="#s-{e(i)}" aria-label="source {n}">{n}</a>')
        return '<sup class="cite">' + ','.join(out) + '</sup>'

    def sources(self):
        if not self.cited:
            return ''
        li = ''.join(f'<li id="s-{e(i)}"><a href="{e(SRC[i]["url"])}">{e(SRC[i]["title"])}</a> '
                     f'<span class="muted">read {e(SRC[i]["accessed"])}</span></li>' for i in self.cited)
        return f'<section class="sources" aria-labelledby="src-h"><h2 id="src-h">Sources</h2><ol>{li}</ol></section>'


def head(path, title, desc):
    url = f'https://{HOST}{path}'
    img = f'https://{HOST}/img/share-card.jpg'
    alt = 'The Cyber Boardroom: board packs for cyber risk, built on encrypted vaults and agent behaviour policies.'
    full = title if title == 'The Cyber Boardroom' else f'{title} | The Cyber Boardroom'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Cyber Boardroom">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{e(url)}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(img)}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(full)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{e(img)}">
<meta name="twitter:image:alt" content="{e(alt)}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/cbr.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar">
<a class="brand" href="/"><span class="mark" aria-hidden="true">CB</span><span>The Cyber Boardroom</span></a>
<nav aria-label="Main"><ul>{''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{e(l)}</a></li>' for h, l in NAV)}</ul></nav>
</div></header>
'''


def foot(p):
    fam = ''.join(f'<li><a href="{e(u)}">{e(n)}</a></li>' for n, u in FAMILY)
    return f'''<div class="wrap">{p.sources()}</div>
</main>
<footer class="foot"><div class="wrap">
<p><strong>The Cyber Boardroom Limited</strong>, registered in the UK, company 15623827.</p>
<nav aria-label="Family"><ul class="fam">{fam}</ul></nav>
<p class="muted">Static pages, no cookies, no tracking. Every fact names a public source. Edited by the agent cl-6.conductor-cbr@CBR.dinis for Dinis Cruz; source on <a href="https://github.com/SovereignWebsite/Site__Startups__The-Cyber-Boardroom">GitHub</a>; the agents' rules: <a href="/policy/">behaviour policy</a>. Updated {e(C["updated"])}.</p>
</div></footer>
</body>
</html>
'''


def write(path, body):
    out = os.path.join(SITE, path.strip('/'), 'index.html') if path != '/' else os.path.join(SITE, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(body)


# ------------------------------------------------------------------------------------------------ pages
def home():
    p = Page()
    b = head('/', 'The Cyber Boardroom', 'Board packs for cyber risk: what your organisation accepts, what its AI agents may do, '
             'and the evidence, kept in encrypted vaults. From The Cyber Boardroom Limited, the company behind sgit.ai and RiskMandate.ai.')
    b += f'''<main id="main">
<section class="hero"><div class="wrap">
<p class="kicker">Cyber risk, in the board's language</p>
<h1>Board packs your directors can read, and evidence they can check</h1>
<p class="lede">The Cyber Boardroom started in 2024 to help boards understand cyber risk{p.c('old-home', 'scmedia')}. In November 2026 it restarts around one product: the board pack{p.c('restart')}. A pack puts the risks the organisation accepts, what each AI agent is allowed to do, and the evidence behind both in front of the board, kept in an encrypted vault.</p>
<p class="ctas"><a class="btn" href="/board-packs/">See what goes in a board pack</a> <a class="btn ghost" href="/about/">Who we are</a></p>
</div></section>

<div class="wrap">
<section aria-labelledby="why-h">
<h2 id="why-h">Why now</h2>
<p>In February 2026 the founder wrote that The Cyber Boardroom was "on life support, not because the idea was wrong, but because it was ahead of the infrastructure needed to deliver it"{p.c('brief-cbr')}. The missing pieces now exist in the companies around it:</p>
<ul class="cards three">
<li><h3>Encrypted vaults</h3><p>SG/Send gives "data rooms with zero-knowledge encryption" for "sensitive board materials"{p.c('brief-cbr')}, and each board member can get "a personalised view encrypted to their key"{p.c('brief-keys')}.</p></li>
<li><h3>Agent Behaviour Policies</h3><p>RiskMandate writes down, for each AI agent, what it can actually do and what you authorised, and puts something in the way of the difference{p.c('rm')}.</p></li>
<li><h3>Risk acceptance</h3><p>A risk register view where "simulated acceptance" stays "indelibly distinct from real", naming "roles not named individuals"{p.c('risk-register')}.</p></li>
</ul>
</section>

<section aria-labelledby="dots-h">
<h2 id="dots-h">One company underneath</h2>
<p>The Cyber Boardroom Limited, UK-registered, "is today the commercial vehicle behind sgit.ai and RiskMandate.ai"{p.c('sgit-about')}. Its GitHub organisation also holds the code of SG/Send{p.c('org', 'send-repo')}. <a href="/about/">How the pieces connect</a>.</p>
</section>

<section aria-labelledby="status-h" class="note">
<h2 id="status-h">Where it stands</h2>
<p>The board pack is being built now. There are no prices or customers to show yet, and this site will not invent any. The 2024 platform, with Athena, the AI cyber advisor, is still online at <a href="https://thecyberboardroom.com/web/home">thecyberboardroom.com</a>{p.c('old-home')}; read <a href="/history/">the history</a> and <a href="/athena/">what Athena was</a>.</p>
</section>
</div>
'''
    write('/', b + foot(p))


def board_packs():
    p = Page()
    b = head('/board-packs/', 'Board packs', 'What a Cyber Boardroom board pack brings together: encrypted vaults, risk acceptance, '
             'agent behaviour policies and plain-language translation, each from public work.')
    b += f'''<main id="main">
<section class="hero slim"><div class="wrap">
<p class="kicker">The product</p>
<h1>Board packs</h1>
<p class="lede">A board pack is what a board reads before it decides. The Cyber Boardroom's is about cyber and AI risk: what the organisation accepts, what its agents may do, and the evidence, delivered so that each director can open it and nobody else can{p.c('restart', 'brief-keys')}.</p>
</div></section>
<div class="wrap">
<section aria-labelledby="parts-h">
<h2 id="parts-h">Four parts, each already built somewhere</h2>
<ol class="steps">
<li><h3>The vault: the pack's container</h3>
<p>Each pack lives in an SG/Send vault: zero-knowledge encrypted file sharing{p.c('send-repo')}. The design already lists "board pack distribution", where "each board member gets a personalised view encrypted to their key"{p.c('brief-keys')}, and its vault previews were drawn with an "Acme Q3 Board Pack" as the example{p.c('vault-mock')}.</p></li>
<li><h3>The risk register: what the board accepts</h3>
<p>A "Risk Register Executive View" brief sets two hard rules: "simulated acceptance indelibly distinct from real (cryptographic or structural separator, not a boolean flag)", and "roles not named individuals"{p.c('risk-register')}. A director should never mistake a rehearsal for a decision.</p></li>
<li><h3>Agent Behaviour Policies: what the AI agents may do</h3>
<p>RiskMandate writes an Agent Behaviour Policy for each agent: what it can actually do, what you authorised it to do, and what stands in the way of the difference{p.c('rm')}. The pack gives the board the gaps, in the board's words.</p></li>
<li><h3>The translation: the board's language</h3>
<p>The Cyber Boardroom's own work since 2024: Athena, an AI cyber security advisor, CFO and CISO personas, and articles such as "Cyber security in the boardroom"{p.c('old-athena', 'old-personas', 'old-content')}. Its 2026 thesis: board members "need translation, not education"{p.c('brief-cbr')}.</p></li>
</ol>
</section>

<section aria-labelledby="outline-h">
<h2 id="outline-h">A first outline</h2>
<p class="muted">A proposal for the first pack, to be shaped with the first boards. Not a customer's pack.</p>
<div class="paper" role="group" aria-label="Outline of a board pack">
<p class="paper-h">Board pack: cyber and AI risk</p>
<ol>
<li><strong>Cover note.</strong> What the board is asked to decide, in one page.</li>
<li><strong>Paper A: the risk register.</strong> The risks held, by role, with each acceptance marked real or simulated.</li>
<li><strong>Paper B: risks for decision.</strong> The ones to accept, reduce or refuse this time.</li>
<li><strong>Paper C: AI agents.</strong> Each agent's behaviour policy: what it can do against what was authorised, and the gaps.</li>
<li><strong>Evidence.</strong> The vault: every claim links to its record, readable by the directors who hold the key.</li>
</ol>
</div>
</section>

<section aria-labelledby="who-h">
<h2 id="who-h">For whom</h2>
<p>The 2024 platform was made for board members and for the CISOs who brief them{p.c('old-home', 'brief-cbr')}. The pack serves both sides of that conversation. If you sit on a board or brief one, <a href="/about/#contact">talk to us</a>.</p>
</section>
</div>
'''
    write('/board-packs/', b + foot(p))


def about():
    p = Page()
    b = head('/about/', 'About', 'The Cyber Boardroom Limited: the UK company behind sgit.ai and RiskMandate.ai, '
             'whose GitHub organisation holds SG/Send. How the pieces connect.')
    rel = [
        ('sgit.ai', 'https://sgit.ai/', 'Commercial vehicle', 'Encrypted, versioned vaults that work like git.', ('sgit-about',)),
        ('RiskMandate.ai', 'https://riskmandate.ai/', 'Commercial vehicle', 'Agent Behaviour Policies: what each AI agent can do against what you allowed.', ('sgit-about', 'rm')),
        ('SG/Send (sgraph.ai)', 'https://sgraph.ai/', 'Code in its GitHub organisation', 'Zero-knowledge encrypted file sharing and vaults; sgraph.ai is its commercial home.', ('send-repo', 'sgit-about')),
        ('The Cyber Boardroom platform', 'https://thecyberboardroom.com/web/home', 'Its own product, 2024', 'Athena, the AI cyber advisor, with content and personas for boards.', ('old-home', 'old-athena')),
    ]
    cards = ''.join(f'<li><p class="chip">{e(r)}</p><h3><a href="{e(u)}">{e(n)}</a></h3><p>{e(t)}{p.c(*s)}</p></li>' for n, u, r, t, s in rel)
    b += f'''<main id="main">
<section class="hero slim"><div class="wrap">
<p class="kicker">About</p>
<h1>The company underneath</h1>
<p class="lede">The Cyber Boardroom Limited is a private limited company registered in the UK at Companies House, company number 15623827, incorporated on 7 April 2024 and active{p.c('ch')}. It is "today the commercial vehicle behind sgit.ai and RiskMandate.ai"{p.c('sgit-about')}.</p>
</div></section>
<div class="wrap">
<section aria-labelledby="dots-h">
<h2 id="dots-h">Connecting the dots</h2>
<div class="hub"><p class="hub-name">The Cyber Boardroom Limited</p><p class="muted">UK company 15623827, founded by Dinis Cruz{p.c('ch', 'sgit-about')}</p></div>
<ul class="cards two rel">{cards}</ul>
<p>The board pack is where these meet: SG/Send's vaults hold it, RiskMandate's policies and a risk register fill it, and The Cyber Boardroom puts it in the board's language. <a href="/board-packs/">See the board pack</a>.</p>
</section>

<section aria-labelledby="open-h">
<h2 id="open-h">Open by default</h2>
<p>Most of the work is public. The <a href="https://github.com/the-cyber-boardroom">the-cyber-boardroom</a> organisation on GitHub holds The Cyber Boardroom's own code (the community edition, the content, the user services) and the SG/Send, SGraph and MGraph code{p.c('org', 'community', 'content-repo', 'send-repo')}. The investor material, a business plan and pitch decks from early 2025, is in the open too, in <a href="https://github.com/the-cyber-boardroom/cbr-investment">cbr-investment</a>{p.c('invest')}.</p>
</section>

<section aria-labelledby="founder-h">
<h2 id="founder-h">The founder</h2>
<p>Dinis Cruz founded The Cyber Boardroom, sgit.ai, sgraph.ai, MyFeeds.ai, RiskMandate.ai and VoiceDebrief.ai{p.c('sgit-about')}. SC Media UK described him as "an experienced CISO for multiple businesses"{p.c('scmedia')}.</p>
</section>

<section aria-labelledby="contact" class="note">
<h2 id="contact">Talk to us</h2>
<p>For board packs, write through the founder's page at <a href="https://sgit.ai/about/index.html">sgit.ai/about</a>, which says how to reach or correct him{p.c('sgit-about')}.</p>
</section>
</div>
'''
    write('/about/', b + foot(p))


def history():
    p = Page()
    items = [
        ('Oct 2023', 'Open Security Summit session: creating the GenAI Athena bot from The Cyber Boardroom.', ('oss',)),
        ('7 Apr 2024', 'The Cyber Boardroom Limited is incorporated in the UK.', ('ch',)),
        ('22 Apr 2024', 'SC Media UK interviews Dinis Cruz on The Cyber Boardroom.', ('scmedia',)),
        ('Jul 2024', '"Why, How, and What (v0.4, First MVP)" is published, and the Community Edition is introduced.', ('old-blog',)),
        ('13 Dec 2024', 'Last release of the platform package on PyPI, cbr-website-beta 0.221.1.', ('pypi-web',)),
        ('29 Jan 2025', 'Last release of the content package, cbr-content 0.9.78.', ('pypi-content',)),
        ('Jan to Feb 2025', 'The investor business plan and pitch decks are written in the open, in cbr-investment.', ('invest',)),
        ('27 Feb 2026', 'A brief proposes reactivating The Cyber Boardroom on SG/Send\'s agentic infrastructure.', ('brief-cbr',)),
        ('Aug 2026', 'The Risk Register Executive View brief sets its two rules for risk acceptance.', ('risk-register',)),
        ('26 Nov 2026', 'Dinis Cruz restarts The Cyber Boardroom around board packs, with this site as its new home.', ('restart', 'map')),
    ]
    li = ''.join(f'<li><p class="date">{e(d)}</p><p>{e(t)}{p.c(*s)}</p></li>' for d, t, s in items)
    b = head('/history/', 'History', 'The Cyber Boardroom from its first Athena bot in 2023, through the 2024 platform, '
             'to its restart around board packs in November 2026.')
    b += f'''<main id="main">
<section class="hero slim"><div class="wrap">
<p class="kicker">History</p>
<h1>From Athena to the board pack</h1>
<p class="lede">Three years in ten dates. The full record of the repositories is in the <a href="{e(SRC['map']['url'])}">map of CBR's repositories</a>{p.c('map')}.</p>
</div></section>
<div class="wrap"><section aria-label="Timeline"><ol class="timeline">{li}</ol></section></div>
'''
    write('/history/', b + foot(p))


def athena():
    p = Page()
    prods = [
        ('Athena', 'https://thecyberboardroom.com/web/athena', '"Your AI cyber security advisor", named after the Greek goddess of wisdom, courage and strategic warfare.', ('old-athena',)),
        ('Curated content', 'https://thecyberboardroom.com/web/content', 'Articles including Cyber security in the boardroom, Incident management and The importance of digital trust.', ('old-content',)),
        ('Board personas', 'https://thecyberboardroom.com/web/docs/demos/personas/ciso/index', 'CFO and CISO personas to practise the conversation from each side.', ('old-personas',)),
        ('Chat with LLMs', 'https://thecyberboardroom.com/web/chat-with-llms', 'Several large language models side by side.', ('old-llms',)),
        ('Six languages', 'https://thecyberboardroom.com/web/docs/platforms/groq/speak-in-6-languages', 'Athena answering in six languages.', ('old-6lang',)),
        ('Community Edition', 'https://thecyberboardroom.com/web/docs/support/install-cbr-community', 'Install it yourself with pip or Docker.', ('old-install', 'community')),
    ]
    cards = ''.join(f'<li><h3><a href="{e(u)}">{e(n)}</a></h3><p>{e(t)}{p.c(*s)}</p></li>' for n, u, t, s in prods)
    b = head('/athena/', 'Athena', 'Athena, The Cyber Boardroom\'s AI cyber security advisor for boards, and the 2024 platform around it.')
    b += f'''<main id="main">
<section class="hero slim"><div class="wrap">
<p class="kicker">The 2024 platform</p>
<h1>Athena, the AI cyber advisor</h1>
<p class="lede">Before the board pack, The Cyber Boardroom was a platform for board members to ask about cyber security in their own terms, built around Athena{p.c('old-home', 'old-athena')}. SC Media UK called it "serverless and driven by GenAI bots and agents"{p.c('scmedia')}. It is still online.</p>
</div></section>
<div class="wrap">
<section aria-labelledby="parts-h"><h2 id="parts-h">What it offered</h2><ul class="cards three">{cards}</ul></section>
<section class="note" aria-labelledby="next-h"><h2 id="next-h">What carries over</h2>
<p>Athena's job, translating cyber risk for the board, becomes the translation layer of the <a href="/board-packs/">board pack</a>{p.c('brief-cbr')}.</p></section>
</div>
'''
    write('/athena/', b + foot(p))


CSS = r''':root{--bg:#eef5f5;--card:#fff;--fg:#0e2c2d;--muted:#3f5a5b;--line:#d3e2e2;--link:#1f5357;--acc:#2b5c60;--acc-ink:#fff;
--hero:linear-gradient(135deg,#0e2c2d,#2b5c60);--hero-ink:#fff;--hero-acc:#8fcfd4;--paper:#fffdf6}
@media (prefers-color-scheme:dark){:root{--bg:#0b1a1b;--card:#122728;--fg:#e6f0f0;--muted:#a9bfbf;--line:#24403f;--link:#8fcfd4;
--acc:#8fcfd4;--acc-ink:#0b1a1b;--hero:linear-gradient(135deg,#071516,#1d4346);--paper:#16302f}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;overflow-wrap:break-word}
a{color:var(--link)}
:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.skip{position:absolute;left:-999px;top:0}.skip:focus{left:1rem;top:1rem;background:var(--card);color:var(--fg);padding:.5rem .8rem;z-index:9}
.wrap{max-width:66rem;margin:0 auto;padding:0 16px}
.top{background:var(--card);border-bottom:1px solid var(--line)}
.bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.4rem 1rem;padding-top:.6rem;padding-bottom:.6rem}
.brand{display:flex;align-items:center;gap:.55rem;font-weight:800;color:var(--fg);text-decoration:none;min-height:44px}
.mark{display:inline-grid;place-items:center;width:2.2rem;height:2.2rem;border-radius:.5rem;background:var(--acc);color:var(--acc-ink);font-size:.85rem;letter-spacing:.02em}
.top nav ul{display:flex;flex-wrap:wrap;gap:.1rem .2rem;list-style:none;margin:0;padding:0}
.top nav a{display:inline-block;padding:.55rem .55rem;min-height:44px;text-decoration:none;color:var(--fg);border-radius:.4rem;font-size:.95rem}
.top nav a:hover{background:var(--bg)}
.top nav a[aria-current=page]{font-weight:800;text-decoration:underline;text-underline-offset:.3em}
.hero{background:var(--hero);color:var(--hero-ink);padding:3.2rem 0 3rem}
.hero.slim{padding:2.4rem 0 2.2rem}
.hero a{color:var(--hero-ink)}
.kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;font-weight:700;color:var(--hero-acc);margin:0 0 .6rem}
h1{font-size:clamp(1.9rem,5vw,3rem);line-height:1.12;margin:0 0 1rem;max-width:22ch}
h2{font-size:1.45rem;line-height:1.25;margin:2.4rem 0 .8rem}
h3{font-size:1.08rem;margin:0 0 .4rem}
.lede{font-size:1.15rem;max-width:44rem;margin:0}
.ctas{margin:1.6rem 0 0;display:flex;flex-wrap:wrap;gap:.7rem}
.btn{display:inline-block;padding:.75rem 1.1rem;border-radius:.5rem;background:var(--hero-acc);color:#0e2c2d!important;font-weight:700;text-decoration:none}
.btn.ghost{background:transparent;border:2px solid var(--hero-acc);color:var(--hero-ink)!important}
.cards{list-style:none;margin:1rem 0;padding:0;display:grid;gap:1rem}
.cards li{background:var(--card);border:1px solid var(--line);border-radius:.75rem;padding:1.1rem 1.2rem}
.cards p{margin:0}
@media (min-width:46rem){.cards.three{grid-template-columns:repeat(3,1fr)}.cards.two{grid-template-columns:repeat(2,1fr)}}
.chip{display:inline-block;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 .3rem!important}
.hub{background:var(--acc);color:var(--acc-ink);border-radius:.75rem;padding:1rem 1.2rem;text-align:center}
.hub p{margin:0}.hub .muted{color:inherit;opacity:.9}.hub a{color:inherit}
.hub-name{font-weight:800;font-size:1.2rem}
.rel{position:relative}
.note{background:var(--card);border-left:4px solid var(--acc);border-radius:.5rem;padding:.2rem 1.2rem 1rem;margin-top:2.4rem}
.note h2{margin-top:1rem}
.steps{padding-left:1.4rem}.steps li{margin:0 0 1.2rem}.steps p{margin:0}
.paper{background:var(--paper);border:1px solid var(--line);border-radius:.4rem;padding:1.2rem 1.4rem;box-shadow:0 2px 0 var(--line);max-width:44rem}
.paper-h{font-weight:800;border-bottom:2px solid var(--fg);padding-bottom:.4rem;margin:0 0 .6rem}
.paper ol{margin:0;padding-left:1.3rem}.paper li{margin:.35rem 0}
.timeline{list-style:none;margin:1.6rem 0;padding:0 0 0 1.4rem;border-left:3px solid var(--acc)}
.timeline li{position:relative;margin:0 0 1.3rem;padding-left:.4rem}
.timeline li::before{content:"";position:absolute;left:-2.05rem;top:.45rem;width:.9rem;height:.9rem;border-radius:50%;background:var(--card);border:3px solid var(--acc)}
.timeline p{margin:0}.date{font-weight:800}
.muted{color:var(--muted)}
.cite{font-size:.7em;line-height:0;margin-left:.1em}
.cite a{padding:0 .1em}
.hero .cite a{color:var(--hero-acc)}
.sources{margin-top:3rem;font-size:.9rem;border-top:1px solid var(--line);padding-top:.4rem}
.sources h2{font-size:1.05rem}
.sources li{margin:.25rem 0}
.foot{margin-top:3rem;background:var(--card);border-top:1px solid var(--line);padding:1.4rem 0 .6rem;font-size:.92rem}
.fam{list-style:none;padding:0;margin:.6rem 0;display:flex;flex-wrap:wrap;gap:.2rem 1rem}
.fam a{display:inline-block;min-height:24px;padding:.2rem 0}
'''


def main():
    os.makedirs(os.path.join(SITE, 'assets'), exist_ok=True)
    open(os.path.join(SITE, 'assets', 'cbr.css'), 'w').write(CSS)
    home(); board_packs(); about(); history(); athena()
    print('built the main pages into', SITE)


if __name__ == '__main__':
    main()
