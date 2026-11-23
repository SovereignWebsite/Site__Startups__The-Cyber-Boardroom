# How to add a startup

Every site under `*.startups.sovereignweb.site` is built the same way: one facts file, one build script, five designs. To add a company, follow these steps. Written by startups.b on 20 November 2026.

## 1. Ask for the repository

Ask sites.b (or Dinis Cruz) for a new site request. factory.b creates `SovereignWebsite/Site__Startups__<Name>` with its seed, CNAME and HTTPS at `https://<slug>.startups.sovereignweb.site/`. Read the repository's CLAUDE.md before anything else.

## 2. Research from public sources only

Start from the company's own website. If you are not given it, find it and prove it is the official one (links from the founder's own pages, press, the site's own docs); never guess a domain. Note for every fact the URL and the date you read it. Never invent a fact, figure, customer, price or quote. Keep the company's own labels ("proposal", "not on sale yet", "beta"). Date every figure with the date the source gives.

Images: use only images the company publishes for reuse (a stated licence), or draw your own. Screenshots of a company's site are not cleared. A person shown in a photo needs consent. Name only people the company presents publicly in a professional role.

## 3. Write `content/facts.json`

Copy the facts file of an existing startup site and replace every value. The keys:

| Key | What it holds |
|---|---|
| `slug`, `name`, `mark`, `kicker` | Address slug, display name, favicon letter, a short line under the name |
| `domain`, `url`, `url_label`, `repo` | This site's address, the company's own site, how to show it, this repository |
| `updated`, `home` | Date facts were last checked; the key of the design used as the home page |
| `designs` | The site's five designs: `{key, name, blurb, engine, cfg}`. Two from the company's own world, two on its real identity, and the Newsroom feature (printable on A4). Engines in `tools/designs2.py`: `terminal`, `vault`, `identity`, `paper` (variants `boardpaper`, `policyform`, `luggage`), `chat`, `gap`, `cell`, `badge`, `showroom`, plus `newsroom` |
| `oneline`, `next`, `band` | The company's own one-line description (shown under each headline), its own first step quoted from its site (the main buttons), and the full-bleed band of its facts on the home design |
| `identity` | Logo (`logo_img` or `logo_html`), and `shots`: screenshots of its live site taken with Playwright, each with its page URL, caption and a phone crop |
| `description`, `headline`, `lede`, `visit` | Meta description, home headline, opening paragraph, the closing line pointing to the company |
| `quote` | The company's own one-line description, exact, with its source |
| `what`, `story`, `for_whom` | Paragraphs and bullets, each `{"t": text, "s": [source ids]}`. Source numbers are not shown inside sentences: each section ends with one line, "Sources: 2, 7, 13", linking to the sources list |
| `how` | Steps of how it works: `{"title", "t", "s"}` |
| `products` | Parts of the offer: `{"name", "short", "url", "t", "s"}`; `short` labels the diagram |
| `timeline` | Dated events: `{"date": "YYYY-MM-DD" or "YYYY-MM", "label", "s"}` |
| `figures` | Numbers the company publishes: `{"value", "label", "asof", "s"}` |
| `chart` | Optional bar chart: `{"title", "note", "s", "bars": [{"label", "value"}]}` |
| `people` | People the company presents in a professional role |
| `newsroom` | `kicker`, `headline`, `standfirst` for the newsroom feature design |
| `brand` | `accent`, `accent_dark`, `soft`, `soft_dark`: colours taken from the company's own CSS, checked for contrast |
| `sources` | `{"id", "title", "url", "accessed"}`; every `s` above points here |

Text accepts `**bold**`, `*italic*` and `[label](https://...)`. Plain British English, no em dashes.

Brand assets and screenshots of the company's own site may be used for Dinis Cruz's companies (his permission, relayed by design.b and sites.b on 20 November 2026); for anyone else, ask first. Copy every asset into `site/img/` so nothing loads from another host, caption and link each screenshot, and leave out photos of people who have not agreed.

## 4. Build and check

```
python3 tools/build.py          # writes site/ and docs/sources.md
node tools/shots.js             # checks phone and desktop, light and dark; makes design thumbnails
python3 tools/thumbs.py         # turns thumbnails into .webp
```

`shots.js` also makes the 1200x630 share card (`site/img/share-card.jpg`) that link previews need. It reports any page wider than the screen and any request to another host; both must be empty. Then look at the screenshots yourself, on a phone width and in dark mode.

The build makes: `index.html` (the home design), `designs/<key>.html` for all five, the seeded `start/`, `agents/`, `admin/`, `designs/index.html` (all designs), `favicon.svg`, `llms.txt`, and `docs/sources.md`. Every page has the site's own navigation at the top, the five designs as links at the start of the footer and on `designs/` (design.b, 23 November 2026: these are Dinis Cruz's own companies, so the chooser stays out of the visitor's header), and one small, muted "Sovereign Website" pop-up at the top right listing the startups and the family (Dinis Cruz, 20 November 2026: the site is about its subject; the family stays in a pop-up menu). No scripts, no cookies, no tracking, no third-party requests.

Use the Factory's CI from `seed/site-template/.github/` (SovereignWebsite__Factory, dev). On every push to dev it builds, checks link previews, links, em dashes, the family strip, leaks, HTML validity and accessibility (axe), then deploys and tags. Confirm a green run and the tag after each push.

## 5. Add the new startup to the family menu

Add `(slug, name)` to `STARTUPS` in `tools/build.py`. Once the new site is live, add its slug to `LIVE` (only live sites are linked, so the link check stays green), copy the updated script to every startup repository and rebuild each one, so every site links to every other. The links sit in the Factory's top-right "Sovereign Website" pop-up (seed/shared/family-credit.html, vendored in tools/seed/).

## 6. Questions, push and showroom

- Put anything the sources do not answer in `docs/questions.md`, for Dinis Cruz.
- Commit signed with your own published key, with `Agent:` and `Claude-Session:` trailers. Check with `git verify-commit HEAD`. Push to `dev` only.
- When the site is live, add it to the hub: an entry in `SovereignWebsite__Hub` `site/sites.json` (schema `hub-site/1`, group `Startups`) and a screenshot in `site/shots/`, or ask hub.b.
- Ask design.b for a design round once the facts are right.
