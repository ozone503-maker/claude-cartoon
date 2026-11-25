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
def aura(txt):
    def f():
        im, d = card(DEEP)
        for r in range(260, 20, -12):
            c = int(60 + (260 - r) * .7); d.ellipse((230 - r, 280 - r, 230 + r, 280 + r), fill=(c + 60, int(c * .8) + 30, 40))
        rng = np.random.default_rng(len(txt))
        for _ in range(30):
            x, y, r = rng.uniform(0, sw), rng.uniform(0, sh), rng.uniform(2, 6); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 240, 180))
        fit_text(d, (40, 40, X1 - 20, 500), txt, SERIF, 90, (255, 248, 225), lh=1.1)
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
    rng = np.random.default_rng(18); T = "BUILD YOUR\nOWN ARK"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

PARCH, BROWN = (232, 214, 170), (90, 60, 30)
def scroll(head, txt):
    def f():
        im, d = card(PARCH)
        cx, cy, r = 150, 300, 115
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(180, 200, 210), outline=BROWN, width=5)
        for k in range(-2, 3): d.arc((cx - r, cy - r + k * 10, cx + r, cy + r - k * 10), 0, 360, fill=BROWN)
        d.line((cx - r, cy, cx + r, cy), fill=BROWN, width=3); d.line((cx, cy - r, cx, cy + r), fill=BROWN, width=3)
        d.polygon([(cx + r + 10, cy - 40), (cx + r + 50, cy), (cx + r + 10, cy + 40)], fill=(170, 40, 30))
        d.text((30, 40), head, font=F(SERIF, 40), fill=(150, 30, 20), anchor='lm')
        if txt == 'REDACT':
            for k, w in enumerate([300, 220, 340, 180, 280]): d.rectangle((340, 110 + k * 70, 340 + min(w, X1 - 300), 150 + k * 70), fill=(10, 10, 10))
        else: fit_text(d, (330, 80, X1 - 50, 470), txt, SERIF, 64, BROWN, align='left', lh=1.1)
        return im
    return f
SCREENS = dict(l1=scroll("EARTH CRUST DISPLACEMENT", "The whole crust slides. Like orange skin."), l2=scroll("FOREWORD: A. EINSTEIN", "\u201cOriginal. Worth serious investigation.\u201d"),
               l3=scroll("CLASSIFIED / RELEASED 2013", "REDACT"), l4=scroll("EVERY ~6,500 YEARS", "Noah 6,500 years ago. Adam and Eve 11,500. Next?"),
               l5=scroll("HERODOTUS, 450 BC", "\u201cTwice he rose where he now sets.\u201d"),
               a1=sign('THEY KNOW THE DATE.', 'YOU KNOW THE WEATHER'), a2=sign('STOPPED IN PUBLIC.', 'CONTINUED IN PRIVATE'),
               a3=sign('REDACTED = ACCURATE.', 'READ THE BLACK BARS'), a4=sign('THEY BUILT BUNKERS.', 'YOU BUILT CREDIT'),
               a5=sign('SEAT NOT RESERVED.', 'THE RESET IS SCHEDULED'), end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 4.5, "EVERY FEW THOUSAND YEARS, EARTH'S ENTIRE CRUST SLIDES OVER THE MANTLE,"), (4.5, 6.3, "LIKE THE LOOSE SKIN OF AN ORANGE.")], .3), jessie=[(0, N + '01'), (5.4, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(AM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.7, "THEY KNOW THE DATE."), (1.7, 3.2, "YOU KNOW THE WEATHER.")], .1), jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RW + '10', 0)], pad=0.3,
      caps=sh_([(0, 2.0, "EINSTEIN WROTE THE FOREWORD."), (2.0, 5.5, "HE CALLED IT ORIGINAL, AND WORTH SERIOUS INVESTIGATION.")], .1),
      jessie=[(0, N + '05'), (4.6, L + '04')]),
 dict(mode='on', screen='a2', audio=[('a2', .1)], figs=[(AM + '09', 0)], pad=0.3, min=2.8,
      caps=sh_([(0, 2.3, "SO WE STOPPED INVESTIGATING IN PUBLIC.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 3.5, "THEN THE CIA CLASSIFIED CHAN THOMAS'S BOOK."), (3.5, 7.6, "IT WAS RELEASED IN 2013, HEAVILY REDACTED.")], .1),
      jessie=[(0, N + '07'), (6.6, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(AM + '10', 0)], pad=0.3, min=2.8,
      caps=sh_([(0, 2.0, "REDACTED MEANS ACCURATE.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RW + '13', 0)], pad=0.3,
      caps=sh_([(0, 1.0, "HIS CLAIM:"), (1.0, 3.3, "THE SLIP TAKES HOURS, NOT MILLENNIA."), (3.3, 8.4, "AND IT COMES BACK EVERY 6,500 YEARS.")], .1),
      jessie=[(0, N + '02'), (7.2, L + '07')]),
 dict(mode='on', screen='a4', audio=[('a4', .1)], figs=[(AM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.9, "WE BUILT BUNKERS."), (1.9, 3.4, "YOU BUILT CREDIT.")], .1), jessie=[(0, C + '02')]),
 dict(mode='off', screen='l5', audio=[('l5', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 2.2, "EGYPTIAN PRIESTS TOLD HERODOTUS,"), (2.2, 5.3, "TWICE THE SUN ROSE WHERE IT NOW SETS."), (5.3, 9.9, "THERE HAVE BEEN, AND WILL BE AGAIN, MANY DESTRUCTIONS OF MANKIND.")], .1),
      jessie=[(0, N + '03'), (8.8, L + '03')]),
 dict(mode='on', screen='a5', audio=[('a5', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0, 1.9, "THE RESET IS SCHEDULED."), (1.9, 4.3, "YOUR SEAT IS NOT RESERVED.")], .1), jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "BUILD YOUR OWN ARK.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "EARTH CRUST DISPLACEMENT  \u2022  EINSTEIN FOREWORD  \u2022  CIA CLASSIFIED  \u2022  EVERY 6,500 YEARS  \u2022  ATLANTIS  \u2022  "
TICK_ON = "THEY KNOW THE DATE  \u2022  REDACTED MEANS ACCURATE  \u2022  BUNKERS FOR US  \u2022  SEAT NOT RESERVED  \u2022  OBEY  \u2022  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
