fp = "/Users/bhavishyachaurasia/sales deck/furniture.html"
src = open(fp).read()

# ---------- 1. New slide-3 markup: 2 pages (sofa, chair), raw hero + output stack ----------
def stack_imgs(cat, n):
    cls = {1: "fs c1", 2: "fs c2", 3: "fs c3"}
    out = []
    for i in range(1, n + 1):
        c = cls.get(i, "fs")
        out.append(f'              <img src="assets/furn-{cat}-{i:02d}.jpg" alt="" class="{c}">')
    return "\n".join(out)

def page(cat, label, n, first):
    on = " on" if first else ""
    return f'''        <div class="bap{on}">
          <div class="f3row f3page">
            <figure class="f3raw">
              <img src="assets/furn-{cat}-raw.jpg" alt="Raw {label} photo, sent by client">
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

new_pages = page("sofa", "sofa", 8, True) + "\n" + page("chair", "chair", 8, False)

# Replace everything inside slide-3 .subviews (the 4 placeholder .bap pages) with the 2 new pages
i0 = src.index('<div class="subviews">') + len('<div class="subviews">')
close = '\n      </div>\n      <button class="chev" id="subNext"'
i1 = src.index(close, i0)
src = src[:i0] + "\n" + new_pages + src[i1:]

# ---------- 2. CSS for the hero + stack ----------
css = '''/* slide 3 furniture: raw hero + clickable output stack */
.f3row{display:flex;align-items:stretch;justify-content:center;gap:clamp(12px,2.4vw,36px);width:100%}
.f3raw{position:relative;flex:0 1 46%;max-width:520px;border-radius:16px;overflow:hidden;border:2px solid var(--rose);box-shadow:0 0 0 1px rgba(232,78,126,.3),0 10px 30px rgba(232,78,126,.18)}
.f3raw img{width:100%;height:min(56vh,480px);object-fit:cover;display:block;cursor:zoom-in}
.f3raw figcaption{position:absolute;bottom:10px;left:12px;display:flex;align-items:center;gap:7px;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:rgba(232,78,126,.9);border-radius:999px;padding:5px 11px}
.f3raw .cdot{width:6px;height:6px;border-radius:50%;background:#fff;display:inline-block}
.f3arrow{display:flex;align-items:center;color:var(--rose);flex:0 0 auto}
.f3stack{position:relative;flex:0 1 46%;max-width:520px;height:min(56vh,480px);background:none;border:none;padding:0;cursor:pointer;flex-shrink:0}
.f3stack .fs{position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;border-radius:16px;border:1px solid var(--border);background:var(--surface2);transition:transform .25s ease}
.f3stack .c1{z-index:5;box-shadow:0 14px 36px rgba(0,0,0,.55)}
.f3stack .c2{z-index:4;transform:rotate(-5deg) translateX(-4%)}
.f3stack .c3{z-index:3;transform:rotate(5deg) translateX(4%)}
.f3stack .fs:not(.c1):not(.c2):not(.c3){z-index:1}
.f3stack:hover .c1{transform:translateY(-6px)}
.f3stack:hover .c2{transform:rotate(-8deg) translateX(-8%)}
.f3stack:hover .c3{transform:rotate(8deg) translateX(8%)}
.f3badge{position:absolute;z-index:6;top:10px;right:10px;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:rgba(9,9,9,.62);border:1px solid rgba(255,255,255,.28);border-radius:999px;padding:5px 11px;backdrop-filter:blur(3px)}
.f3hint{position:absolute;z-index:6;bottom:12px;left:0;right:0;text-align:center;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#fff;pointer-events:none;text-shadow:0 1px 6px rgba(0,0,0,.7)}
@media (max-width:760px){.f3raw img,.f3stack{height:38vh}.f3arrow{display:none}}
'''
src = src.replace('/* slide 5 specialisation image strip */', css + '/* slide 5 specialisation image strip */')

# ---------- 3. Lightbox: recognise .f3page group + wire raw/stack clicks ----------
src = src.replace(
    "const grid=img.closest('.bagrid')||img.closest('.jstrip');",
    "const grid=img.closest('.bagrid')||img.closest('.jstrip')||img.closest('.f3page');")
src = src.replace(
    "document.querySelectorAll('.stile img, .jtile img').forEach(img=>img.addEventListener('click',()=>lbOpen(img)));",
    "document.querySelectorAll('.stile img, .jtile img, .f3raw img').forEach(img=>img.addEventListener('click',()=>lbOpen(img)));\n"
    "document.querySelectorAll('.f3stack').forEach(st=>st.addEventListener('click',()=>{const t=st.querySelector('.c1')||st.querySelector('img');if(t)lbOpen(t);}));")

open(fp, "w").write(src)
print("done. bytes:", len(src))
print("bap pages:", src.count('<div class="bap'))
print("f3stack blocks:", src.count('class="f3stack"'))
print("furn asset refs:", src.count('assets/furn-'))
