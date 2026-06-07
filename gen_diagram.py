# -*- coding: utf-8 -*-
import re, random

random.seed(7)

BLUE="#8AB4F8"; MINT="#5EEAD4"; PURP="#B79CF0"; GOLD="#F4C77B"
SUB="#9AA6CC"; INK="#FFFFFF"; FILL="#141C32"
W,H=2080,1300

def esc(s): return s.replace("&","&amp;")

# ---- nodes: x,y are CENTER ----
NH=58
N = {
 'pattern':   dict(x=340,  y=655, w=210, t='PATTERN',            s='compressible by a model',            c=MINT, origin=True),
 'attractor': dict(x=720,  y=655, w=226, t='ATTRACTOR',          s='stable region in state-space',       c=BLUE),
 'form':      dict(x=1085, y=655, w=210, t='FORM',               s='attractor realized in matter',       c=BLUE),
 'agency':    dict(x=1445, y=655, w=200, t='AGENCY',             s='a defended pattern',                 c=BLUE),
 'mind':      dict(x=1790, y=655, w=200, t='MIND',               s='models possible patterns',           c=BLUE),

 'compression':dict(x=340, y=415, w=210, t='COMPRESSION',        s='pattern as description',             c=BLUE),
 'dynstab':   dict(x=720,  y=415, w=238, t='DYNAMICAL STABILITY',s='pattern as return',                  c=BLUE),
 'time':      dict(x=1085, y=415, w=178, t='TIME',               s='pattern unfolding',                  c=BLUE),
 'compute':   dict(x=1445, y=415, w=224, t='COMPUTE',            s='substrate-general; cells compute',   c=BLUE),

 'beauty':    dict(x=340,  y=195, w=196, t='BEAUTY',             s='compression progress',               c=MINT),
 'possible':  dict(x=900,  y=180, w=228, t='POSSIBLE PATTERNS',  s='what could be · Platonic?',      c=PURP),
 'logic':     dict(x=1360, y=180, w=216, t='LOGIC',              s='first filter: non-contradiction',    c=BLUE),

 'isreal':    dict(x=340,  y=895, w=200, t='IS IT REAL?',        s='recoverable + predictive',           c=BLUE),
 'reality':   dict(x=340,  y=1095,w=234, t='REALITY CONSTRAINT', s='reality pushes back',                c=BLUE),
 'existence': dict(x=720,  y=895, w=198, t='EXISTENCE',          s='pattern that persists',              c=BLUE),
 'attrtypes': dict(x=1085, y=895, w=252, t='ATTRACTOR TYPES',    s='cell fate · phenotypes · neurotypes?', c=MINT),
 'ideaattr':  dict(x=1455, y=895, w=216, t='IDEA ATTRACTORS',    s='patterns in idea-space',             c=MINT),
 'scale':     dict(x=1085, y=1095,w=244, t='SCALE CONFLICT',     s='local attractor, global harm',       c=PURP),
 'selection': dict(x=1795, y=895, w=210, t='SELECTION',          s='which to realize?',                  c=PURP),
 'ourrole':   dict(x=1820, y=1095,w=226, t='OUR ROLE',           s='search · test · choose · realize', c=PURP),
}

# ---- edges: (src, dst, label, color, dashed, thick, t) ; arrow points at dst ----
E = [
 ('pattern','attractor','becomes stable',BLUE,False,True,0.5),
 ('attractor','form','realized in matter',BLUE,False,True,0.5),
 ('form','agency','defended under load',BLUE,False,True,0.5),
 ('agency','mind','modeled by',BLUE,False,True,0.5),

 ('pattern','compression','seen as',BLUE,False,False,0.5),
 ('attractor','dynstab','seen as',BLUE,False,False,0.5),
 ('form','time','unfolds in',BLUE,False,False,0.5),
 ('agency','compute','runs on',BLUE,False,False,0.5),

 ('compression','beauty','felt as',MINT,False,False,0.5),
 ('logic','possible','bounds the possible',PURP,True,False,0.5),
 ('possible','pattern','options',PURP,True,False,0.74),
 ('possible','form','could-be',PURP,True,False,0.66),

 ('pattern','isreal','is it real?',BLUE,False,False,0.5),
 ('reality','isreal','corrects',BLUE,False,False,0.5),
 ('attractor','existence','persists as',BLUE,False,False,0.5),
 ('form','attrtypes','comes in kinds',MINT,False,False,0.5),
 ('mind','ideaattr','lives in minds',MINT,False,False,0.5),
 ('ideaattr','attractor','a kind of attractor',MINT,False,False,0.6),
 ('mind','selection','must choose',PURP,True,False,0.5),
 ('selection','ourrole','falls to us',PURP,True,False,0.5),
 ('scale','selection','forces the choice',PURP,True,False,0.46),
]

# ---- open-question pills (gold), floating ----
PILLS = [
 (575,108,'Beauty = felt ingression?'),
 (1360,96,'Logic: frame or ground?'),
 (520,778,'Mind, or world?'),
 (1632,778,'Threshold or gradient?'),
]

def border(n, tx, ty):
    cx,cy=n['x'],n['y']; hw=n['w']/2+9; hh=NH/2+9
    dx,dy=tx-cx,ty-cy
    if dx==0 and dy==0: return cx,cy
    sx=hw/abs(dx) if dx else 9e9; sy=hh/abs(dy) if dy else 9e9
    s=min(sx,sy)
    return cx+dx*s, cy+dy*s

out=[]
A=out.append
A('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Calibri, Segoe UI, sans-serif" role="img" aria-labelledby="diagram-title diagram-desc">'%(W,H,W,H))
A('<title id="diagram-title">From Pattern to Mind &mdash; concept map</title>')
A('<desc id="diagram-desc">A left-to-right spine reads pattern, attractor, form, agency, mind. Arrows link it to its lenses and tests: logic, compression, dynamical stability, time, compute, beauty, possible patterns, reality, existence, idea attractors, scale conflict, selection. Colour marks how much weight each claim bears: defensible, plausible analogy, speculative or normative, and open question.</desc>')
A('<rect width="%d" height="%d" fill="#0B1020"/>'%(W,H))

# stars
for _ in range(34):
    x=random.randint(20,W-20); y=random.randint(20,H-20); r=random.choice([1.0,1.3,1.6])
    col=random.choice([BLUE,MINT,"#93A0C4"])
    A('<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity="0.10"/>'%(x,y,r,col))

# markers
A('<defs>')
for name,col in [('b',BLUE),('m',MINT),('p',PURP),('g',GOLD)]:
    A('<marker id="ar-%s" markerWidth="13" markerHeight="13" refX="9" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L9,4 L0,8 z" fill="%s"/></marker>'%(name,col))
A('</defs>')

# spine band
A('<rect x="150" y="624" width="1810" height="62" rx="31" fill="#0E1733" opacity="0.45"/>')

# title
A('<text x="40" y="50" fill="#FFFFFF" font-size="25" font-weight="700" font-family="Georgia, serif">From Pattern to Mind</text>')
A('<text x="40" y="74" fill="#93A0C4" font-size="13">logic ▸ pattern ▸ attractor ▸ form ▸ agency ▸ mind</text>')

mk={BLUE:'b',MINT:'m',PURP:'p',GOLD:'g'}
labels=[]
# edges
for src,dst,lab,col,dashed,thick,t in E:
    a=N[src]; b=N[dst]
    x1,y1=border(a,b['x'],b['y']); x2,y2=border(b,a['x'],a['y'])
    w = 3.0 if thick else 1.7
    op = 0.85 if thick else (0.5 if dashed else 0.6)
    dash=' stroke-dasharray="6,6"' if dashed else ''
    A('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" opacity="%.2f"%s marker-end="url(#ar-%s)"/>'%(x1,y1,x2,y2,col,w,op,dash,mk[col]))
    lx=x1+(x2-x1)*t; ly=y1+(y2-y1)*t
    labels.append((lx,ly,lab,col))

# nodes
for k,n in N.items():
    x=n['x']-n['w']/2; y=n['y']-NH/2
    sw = 2.6 if n.get('origin') else 1.7
    A('<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="11" fill="%s" stroke="%s" stroke-width="%.1f"/>'%(x,y,n['w'],NH,FILL,n['c'],sw))
    tl=len(n['t']); fs=15 if tl<=12 else (13 if tl<=17 else 12)
    A('<text x="%d" y="%d" fill="%s" font-size="%d" font-weight="700" text-anchor="middle">%s</text>'%(n['x'],n['y']-3,INK,fs,esc(n['t'])))
    A('<text x="%d" y="%d" fill="%s" font-size="11" text-anchor="middle" font-style="italic">%s</text>'%(n['x'],n['y']+15,SUB,esc(n['s'])))

# edge labels (on top of edges, under nothing else)
for lx,ly,lab,col in labels:
    tw=len(lab)*5.9+16
    A('<rect x="%.1f" y="%.1f" width="%.1f" height="18" rx="5" fill="#0B1020" opacity="0.92"/>'%(lx-tw/2,ly-9,tw))
    A('<text x="%.1f" y="%.1f" fill="%s" font-size="10.5" text-anchor="middle">%s</text>'%(lx,ly+3.5,col,esc(lab)))

# pills
for px,py,txt in PILLS:
    pw=len(txt)*6.0+24
    A('<rect x="%.1f" y="%.1f" width="%.1f" height="28" rx="14" fill="#1A1530" stroke="%s" stroke-width="1.3"/>'%(px-pw/2,py-14,pw,GOLD))
    A('<text x="%.1f" y="%.1f" fill="%s" font-size="11.5" text-anchor="middle">%s</text>'%(px,py+4,GOLD,esc(txt)))

# legend
lx0=44; ly0=1150
A('<text x="%d" y="%d" fill="#93A0C4" font-size="12" font-weight="700">LAYERS</text>'%(lx0,ly0))
leg=[(BLUE,False,'defensible'),(MINT,False,'plausible analogy'),(PURP,True,'speculative / normative'),(GOLD,True,'open question')]
yy=ly0+18
for col,dsh,txt in leg:
    dash=' stroke-dasharray="4,4"' if dsh else ''
    A('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6"%s/>'%(lx0,yy,lx0+28,yy,col,dash))
    A('<text x="%d" y="%d" fill="#CDD6F0" font-size="11.5">%s</text>'%(lx0+36,yy+3,esc(txt)))
    yy+=18

# caption
A('<text x="%d" y="1262" fill="#93A0C4" font-size="12" text-anchor="end" font-style="italic">↻ this map is itself an idea-attractor — a compression to test against reality, then drop where it fails.</text>'%(W-40))

A('</svg>')
svg="\n".join(out)

p=r"index.html"
html=open(p,encoding="utf-8").read()
new=re.sub(r'<svg xmlns="http://www\.w3\.org/2000/svg".*?</svg>', lambda m: svg, html, count=1, flags=re.S)
assert new!=html and new.count("<svg")>=1
open(p,"w",encoding="utf-8").write(new)
print("done; svg chars:",len(svg))
