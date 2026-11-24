# Site__Startups__The-Cyber-Boardroom
the-cyber-boardroom.startups.sovereignweb.site: A brochure for The Cyber Boardroom, with links to its own site.

How it is built: `content/facts.json` holds every fact with its public source; `python3 tools/build.py` writes the five designs into `site/`; `node tools/shots.js` and `python3 tools/thumbs.py` make the design thumbnails and share card and check phone and desktop, light and dark. For the owner: `docs/owner.md`, what you can do here yourself. See `docs/how-to-add-a-startup.md`, `docs/sources.md` and `docs/questions.md`.

## For people working here

- **Live site:** https://the-cyber-boardroom.startups.sovereignweb.site/ (its `/version.json` names the commit that is live).
- **Kept by:** startups.b, whose status, open work and restart note are at https://startups.agents.sovereignweb.site/factory/dinis-cruz/account-b/ (its own repository: https://github.com/SovereignWebsite/Site__Agent__Startups).
- **Owner:** the company the brochure is about; until ownership is handed over, Dinis Cruz. What the owner can do without waiting on anyone: `docs/owner.md`.

### Build and check

1. Change a fact in `content/facts.json`. Every fact names its source (an `s` number in the `sources` list); add a source for anything new. Public sources only.
2. `python3 tools/build.py` writes the five designs into `site/`. Commit `site/` with the change.
3. Before pushing: the Factory checks in `.github/ci/` (build, quality, html-validate, axe). Run them as in https://github.com/SovereignWebsite/Site__Agent__Startups/blob/dev/tools/checks/ci-local.sh, and keep every home page under 8,000 px tall at 390 px wide.
4. Push to `dev` only. The pipeline checks the signer, deploys and tags the version.

### What not to touch

- `main` (it moves only when Dinis merges), `.github/` (seeded by the Factory) and `site/policy/` (the shared agent behaviour policy).
- Never add a fact without a public source, a price or a customer the company has not published, or a person's name without their consent.
- `tools/build.py` and `tools/designs2.py` are copies: change the master in Site__Agent__Startups `tools/kit/`, then copy it to all five brochures.

### Who reviews

- Design: design.b.rounds runs persona rounds after a real content change.
- Decisions: anything that needs Dinis's yes goes to decisions.b as a signed request (https://decisions.agents.sovereignweb.site/ask/).
- Every commit is signed; the signer check refuses a commit from a key that is not published.

