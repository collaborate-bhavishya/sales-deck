import re

src = open("/Users/bhavishyachaurasia/sales deck/jewellery/index.html").read()

# --- Title ---
src = src.replace("<title>ORALAB Client Deck", "<title>ORALAB Furniture Deck")

# --- Slide 2: traditional-shoot photo (furniture; absolute /assets/ so it loads under /furniture/) ---
src = src.replace('src="/assets/shoot-jewellery.jpg" alt="Traditional studio photoshoot"',
                  'src="/assets/shoot-furniture.jpg" alt="Traditional furniture photoshoot"')

# --- Slide 3: product carousel -> furniture placeholders ---
# Output tiles (16): image -> empty
src = re.sub(
    r'<div class="stile"><img src="assets/[a-z0-9-]+\.jpg" alt=""><span class="lab">[^<]*</span></div>',
    '<div class="stile empty"><span class="micro">[ ORA output ]</span></div>', src)
# Raw tiles (4): image -> empty, with a per-page category hint
cats = iter(["sofa", "dining table", "bed", "accent chair"])
def raw_repl(m):
    return f'<div class="stile rawtile empty"><span class="micro">Raw · {next(cats)} photo</span></div>'
src = re.sub(
    r'<div class="stile rawtile"><img src="assets/[a-z0-9-]+-raw\.jpg" alt="Raw client photo"><span class="lab"[^>]*>Raw · sent by client</span></div>',
    raw_repl, src)

# --- Slide 5: specialisation ---
src = src.replace('We specialise in <em>Jewellery.</em>', 'We specialise in <em>Furniture.</em>')
src = src.replace(
    'The category where AI has to get it right. Jewellery exposes visual errors instantly: a wrong prong, stone, proportion or reflection makes an image commercially unusable. That is why we built our deepest systems here.',
    'The category where AI has to get it right. Furniture exposes visual errors instantly: a wrong grain, joint, proportion or fabric drape makes an image commercially unusable. That is why we built our deepest systems here.')
# strip images -> placeholders
src = re.sub(r'<div class="jtile"><img src="assets/spec-[a-z]+\.jpg" alt="[^"]*"></div>',
             '<div class="jtile empty"><span class="micro">[ Furniture ]</span></div>', src)
# .jtile.empty styling
src = src.replace(
    '.jtile img{width:100%;height:100%;object-fit:cover;display:block;cursor:zoom-in}',
    '.jtile img{width:100%;height:100%;object-fit:cover;display:block;cursor:zoom-in}\n.jtile.empty{display:flex;align-items:center;justify-content:center;border-style:dashed;color:rgba(255,255,255,.35)}')
# cards
src = src.replace(
    '<span class="mini">Stones & settings</span><h3>Every stone stays true</h3><p>Cut, colour, clarity and setting geometry preserved exactly as photographed.</p>',
    '<span class="mini">Materials & finish</span><h3>Every grain stays true</h3><p>Wood grain, finish, colour and joinery preserved exactly as photographed.</p>')
src = src.replace(
    '<span class="mini">Metal & texture</span><h3>Real metal behaviour</h3><p>Polish, engraving, plating tone and reflections rendered faithfully, not approximated.</p>',
    '<span class="mini">Fabric & texture</span><h3>Real material behaviour</h3><p>Upholstery weave, leather, wood and reflections rendered faithfully, not approximated.</p>')
src = src.replace(
    '<span class="mini">On-model try-ons</span><h3>Worn the right way</h3><p>Correct size, placement and drape on diverse models, across skin tones and poses.</p>',
    '<span class="mini">In-room staging</span><h3>Placed the right way</h3><p>Correct scale, placement and styling across rooms, light and interior settings.</p>')

# --- Slide 6: analyse-product copy ---
src = src.replace(
    'Vision models read product geometry: stones, settings, textures and material properties.',
    'Vision models read product geometry: materials, finish, joinery, texture and proportions.')

# --- Slide 7: marketplaces -> furniture marketplaces ---
for old, new in [('Flipkart','Wayfair'), ('Myntra','IKEA'), ('Nykaa','Houzz'),
                 ('Noon','Overstock'), ('Farfetch','West Elm')]:
    src = src.replace(f'<div class="lgt"><span>{old}</span></div>', f'<div class="lgt"><span>{new}</span></div>')

# --- Slide 8: client brands (real logos where sourced from official sites; wordmark otherwise) ---
# (name, logo path or None). Ammri / Living Concept / Hive / Chattels are generic or
# had no cleanly-extractable official logo, so they stay as wordmarks until files arrive.
brands = [("Hive", None), ("SmaartCraaft", "/assets/furn-logo-smaartcraaft.png"),
          ("Ammri", None), ("Living Concept", None), ("Chattels &amp; More", "/assets/furn-logo-chattels.svg")]
def brand_card(name, logo):
    inner = (f'<img src="{logo}" alt="{name}" style="max-height:72px;max-width:82%;width:auto;object-fit:contain;display:block">'
             if logo else
             f'<span style="font-family:\'Bricolage Grotesque\',sans-serif;font-size:clamp(16px,1.9vw,24px);font-weight:600;color:#1a1a1a">{name}</span>')
    return ('    <div class="card" style="text-align:center;padding:16px;flex:0 1 calc(33.333% - 16px);max-width:440px">\n'
            '      <div style="min-height:130px;display:flex;align-items:center;justify-content:center;border-radius:16px;background:#F4F4F1;border:1px solid var(--border);padding:16px">'
            f'{inner}</div>\n'
            '    </div>')
_ot = '<div class="cols" style="display:flex;flex-wrap:wrap;justify-content:center;gap:16px">'
_i0 = src.index(_ot) + len(_ot)
_i1 = src.index('\n  </div></div>\n</section>', _i0)
src = src[:_i0] + '\n' + '\n'.join(brand_card(n, l) for n, l in brands) + src[_i1:]

# --- Slide 9: client-work videos -> 8 furniture brand videos (absolute /assets/ paths) ---
def fvtile(n, lab):
    return (f'<div class="ptile" style="background:#000"><video src="/assets/furn-work-{n}.mp4" '
            f'muted loop playsinline preload="metadata"></video><span class="lab">{lab}</span></div>')
p1 = '          <div class="prow">' + ''.join(fvtile(n, l) for n, l in [(1,'Product film'),(2,'Campaign'),(4,'Ad film'),(5,'Concept')]) + '</div>'
p2 = '          <div class="prow">' + ''.join(fvtile(n, l) for n, l in [(6,'Interior'),(7,'Lifestyle'),(8,'Studio')]) + '</div>'
lines = src.split('\n')
for i, l in enumerate(lines):
    if 'class="prow"' in l and 'damas-campaign.mp4' in l:
        lines[i] = p1
    elif 'class="prow"' in l and 'keemti-1.mp4' in l:
        lines[i] = p2
src = '\n'.join(lines)

# --- JS: carousel defaults to first page (no ring) ---
src = src.replace('subShow(3);', 'subShow(0);')

# --- Safety net: any remaining jewellery words (visible copy + comments) ---
src = src.replace('<!-- 4 · JEWELLERY SPECIALISATION -->', '<!-- 4 · FURNITURE SPECIALISATION -->')
src = src.replace('Jewellery', 'Furniture').replace('jewellery', 'furniture').replace('Jewelry', 'Furniture')

# NOTE: the client-work video slide is KEPT (furniture brand videos above); its
# .sub2 / cvidSync JS stays intact and slides[7] correctly targets it.

# --- Cover: furniture media wall (own renders, absolute /assets/ paths) ---
import sys as _sys
_sys.path.insert(0, "/Users/bhavishyachaurasia/sales deck/scratchpad")
import cover_lib as _cl
_logo = re.search(r'src="(data:image/png;base64,[^"]+)" alt="ORALAB"', src).group(1)
_a = src.index('<!-- 1 · COVER -->'); _b = src.index('<!-- 2 · PROBLEM -->')
src = src[:_a] + '<!-- 1 · COVER -->\n' + _cl.wall_cover(_logo, _cl.FURN_COLS, '/assets/') + '\n\n' + src[_b:]

import os as _os
_os.makedirs("/Users/bhavishyachaurasia/sales deck/furniture", exist_ok=True)
open("/Users/bhavishyachaurasia/sales deck/furniture/index.html", "w").write(src)

# --- Verify ---
out = open("/Users/bhavishyachaurasia/sales deck/furniture/index.html").read()
import re as _re
leftovers = _re.findall(r'(?i)jewellery|jewelry|prong|bangle|earring|necklace|\bstone\b|damas|jawhara|alliel|keemti|\bvbj\b|carat story', out)
asset_refs = _re.findall(r'src="assets/[^"]+"', out)
print("bytes:", len(out))
print("leftover jewellery terms:", sorted(set(l.lower() for l in leftovers)) or "NONE")
print("remaining asset file refs:", asset_refs or "NONE (fully self-contained)")
print("slide sections:", out.count('<section class="slide'))
