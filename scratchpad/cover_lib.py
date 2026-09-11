# Shared cover builder for all three decks (moving media wall + tinted panel).

def cover_css():
    return """
/* --- cover: moving media wall + tinted panel --- */
.slide.cover{padding:0!important;overflow:hidden;align-items:center;justify-content:center}
/* !important beats the deck's .slide>*:not(.blob){position:relative;z-index:1} rule */
.slide.cover .cvwall{position:absolute!important;inset:0;display:flex;gap:12px;padding:12px;z-index:0!important}
.cvcol{flex:1;overflow:hidden;min-width:0}
.cvcol .cvtrack{display:flex;flex-direction:column;gap:12px;will-change:transform}
.cvcol.up .cvtrack{animation:cvup var(--dur,36s) linear infinite}
.cvcol.down .cvtrack{animation:cvdown var(--dur,36s) linear infinite}
@keyframes cvup{from{transform:translateY(0)}to{transform:translateY(-50%)}}
@keyframes cvdown{from{transform:translateY(-50%)}to{transform:translateY(0)}}
.cvtile{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:3/4;border:1px solid rgba(255,255,255,.06);flex:0 0 auto;background:var(--surface2)}
.cvtile img{width:100%;height:100%;object-fit:cover;display:block}
.cvpb{position:absolute;top:9px;right:9px;width:26px;height:26px;border-radius:50%;background:rgba(232,78,126,.94);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,.4)}
.cvpb::before{content:"";border-style:solid;border-width:5px 0 5px 8px;border-color:transparent transparent transparent #fff;margin-left:2px}
.slide.cover .cvscrim{position:absolute!important;inset:0;z-index:1!important;pointer-events:none;background:radial-gradient(ellipse 72% 66% at 50% 48%, rgba(9,9,9,.5), rgba(9,9,9,.28) 62%, rgba(9,9,9,.52) 100%)}
.slide.cover .cvpanel{position:relative;z-index:2!important;background:rgba(9,9,9,.5);backdrop-filter:blur(14px) saturate(120%);-webkit-backdrop-filter:blur(14px) saturate(120%);border:1px solid rgba(255,255,255,.09);border-radius:28px;padding:clamp(26px,3.6vw,48px) clamp(30px,5vw,76px);display:flex;flex-direction:column;align-items:center;text-align:center;box-shadow:0 40px 110px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.05);max-width:min(92vw,760px)}
.cvpanel .clogo{height:clamp(60px,9vh,100px);width:auto;margin-bottom:16px;filter:drop-shadow(0 6px 26px rgba(0,0,0,.7))}
.slide.cover .headline{margin-bottom:0;text-shadow:0 6px 34px rgba(0,0,0,.75)}
.slide.cover .headline em{color:var(--rose)}
.slide.cover .cvtags{position:absolute!important;left:0;right:0;bottom:min(7vh,54px);display:flex;gap:10px;justify-content:center;z-index:3!important}
.cvtags .badge{background:rgba(9,9,9,.55);backdrop-filter:blur(4px)}
@media (prefers-reduced-motion:reduce){.cvcol .cvtrack{animation:none}}
@media (max-width:820px){.cvpanel{padding:22px 24px;border-radius:22px}.cvwall{gap:8px;padding:8px}}
"""

_DIRS = ["up", "down", "up", "down", "up"]
_DURS = [34, 42, 30, 46, 36]

def _tile(src, video, prefix):
    pb = '<div class="cvpb"></div>' if video else ''
    return f'<div class="cvtile"><img src="{prefix}{src}.jpg" alt="">{pb}</div>'

def _col(items, d, dur, prefix):
    inner = "".join(_tile(a, v, prefix) for a, v in items)
    return f'<div class="cvcol {d}" style="--dur:{dur}s"><div class="cvtrack">{inner}{inner}</div></div>'

def wall_cover(logo, cols, prefix):
    wall = "".join(_col(c, _DIRS[i % 5], _DURS[i % 5], prefix) for i, c in enumerate(cols))
    return f'''<section class="slide cover">
  <div class="cvwall">{wall}</div>
  <div class="cvscrim"></div>
  <div class="cvpanel">
    <img class="clogo" src="{logo}" alt="ORALAB">
    <h2 class="headline">The AI creative platform for <em>studio-quality product images and video.</em></h2>
  </div>
  <div class="cvtags"><span class="badge" style="color:var(--rose);border-color:#3A2029">Applied AI Research Lab</span><span class="badge" style="color:var(--platinum)">Visual Commerce</span></div>
</section>'''

def simple_cover(logo):
    return f'''<section class="slide cover" style="align-items:center;justify-content:center;text-align:center">
  <div class="blob" style="width:34vw;height:34vw;background:#F19AB0;opacity:.07;top:-12vw;right:-8vw"></div>
  <div class="blob" style="width:22vw;height:22vw;background:#8FB8F0;opacity:.06;bottom:-6vw;right:16vw"></div>
  <img src="{logo}" alt="ORALAB" style="height:clamp(90px,13vh,150px);width:auto;align-self:center;object-fit:contain;margin-bottom:10px">
  <h2 class="headline" style="margin-top:26px;max-width:22ch;align-self:center;text-align:center">The AI creative platform for <em>studio-quality product images and video.</em></h2>
  <div style="position:absolute;left:0;right:0;bottom:min(10vh,92px);display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:center">
    <span class="badge" style="color:var(--rose);border-color:#3A2029">Applied AI Research Lab</span>
    <span class="badge" style="color:var(--platinum)">Visual Commerce</span>
  </div>
</section>'''

# image columns per vertical (asset-basename, is_video)
JEWEL_COLS = [
    [("ring-studio",True),("necklace-neck",False),("bangle-wrist",False),("earring-jasmine",True)],
    [("earring-studio",False),("ring-hand",True),("necklace-marble",False),("spec-bangle",False)],
    [("necklace-resort",True),("bangle-golden",False),("ring-velvet",False),("earring-ear",True)],
    [("spec-necklace",False),("bangle-angled",True),("necklace-silk",False),("ring-evening",False)],
    [("earring-stone",False),("spec-rings",True),("bangle-luxury",False),("ring-studio",False)],
]
FURN_COLS = [
    [("furn-sofa-01",True),("furn-chair-02",False),("furn-sofa-03",False),("furn-chair-04",True)],
    [("furn-chair-01",False),("furn-sofa-02",True),("furn-chair-03",False),("furn-sofa-04",False)],
    [("furn-sofa-05",True),("furn-chair-06",False),("furn-sofa-07",False),("furn-chair-08",True)],
    [("furn-chair-05",False),("furn-sofa-06",True),("furn-chair-07",False),("furn-sofa-08",False)],
    [("furn-sofa-raw",False),("furn-chair-raw",False),("furn-sofa-01",False),("furn-chair-02",False)],
]
