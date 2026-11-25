import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
INK, GREY = (12, 12, 12), (235, 235, 235)
GOLD, DEEP = (240, 195, 70), (40, 25, 60)
SERIF = GF + 'cardo/Cardo-Bold.ttf'
X1 = sw - 170
def card(bg):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)
FLY = Image.open('flyer.png').convert('RGB'); VEN = Image.open('venmo.jpg').convert('RGB')
def k(b): f = FLY.width / 1659; return tuple(int(v * f) for v in b)
def panel(box, cap=None):
    def f():
        im, d = card(GREY); src = FLY.crop(box)
        r = min((sw - 30) / src.width, (sh - 30) / src.height); p = src.resize((int(src.width * r), int(src.height * r)), Image.LANCZOS)
        x = (sw - p.width) // 2; im.paste(p, (x, 15)); return im
    return f
def item(box, name, old, new, extra=None):
    def f():
        im, d = card((236, 228, 210)); src = FLY.crop(box)
        r = min(250 / src.width, (sh - 40) / src.height); p = src.resize((int(src.width * r), int(src.height * r)), Image.LANCZOS)
        im.paste(p, (15, (sh - p.height) // 2))
        x0, x1 = 280, X1 + 10
        fit_text(d, (x0, 20, x1, 170), name, ANTON, 70, INK, lh=.95)
        f2 = F(ANTON, 54); w = d.textlength(old, font=f2); cx = (x0 + x1) / 2
        d.text((cx, 205), old, font=f2, fill=(110, 100, 90), anchor='mm'); d.line((cx - w / 2 - 6, 205, cx + w / 2 + 6, 205), fill=(190, 30, 30), width=7)
        fit_text(d, (x0, 240, x1, 400), new, ANTON, 170, INK)
        if extra: fit_text(d, (x0, 410, x1, 500), extra, ARCH, 40, INK)
        return im
    return f
def pricelist():
    im, d = card((236, 228, 210))
    fit_text(d, (20, 10, X1 + 40, 80), "EVERYTHING HALF PRICE", ANTON, 70, INK)
    rows = [("CUSTOM CHATBOT", "$240"), ("BASIC WEBSITE", "$240"), ("COMMERCIALS / MIN", "$120"), ("DIGITAL WALLETS", "$480"),
            ("AGENTIC STOREFRONTS", "$680"), ("CRYPTO INTEGRATION", "$1,220"), ("BATTLE STATION", "$2,480")]
    for k2, (a, b) in enumerate(rows):
        y = 105 + k2 * 52; d.text((25, y), a, font=F(ARCH, 27), fill=INK, anchor='lm'); d.text((X1 + 35, y), b, font=F(ANTON, 42), fill=INK, anchor='rm')
        d.line((25, y + 24, X1 + 35, y + 24), fill=(180, 170, 150), width=2)
    d.rectangle((20, 478, X1 + 40, 535), fill=INK); d.text(((X1 + 60) / 2, 506), "FINANCING AVAILABLE", font=F(ANTON, 40), fill=(236, 228, 210), anchor='mm')
    return im
def proof():
    im, d = card(GREY)
    fit_text(d, (20, 20, X1 + 40, 120), "REAL CUSTOMER. REAL MONEY.", ANTON, 80, INK)
    src = VEN.crop((30, 1020, 1079, 1200)); r = (X1 + 20) / src.width; p = src.resize((int(src.width * r), int(src.height * r)), Image.LANCZOS)
    im.paste(p, (20, 170)); d.rectangle((16, 166, 24 + p.width, 174 + p.height), outline=INK, width=5)
    fit_text(d, (20, 330, X1 + 30, 470), "BROBOTS.SPACE", ANTON, 100, INK)
    return im
def hype(top, mid, bot, bg, fg):
    def f():
        im, d = card(bg)
        for k2 in range(14):
            a = math.radians(k2 * 360 / 14); d.polygon([(230, 290), (230 + 600 * math.cos(a), 290 + 600 * math.sin(a)), (230 + 600 * math.cos(a + .2), 290 + 600 * math.sin(a + .2))], fill=tuple(min(255, c + 30) for c in bg))
        fit_text(d, (20, 20, X1 + 40, 130), top, ANTON, 110, fg)
        fit_text(d, (20, 150, X1 + 40, 380), mid, ANTON, 200, (255, 255, 255))
        fit_text(d, (20, 390, X1 + 40, 500), bot, ANTON, 90, fg)
        return im
    return f
def sign(main, sub):
    def f():
        im, d = card(GREY)
        fit_text(d, (30, 40, X1 + 40, 390), main, ANTON, 200, INK, lh=0.95)
        fit_text(d, (30, 410, X1 + 20, 500), sub, ARCH, 40, INK)
        return im
    return f
def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(22); T = "INVEST IN\nYOURSELF"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(l1=hype("DOORBUSTER!", '85" TV', "40% OFF! NO ROOM? NO PROBLEM!", (200, 20, 20), (255, 230, 0)),
               l2=hype("AIR FRYERS!", "MYSTERY BOX", "BUY NOW, PAY LATER!", (230, 120, 0), (255, 255, 120)),
               l3=hype("MIDNIGHT!", "LAST ONE!", "FIGHT FOR IT!", (20, 60, 200), (255, 230, 0)),
               l4=hype("EVERYTHING", "MUST GO!", "CREDIT CARD READY!", (200, 20, 120), (255, 230, 0)),
               a1=panel((0, 0, 1728, 2304)), a2a=item((0, 600, 400, 1140), "CUSTOM CHATBOT", "$480", "$240", "50% OFF"),
               a2b=item((928, 1248, 1380, 1600), "BASIC WEBSITE", "$480", "$240", "50% OFF"),
               a3=item((32, 1700, 440, 2120), "CUSTOM COMMERCIAL", "$220", "$120", "FIRST MINUTE. $60 EACH AFTER"),
               a4=pricelist, proof=proof,
               end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.5, "BLACK FRIDAY!"), (1.5, 3.1, "DOORBUSTERS!"), (3.1, 6.6, "AN 85-INCH TV YOU DON'T HAVE ROOM FOR,"), (6.6, 8.6, "40% OFF!")], .3),
      jessie=[(0, N + '01'), (7.6, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.25, "INVEST IN YOURSELF."), (1.25, 2.4, "NOT IN A TV.")], .1), min=3.0, jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.0, "AIR FRYERS!"), (1.0, 2.5, "MASSAGE GUNS!"), (2.5, 3.9, "MYSTERY BOXES!"), (3.9, 5.8, "BUY NOW, PAY LATER!")], .1),
      jessie=[(0, N + '05'), (4.8, L + '04')]),
 dict(mode='on', screen=lambda r: 'a2a' if r < 4.6 else 'a2b', audio=[('a2', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.7, "BUILD A BETTER BUSINESS."), (1.7, 4.6, "A CUSTOM CHATBOT, $240."), (4.6, 7.5, "A WEBSITE, $240.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.4, "LINE UP AT MIDNIGHT!"), (1.4, 3.0, "FIGHT FOR THE LAST ONE!"), (3.0, 4.5, "IT'S GOING FAST!")], .1),
      jessie=[(0, N + '07'), (3.5, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 2.7, "YOUR OWN COMMERCIAL, THAT LOOKS JUST LIKE YOU."), (2.7, 5.1, "$120 FOR THE FIRST MINUTE.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.6, "EVERYTHING MUST GO!"), (1.6, 3.8, "GET YOUR CREDIT CARD READY!")], .1),
      jessie=[(0, N + '02'), (2.8, L + '07')]),
 dict(mode='on', screen=lambda r: 'a4' if r < 6.4 else 'proof', audio=[('a4', .1)], figs=[(RM + '14', 0)], min=9.4,
      caps=sh_([(0, 3.0, "TAKE ADVANTAGE OF THE OPPORTUNITY TO GROW YOUR VALUE."), (3.0, 4.6, "EVERYTHING IS HALF PRICE."), (4.6, 6.1, "FINANCING AVAILABLE."), (6.3, 9.2, "REAL CUSTOMER. REAL MONEY.")], .1),
      jessie=[(0, C + '02')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "INVEST IN YOURSELF.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "DOORBUSTERS  \u2022  85-INCH TV  \u2022  AIR FRYERS  \u2022  BUY NOW PAY LATER  \u2022  EVERYTHING MUST GO  \u2022  LINE UP AT MIDNIGHT  \u2022  "
TICK_ON = "BROBOTS SPACE FACTORY  \u2022  BLACK FRIDAY  \u2022  EVERYTHING HALF PRICE  \u2022  FINANCING AVAILABLE  \u2022  BROBOTS.SPACE  \u2022  CHATBOTS $240  \u2022  WEBSITES $240  \u2022  COMMERCIALS $120  \u2022  BATTLE STATION $2,480  \u2022  "

TEMPO = 1.25
for _s in SEGS[:-1]:
    if isinstance(_s.get('caps'), list): _s['caps'] = [(x / TEMPO, y / TEMPO, t) for x, y, t in _s['caps']]
    if 'jessie' in _s: _s['jessie'] = [(x / TEMPO, p) for x, p in _s['jessie']]
    if 'min' in _s: _s['min'] = _s['min'] / TEMPO
    _s['pad'] = 0.1
    if callable(_s.get('screen')):
        _f = _s['screen']; _s['screen'] = (lambda f: lambda r: f(r * TEMPO))(_f)

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THE TRUTH', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
