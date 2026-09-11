import re, os

src = open("/Users/bhavishyachaurasia/sales deck/index.html").read()

# --- Title ---
src = src.replace("<title>ORALAB Client Deck", "<title>ORALAB Fashion Deck")

# --- Slide 2: traditional-shoot photo (fashion; absolute /assets/ so it loads under /fashion/) ---
src = src.replace('src="assets/shoot-jewellery.jpg" alt="Traditional studio photoshoot"',
                  'src="/assets/shoot-fashion.jpg" alt="Traditional fashion photoshoot"')

# --- Slide 3: fashion placeholders in the raw-hero + output-stack layout ---
# index.html now uses the f3row/f3raw/f3stack layout for slide 3 (jewellery
# images). Fashion has no product images yet, so overwrite the subviews with
# placeholder pages that reuse the inherited f3 CSS but carry no image srcs
# (dashed boxes) so the deck stays fully self-contained under /fashion/.
FCATS = ["dress", "handbag", "footwear", "outerwear"]
def fpage(label, first):
    on = " on" if first else ""
    return f'''        <div class="bap{on}">
          <div class="f3row f3page">
            <div class="f3raw" style="border-style:dashed;box-shadow:none;display:flex;align-items:center;justify-content:center;height:min(56vh,480px)">
              <span style="color:rgba(255,255,255,.45);letter-spacing:.12em;text-transform:uppercase;font-size:11px">Raw &middot; {label} photo</span>
            </div>
            <div class="f3arrow"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
            <div class="f3stack" style="border:1px dashed var(--border);border-radius:16px;display:flex;align-items:center;justify-content:center">
              <span style="color:rgba(255,255,255,.35);letter-spacing:.12em;text-transform:uppercase;font-size:11px">ORA outputs &middot; coming soon</span>
            </div>
          </div>
        </div>'''
_f3new = "\n".join(fpage(c, i == 0) for i, c in enumerate(FCATS))
_f3i0 = src.index('<div class="subviews">') + len('<div class="subviews">')
_f3close = '\n      </div>\n      <button class="chev" id="subNext"'
_f3i1 = src.index(_f3close, _f3i0)
src = src[:_f3i0] + "\n" + _f3new + src[_f3i1:]

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

# --- Cover: simple (no fashion product images yet; swap to a wall once they exist) ---
import sys as _sys
_sys.path.insert(0, "/Users/bhavishyachaurasia/sales deck/scratchpad")
import cover_lib as _cl
_logo = re.search(r'src="(data:image/png;base64,[^"]+)" alt="ORALAB"', src).group(1)
_a = src.index('<!-- 1 · COVER -->'); _b = src.index('<!-- 2 · PROBLEM -->')
src = src[:_a] + '<!-- 1 · COVER -->\n' + _cl.simple_cover(_logo) + '\n\n' + src[_b:]

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
