fp = "/Users/bhavishyachaurasia/sales deck/furniture/index.html"
src = open(fp).read()

# The raw-hero + output-stack layout (f3row/f3raw/f3stack) now lives in
# index.html (jewellery uses it too), so its CSS and the lightbox JS wiring
# are inherited when build_furniture.py copies index.html. This script only
# swaps the subviews content for the furniture pages (absolute /assets/ srcs).

# ---------- New slide-3 markup: 2 pages (sofa, chair), raw hero + output stack ----------
def stack_imgs(cat, n):
    cls = {1: "fs c1", 2: "fs c2", 3: "fs c3"}
    out = []
    for i in range(1, n + 1):
        c = cls.get(i, "fs")
        out.append(f'              <img src="/assets/furn-{cat}-{i:02d}.jpg" alt="" class="{c}">')
    return "\n".join(out)

def page(cat, label, n, first):
    on = " on" if first else ""
    return f'''        <div class="bap{on}">
          <div class="f3row f3page">
            <figure class="f3raw">
              <img src="/assets/furn-{cat}-raw.jpg" alt="Raw {label} photo, sent by client">
              <figcaption><span class="cdot"></span>Raw &middot; sent by client</figcaption>
            </figure>
            <div class="f3arrow"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
            <button type="button" class="f3stack" aria-label="View {n} ORA outputs of this {label}">
{stack_imgs(cat, n)}
              <span class="f3badge">{n} ORA outputs</span>
              <span class="f3hint">Click to view all</span>
            </button>
          </div>
        </div>'''

new_pages = "\n".join([
    page("sofa", "sofa", 8, True),
    page("chair", "chair", 8, False),
    page("bed", "bed", 8, False),
    page("tvunit", "TV unit", 8, False),
    page("sofa2", "sofa", 8, False),
])

# Replace everything inside slide-3 .subviews (the 4 placeholder .bap pages) with the 2 new pages
i0 = src.index('<div class="subviews">') + len('<div class="subviews">')
close = '\n      </div>\n      <button class="chev" id="subNext"'
i1 = src.index(close, i0)
src = src[:i0] + "\n" + new_pages + src[i1:]

open(fp, "w").write(src)
print("done. bytes:", len(src))
print("bap pages:", src.count('<div class="bap'))
print("f3stack blocks:", src.count('class="f3stack"'))
print("furn asset refs:", src.count('assets/furn-'))
print("f3 css inherited:", '.f3raw{' in src)
print("lightbox f3page inherited:", "img.closest('.f3page')" in src)
