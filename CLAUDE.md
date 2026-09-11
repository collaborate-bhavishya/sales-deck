# ORALAB Client Deck

Single-file sales deck for ORA / ORALAB, an AI creative platform for jewellery product images and video. The entire deck lives in `index.html` (inline CSS + markup + JS); media sits in `assets/`. GitHub repo: `collaborate-bhavishya/sales-deck`. Hosted on AWS Amplify at `deck.oralab.ai`, deploying from `main` (build spec `amplify.yml`, static, no build step — the console build command is `mkdir -p dist && cp -r index.html furniture fashion assets dist/`; note `assets/`, `furniture/` and `fashion/` must all be copied). A push updates the live link. Netlify may also still be connected from the earlier setup and would redeploy too.

> Note: the original CLAUDE.md from the first build session was lost. This file was reconstructed on 2026-08-11 from the deck source and the handoff summary. Items marked ⚠ could not be recovered and need confirming against the original conversation.

## Repo layout

- `index.html` — the whole deck: styles, 12 slide sections, carousel JS at the bottom
- `assets/` — `bangle-*.jpg` (slide 3 sub-carousel) and client `.mp4` videos
- `furniture/index.html` — a furniture-vertical variant of the deck (same ORALAB brand/team/platform, furniture copy). Served by the same Amplify app at `deck.oralab.ai/furniture/` (it lives in a real `furniture/` folder so the trailing-slash URL resolves; its slide-3 asset `src`s are root-absolute `/assets/furn-...` so they load under the `/furniture/` path). Built in two steps: `scratchpad/build_furniture.py` scaffolds it from `index.html` (swaps all jewellery copy to furniture, marketplaces to Amazon/Wayfair/IKEA/Houzz/Etsy/Walmart/Overstock/West Elm, and turns every product slot into a placeholder), then `scratchpad/fill_slide3.py` rebuilds slide 3 into the real chair+sofa layout. Re-run BOTH in order to regenerate (running only build_furniture.py reverts slide 3 to placeholders). Slide 3 is a 2-page `.bap` carousel (sofa, chair) with a new "raw hero + output stack" layout: a rose-framed raw client photo (`.f3raw`) shown by default beside a fanned pile of ORA outputs (`.f3stack`) that opens the `#lightbox` on click (group = raw + 8 outputs, from `img.closest('.f3page')`); assets are `furn-{sofa,chair}-raw.jpg` + `furn-{sofa,chair}-01..08.jpg`. The client-work / video slide IS present in the furniture deck (11 slides, same order as the jewellery deck; client-work at `slides[7]`). build_furniture.py replaces the jewellery video prows with 7 furniture brand videos `furn-work-1,2,4,5,6,7,8.mp4` (absolute `/assets/` srcs, so they load under `/furniture/`), 4+3 across the 2 `.sub2` pages, type labels (Product film/Campaign/Ad film/Concept · Interior/Lifestyle/Studio), no brand `.ctag`. (furn-work-3 was removed per request.) The `.sub2`/`cvidSync`/`#vlb` JS is kept intact (paused thumbnails + click-to-fullscreen, see slide 9). `furn-work-2.mp4` is landscape (crops in the portrait tile) and ~12MB (ffmpeg not installed to compress). Slide 8 shows 5 client brands as text wordmarks (Hive, SmaartCraaft, Ammri, Living Concept, Chattels & More) — build_furniture.py rebuilds the whole slide-8 card grid; swap the wordmarks for real logo files when available.
- `fashion/index.html` — a fashion-vertical variant, same pattern as furniture, served at `deck.oralab.ai/fashion/`. Built by `scratchpad/build_fashion.py` (single step) from `index.html`: fashion copy, marketplaces to Amazon/Ajio/Myntra/Nykaa/ASOS/Zalando/Shein/Farfetch, slide-3 categories dress/handbag/footwear/outerwear, client-work video slide removed → 10 slides. Slide 8 shows 3 client brands as text wordmarks (Kameez, Shaurya Sanadhya, Cotton Culture) — build_fashion.py rebuilds the slide-8 grid; swap for real logos when available. Slide 3 is still a placeholder scaffold (no real fashion product images yet); it is fully self-contained (base64 cover logo only, works under `/fashion/` with no absolute-path needs). Re-run `build_fashion.py` to regenerate.

## Slide map (12 `<section class="slide">` elements)

1. Cover — "The AI creative platform for studio-quality product images and video." Redesigned as a moving media wall: `.cvwall` = 5 vertical `.cvcol` columns of `.cvtile` product/video tiles scrolling up/down (`cvup`/`cvdown` keyframes, alternating per column), a radial `.cvscrim`, and a frosted tinted `.cvpanel` (logo + headline) centred on top, with the two positioning-tag badges (`.cvtags`) pinned at the bottom. Rose `.cvpb` ▶ badges mark video tiles. Built by `scratchpad/cover_lib.py` (`wall_cover()` + `cover_css()`); the jewellery deck uses `JEWEL_COLS` with relative `assets/` srcs, furniture uses `FURN_COLS` with absolute `/assets/`, fashion uses `simple_cover()` (no wall) until it has product images. The cover CSS uses `.slide.cover .cvwall/.cvscrim/.cvpanel{position:...!important}` to beat the deck's `.slide>*:not(.blob){position:relative;z-index:1}` rule.
2. Traditional production can be beautiful, but slow, expensive and tedious. (sub bridges into the 5 problem icon-cards; was "Great products deserve better visual velocity.") There is no `.sub` and no photo caption on this slide (both removed for a cleaner look). The left `.card` is just a `.mini` "The traditional way" label over a real "traditional shoot" photo that fills the card (replacing the old inline SVG illustration); the right column is a 2x2 grid of 4 problem `.icard`s. The photo box is `flex:1;min-height:clamp(130px,18vh,180px);position:relative` and the `<img>` inside is `position:absolute;inset:0;width:100%;height:100%;object-fit:cover` — the absolute positioning is REQUIRED: with a normal in-flow `height:100%` img, the image's intrinsic height feeds the grid-cell sizing and balloons the whole row past `.grow` (headline overlap). Absolute-positioning takes the img out of flow so the box (and thus the left card) matches the right icon grid's height exactly and crops via cover. Photo is `assets/shoot-jewellery.jpg` (jewellery), swapped by the build scripts to root-absolute `/assets/shoot-furniture.jpg` and `/assets/shoot-fashion.jpg` for the subfolder decks.
3. With ORA AI, one raw photo becomes a full campaign in minutes. (headline; standard size, wraps to ~3 lines; standard padding, chevrons sit in the `.subwrap` flex row; no footnote) — 4-page `.bap` sub-carousel; each page is a 5-column `.bagrid` of square (`aspect-ratio:1/1`) tiles with bottom labels: one raw client tile (kept its rose highlight border) then 4 ORA output tiles, no divider. Defaults to the ring page (`subShow(3)`). All four pages are filled, one product category each: page 1 bangle (bangle-raw, bangle-angled, bangle-wrist, bangle-golden, bangle-luxury), page 2 earrings (earring-raw, -studio, -ear, -jasmine, -stone), page 3 necklace (necklace-raw, -neck, -resort, -marble, -silk), page 4 ring (ring-raw, -studio, -hand, -evening, -velvet). The full source sets (10+ shots per category, PNG) are in `~/Downloads/Images for portfolio-20260810T162521Z-1-001.zip`; deck assets are 1024px JPEGs converted from those with sips. `bangle-petals.jpg` is unused (dropped when the row went from 5 outputs to 4 for bigger tiles) but kept in `assets/` as a spare. Clicking any `.stile img` opens it in a fullscreen `#lightbox` (arrows/Prev/Next cycle within that page's 5 tiles, Esc or backdrop/image click closes). The lightbox keydown handler is registered in the capture phase and calls `stopPropagation()` so deck ArrowLeft/Right nav does not fire while it is open.
4. AI generation is easy. Reliable production is not. — `.cmp` comparison table: all cells left-aligned, header row highlighted with a light band (ORALAB header keeps its green `.ora` tint), no footnote.
5. We specialise in Jewellery. — a `.jstrip` row of 4 category images (spec-ring, spec-bangle, spec-necklace, spec-rings) spanning the full width above the 4 `.card` text boxes; `.jtile img` are wired into the `#lightbox` (cycle within the strip).
6. 5 steps from raw image to final campaign, powered by the ORA Agent.
7. One platform for all your creative needs. — three cards (Social Media, Website, Marketplaces), each with a `.lgrid` logo collage of `.lgt` tiles above the copy. Social Media and Website use inline monochrome simple-icons brand glyphs in 2x2 grids (Instagram/Meta/YouTube/Pinterest; Shopify/WooCommerce/Wix/Webflow) with tag pills beneath; Marketplaces uses a self-labeled wordmark wall (Amazon, Flipkart, Myntra, Nykaa, Etsy, Walmart, Noon, Farfetch) as a 4-col x 2-row grid (`.lgrid.m4`) and no duplicate tags. All `.lgt` tiles share one fixed height so the three grids are the same height; cards are `.ucard` flex columns with `.utags` pinned to the bottom (`margin-top:auto`), so grids, descriptions and tag rows line up across the three cards. The old `[Image]` placeholders and the `oralab-diamond.mp4` preview were removed (that mp4 is now unused but kept in `assets/`). Marketplace brand logos are text because they are not in the open-source simple-icons set; swap in real logo files if provided.
8. Global brands trust us for their most important visuals. — 5 client-logo cards (Damas, Jawhara, Alliel, Carat Story, VBJ) in a centered flex-wrap (3+2 rows) with enlarged logos; no footnote.
9. Work ORA shipped for real brands. — 2-page `.sub2` client-work carousel. Behaviour: every tile is PAUSED by default (first frame + `.paused` play-button overlay, no autoplay); clicking a tile opens the fullscreen `#vlb` video lightbox which plays that video with controls and has prev/next (`vlbStep`) to move through all `.sub2 video` in order, Esc/backdrop/✕ to close. `cvidSync()` is now just "pause every `.sub2 video`" (called from `show()`/`sub2Show()` on slide/page change; the client-work slide index is `slides[7]` after slide 5 was removed). This behaviour is shared across decks (in `index.html`). Jewellery videos: damas-campaign, jawhara-campaign, alliel-social, vbj-bridal (page 1) + keemti-1/3/4 and hillside-campaign (page 2).
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
