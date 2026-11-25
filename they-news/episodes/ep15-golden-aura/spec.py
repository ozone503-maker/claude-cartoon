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
    rng = np.random.default_rng(15); T = "EGO IS\nTHE LEASH"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(l1=aura("Chosen being, you have a golden aura."), l2=aura("People are addicted to you, but intimidated."),
               l3=aura("There's POWER in your presence."), l4=aura("You beat death. You glow differently."),
               l5=aura("Those on the outside are offended."),
               a1=sign('YOU ARE SPECIAL.', 'KEEP SCROLLING'), a2=sign('ONLY THIS POST GETS YOU.', 'NOBODY ELSE'),
               a3=sign('FEEL POWERFUL.', 'CHANGE NOTHING'), a4=sign('SUFFERING IS YOUR BRAND.', 'WEAR IT'),
               a5=sign('TRUST NO ONE.', 'THEY ARE BENEATH YOU'), end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RW + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.1, "CHOSEN BEING."), (1.1, 3.4, "YOU HAVE A GOLDEN AURA.")], .3), jessie=[(0, N + '01'), (2.6, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(AM + '14', 0)], pad=0.3, min=2.8,
      caps=sh_([(0, 1.1, "YOU ARE SPECIAL."), (1.1, 2.5, "KEEP SCROLLING.")], .1), jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RW + '13', 0)], pad=0.3,
      caps=sh_([(0, 2.4, "THE REASON PEOPLE ARE ADDICTED TO YOU,"), (2.4, 4.4, "BUT INTIMIDATED AT THE SAME TIME,"), (4.4, 7.9, "IS BECAUSE THE TRUTH ABOUT WHO YOU ARE SPEAKS FOR ITSELF.")], .1),
      jessie=[(0, N + '05'), (7.0, L + '04')]),
 dict(mode='on', screen='a2', audio=[('a2', .1)], figs=[(AM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.9, "NOBODY UNDERSTANDS YOU."), (1.9, 4.1, "ONLY THIS POST.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RW + '10', 0)], pad=0.3, min=3.6,
      caps=sh_([(0, 3.3, "THERE'S POWER IN YOUR PRESENCE THAT CAN'T BE IGNORED.")], .1), jessie=[(0, N + '07'), (2.6, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(AM + '10', 0)], pad=0.3, min=3.0,
      caps=sh_([(0, 1.3, "FEEL POWERFUL."), (1.3, 2.7, "CHANGE NOTHING.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RW + '13', 0)], pad=0.3,
      caps=sh_([(0, 2.5, "YOU'VE LIVED THROUGH HUMILIATION RITUALS."), (2.5, 4.4, "CLIMBED OUT OF DARK SPACES."), (4.4, 5.5, "BEAT DEATH."), (5.5, 7.2, "YOU GLOW DIFFERENTLY.")], .1),
      jessie=[(0, N + '02'), (6.3, L + '07')]),
 dict(mode='on', screen='a4', audio=[('a4', .1)], figs=[(AM + '14', 0)], pad=0.3,
      caps=sh_([(0, 2.7, "YOUR SUFFERING IS YOUR BRAND."), (2.7, 3.6, "WEAR IT.")], .1), jessie=[(0, C + '02')]),
 dict(mode='off', screen='l5', audio=[('l5', .1)], figs=[(RW + '10', 0)], pad=0.3,
      caps=sh_([(0, 2.1, "THOSE WHO CAN RELATE RESPECT IT."), (2.1, 5.9, "AND THOSE ON THE OUTSIDE ARE THE ONES WHO ARE OFFENDED.")], .1),
      jessie=[(0, N + '03'), (5.0, L + '03')]),
 dict(mode='on', screen='a5', audio=[('a5', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0, 2.4, "ANYONE WHO DISAGREES IS BENEATH YOU."), (2.4, 4.0, "TRUST NO ONE.")], .1), jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "EGO IS THE LEASH.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "CHOSEN BEING  •  GOLDEN AURA  •  POWER IN YOUR PRESENCE  •  YOU GLOW DIFFERENTLY  •  THEY'RE JUST OFFENDED  •  "
TICK_ON = "YOU ARE SPECIAL  •  KEEP SCROLLING  •  FEEL POWERFUL  •  CHANGE NOTHING  •  TRUST NO ONE  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
