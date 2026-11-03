# CLAUDE.md — castechai.com (CasTech AI)

Site for **CasTech AI**, the computer-vision division of Virexa AI Technologies for casino table games. Owner: Bilal Durmaz. He talks to you in Turkish or English. The site is English only.

## Working rules

- Follow the karpathy-guidelines skill: state assumptions, minimum code, surgical changes, verify before saying "done".
- Never change copy, logo, images or structure on your own initiative. Do only what was asked; mention other issues instead of fixing them.
- `main` is published as-is to castechai.com (GitHub Pages from the branch, no build). Anything pushed to `main` is live, and every file in the repo is public. For anything bigger than a text fix, work on a branch and open a PR.
- Commit messages: short, English, imperative.

## Stack

- Static `index.html`, plus `privacy.html` and `terms.html`. Inline CSS/JS, no framework, no build, no npm. Do not introduce one.
- `CNAME` (castechai.com), `.nojekyll`, `.well-known/`, `robots.txt`: do not touch. If you add a page, add it to `sitemap.xml`.
- Font: **Inter**, self-hosted in `assets/fonts/` (same as virexa-tech.com). No other fonts. If fonts or third-party services change, update the matching text in `privacy.html`.
- Contact is by email only: `info@castechai.com` (mailto links with subjects). There is no form. Do not add one unless asked; if asked, use FormSubmit → `sales@virexa-tech.com` like the other brand sites.

Preview locally: `python3 -m http.server` in the repo root.

## Claims: the most important rule

CasTech AI is **in development**. The current focus is AI-assisted **Blackjack** table monitoring.

- Never claim it is launched, deployed in a casino, certified or approved by a regulator, or has a measured accuracy. Do not invent clients, pilots, partners, numbers or testimonials.
- Keep the existing qualifiers: capabilities describe engineering scope; the table UI is a "conceptual illustration"; roadmap modules are "planned", not launched products.
- Keep the "human-led decisions" positioning: the system supports staff and flags events for review; it does not make final decisions.
- Roadmap order: Blackjack (initial focus), then 6 Card Poker, Russian Poker, Ultimate Poker, 5 Card Poker, Mini Baccarat, Mini Texas, Roulette. Change it only when asked.
- "Discuss a pilot" is an invitation, not a claim that pilots exist.

## Company details

- A Virexa AI Technologies s.r.o. division. IČO 29716055, Cihlářská 782/10a, Prosek, 190 00 Praha 9. Commercial Register, Municipal Court in Prague, section C, file 451241.
- Sister company: Deniz Trade LLC, Batumi, ID 445613480.
- Background to draw on: 22 years of international casino operations (slot, surveillance, IT and technical management, casino openings).
