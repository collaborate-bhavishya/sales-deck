import re

src = open("/Users/bhavishyachaurasia/sales deck/index.html").read()

# --- Title ---
src = src.replace("<title>ORALAB Client Deck", "<title>ORALAB Furniture Deck")

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

# --- Slide 8: client logos -> placeholders, drop region badges ---
src = re.sub(r'<img src="data:image/png;base64,[^"]*" alt="[^"]*" style="max-height:[^"]*">',
             '<span class="micro" style="color:rgba(255,255,255,.4)">[ Client logo ]</span>', src)
src = re.sub(r'<span class="badge" style="font-size:10px;padding:5px 12px">[^<]*</span>', '', src)

# --- Slide 9: client-work videos -> placeholders (line-based) ---
lines = src.split('\n')
ptile = '<div class="ptile" style="background:#101010"><span class="micro" style="color:rgba(255,255,255,.4)">[ Client work ]</span></div>'
prow = '          <div class="prow">' + ptile * 4 + '</div>'
for i, l in enumerate(lines):
    if 'class="prow"' in l and ('damas-campaign.mp4' in l or 'keemti-1.mp4' in l):
        lines[i] = prow
src = '\n'.join(lines)

# --- JS: carousel defaults to first page (no ring) ---
src = src.replace('subShow(3);', 'subShow(0);')

# --- Safety net: any remaining jewellery words (visible copy + comments) ---
src = src.replace('<!-- 4 · JEWELLERY SPECIALISATION -->', '<!-- 4 · FURNITURE SPECIALISATION -->')
src = src.replace('Jewellery', 'Furniture').replace('jewellery', 'furniture').replace('Jewelry', 'Furniture')

# --- Remove the client-work / video slide (no furniture videos yet) ---
a = src.index('<!-- CLIENT WORK -->')
b = src.index('<!-- 10 · HOW WE WORK -->')
src = src[:a] + src[b:]
# and its carousel JS (subs2 / sub2Show / cvidSync / video handlers) so nothing references the removed elements
ja = src.index('/* client work sub-carousel */')
jb = src.index('sub2Show(0);', ja) + len('sub2Show(0);')
src = src[:ja] + src[jb:]

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
