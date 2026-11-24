# They Live parody engine: multi-flip episodes driven by a spec.
import numpy as np, subprocess, wave, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from scipy.signal import butter, sosfilt

W, H, FPS, SR = 1080, 1920, 30, 44100
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = os.path.join(HERE, '..', 'cuts') + '/'
MUSIC = os.path.join(HERE, '..', 'music', 'bed.wav')
GF = '/usr/share/fonts/truetype/google-fonts/ofl/'
ANTON = GF + 'anton/Anton-Regular.ttf'
ARCH = GF + 'archivoblack/ArchivoBlack-Regular.ttf'
_fc = {}
def F(p, s):
    k = (p, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(p, int(s))
    return _fc[k]

SX0, SY0, SX1, SY1 = 50, 200, 740, 750
FLOOR, TK0, TK1, TXT0 = 1430, 1500, 1570, 1585
JC, JR = (262, 975), 245

# ---------- art ----------
_img = {}
def load(n):
    if n not in _img: _img[n] = Image.open(CUTS + n + '.png').convert('RGBA')
    return _img[n]
FIG_SCALE = 960 / 505
_fig = {}
def fig(n, flip=True, bw=False, sc=1.0):
    k = (n, flip, bw, sc)
    if k not in _fig:
        im = load(n)
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im = im.resize((int(im.width * FIG_SCALE * sc), int(im.height * FIG_SCALE * sc)), Image.LANCZOS)
        if bw: im = Image.merge('RGBA', (*to_bw(im.convert('RGB')).split(), im.split()[3]))
        _fig[k] = im
    return _fig[k]

def to_bw(im, auto=True):
    g = ImageOps.grayscale(im)
    if auto: g = ImageOps.autocontrast(g, cutoff=2)
    g = g.point(lambda v: int(255 * (1 / (1 + math.exp(-(v - 120) / 28)))))
    return Image.merge('RGB', (g, g, g))

def halftone(step=9, r=1.6, alpha=40):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for y in range(0, H, step):
        off = (y // step % 2) * step / 2
        for x in range(0, W + step, step):
            d.ellipse((x + off - r, y - r, x + off + r, y + r), fill=(0, 0, 0, alpha))
    return lay

def studio(wall=((26, 36, 54), (22, 31, 47))):
    im = Image.new('RGB', (W, H), (20, 27, 40)); d = ImageDraw.Draw(im)
    for i, x in enumerate(range(0, W, 135)):
        d.rectangle((x, 0, x + 130, FLOOR), fill=wall[i % 2])
        d.line((x + 131, 0, x + 131, FLOOR), fill=(12, 16, 24), width=4)
    for x in (70, 540, 990):
        cone = Image.new('L', (W, H), 0); cd = ImageDraw.Draw(cone)
        cd.polygon([(x - 30, 0), (x + 30, 0), (x + 230, FLOOR), (x - 230, FLOOR)], fill=38)
        im.paste((200, 210, 255), (0, 0), cone.filter(ImageFilter.GaussianBlur(30)))
    d.rectangle((0, FLOOR, W, TXT0), fill=(12, 14, 20)); d.line((0, FLOOR, W, FLOOR), fill=(70, 80, 110), width=3)
    d.rectangle((0, TXT0, W, H), fill=(18, 17, 16))
    ht = halftone(); im.paste(ht, (0, 0), ht)
    d.rectangle((SX0 - 22, SY0 - 22, SX1 + 22, SY1 + 22), fill=(8, 8, 10))
    d.rectangle((SX0 - 22, SY0 - 22, SX1 + 22, SY1 + 22), outline=(90, 100, 130), width=4)
    d.rectangle((SX1 - 160, SY1 + 22, SX1 - 120, SY1 + 120), fill=(8, 8, 10))
    return im
BASE_OFF = studio(); BASE_ON = to_bw(studio(), auto=False)

def wrap(d, txt, f, maxw):
    out = []
    for para in txt.split('\n'):
        words, cur = para.split(), ''
        for w_ in words:
            tst = (cur + ' ' + w_).strip()
            if d.textlength(tst, font=f) <= maxw: cur = tst
            else: out.append(cur); cur = w_
        out.append(cur)
    return out

def fit_text(d, box, txt, font, maxsize, fill, align='center', lh=1.05, minsize=30):
    x0, y0, x1, y1 = box; size = maxsize
    while True:
        f = F(font, size); ls = wrap(d, txt, f, x1 - x0)
        if len(ls) * size * lh <= y1 - y0 or size <= minsize: break
        size -= 4
    y = (y0 + y1) / 2 - size * lh * (len(ls) - 1) / 2
    for l in ls:
        if align == 'center': d.text(((x0 + x1) / 2, y), l, font=f, fill=fill, anchor='mm')
        else: d.text((x0, y), l, font=f, fill=fill, anchor='lm')
        y += size * lh

def bug(d, txt, on, live=True):
    f = F(ARCH, 38); w = d.textlength(txt, font=f) + 50
    d.rectangle((40, 60, 40 + w, 128), fill=(255, 255, 255) if on else (190, 30, 30), outline=(0, 0, 0), width=4)
    d.text((40 + w / 2, 94), txt, font=f, fill=(0, 0, 0) if on else (255, 255, 255), anchor='mm')
    if live and not on:
        d.rectangle((40, 136, 160, 180), fill=(255, 255, 255)); d.text((100, 158), "LIVE", font=F(ARCH, 28), fill=(190, 30, 30), anchor='mm')

def mkstrip(txt, on):
    f = F(ARCH, 40)
    st = Image.new('RGBA', (6000, 60), (0, 0, 0, 0))
    ImageDraw.Draw(st).text((0, 30), txt.rstrip(), font=f, fill=(0, 0, 0) if on else (255, 255, 255), anchor='lm')
    xs = np.where(np.asarray(st)[..., 3].max(0) > 0)[0]
    return st.crop((0, 0, int(xs.max()) + 60, 60))

def ticker(im, t, strip, on):
    d = ImageDraw.Draw(im)
    d.rectangle((0, TK0, W, TK1), fill=(255, 255, 255) if on else (190, 30, 30))
    d.line((0, TK0, W, TK0), fill=(0, 0, 0), width=4); d.line((0, TK1, W, TK1), fill=(0, 0, 0), width=4)
    tw = strip.width; x = -int((t * 170) % tw)
    while x < W: im.paste(strip, (x, TK0 + 5), strip); x += tw

def jessie(im, n, age):
    k = min(1, age / 0.18); sc = 1.07 - 0.07 * k
    r = int(JR * sc); src = load(n).convert('RGB'); s_ = min(src.size)
    src = src.crop(((src.width - s_) // 2, (src.height - s_) // 2, (src.width + s_) // 2, (src.height + s_) // 2))
    face = src.resize((int(2 * r * 1.08), int(2 * r * 1.08)), Image.LANCZOS)
    off = (face.width - 2 * r) // 2; face = face.crop((off, off - 6, off + 2 * r, off + 2 * r - 6))
    m = Image.new('L', (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    d = ImageDraw.Draw(im); cx, cy = JC
    d.ellipse((cx - r - 30, cy - r - 20, cx + r + 30, cy + r + 40), fill=(0, 0, 0))
    d.ellipse((cx - r - 24, cy - r - 24, cx + r + 24, cy + r + 24), fill=(0, 0, 0))
    d.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), fill=(245, 240, 225))
    d.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), fill=(0, 0, 0))
    im.paste(face, (cx - r, cy - r), m)

# ---------- ransom note ----------
RF = [ANTON, ARCH, GF + 'cardo/Cardo-Bold.ttf', GF + 'crimsontext/CrimsonText-Bold.ttf', GF + 'firasans/FiraSans-Black.ttf',
      '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf',
      '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf']
PAL_OFF = [((250, 247, 235), (0, 0, 0)), ((255, 221, 60), (0, 0, 0)), ((200, 35, 35), (255, 255, 255)), ((20, 20, 20), (255, 255, 255)),
           ((90, 170, 225), (0, 0, 0)), ((235, 225, 200), (180, 30, 30)), ((255, 255, 255), (30, 60, 160))]
PAL_ON = [((255, 255, 255), (0, 0, 0)), ((0, 0, 0), (255, 255, 255)), ((225, 225, 225), (0, 0, 0))]
def piece(word, rng, on, scale):
    fp = ANTON if on and rng.random() < .5 else RF[rng.integers(len(RF))]
    size = int(rng.uniform(85, 175) * scale); f = F(fp, size)
    word_ = word if fp in (RF[2], RF[3]) else (word.upper() if rng.random() < .7 else word)
    pal = PAL_ON if on else PAL_OFF; paper, ink = pal[rng.integers(len(pal))]
    outline = rng.random() < .35; sw = max(3, size // 22) if outline else 0
    bb = f.getbbox(word_, stroke_width=sw); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    px, py = int(size * .18), int(size * .14); w, h = tw + 2 * px, th + 2 * py
    img = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    j = lambda: rng.uniform(-6, 6)
    poly = [(10 + j(), 10 + j()), (10 + w + j(), 10 + j()), (10 + w + j(), 10 + h + j()), (10 + j(), 10 + h + j())]
    d.polygon([(x + 5, y + 6) for x, y in poly], fill=(0, 0, 0, 120)); d.polygon(poly, fill=paper + (255,))
    if outline:
        fill_, stroke_ = (paper, ink) if rng.random() < .5 else (ink, (0, 0, 0) if ink != (0, 0, 0) else (255, 255, 255))
        d.text((10 + px - bb[0], 10 + py - bb[1]), word_, font=f, fill=fill_, stroke_width=sw, stroke_fill=stroke_)
    else:
        d.text((10 + px - bb[0], 10 + py - bb[1]), word_, font=f, fill=ink)
    return img.rotate(rng.uniform(-6, 6), resample=Image.BICUBIC, expand=True)
_rc = {}
def ransom_layout(txt, on):
    if (txt, on) in _rc: return _rc[(txt, on)]
    words = txt.split(); seed = sum(map(ord, txt)) + (7 if on else 0)
    for scale in [1, .9, .8, .72, .64, .56, .5, .44, .38]:
        rng = np.random.default_rng(seed); ps = [piece(w_, rng, on, scale) for w_ in words]
        rows, cur, cw = [], [], 0
        for p in ps:
            if cur and cw + p.width - 8 > W - 50: rows.append(cur); cur, cw = [], 0
            cur.append(p); cw += p.width - 8
        rows.append(cur); tot = sum(max(p.height for p in r) - 10 for r in rows)
        if tot <= H - TXT0 - 30: break
    pos = []; y = TXT0 + (H - TXT0 - tot) / 2
    for r in rows:
        rh = max(p.height for p in r) - 10; rw = sum(p.width - 8 for p in r); x = (W - rw) / 2
        for p in r: pos.append((p, int(x), int(y + (rh - p.height) / 2 + rng.uniform(-6, 6)))); x += p.width - 8
        y += rh
    _rc[(txt, on)] = pos; return pos
def ransom(im, txt, on, age, dur):
    pos = ransom_layout(txt, on); n = len(pos); span = max(0.25, min(dur - 0.4, 0.28 * n))
    for i, (p, x, y) in enumerate(pos):
        ta = span * i / n
        if age < ta: break
        k = min(1, (age - ta) / 0.1); sc = 1.25 - 0.25 * k
        q = p if k >= 1 else p.resize((max(1, int(p.width * sc)), max(1, int(p.height * sc))))
        im.paste(q, (x - (q.width - p.width) // 2, y - (q.height - p.height) // 2), q)

PAPER, BINK, BRED = (232, 225, 208), (20, 20, 15), (184, 50, 30)
def brand_plate(im, age):
    d = ImageDraw.Draw(im); d.rectangle((0, TXT0, W, H), fill=(18, 17, 16))
    k = min(1, age / 0.18); sc = 1.12 - 0.12 * k
    pw, ph = int(980 * sc), int(300 * sc); cx, cy = W // 2, (TXT0 + H) // 2
    x0, y0 = cx - pw // 2, cy - ph // 2
    d.rectangle((x0 + 12, y0 + 12, x0 + pw + 12, y0 + ph + 12), fill=(0, 0, 0))
    d.rectangle((x0, y0, x0 + pw, y0 + ph), fill=PAPER, outline=BINK, width=8)
    t = "BECAUSE EVERYTHING IS A PSY-OP"; fs = int(80 * sc)
    while d.textlength(t, font=F(ANTON, fs)) > pw - 60: fs -= 2
    d.text((cx, y0 + ph * .30), t, font=F(ANTON, fs), fill=BINK, anchor='mm')
    d.rectangle((x0 + 30, y0 + ph * .56, x0 + pw - 30, y0 + ph - 26), fill=BRED)
    d.text((cx, y0 + ph * .765), "BROBOTS.SPACE", font=F(ARCH, int(78 * sc)), fill=PAPER, anchor='mm')

def anaglyph(im, amt):
    r, g, b = im.split(); o = int(amt)
    r = r.transform(im.size, Image.AFFINE, (1, 0, -o, 0, 1, 0)); g = g.transform(im.size, Image.AFFINE, (1, 0, o, 0, 1, 0))
    b = b.transform(im.size, Image.AFFINE, (1, 0, o, 0, 1, 0)); return Image.merge('RGB', (r, g, b))

# ---------- timeline ----------
def rd(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels()).mean(1) if w.getnchannels() > 1 else x

def plan(segs, d):
    """segs: list of dicts {mode, audio:[(file, rel_t)], caps:[(rel_s, rel_e, text)], screen, figs, jessie:[(rel_t, pose)], pad}
    returns segments with absolute start/end and the flip times"""
    t = 0.4; out = []; flips = []
    for i, s in enumerate(segs):
        aud_end = max([at_ + len(rd(f'{d}/{f}.wav')) / SR for f, at_ in s['audio']] + [s.get('min', 0)])
        dur = aud_end + s.get('pad', 0.5)
        if i > 0 and segs[i - 1]['mode'] != s['mode']:
            flips.append((t, s['mode'])); t += 0.45 if s['mode'] == 'on' else 0.3
        s = dict(s, start=t, end=t + dur); out.append(s); t += dur
    return out, flips, t + 0.6

def render(segs, d, screens, tick_off, tick_on, bug_off, bug_on, out, music, music_off=0.0, still=None):
    segs, flips, TOTAL = plan(segs, d)
    strips = {False: mkstrip(tick_off, False), True: mkstrip(tick_on, True)}
    scr = {k: v() for k, v in screens.items()}
    def seg_at(t):
        cur = segs[0]
        for s in segs:
            if t >= s['start'] - 0.0001: cur = s
        return cur
    def flash_at(t):
        for ft, mode in flips:
            span = 0.65 if mode == 'on' else 0.35
            if ft - 0.1 <= t < ft + span: return (t - ft + 0.1) / (span + 0.1), mode, ft
        return None
    def frame(t):
        s = seg_at(t); on = s['mode'] == 'on'
        fl = flash_at(t)
        if fl and t < fl[2]: s_prev = [x for x in segs if x['end'] <= fl[2] + 0.001]; s = s_prev[-1] if s_prev else s; on = s['mode'] == 'on'
        rel = t - s['start']
        sk = s['screen'](rel) if callable(s['screen']) else s['screen']
        im = (BASE_ON if on else BASE_OFF).copy(); im.paste(scr[sk], (SX0, SY0))
        figs = s['figs'](rel) if callable(s['figs']) else s['figs']
        for f_ in figs:
            n, dx = f_[0], f_[1]; m = fig(n, bw=on, sc=f_[2] if len(f_) > 2 else 1.0); bob = 4 * math.sin(t * 3.1) if not on else 0
            im.paste(m, (W - m.width + 10 + dx, int(FLOOR + 22 - m.height + bob)), m)
        dr = ImageDraw.Draw(im); bug(dr, bug_on if on else bug_off, on)
        ticker(im, t, strips[on], on)
        js = [(a, p) for a, p in s['jessie'] if rel >= a]; ja, jp = js[-1] if js else s['jessie'][0]
        jessie(im, jp, rel - ja if s is not segs[0] or ja > 0 else 1)
        if s.get('brand') is not None and rel >= s['brand']:
            brand_plate(im, rel - s['brand'])
        else:
            for a, b, txt in s['caps']:
                if a <= rel < b: ransom(im, txt, on, rel - a, b - a)
        if fl:
            u, mode, ft = fl; amt = (40 if mode == 'on' else 26) * math.sin(max(0, min(1, u)) * math.pi)
            im = anaglyph(im, amt)
            if abs(t - ft) < 0.06 and mode == 'on': im = Image.blend(im, Image.new('RGB', (W, H), (255, 255, 255)), 0.75)
            jit = int((18 if mode == 'on' else 10) * math.sin(t * 90)); im = im.transform(im.size, Image.AFFINE, (1, 0, jit, 0, 1, 0))
        if t < 0.3: im = Image.blend(Image.new('RGB', (W, H)), im, t / 0.3)
        if t > TOTAL - 0.5: im = Image.blend(Image.new('RGB', (W, H)), im, max(0, (TOTAL - t) / 0.5))
        return im
    if still:
        for t in still: frame(t).save(f'still_{t}.jpg', quality=85)
        return segs, flips, TOTAL
    # audio
    N = int(TOTAL * SR); mix = np.zeros(N, np.float32); tt = np.arange(N) / SR
    mu = rd(music)[int(music_off * SR):]
    while len(mu) < N:
        xf = int(1.0 * SR); a = mu[-xf:] * np.linspace(1, 0, xf) + rd(music)[:xf] * np.linspace(0, 1, xf)
        mu = np.concatenate([mu[:-xf], a, rd(music)[xf:]])
    mu = mu[:N]; muf = sosfilt(butter(2, 500, 'low', fs=SR, output='sos'), mu) * 1.8
    onmask = np.zeros(N, bool)
    for s in segs:
        if s['mode'] == 'on': onmask[int(s['start'] * SR):int(s['end'] * SR)] = True
    for ft, mode in flips:
        if mode == 'on': onmask[int(ft * SR):int((ft + 0.45) * SR)] = True
    g = np.where(onmask, 0.40, 0.28) * np.clip(tt / 0.4, 0, 1) * np.clip((TOTAL - tt) / 0.8, 0, 1)
    mix += np.where(onmask, muf, mu) * g
    def put(at_, sig, gain=1.0):
        i = int(at_ * SR); mix[i:i + len(sig)] += sig[:max(0, N - i)] * gain
    for s in segs:
        for f, at_ in s['audio']:
            v = rd(f'{d}/{f}.wav'); act = v[np.abs(v) > 0.02]
            rms = np.sqrt((act ** 2).mean()) if len(act) else 0.1
            put(s['start'] + at_, np.tanh(v * (0.12 / rms) * 1.2) / 1.2)
    rng = np.random.default_rng(1)
    def lp(x, a):
        y = np.zeros_like(x); st = 0.0; a = np.broadcast_to(a, x.shape)
        for i in range(len(x)): st += a[i] * (x[i] - st); y[i] = st
        return y
    n = int(.03 * SR); click = rng.standard_normal(n) * np.exp(-np.arange(n) / 120); click -= lp(click, .3)
    for ft, mode in flips:
        put(ft - 0.05, click * .5); put(ft, click * .35)
        if mode == 'on':
            n = int(.5 * SR); x = rng.standard_normal(n).astype(np.float32); u = np.linspace(0, 1, n)
            rs = lp(x, 0.02 + 0.3 * u); rs *= u ** 2 * .25 / np.abs(rs).max(); put(ft - .45, rs)
            n = int(1.6 * SR); u = np.arange(n) / SR
            put(ft + 0.2, np.sin(2 * np.pi * (48 + 30 * np.exp(-u * 8)) * u) * np.exp(-u * 2.2) * .5 + np.sin(2 * np.pi * 110 * u) * .06 * np.exp(-u * 1.2))
        else:
            n = int(.35 * SR); x = rng.standard_normal(n).astype(np.float32); u = np.linspace(1, 0, n)
            ws = lp(x, 0.02 + 0.25 * u); ws *= np.sin(np.pi * (1 - u)) ** 2 * .12 / np.abs(ws).max(); put(ft - .1, ws)
    mix = np.tanh(mix * 1.1) / np.tanh(1.1); pk = np.abs(mix).max(); mix /= max(1, pk / 0.97)
    with wave.open(f'{d}/mix.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-i', f'{d}/mix.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    return segs, flips, TOTAL
