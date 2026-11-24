# They Live parody episode builder: python3 build.py  -> out.mp4
import numpy as np, subprocess, wave, math, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W, H, FPS = 1080, 1920, 30
CUTS = os.path.join(HERE, '..', '..', 'cuts') + '/'
ANTON = '/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf'
ARCH = '/usr/share/fonts/truetype/google-fonts/ofl/archivoblack/ArchivoBlack-Regular.ttf'
F = lambda p, s: ImageFont.truetype(p, s)

# ---------------- episode spec ----------------
V1_AT, V2_AT = 0.5, 7.7
FLASH = 7.1            # glasses go on
ON = 7.3               # world switches
TOTAL = 17.8
BRAND = 13.7
CAP_OFF = [(0.5, 2.05, "CLOUDY SKIES TODAY, FOLKS!"),
           (2.05, 4.1, "JUST SOME HARMLESS HAZE UP THERE."),
           (4.6, 7.1, "NOTHING TO WORRY ABOUT. ENJOY YOUR DAY!")]
CAP_ON = [(7.7, 9.2, "DON'T LOOK UP."),
          (9.2, 10.55, "BREATHE DEEP."),
          (10.55, 12.6, "STAY ASLEEP."),
          (12.6, 13.7, "OBEY.")]
JESSIE = [(0, 'jessie-cool-no-glasses-01'), (2.2, 'jessie-cool-no-glasses-03'), (5.0, 'jessie-cool-glasses-lowered-07'),
          (FLASH + 0.1, 'jessie-cool-glasses-worn-01'), (10.55, 'jessie-cool-glasses-worn-04'), (12.6, 'jessie-cool-glasses-lowered-08')]
MAN = [(0, 'fullbody-regular-man-09'), (4.6, 'fullbody-regular-man-10'),
       (ON, 'fullbody-alien-man-09'), (9.2, 'fullbody-alien-man-10'), (10.55, 'fullbody-alien-man-11')]
SCREEN_ON = [(ON, "DON'T\nLOOK UP"), (12.6, "OBEY")]
TICK_OFF = "TODAY: PARTLY CLOUDY  •  HARMLESS HAZE  •  NOTHING TO WORRY ABOUT  •  ENJOY YOUR DAY  •  "
TICK_ON = "NOTHING TO SEE HERE  •  STAY ASLEEP  •  DON'T LOOK UP  •  OBEY  •  "
BUG_OFF, BUG_ON = "THEY NEWS", "THEY LIE"

def at(lst, t):
    cur = lst[0][1]
    for s, v in lst:
        if t >= s: cur = v
    return cur

# ---------------- static art ----------------
def load(n): return Image.open(CUTS + n + '.png').convert('RGBA')
man_cache, jes_cache = {}, {}
MAN_SCALE = 960 / 505
def man_img(n):
    if n not in man_cache:
        im = load(n).transpose(Image.FLIP_LEFT_RIGHT); man_cache[n] = im.resize((int(im.width * MAN_SCALE), int(im.height * MAN_SCALE)), Image.LANCZOS)
    return man_cache[n]
JP = 470
def jes_img(n):
    if n not in jes_cache:
        im = load(n).convert('RGB'); s = min(im.size); im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
        jes_cache[n] = im.resize((JP, JP), Image.LANCZOS)
    return jes_cache[n]

def halftone(col, step=9, r=1.6, alpha=40):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for y in range(0, H, step):
        off = (y // step % 2) * step / 2
        for x in range(0, W + step, step):
            d.ellipse((x + off - r, y - r, x + off + r, y + r), fill=col + (alpha,))
    return lay

SX0, SY0, SX1, SY1 = 50, 200, 740, 750   # map screen
FLOOR, TK0, TK1, TXT0 = 1430, 1500, 1570, 1585
def studio():
    im = Image.new('RGB', (W, H), (20, 27, 40)); d = ImageDraw.Draw(im)
    # wall panels with light stripes
    for i, x in enumerate(range(0, W, 135)):
        d.rectangle((x, 0, x + 130, FLOOR), fill=(26, 36, 54) if i % 2 else (22, 31, 47))
        d.line((x + 131, 0, x + 131, FLOOR), fill=(12, 16, 24), width=4)
    for x in (70, 540, 990):  # spot light cones
        cone = Image.new('L', (W, H), 0); cd = ImageDraw.Draw(cone)
        cd.polygon([(x - 30, 0), (x + 30, 0), (x + 230, FLOOR), (x - 230, FLOOR)], fill=38)
        cone = cone.filter(ImageFilter.GaussianBlur(30)); im.paste((200, 210, 255), (0, 0), cone)
    d.rectangle((0, FLOOR, W, TXT0), fill=(12, 14, 20))       # floor
    d.line((0, FLOOR, W, FLOOR), fill=(70, 80, 110), width=3)
    d.rectangle((0, TXT0, W, H), fill=(18, 17, 16))            # ransom board
    im.paste(halftone((0, 0, 0)), (0, 0), halftone((0, 0, 0)))
    # screen bezel
    d.rectangle((SX0 - 22, SY0 - 22, SX1 + 22, SY1 + 22), fill=(8, 8, 10))
    d.rectangle((SX0 - 22, SY0 - 22, SX1 + 22, SY1 + 22), outline=(90, 100, 130), width=4)
    d.rectangle((SX1 - 160, SY1 + 22, SX1 - 120, SY1 + 120), fill=(8, 8, 10))
    return im

def cloud(d, cx, cy, s, fill, face=True, outline=(0, 0, 0)):
    for dx, dy, r in [(-0.9, 0.15, .55), (-0.35, -0.25, .72), (0.35, -0.15, .62), (0.9, 0.18, .5), (0, 0.25, .6)]:
        d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=fill, outline=outline, width=5)
    for dx, dy, r in [(-0.9, 0.15, .55), (-0.35, -0.25, .72), (0.35, -0.15, .62), (0.9, 0.18, .5), (0, 0.25, .6)]:
        rr = r * s - 5; d.ellipse((cx + dx * s - rr, cy + dy * s - rr, cx + dx * s + rr, cy + dy * s + rr), fill=fill)
    if face:
        e = s * 0.12
        d.ellipse((cx - s * .3 - e / 2, cy - e, cx - s * .3 + e / 2, cy), fill=(0, 0, 0))
        d.ellipse((cx + s * .25 - e / 2, cy - e, cx + s * .25 + e / 2, cy), fill=(0, 0, 0))
        d.arc((cx - s * .35, cy - s * .15, cx + s * .3, cy + s * .35), 20, 160, fill=(0, 0, 0), width=6)

_T = [(-40, 60, 760, 330, .8), (-40, 300, 760, 120, .7), (100, -20, 560, 600, .75), (700, -20, 160, 600, .85), (-40, 470, 760, 420, .9), (300, -20, 720, 380, .65)]
TRAILS = [(x0, y0, x0 + (x1 - x0) * f, y0 + (y1 - y0) * f) for x0, y0, x1, y1, f in _T]
def trails(d, col_soft, col_core):
    for x0, y0, x1, y1 in TRAILS:
        for w, c in [(30, col_soft), (16, col_soft), (6, col_core)]:
            d.line((x0, y0, x1, y1), fill=c, width=w)
def plane(d, x, y, ang, col):
    ca, sa = math.cos(ang), math.sin(ang); P = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    d.polygon([P(18, 0), P(-14, -3), P(-14, 3)], fill=col)
    d.polygon([P(4, 0), P(-6, -16), P(-10, -16), P(-4, 0), P(-10, 16), P(-6, 16)], fill=col)
    d.polygon([P(-12, 0), P(-17, -7), P(-19, -7), P(-16, 0), P(-19, 7), P(-17, 7)], fill=col)

def screen_off():
    sw, sh = SX1 - SX0, SY1 - SY0
    im = Image.new('RGB', (sw, sh), (70, 150, 215)); d = ImageDraw.Draw(im)
    for y in range(0, sh, 26): d.line((0, y, sw, y), fill=(64, 142, 206), width=2)
    soft = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); trails(ImageDraw.Draw(soft), (255, 255, 255, 70), (255, 255, 255, 235))
    im.paste(soft.filter(ImageFilter.GaussianBlur(3)), (0, 0), soft.filter(ImageFilter.GaussianBlur(3)))
    for x0, y0, x1, y1 in TRAILS:
        ang = math.atan2(y1 - y0, x1 - x0); fx, fy = x1 + 14 * math.cos(ang), y1 + 14 * math.sin(ang)
        if 0 < fx < sw and 0 < fy < sh: plane(d, fx, fy, ang, (40, 40, 50))
    d.ellipse((560, 30, 660, 130), fill=(255, 205, 60), outline=(0, 0, 0), width=5)
    d.rounded_rectangle((20, 20, 200, 100), 10, fill=(240, 240, 240), outline=(0, 0, 0), width=4)
    d.text((110, 60), "78\u00b0", font=F(ANTON, 62), fill=(200, 40, 30), anchor='mm')
    d.rounded_rectangle((20, sh - 90, 330, sh - 20), 10, fill=(240, 240, 240), outline=(0, 0, 0), width=4)
    d.text((175, sh - 55), "HAZY SKIES", font=F(ARCH, 40), fill=(20, 20, 20), anchor='mm')
    return im

def screen_on(txt):
    sw, sh = SX1 - SX0, SY1 - SY0
    im = Image.new('RGB', (sw, sh), (235, 235, 235)); d = ImageDraw.Draw(im)
    trails(d, (190, 190, 190), (90, 90, 90))
    font = F(ANTON, 150 if '\n' in txt else 260)
    d.multiline_text((sw * 0.5, sh / 2 + 20), txt, font=font, fill=(0, 0, 0), anchor='mm', align='center', spacing=-10, stroke_width=10, stroke_fill=(235, 235, 235))
    return im

def to_bw(im, auto=True):
    g = ImageOps.grayscale(im)
    if auto: g = ImageOps.autocontrast(g, cutoff=2)
    g = g.point(lambda v: int(255 * (1 / (1 + math.exp(-(v - 120) / 28)))))
    return Image.merge('RGB', (g, g, g))

BASE_OFF = studio(); BASE_OFF.paste(screen_off(), (SX0, SY0))
BASE_ON_STUDIO = to_bw(studio(), auto=False)
SCR_ON = {t: screen_on(t) for _, t in SCREEN_ON}

def bug(d, txt, on):
    f = F(ARCH, 38); w = d.textlength(txt, font=f) + 50
    d.rectangle((40, 60, 40 + w, 128), fill=(255, 255, 255) if on else (190, 30, 30))
    d.rectangle((40, 60, 40 + w, 128), outline=(0, 0, 0), width=4)
    d.text((40 + w / 2, 94), txt, font=f, fill=(0, 0, 0) if on else (255, 255, 255), anchor='mm')
    if not on:
        d.rectangle((40, 136, 160, 180), fill=(255, 255, 255)); d.text((100, 158), "LIVE", font=F(ARCH, 28), fill=(190, 30, 30), anchor='mm')

def ticker(im, t, txt, on):
    d = ImageDraw.Draw(im); y0, y1 = TK0, TK1
    d.rectangle((0, y0, W, y1), fill=(255, 255, 255) if on else (190, 30, 30))
    d.line((0, y0, W, y0), fill=(0, 0, 0), width=4); d.line((0, y1, W, y1), fill=(0, 0, 0), width=4)
    strip = TSTRIP[on]; tw = strip.width; x = -int((t * 170) % tw)
    while x < W:
        im.paste(strip, (x, y0 + 5), strip); x += tw

def wrap(d, txt, f, maxw):
    words, lines, cur = txt.split(), [], ''
    for w_ in words:
        tst = (cur + ' ' + w_).strip()
        if d.textlength(tst, font=f) <= maxw: cur = tst
        else: lines.append(cur); cur = w_
    lines.append(cur); return lines

def mkstrip(txt, on):
    f = F(ARCH, 40)
    st = Image.new('RGBA', (4000, 60), (0, 0, 0, 0)); ImageDraw.Draw(st).text((0, 30), txt.rstrip(), font=f, fill=(0, 0, 0) if on else (255, 255, 255), anchor='lm')
    xs = np.where(np.asarray(st)[..., 3].max(0) > 0)[0]
    return st.crop((0, 0, int(xs.max()) + 60, 60))
TSTRIP = {False: mkstrip(TICK_OFF, False), True: mkstrip(TICK_ON, True)}
CX0, CY0, CX1, CY1 = 545, 1325, 1045, 1325 + JP
def caption(im, t):
    d = ImageDraw.Draw(im); on = t >= ON
    cap = None
    for s, e, txt in (CAP_ON if on else CAP_OFF):
        if s <= t < e: cap, cs = txt, s
    d.rectangle((CX0, CY0, CX1, CY1), fill=(255, 255, 255) if on else (24, 30, 44))
    d.rectangle((CX0, CY0, CX1, CY1), outline=(0, 0, 0) if on else (230, 230, 230), width=8)
    if not cap: return
    pop = min(1, (t - cs) / 0.12)
    if on:
        size = 150
        while True:
            f = F(ANTON, size); ls = wrap(d, cap, f, CX1 - CX0 - 50)
            if len(ls) * size * 1.05 < CY1 - CY0 - 60 or size < 60: break
            size -= 6
        col = (0, 0, 0)
    else:
        size = 64; f = F(ARCH, size); ls = wrap(d, cap, f, CX1 - CX0 - 60)
        while len(ls) * size * 1.25 > CY1 - CY0 - 60: size -= 4; f = F(ARCH, size); ls = wrap(d, cap, f, CX1 - CX0 - 60)
        col = (255, 255, 255)
    lh = size * (1.05 if on else 1.25); y = (CY0 + CY1) / 2 - lh * (len(ls) - 1) / 2 + (1 - pop) * 30
    for l in ls:
        d.text(((CX0 + CX1) / 2, y), l, font=f, fill=col, anchor='mm'); y += lh

def jessie(im, t):
    n = at(JESSIE, t); start = max(s for s, v in JESSIE if t >= s)
    j = jes_img(n); k = min(1, (t - start) / 0.18); sc = 1.06 - 0.06 * k if start > 0 else 1
    jj = j.resize((int(JP * sc), int(JP * sc)), Image.LANCZOS)
    x0, y0 = 35, 1325
    d = ImageDraw.Draw(im); d.rectangle((x0 - 14, y0 - 14, x0 + JP + 14, y0 + JP + 14), fill=(245, 240, 225))
    box = jj.crop(((jj.width - JP) // 2, (jj.height - JP) // 2, (jj.width - JP) // 2 + JP, (jj.height - JP) // 2 + JP))
    im.paste(box, (x0, y0)); d.rectangle((x0 - 4, y0 - 4, x0 + JP + 4, y0 + JP + 4), outline=(0, 0, 0), width=8)

JC, JR = (262, 975), 245
_mask = None
def jessie(im, t):
    global _mask
    n = at(JESSIE, t); start = max(s_ for s_, v in JESSIE if t >= s_)
    k = min(1, (t - start) / 0.18); sc = 1.07 - 0.07 * k if start > 0 else 1
    r = int(JR * sc); src = load(n).convert('RGB'); s_ = min(src.size)
    src = src.crop(((src.width - s_) // 2, (src.height - s_) // 2, (src.width + s_) // 2, (src.height + s_) // 2))
    face = src.resize((int(2 * r * 1.08), int(2 * r * 1.08)), Image.LANCZOS)
    off = (face.width - 2 * r) // 2; face = face.crop((off, off - 6, off + 2 * r, off + 2 * r - 6))
    m = Image.new('L', (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    d = ImageDraw.Draw(im); cx, cy = JC
    d.ellipse((cx - r - 30, cy - r - 30 + 10, cx + r + 30, cy + r + 30 + 10), fill=(0, 0, 0))   # shadow
    d.ellipse((cx - r - 24, cy - r - 24, cx + r + 24, cy + r + 24), fill=(0, 0, 0))
    d.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), fill=(245, 240, 225))
    d.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), fill=(0, 0, 0))
    im.paste(face, (cx - r, cy - r), m)

RF = ['/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf', ARCH,
      '/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf',
      '/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/CrimsonText-Bold.ttf',
      '/usr/share/fonts/truetype/google-fonts/ofl/firasans/FiraSans-Black.ttf',
      '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
      '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf',
      '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf']
PAL_OFF = [((250, 247, 235), (0, 0, 0)), ((255, 221, 60), (0, 0, 0)), ((200, 35, 35), (255, 255, 255)),
           ((20, 20, 20), (255, 255, 255)), ((90, 170, 225), (0, 0, 0)), ((235, 225, 200), (180, 30, 30)),
           ((255, 255, 255), (30, 60, 160))]
PAL_ON = [((255, 255, 255), (0, 0, 0)), ((0, 0, 0), (255, 255, 255)), ((225, 225, 225), (0, 0, 0))]

def piece(word, rng, on, scale):
    fp = RF[0] if on and rng.random() < .5 else RF[rng.integers(len(RF))]
    size = int(rng.uniform(85, 175) * scale); f = F(fp, size)
    if fp == RF[3] or fp == RF[2]: word_ = word
    else: word_ = word.upper() if rng.random() < .7 else word
    paper, ink = (PAL_ON if on else PAL_OFF)[rng.integers(len(PAL_ON if on else PAL_OFF))]
    outline = rng.random() < .35
    sw = max(3, size // 22) if outline else 0
    bb = f.getbbox(word_, stroke_width=sw); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    px, py = int(size * .18), int(size * .14)
    w, h = tw + 2 * px, th + 2 * py
    img = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    j = lambda: rng.uniform(-6, 6)
    poly = [(10 + j(), 10 + j()), (10 + w + j(), 10 + j()), (10 + w + j(), 10 + h + j()), (10 + j(), 10 + h + j())]
    d.polygon([(x + 5, y + 6) for x, y in poly], fill=(0, 0, 0, 120))
    d.polygon(poly, fill=paper + (255,))
    if outline:
        fill_, stroke_ = (paper, ink) if rng.random() < .5 else (ink, (0, 0, 0) if ink != (0, 0, 0) else (255, 255, 255))
        d.text((10 + px - bb[0], 10 + py - bb[1]), word_, font=f, fill=fill_, stroke_width=sw, stroke_fill=stroke_)
    else:
        d.text((10 + px - bb[0], 10 + py - bb[1]), word_, font=f, fill=ink)
    return img.rotate(rng.uniform(-6, 6), resample=Image.BICUBIC, expand=True)

_rcache = {}
def ransom_layout(txt, on):
    key = (txt, on)
    if key in _rcache: return _rcache[key]
    words = txt.split(); seed = sum(map(ord, txt))
    for scale in [1, .9, .8, .72, .64, .56, .5, .44]:
        rng = np.random.default_rng(seed)
        ps = [piece(w_, rng, on, scale) for w_ in words]
        rows, cur, cw = [], [], 0; maxw = W - 50
        for p in ps:
            if cur and cw + p.width - 8 > maxw: rows.append(cur); cur, cw = [], 0
            cur.append(p); cw += p.width - 8
        rows.append(cur)
        tot = sum(max(p.height for p in r) - 10 for r in rows)
        if tot <= H - TXT0 - 30: break
    pos = []; y = TXT0 + (H - TXT0 - tot) / 2
    for r in rows:
        rh = max(p.height for p in r) - 10; rw = sum(p.width - 8 for p in r); x = (W - rw) / 2
        for p in r:
            pos.append((p, int(x), int(y + (rh - p.height) / 2 + rng.uniform(-6, 6)))); x += p.width - 8
        y += rh
    _rcache[key] = pos; return pos

def ransom(im, t):
    on = t >= ON
    for s_, e, txt in (CAP_ON if on else CAP_OFF):
        if s_ <= t < e:
            pos = ransom_layout(txt, on); n = len(pos); span = max(0.25, min(e - s_ - 0.4, 0.28 * n))
            for i, (p, x, y) in enumerate(pos):
                ta = s_ + span * i / n
                if t < ta: break
                k = min(1, (t - ta) / 0.1); sc = 1.25 - 0.25 * k
                q = p if k >= 1 else p.resize((max(1, int(p.width * sc)), max(1, int(p.height * sc))))
                im.paste(q, (x - (q.width - p.width) // 2, y - (q.height - p.height) // 2), q)

def anaglyph(im, amt):
    r, g, b = im.split(); o = int(amt)
    r = r.transform(im.size, Image.AFFINE, (1, 0, -o, 0, 1, 0)); b = b.transform(im.size, Image.AFFINE, (1, 0, o, 0, 1, 0))
    g2 = g.transform(im.size, Image.AFFINE, (1, 0, o, 0, 1, 0))
    return Image.merge('RGB', (r, g2, b))

def frame(t):
    on = t >= ON
    if on:
        im = BASE_ON_STUDIO.copy(); im.paste(SCR_ON[at(SCREEN_ON, t)], (SX0, SY0))
    else:
        im = BASE_OFF.copy()
    m = man_img(at(MAN, t))
    if on: m = Image.merge('RGBA', (*to_bw(m.convert('RGB')).split()[:3], m.split()[3]))
    bob = 4 * math.sin(t * 3.1) if not on else 0
    im.paste(m, (W - m.width + 10, int(FLOOR + 22 - m.height + bob)), m)
    d = ImageDraw.Draw(im); bug(d, BUG_ON if on else BUG_OFF, on)
    ticker(im, t, TICK_ON if on else TICK_OFF, on)
    jessie(im, t); ransom(im, t)
    if t >= BRAND:
        from engine import brand_plate; brand_plate(im, t - BRAND)
    # glasses flash: anaglyph split + white pop + jitter
    if FLASH - 0.05 <= t < ON + 0.35:
        u = (t - FLASH) / (ON + 0.35 - FLASH)
        amt = 40 * math.sin(max(0, min(1, u)) * math.pi)
        im = anaglyph(im, amt)
        if abs(t - ON) < 0.06: im = Image.blend(im, Image.new('RGB', (W, H), (255, 255, 255)), 0.75)
        jit = int(18 * math.sin(t * 90)); im = im.transform(im.size, Image.AFFINE, (1, 0, jit, 0, 1, 0))
    if t < 0.3: im = Image.blend(Image.new('RGB', (W, H)), im, t / 0.3)
    if t > TOTAL - 0.4: im = Image.blend(Image.new('RGB', (W, H)), im, max(0, (TOTAL - t) / 0.4))
    return im

# ---------------- audio ----------------
SR = 44100
def rd(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels()).mean(1) if w.getnchannels() > 1 else x
def lp(x, a):
    y = np.zeros_like(x); s = 0.0; a = np.broadcast_to(a, x.shape)
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
def audio():
    N = int(TOTAL * SR); mix = np.zeros(N, np.float32)
    mu = rd(os.path.join(HERE, '..', '..', 'music', 'bed.wav'))[int(2.0 * SR):][:N]; mu = np.pad(mu, (0, N - len(mu)))
    t = np.arange(N) / SR
    on_i = int(ON * SR)
    from scipy.signal import butter, sosfilt
    muf = sosfilt(butter(2, 500, 'low', fs=SR, output='sos'), mu) * 1.8
    g = np.where(t < FLASH, 0.30, 0.42); g = g * np.clip(t / 0.4, 0, 1) * np.clip((TOTAL - t) / 0.8, 0, 1)
    m = np.where(np.arange(N) < on_i, mu, muf) * g
    m[int(FLASH * SR):on_i] *= 0.2
    mix += m
    v1 = rd('v1_44.wav'); v2 = rd('v2_44.wav')
    def put(at_, s, gain=1.0):
        i = int(at_ * SR); mix[i:i + len(s)] += s[:N - i] * gain
    put(V1_AT, v1, 1.0); put(V2_AT, v2, 1.15); put(BRAND + 0.35, rd(os.path.join(HERE, '..', '..', 'shared', 'tag.wav')), 1.3)
    rng = np.random.default_rng(1)
    # glasses click
    n = int(.03 * SR); c = rng.standard_normal(n) * np.exp(-np.arange(n) / 120); c -= lp(c, .3); put(FLASH, c * .5)
    put(FLASH + .05, c * .35)
    # riser into flash
    n = int(.5 * SR); x = rng.standard_normal(n).astype(np.float32); tt = np.linspace(0, 1, n)
    rs = lp(x, 0.02 + 0.3 * tt); rs *= tt ** 2 * .25 / np.abs(rs).max(); put(FLASH - .45, rs)
    # low boom + hum when world flips
    n = int(1.6 * SR); tt = np.arange(n) / SR
    boom = (np.sin(2 * np.pi * (48 + 30 * np.exp(-tt * 8)) * tt) * np.exp(-tt * 2.2) * .5
            + np.sin(2 * np.pi * 110 * tt) * .06 * np.exp(-tt * 1.2))
    put(ON, boom)
    # end sting tick
    n = int(.4 * SR); tt = np.arange(n) / SR; put(12.6, np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 6) * .5)
    pk = np.abs(mix).max(); mix /= max(1, pk / 0.95)
    with wave.open('mix.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in map(float, sys.argv[2:]): frame(t).save(f'still_{t}.jpg', quality=85)
        sys.exit()
    audio()
    out = sys.argv[1] if len(sys.argv) > 1 else 'out.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-i', 'mix.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)):
        enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print('done', out)
