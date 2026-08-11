# ORALAB Client Deck

Single-file sales deck for ORA / ORALAB, an AI creative platform for jewellery product images and video. The entire deck lives in `index.html` (inline CSS + markup + JS); media sits in `assets/`. GitHub repo: `collaborate-bhavishya/sales-deck`. Netlify deploys from `main`, so a push updates the live link.

> Note: the original CLAUDE.md from the first build session was lost. This file was reconstructed on 2026-08-11 from the deck source and the handoff summary. Items marked ⚠ could not be recovered and need confirming against the original conversation.

## Repo layout

- `index.html` — the whole deck: styles, 12 slide sections, carousel JS at the bottom
- `assets/` — `bangle-*.jpg` (slide 3 sub-carousel) and client `.mp4` videos

## Slide map (12 `<section class="slide">` elements)

1. Cover — "The AI creative platform for studio-quality product images and video."
2. Great products deserve better visual velocity.
3. From raw images to campaigns in minutes, with ORA AI. — 4-page `.bap` sub-carousel (bangle-raw, bangle-angled, bangle-wrist, bangle-golden, bangle-luxury, bangle-petals)
4. AI generation is easy. Reliable production is not.
5. We specialise in Jewellery.
6. 5 steps from raw image to final campaign, powered by the ORA Agent.
7. One platform for all your creative needs. — plays `oralab-diamond.mp4`
8. Global brands trust us for their most important visuals.
9. Work ORA shipped for real brands. — 2-page `.sub2` client-work carousel: damas-campaign, jawhara-campaign, alliel-social, vbj-bridal, keemti-1 through keemti-4
10. Bring us the brief, or bring your team.
11. Operators and researchers, not tourists in AI.
12. Give ORA a few SKUs. See what comes back.

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

Related trap: the ArrowUp/ArrowDown handlers hardcode parent-slide indices (`slides[2]` for the `.bap` carousel, `slides[8]` for `.sub2`). If slides are added, removed, or reordered, update those indices.

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

- Commit and push to `main` after each meaningful change; Netlify redeploys the live link automatically.
- Remote is HTTPS with the macOS keychain credential helper; git user is `collaborate-bhavishya`.
