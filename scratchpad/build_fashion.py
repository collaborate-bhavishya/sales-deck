import re, os

src = open("/Users/bhavishyachaurasia/sales deck/jewellery/index.html").read()

# --- Title ---
src = src.replace("<title>ORALAB Client Deck", "<title>ORALAB Fashion Deck")

# --- Slide 2: traditional-shoot photo (fashion; absolute /assets/ so it loads under /fashion/) ---
src = src.replace('src="/assets/shoot-jewellery.jpg" alt="Traditional studio photoshoot"',
                  'src="/assets/shoot-fashion.jpg" alt="Traditional fashion photoshoot"')

# --- Slide 3: fashion = raw client photo + AI-video output stack ---
# Same raw-hero layout as the other decks (f3 CSS + lightbox wiring inherited
# from index.html), but the outputs are AI VIDEOS: the stack shows poster
# frames carrying data-vsrc/data-vcap, and the shared .f3stack handler opens
# the fullscreen #vlb player cycling that category's videos. The row has NO
# .f3page class, so clicking the raw photo just zooms the raw in #lightbox.
# All srcs are root-absolute /assets/ so they load under /fashion/.
# (key, label, video count)
# (key, label, video count, raw_photo_ready)
FASH = [
    ("dress",  "Dress",          1, True),
    ("print",  "Printed shirt",  5, True),
    ("stripe", "Striped shirt",  3, True),
    ("jacket", "Leather jacket", 1, True),
]
_PLAY = ('<span aria-hidden="true" style="position:absolute;z-index:6;top:50%;left:50%;'
         'transform:translate(-50%,-50%);width:60px;height:60px;border-radius:50%;'
         'background:rgba(232,78,126,.92);display:flex;align-items:center;justify-content:center;'
         'box-shadow:0 10px 30px rgba(0,0,0,.5);pointer-events:none">'
         '<span style="border-style:solid;border-width:10px 0 10px 17px;'
         'border-color:transparent transparent transparent #fff;margin-left:4px"></span></span>')

def vstack(key, label, n):
    cls = {1: "fs c1", 2: "fs c2", 3: "fs c3"}
    out = []
    for i in range(1, n + 1):
        c = cls.get(i, "fs")
        out.append(f'              <img src="/assets/fash-{key}-{i}.jpg" data-vsrc="/assets/fash-{key}-{i}.mp4" data-vcap="{label}" alt="" class="{c}">')
    return "\n".join(out)

def raw_block(key, label, ready):
    if ready:
        return (f'            <figure class="f3raw">\n'
                f'              <img src="/assets/fash-{key}-raw.jpg" alt="Raw {label} photo, sent by client">\n'
                f'              <figcaption><span class="cdot"></span>Raw &middot; sent by client</figcaption>\n'
                f'            </figure>')
    # raw photo not supplied yet: honest dashed placeholder (no misleading stand-in)
    return (f'            <div class="f3raw" style="border-style:dashed;box-shadow:none;display:flex;'
            f'align-items:center;justify-content:center;text-align:center;padding:16px">'
            f'<span style="color:rgba(255,255,255,.5);letter-spacing:.12em;text-transform:uppercase;'
            f'font-size:11px;line-height:1.8">Raw {label}<br>photo coming</span></div>')

def fpage(key, label, n, ready, first):
    on = " on" if first else ""
    s = "" if n == 1 else "s"
    return f'''        <div class="bap{on}">
          <div class="f3row f3tall">
{raw_block(key, label, ready)}
            <div class="f3arrow"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
            <button type="button" class="f3stack" aria-label="Play {n} ORA video{s} of this {label}">
{vstack(key, label, n)}
              {_PLAY}
              <span class="f3badge">{n} ORA video{s}</span>
              <span class="f3hint">Click to play</span>
            </button>
          </div>
        </div>'''

_f3new = "\n".join(fpage(k, l, n, r, i == 0) for i, (k, l, n, r) in enumerate(FASH))
_f3i0 = src.index('<div class="subviews">') + len('<div class="subviews">')
_f3close = '\n      </div>\n      <button class="chev" id="subNext"'
_f3i1 = src.index(_f3close, _f3i0)
src = src[:_f3i0] + "\n" + _f3new + src[_f3i1:]

# --- Fashion 'What we do' (video) slide: small "Image to video" sub label.
#     Done here while the heading is still unique (the raw->images slide below reuses it). ---
src = src.replace(
    '<h2 class="headline">One raw photo becomes a full campaign <em>in minutes.</em></h2>',
    '<h2 class="headline">One raw photo becomes a full campaign <em>in minutes.</em></h2>\n  <p class="sub">Image to video</p>', 1)

# --- New slide after slide 3: "sketch to finished product" gallery (fashion only) ---
_go = lambda key, cap: (f'        <figure class="fgo"><img src="/assets/fash-velvet-{key}.jpg" alt="{cap} render">'
                        f'<figcaption>{cap}</figcaption></figure>')
_sketch_slide = '''
<!-- SKETCH TO FINISHED (fashion) -->
<section class="slide">
  <div class="blob" style="width:24vw;height:24vw;background:#C79BF0;opacity:.05;top:-9vw;right:-7vw"></div>
  <span class="tag"><span class="dot"></span>Every format</span>
  <h2 class="headline">From sketch to finished product, <em>all with ORA AI in minutes.</em></h2>
  <p class="sub">One tech sketch becomes product, studio, editorial and lifestyle imagery.</p>
  <div class="grow">
    <div class="fgal">
      <div class="fgsketch"><img src="/assets/fash-velvet-sketch.jpg" alt="Technical sketch of the dress"><figcaption>Tech sketch</figcaption></div>
      <div class="fgarrow"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
      <div class="fggrid">
''' + "\n".join([_go("product", "Product"), _go("studio", "Studio"), _go("editorial", "Editorial"), _go("lifestyle", "Lifestyle"), _go("details", "Details")]) + '''
      </div>
    </div>
  </div>
</section>'''
# insert right after slide 3's </section>
_s3end = src.index('</section>', src.index('id="subNext"')) + len('</section>')
src = src[:_s3end] + "\n" + _sketch_slide + src[_s3end:]

# --- New slide after the sketch slide: raw product -> finished images carousel (fashion only) ---
# Uses its OWN carousel (.rap pages + #rawPrev/#rawNext/#rawDots + rawShow() JS in index.html),
# independent of the .bap product carousel. Each page is the f3tall raw-hero + image-output stack
# (no data-vsrc, so the shared .f3stack handler opens the image #lightbox cycling raw + outputs).
RAW2FIN = [("saree", "Saree", 6), ("suit", "Suit", 6), ("fabric", "Fabric to suit", 5), ("shirt", "Shirt", 5)]
def rstack(cat, n):
    cls = {1: "fs c1", 2: "fs c2", 3: "fs c3"}
    return "\n".join(f'              <img src="/assets/fash-out-{cat}-{i}.jpg" alt="" class="{cls.get(i, "fs")}">' for i in range(1, n + 1))
def rpage(cat, label, n, first):
    on = " on" if first else ""
    return f'''        <div class="rap{on}">
          <div class="f3row f3tall f3page">
            <figure class="f3raw">
              <img src="/assets/fash-raw-{cat}.jpg" alt="Raw {label}, sent by client">
              <figcaption><span class="cdot"></span>Raw &middot; sent by client</figcaption>
            </figure>
            <div class="f3arrow"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
            <button type="button" class="f3stack" aria-label="View {n} ORA images of this {label}">
{rstack(cat, n)}
              <span class="f3badge">{n} ORA images</span>
              <span class="f3hint">Click to view all</span>
            </button>
          </div>
        </div>'''
_raps = "\n".join(rpage(c, l, n, i == 0) for i, (c, l, n) in enumerate(RAW2FIN))
_raw_slide = '''
<!-- RAW TO FINISHED (fashion) -->
<section class="slide">
  <div class="blob" style="width:24vw;height:24vw;background:#8FB8F0;opacity:.05;bottom:-8vw;left:-6vw"></div>
  <span class="tag"><span class="dot"></span>Raw to finished</span>
  <h2 class="headline">One raw photo becomes a full campaign <em>in minutes.</em></h2>
  <div class="grow" style="flex-direction:column;justify-content:center">
    <div class="subwrap">
      <button class="chev" id="rawPrev" aria-label="Previous product"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg></button>
      <div class="subviews">
''' + _raps + '''
      </div>
      <button class="chev" id="rawNext" aria-label="Next product"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button>
    </div>
    <div class="subdots" id="rawDots"></div>
  </div>
</section>'''
# place the raw->images slide BEFORE the video ("What we do") slide, so the
# showcase order is: raw->images, raw->videos, sketch->finished
_vidstart = src.index('<!-- 3 · BEFORE / AFTER (product carousel) -->')
src = src[:_vidstart] + _raw_slide.lstrip("\n") + "\n\n" + src[_vidstart:]

# --- Slide 6: analyse-product copy ---
src = src.replace(
    'Vision models read product geometry: stones, settings, textures and material properties.',
    'Vision models read product geometry: fabric, drape, fit, texture and colour.')

# --- Slide 7: marketplaces -> fashion marketplaces ---
# keep Amazon, Myntra, Nykaa, Farfetch (all fashion-relevant); swap the rest
for old, new in [('Flipkart','Ajio'), ('Etsy','ASOS'), ('Walmart','Zalando'), ('Noon','Shein')]:
    src = src.replace(f'<div class="lgt"><span>{old}</span></div>', f'<div class="lgt"><span>{new}</span></div>')

# --- Slide 8: client brands (real logos where sourced from official sites; wordmark otherwise) ---
# (name, logo path or None). Kameez is a generic name (many brands), so it stays a wordmark.
brands = [("Kameez", None), ("Shaurya Sanadhya", "/assets/fash-logo-shaurya.png"),
          ("Cotton Culture", "/assets/fash-logo-cottonculture.jpg")]
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

# --- JS: carousel defaults to first page ---
src = src.replace('subShow(3);', 'subShow(0);')

# --- Safety net: any remaining jewellery words (visible copy + comments) ---
src = src.replace('Jewellery', 'Fashion').replace('jewellery', 'fashion').replace('Jewelry', 'Fashion')

# --- Remove the client-work / video slide (no fashion videos yet) ---
# (It now sits right after slide 3, so remove ONLY its own <section>, not the
#  range up to "How we work" which would delete the middle of the deck.)
a = src.index('<!-- CLIENT WORK -->')
b = src.index('</section>', a) + len('</section>')
src = src[:a] + src[b:]
# and its carousel JS (subs2 / sub2Show / cvidSync / video handlers)
ja = src.index('/* client work sub-carousel */')
jb = src.index('sub2Show(0);', ja) + len('sub2Show(0);')
src = src[:ja] + src[jb:]

# --- Cover: moving media wall (fashion renders, absolute /assets/ paths) ---
import sys as _sys
_sys.path.insert(0, "/Users/bhavishyachaurasia/sales deck/scratchpad")
import cover_lib as _cl
_logo = re.search(r'src="(data:image/png;base64,[^"]+)" alt="ORALAB"', src).group(1)
_a = src.index('<!-- 1 · COVER -->'); _b = src.index('<!-- 2 · PROBLEM -->')
src = src[:_a] + '<!-- 1 · COVER -->\n' + _cl.wall_cover(_logo, _cl.FASH_COLS, '/assets/') + '\n\n' + src[_b:]

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
