# What you can do on this site

For the owner. Nothing on this site waits on you: it is live at https://the-cyber-boardroom.startups.sovereignweb.site/, built only from public sources, and every page is checked on each push. Everything below is optional, and you can do it yourself, here or on GitHub.

## Change it yourself

1. **Edit a fact.** Open `content/facts.json` on GitHub and change the words. Every fact names its source (an `s` number from the `sources` list); add a source for anything new.
2. **Rebuild.** Run `python3 tools/build.py`. It writes all five designs into `site/`.
3. **Publish.** Commit to `dev`. The pipeline checks the pages, deploys them and tags the version; `/version.json` on the live site shows which commit is live.
4. **Pick the home page.** It opens on Identity: The Cyber Boardroom now. Set `home` in `content/facts.json` to any of: `boardpack` (The Board Pack), `ask-athena` (Ask Athena), `cyber-boardroom` (Identity: The Cyber Boardroom), `athena` (Identity: Athena), `newsroom` (The Newsroom).
5. **Add a photo or a screenshot.** Put it in `site/img/` and add it to `content/facts.json` with its credit and source.

## Things you could add

- **Show a real Athena answer.** If you publish one (a page or a post), its link becomes the strongest thing on this site: add it as a source and a quoted fact.
- **Any answer in `docs/questions.md`.** Each one, once answered with a source, becomes a fact on the site.
