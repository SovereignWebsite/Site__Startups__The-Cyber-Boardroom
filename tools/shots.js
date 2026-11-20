// Make the "Choose a design" thumbnails and check every page on phone and desktop, light and dark.
// Usage: node tools/shots.js [outdir-for-check-shots]   (run from the repository root)
// Writes site/img/designs/<design>.png (1280x800, scaled to 640x400 by tools/thumbs.py into .webp).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const facts = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'facts.json')));
const designs = ['brochure', 'blueprint', 'story', 'newsroom', 'brief'];
const check = process.argv[2];

(async () => {
  const browser = await chromium.launch();
  const problems = [];
  {
    const ctx = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(ROOT, 'tools', 'out', 'share-card.html'));
    await page.screenshot({ path: path.join(SITE, 'img', 'share-card.jpg'), type: 'jpeg', quality: 85 });
    await ctx.close();
  }
  for (const d of designs) {
    const file = d === facts.home ? 'index.html' : `designs/${d}.html`;
    const url = 'file://' + path.join(SITE, file);
    for (const [w, h, label] of [[1280, 800, 'desktop'], [390, 844, 'phone']]) {
      for (const scheme of ['light', 'dark']) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: scheme, deviceScaleFactor: 1 });
        const page = await ctx.newPage();
        const external = [];
        page.on('request', r => { if (!r.url().startsWith('file://') && !r.url().startsWith('data:')) external.push(r.url()); });
        await page.goto(url);
        const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (over > 1) problems.push(`${d} ${label} ${scheme}: horizontal overflow ${over}px`);
        if (external.length) problems.push(`${d} ${label} ${scheme}: external requests ${external.join(', ')}`);
        if (label === 'desktop' && scheme === 'light') {
          await page.screenshot({ path: path.join(SITE, 'img', 'designs', `${d}.png`) });
        }
        if (check) {
          fs.mkdirSync(check, { recursive: true });
          await page.screenshot({ path: path.join(check, `${d}-${label}-${scheme}.png`), fullPage: label === 'phone' ? false : false });
        }
        await ctx.close();
      }
    }
  }
  await browser.close();
  console.log(problems.length ? problems.join('\n') : 'all pages: no overflow, no external requests');
})();
