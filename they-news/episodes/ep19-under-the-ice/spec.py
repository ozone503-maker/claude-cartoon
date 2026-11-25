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
    rng = np.random.default_rng(19); T = "THE REVEAL\nIS THE BAIT"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

MONO = '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'
def leak(head, txt):
    def f():
        im, d = card((8, 18, 30))
        for k in range(0, sw, 40): d.line((k, 0, k, sh), fill=(20, 40, 70), width=1)
        for k in range(0, sh, 40): d.line((0, k, sw, k), fill=(20, 40, 70), width=1)
        pts = [(x, 330 + 60 * math.sin(x / 18) * math.sin(x / 140)) for x in range(0, X1 + 40, 4)]
        d.polygon([(0, 420)] + [(x, 380 - 50 * abs(math.sin(x / 60)) - 20 * math.sin(x / 13)) for x in range(0, X1 + 60, 6)] + [(X1 + 60, 420), (X1 + 60, sh), (0, sh)], fill=(210, 235, 250))
        d.rectangle((20, 20, 330, 70), fill=(200, 30, 30)); d.text((175, 45), head, font=F(ARCH, 30), fill=(255, 255, 255), anchor='mm')
        fit_text(d, (30, 90, X1 + 20, 270), txt, MONO, 60, (170, 220, 255), align='left', lh=1.1)
        d.text((30, 470), "SUBGLACIAL-FACILITIES-OPENED", font=F(MONO, 24), fill=(40, 70, 110), anchor='lm')
        return im
    return f
SCREENS = dict(l1=leak("TREATY EXPIRED", "THE ICE IS MELTING. WHAT'S UNDER IT ISN'T NATURAL."), l2=leak("1959-2026", "NEVER ABOUT SCIENCE."),
               l3=leak("GEOTHERMAL ANOMALY", "MELTING FROM BELOW. TECHNOLOGICAL."), l4=leak("WWII ENTRANCES", "SEALED. NOW OPENING."),
               l5=leak("SATELLITE", "LOOK TONIGHT. IT'S BEING EXPOSED."),
               a1=sign('LOOK SOUTH.', 'NOT AT US'), a2=sign('NEVER UNDER US.', 'THE SECRET IS ALWAYS UNDER SOMETHING'),
               a3=sign('SAME SCROLL.', 'NEW MYSTERY'), a4=sign('ALWAYS ABOUT TO.', 'ABOUT TO'),
               a5=sign('KEEP LOOKING.', 'TONIGHT NEVER COMES'), end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 2.4, "THE ANTARCTIC TREATY JUST EXPIRED."), (2.4, 4.1, "THE ICE IS MELTING,"), (4.1, 6.3, "AND WHAT'S UNDER IT ISN'T NATURAL.")], .3), jessie=[(0, N + '01'), (5.3, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(AM + '14', 0)], pad=0.3, min=2.8,
      caps=sh_([(0, 1.2, "LOOK SOUTH."), (1.2, 2.5, "NOT AT US.")], .1), jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 2.3, "THE TREATY WAS NEVER ABOUT SCIENCE."), (2.3, 4.8, "IT WAS ABOUT HIDING WHAT IS UNDER THE ICE.")], .1), jessie=[(0, N + '05'), (3.9, L + '04')]),
 dict(mode='on', screen='a2', audio=[('a2', .1)], figs=[(AM + '10', 0)], pad=0.3,
      caps=sh_([(0, 2.6, "THE SECRET IS ALWAYS UNDER SOMETHING."), (2.6, 4.3, "NEVER UNDER US.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 2.2, "THE ICE IS MELTING FROM BELOW."), (2.2, 4.7, "THE HEAT SOURCE IS NOT NATURAL."), (4.7, 6.1, "IT IS TECHNOLOGICAL.")], .1), jessie=[(0, N + '07'), (5.1, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(AM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.2, "NEW MYSTERY."), (1.2, 3.3, "SAME SCROLL.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 3.0, "THE SEALED ENTRANCES, BUILT DURING WORLD WAR TWO,"), (3.0, 4.3, "ARE BEING OPENED."), (4.3, 7.2, "THE WORLD IS ABOUT TO SEE WHAT WAS KEPT HIDDEN.")], .1),
      jessie=[(0, N + '02'), (6.2, L + '07')]),
 dict(mode='on', screen='a4', audio=[('a4', .1)], figs=[(AM + '14', 0)], pad=0.3, min=2.8,
      caps=sh_([(0, 1.1, "ABOUT TO."), (1.1, 2.6, "ALWAYS ABOUT TO.")], .1), jessie=[(0, C + '02')]),
 dict(mode='off', screen='l5', audio=[('l5', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 2.1, "LOOK AT THE SATELLITE IMAGES TONIGHT."), (2.1, 4.4, "THE COVER-UP IS NOT ENDING."), (4.4, 6.4, "IT IS BEING EXPOSED.")], .1),
      jessie=[(0, N + '03'), (5.4, L + '03')]),
 dict(mode='on', screen='a5', audio=[('a5', .1)], figs=[(AM + '10', 0)], min=3.2,
      caps=sh_([(0, 1.9, "TONIGHT NEVER COMES."), (1.9, 2.9, "KEEP LOOKING.")], .1), jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "THE REVEAL IS THE BAIT.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "ANTARCTIC-TREATY-EXPIRED  \u2022  65-YEAR-COVER-UP-OVER  \u2022  SUBGLACIAL-FACILITIES-OPENED  \u2022  ICE-MELT-ACCELERATED  \u2022  "
TICK_ON = "LOOK SOUTH  \u2022  NOT AT US  \u2022  SAME SCROLL  \u2022  ALWAYS ABOUT TO  \u2022  KEEP LOOKING  \u2022  OBEY  \u2022  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
