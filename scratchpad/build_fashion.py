import re, os

src = open("/Users/bhavishyachaurasia/sales deck/index.html").read()

# --- Title ---
src = src.replace("<title>ORALAB Client Deck", "<title>ORALAB Fashion Deck")

# --- Slide 3: product carousel -> fashion placeholders ---
# Output tiles (16): image -> empty
src = re.sub(
    r'<div class="stile"><img src="assets/[a-z0-9-]+\.jpg" alt=""><span class="lab">[^<]*</span></div>',
    '<div class="stile empty"><span class="micro">[ ORA output ]</span></div>', src)
# Raw tiles (4): image -> empty, per-page category hint
cats = iter(["dress", "handbag", "footwear", "outerwear"])
def raw_repl(m):
    return f'<div class="stile rawtile empty"><span class="micro">Raw · {next(cats)} photo</span></div>'
src = re.sub(
    r'<div class="stile rawtile"><img src="assets/[a-z0-9-]+-raw\.jpg" alt="Raw client photo"><span class="lab"[^>]*>Raw · sent by client</span></div>',
    raw_repl, src)

# --- Slide 6: analyse-product copy ---
src = src.replace(
    'Vision models read product geometry: stones, settings, textures and material properties.',
    'Vision models read product geometry: fabric, drape, fit, texture and colour.')

# --- Slide 7: marketplaces -> fashion marketplaces ---
# keep Amazon, Myntra, Nykaa, Farfetch (all fashion-relevant); swap the rest
for old, new in [('Flipkart','Ajio'), ('Etsy','ASOS'), ('Walmart','Zalando'), ('Noon','Shein')]:
    src = src.replace(f'<div class="lgt"><span>{old}</span></div>', f'<div class="lgt"><span>{new}</span></div>')

# --- Slide 8: client brands (text wordmarks; swap in real logos when available) ---
brands = ["Kameez", "Shaurya Sanadhya", "Cotton Culture"]
def brand_card(name):
    return ('    <div class="card" style="text-align:center;padding:16px;flex:0 1 calc(33.333% - 16px);max-width:440px">\n'
            '      <div style="min-height:130px;display:flex;align-items:center;justify-content:center;border-radius:16px;background:var(--surface2);border:1px solid var(--border);padding:16px">'
            f'<span style="font-family:\'Bricolage Grotesque\',sans-serif;font-size:clamp(16px,1.9vw,24px);font-weight:600;color:rgba(255,255,255,.9)">{name}</span></div>\n'
            '    </div>')
_ot = '<div class="cols" style="display:flex;flex-wrap:wrap;justify-content:center;gap:16px">'
_i0 = src.index(_ot) + len(_ot)
_i1 = src.index('\n  </div></div>\n</section>', _i0)
src = src[:_i0] + '\n' + '\n'.join(brand_card(b) for b in brands) + src[_i1:]

# --- JS: carousel defaults to first page ---
src = src.replace('subShow(3);', 'subShow(0);')

# --- Safety net: any remaining jewellery words (visible copy + comments) ---
src = src.replace('Jewellery', 'Fashion').replace('jewellery', 'fashion').replace('Jewelry', 'Fashion')

# --- Remove the client-work / video slide (no fashion videos yet) ---
a = src.index('<!-- CLIENT WORK -->')
b = src.index('<!-- 10 · HOW WE WORK -->')
src = src[:a] + src[b:]
# and its carousel JS (subs2 / sub2Show / cvidSync / video handlers)
ja = src.index('/* client work sub-carousel */')
jb = src.index('sub2Show(0);', ja) + len('sub2Show(0);')
src = src[:ja] + src[jb:]

os.makedirs("/Users/bhavishyachaurasia/sales deck/fashion", exist_ok=True)
open("/Users/bhavishyachaurasia/sales deck/fashion/index.html", "w").write(src)

# --- Verify ---
out = open("/Users/bhavishyachaurasia/sales deck/fashion/index.html").read()
leftovers = re.findall(r'(?i)jewellery|jewelry|prong|bangle|earring|necklace|\bstone\b|damas|jawhara|alliel|keemti|\bvbj\b|carat story', out)
asset_refs = re.findall(r'src="assets/[^"]+"', out)
print("bytes:", len(out))
print("leftover jewellery terms:", sorted(set(l.lower() for l in leftovers)) or "NONE")
print("remaining asset file refs:", asset_refs or "NONE (fully self-contained)")
print("slide sections:", out.count('<section class="slide'))
print("title:", "Fashion" if "ORALAB Fashion Deck" in out else "??")
print("marketplaces present:", [m for m in ['Ajio','ASOS','Zalando','Shein','Amazon','Myntra','Nykaa','Farfetch'] if f'<span>{m}</span>' in out])
