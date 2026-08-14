# ORALAB Client Deck

Single-file sales deck for ORA / ORALAB, an AI creative platform for jewellery product images and video. The entire deck lives in `index.html` (inline CSS + markup + JS); media sits in `assets/`. GitHub repo: `collaborate-bhavishya/sales-deck`. Hosted on AWS Amplify at `deck.oralab.ai`, deploying from `main` (build spec `amplify.yml`, static, no build step — the console build command is `mkdir -p dist && cp -r index.html furniture assets dist/`; note `assets/` and the `furniture/` folder must both be copied). A push updates the live link. Netlify may also still be connected from the earlier setup and would redeploy too.

> Note: the original CLAUDE.md from the first build session was lost. This file was reconstructed on 2026-08-11 from the deck source and the handoff summary. Items marked ⚠ could not be recovered and need confirming against the original conversation.

## Repo layout

- `index.html` — the whole deck: styles, 12 slide sections, carousel JS at the bottom
- `assets/` — `bangle-*.jpg` (slide 3 sub-carousel) and client `.mp4` videos
- `furniture/index.html` — a furniture-vertical variant of the deck (same ORALAB brand/team/platform, furniture copy). Served by the same Amplify app at `deck.oralab.ai/furniture/` (it lives in a real `furniture/` folder so the trailing-slash URL resolves; its slide-3 asset `src`s are root-absolute `/assets/furn-...` so they load under the `/furniture/` path). Built in two steps: `scratchpad/build_furniture.py` scaffolds it from `index.html` (swaps all jewellery copy to furniture, marketplaces to Amazon/Wayfair/IKEA/Houzz/Etsy/Walmart/Overstock/West Elm, and turns every product slot into a placeholder), then `scratchpad/fill_slide3.py` rebuilds slide 3 into the real chair+sofa layout. Re-run BOTH in order to regenerate (running only build_furniture.py reverts slide 3 to placeholders). Slide 3 is a 2-page `.bap` carousel (sofa, chair) with a new "raw hero + output stack" layout: a rose-framed raw client photo (`.f3raw`) shown by default beside a fanned pile of ORA outputs (`.f3stack`) that opens the `#lightbox` on click (group = raw + 8 outputs, from `img.closest('.f3page')`); assets are `furn-{sofa,chair}-raw.jpg` + `furn-{sofa,chair}-01..08.jpg`. The client-work / video slide is REMOVED from the furniture deck (no furniture videos yet), so it has 11 slides not 12; build_furniture.py strips that `<section>` and its `.sub2`/`cvidSync` JS (the guarded `cvidSync()` call in `show()` becomes a no-op). Still-placeholder slots awaiting content: slide 5 `.jstrip` (`.jtile empty`), slide 8 client logos (`[ Client logo ]`).

## Slide map (12 `<section class="slide">` elements)

1. Cover — "The AI creative platform for studio-quality product images and video." Logo + headline centred; the bottom of the slide holds one badge row with the two positioning tags "Applied AI Research Lab" / "Visual Commerce". The old "Powered by" label and the partner badges (Amazon / NVIDIA / Google / Startup India Program) were removed. The `.pwr` CSS class is now unused.
2. Traditional production can be beautiful, but slow, expensive and tedious. (sub bridges into the 5 problem icon-cards; was "Great products deserve better visual velocity.")
3. With ORA AI, one raw photo becomes a full campaign in minutes. (headline; standard size, wraps to ~3 lines; standard padding, chevrons sit in the `.subwrap` flex row; no footnote) — 4-page `.bap` sub-carousel; each page is a 5-column `.bagrid` of square (`aspect-ratio:1/1`) tiles with bottom labels: one raw client tile (kept its rose highlight border) then 4 ORA output tiles, no divider. Defaults to the ring page (`subShow(3)`). All four pages are filled, one product category each: page 1 bangle (bangle-raw, bangle-angled, bangle-wrist, bangle-golden, bangle-luxury), page 2 earrings (earring-raw, -studio, -ear, -jasmine, -stone), page 3 necklace (necklace-raw, -neck, -resort, -marble, -silk), page 4 ring (ring-raw, -studio, -hand, -evening, -velvet). The full source sets (10+ shots per category, PNG) are in `~/Downloads/Images for portfolio-20260810T162521Z-1-001.zip`; deck assets are 1024px JPEGs converted from those with sips. `bangle-petals.jpg` is unused (dropped when the row went from 5 outputs to 4 for bigger tiles) but kept in `assets/` as a spare. Clicking any `.stile img` opens it in a fullscreen `#lightbox` (arrows/Prev/Next cycle within that page's 5 tiles, Esc or backdrop/image click closes). The lightbox keydown handler is registered in the capture phase and calls `stopPropagation()` so deck ArrowLeft/Right nav does not fire while it is open.
4. AI generation is easy. Reliable production is not. — `.cmp` comparison table: all cells left-aligned, header row highlighted with a light band (ORALAB header keeps its green `.ora` tint), no footnote.
5. We specialise in Jewellery. — a `.jstrip` row of 4 category images (spec-ring, spec-bangle, spec-necklace, spec-rings) spanning the full width above the 4 `.card` text boxes; `.jtile img` are wired into the `#lightbox` (cycle within the strip).
6. 5 steps from raw image to final campaign, powered by the ORA Agent.
7. One platform for all your creative needs. — three cards (Social Media, Website, Marketplaces), each with a `.lgrid` logo collage of `.lgt` tiles above the copy. Social Media and Website use inline monochrome simple-icons brand glyphs in 2x2 grids (Instagram/Meta/YouTube/Pinterest; Shopify/WooCommerce/Wix/Webflow) with tag pills beneath; Marketplaces uses a self-labeled wordmark wall (Amazon, Flipkart, Myntra, Nykaa, Etsy, Walmart, Noon, Farfetch) as a 4-col x 2-row grid (`.lgrid.m4`) and no duplicate tags. All `.lgt` tiles share one fixed height so the three grids are the same height; cards are `.ucard` flex columns with `.utags` pinned to the bottom (`margin-top:auto`), so grids, descriptions and tag rows line up across the three cards. The old `[Image]` placeholders and the `oralab-diamond.mp4` preview were removed (that mp4 is now unused but kept in `assets/`). Marketplace brand logos are text because they are not in the open-source simple-icons set; swap in real logo files if provided.
8. Global brands trust us for their most important visuals. — 5 client-logo cards (Damas, Jawhara, Alliel, Carat Story, VBJ) in a centered flex-wrap (3+2 rows) with enlarged logos; no footnote.
9. Work ORA shipped for real brands. — 2-page `.sub2` client-work carousel: damas-campaign, jawhara-campaign, alliel-social, vbj-bridal, keemti-1 through keemti-4. Videos do NOT autoplay-all: `cvidSync()` pauses every `.sub2 video` and autoplays only the first tile of the active page, and only while this slide (`slides[8]`) is the active deck slide. Clicking a tile toggles play/pause; any video starting pauses all others (one at a time). Paused tiles show a `.paused` play-button overlay. `cvidSync()` is called from `show()` (on every slide change) and from `sub2Show()` (on carousel page change).
10. Two ways to work with us. (was "Bring us the brief, or bring your team.") — two `.wway` vertical cards: ORA Studio (Managed Studio) and ORA Platform (Self-serve), each a big `.wlogo` mark + `.wtitle` over smaller `.wbody` copy with a bottom-anchored "Best for" line.
11. About ORA. (was "Operators and researchers, not tourists in AI.", now the subhead) — 4 founder cards, then a bottom row split into two rose-labelled groups: "Offices" (HQ · Gurgaon, Mumbai, Bangalore, London) and "Powered by" (Amazon, NVIDIA, Google, Startup India).
12. Next steps. (closing) — two cards, "Try ORA Platform" (Take a live demo and trial access for you and your team) and "Try ORA Studio" (Share a few product photos and get finished, quality-checked imagery back), then a rose `.cta` "Platform Walkthrough" button, and a `.s12foot` footer pinned to the slide bottom with the website (oralab.ai) and email (hello@oralab.ai). The CTA href is a placeholder (`https://oralab.ai`) - point it at the real walkthrough URL when there is one. Note: `.s12foot` needs the `.slide .s12foot` selector so its `position:absolute` beats the deck's `.slide>*:not(.blob){position:relative}` rule.

## Style guide (hard rules)

- No em dashes anywhere in copy.
- Headings stay white (`--ink: #FFFFFF`). Rose (`--rose: #E84E7E`) is the only accent colour for emphasis.
- Palette variables in `:root`: `--black #090909`, `--platinum #D8D8D2`, `--surface #161616`, `--border #242424`, plus `--grad-brand` (gold → pink → violet → blue) already defined; do not invent new colours.

## Content rules (agreed with the client; do not undo)

- Jewellery-only positioning. No non-jewellery examples anywhere.
- Never present stock or generic AI footage as client work. The client-work slide contains only real client deliverables.
- Say "100% checked", never "100% accurate".

## Class-name bug to avoid

The main deck JS collects slides with `document.querySelectorAll('.slide')`. Pages inside the nested carousels must NOT use `class="slide"`:

- Slide 3 sub-carousel pages use `.bap`, toggled with `.on`
- Slide 9 client-work pages use `.sub2`, toggled with `.on`

Giving an inner page `class="slide"` silently adds it to the main deck's slide list and breaks the count, dots, and arrow navigation.

Related trap: several places hardcode parent-slide indices: the ArrowUp/ArrowDown handlers (`slides[2]` for the `.bap` carousel, `slides[8]` for `.sub2`) and the slide 9 video autoplay guard in `cvidSync()` (`slides[8]`, the client-work slide). If slides are added, removed, or reordered, update every one of those indices.

## Video compression (ffmpeg)

⚠ Reconstructed default; the original session's exact settings were lost. Current assets are 1–9 MB each, so match that budget. Starting point:

```
ffmpeg -i input.mp4 -vf "scale=-2:720" -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -an -movflags +faststart output.mp4
```

ffmpeg is not installed on this Mac (`brew install ffmpeg` first).

## Outstanding tasks

- Add Keemti's logo (carried over from the handoff)
- ⚠ Other outstanding items from the original session were lost; restore them from the original conversation if needed

## Workflow

- Always auto commit and push to `main` after each meaningful change, without asking for confirmation; AWS Amplify (and Netlify, if still connected) redeploys the live link automatically.
- Remote is HTTPS with the macOS keychain credential helper; git user is `collaborate-bhavishya`.
