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
def cat(d, cx, cy, s, col, eye):
    d.ellipse((cx - 70 * s, cy - 10 * s, cx + 70 * s, cy + 110 * s), fill=col)
    d.ellipse((cx - 50 * s, cy - 100 * s, cx + 50 * s, cy), fill=col)
    d.polygon([(cx - 48 * s, cy - 70 * s), (cx - 40 * s, cy - 135 * s), (cx - 10 * s, cy - 95 * s)], fill=col)
    d.polygon([(cx + 48 * s, cy - 70 * s), (cx + 40 * s, cy - 135 * s), (cx + 10 * s, cy - 95 * s)], fill=col)
    d.arc((cx + 30 * s, cy + 20 * s, cx + 150 * s, cy + 130 * s), 180, 330, fill=col, width=int(18 * s))
    for ex in (-20, 20): d.ellipse((cx + (ex - 9) * s, cy - 62 * s, cx + (ex + 9) * s, cy - 44 * s), fill=eye)
def catcard(title, bg):
    def f():
        im, d = card(bg)
        for r in range(220, 60, -16):
            c = tuple(min(255, int(v + (220 - r) * .5)) for v in bg); d.ellipse((230 - r, 370 - r, 230 + r, 370 + r), fill=c)
        cat(d, 230, 370, 1.15, (30, 25, 35), (250, 220, 90))
        fit_text(d, (30, 25, X1 + 40, 175), title, SERIF, 80, (60, 30, 70), lh=1.05)
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
    rng = np.random.default_rng(21); T = "GET A\nCAT"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(l1=catcard("Living frequencies of love.", (240, 215, 240)), l2=catcard("A portable vortex.", (215, 225, 250)),
               l3=catcard("They absorb your grief.", (250, 225, 210)), l4=catcard("Sacred protection.", (220, 245, 225)),
               l5=catcard("An energetic shield.", (250, 240, 200)),
               a1=sign('THE CAT IS A PEST.', 'FEAR IS OUR CROP'), a2=sign('25 Hz JAMS OUR SIGNAL.', 'THEY PURR AT IT'),
               a3=sign('THEY EAT WHAT WE PLANT.', 'EVERY NIGHT'), a4=sign('NO PETS ALLOWED.', 'WHY WE INVENTED THE LANDLORD'),
               a5=sign('WATCH WHERE THEY STARE.', 'THEY ALWAYS SAW US'), end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 4.2, "CATS ARRIVE AS LIVING FREQUENCIES OF UNCONDITIONAL LOVE,"), (4.2, 7.8, "INCARNATING TO DISSOLVE THE DENSE VIBRATION OF FEAR"), (7.8, 9.9, "THAT KEEPS THE HUMAN HEART CLOSED.")], .3),
      jessie=[(0, N + '01'), (8.8, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(AM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.4, "FEAR IS OUR CROP."), (1.4, 2.9, "THE CAT IS A PEST.")], .1), jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 3.8, "A CAT IS A PORTABLE VORTEX OF PURE RECEPTIVITY."), (3.8, 4.8, "SOFT."), (4.8, 5.8, "MAGNETIC."), (5.8, 6.8, "UNFORCED.")], .1),
      jessie=[(0, N + '05'), (5.7, L + '04')]),
 dict(mode='on', screen='a2', audio=[('a2', .1)], figs=[(AM + '10', 0)], pad=0.3,
      caps=sh_([(0, 2.0, "THEY PURR AT 25 HERTZ."), (2.0, 3.5, "IT JAMS OUR SIGNAL.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 3.2, "THEY ABSORB THE DENSE RESIDUES OF GRIEF, ANXIETY AND PAIN,"), (3.2, 7.1, "AND TRANSMUTE THEM THROUGH THEIR OWN BODIES,"), (7.1, 8.5, "SO YOU CAN FEEL LIGHTER.")], .1),
      jessie=[(0, N + '07'), (7.4, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(AM + '09', 0)], pad=0.3,
      caps=sh_([(0, 2.2, "THEY EAT WHAT WE PLANT IN YOU."), (2.2, 3.3, "EVERY NIGHT.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.2, "IN RARE CASES,"), (1.2, 3.7, "A CAT MAY CONSCIOUSLY TAKE ON ILLNESS,"), (3.7, 5.8, "AS AN ACT OF SACRED PROTECTION.")], .1),
      jessie=[(0, N + '02'), (4.8, L + '07')]),
 dict(mode='on', screen='a4', audio=[('a4', .1)], figs=[(AM + '14', 0)], pad=0.3,
      caps=sh_([(0, 2.5, "THAT'S WHY WE INVENTED THE LANDLORD."), (2.5, 4.0, "NO PETS ALLOWED.")], .1), jessie=[(0, C + '02')]),
 dict(mode='off', screen='l5', audio=[('l5', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 3.3, "THEIR LOVE WEAVES AN ENERGETIC SHIELD AROUND THE HOME,"), (3.3, 5.8, "FILTERING LOWER VIBRATIONAL INTERFERENCE.")], .1),
      jessie=[(0, N + '03'), (4.8, L + '03')]),
 dict(mode='on', screen='a5', audio=[('a5', .1)], figs=[(AM + '10', 0)],
      caps=sh_([(0, 1.2, "THEY SEE US."), (1.2, 3.0, "THEY ALWAYS SAW US."), (3.0, 4.6, "WATCH WHERE THEY STARE.")], .1), jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "GET A CAT.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "LIVING FREQUENCIES OF LOVE  \u2022  PORTABLE VORTEX  \u2022  SUBTLE-BODY ALCHEMISTS  \u2022  SACRED PROTECTION  \u2022  ENERGETIC SHIELD  \u2022  "
TICK_ON = "FEAR IS OUR CROP  \u2022  25 HZ JAMS OUR SIGNAL  \u2022  NO PETS ALLOWED  \u2022  WATCH WHERE THEY STARE  \u2022  OBEY  \u2022  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
