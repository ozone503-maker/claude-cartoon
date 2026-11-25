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
    rng = np.random.default_rng(17); T = "NOBODY'S\nCOMING"; fs = 160; f = F(ANTON, fs)
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
        im, d = card((8, 18, 12))
        for k in range(0, sw, 40): d.line((k, 0, k, sh), fill=(16, 40, 24), width=1)
        for k in range(0, sh, 40): d.line((0, k, sw, k), fill=(16, 40, 24), width=1)
        pts = [(x, 330 + 60 * math.sin(x / 18) * math.sin(x / 140)) for x in range(0, X1 + 40, 4)]
        d.line(pts, fill=(80, 255, 120), width=4)
        d.rectangle((20, 20, 330, 70), fill=(200, 30, 30)); d.text((175, 45), head, font=F(ARCH, 30), fill=(255, 255, 255), anchor='mm')
        fit_text(d, (30, 90, X1 + 20, 270), txt, MONO, 60, (140, 255, 160), align='left', lh=1.1)
        d.text((30, 470), "URBAN-HIVE / 14HZ-FENCE", font=F(MONO, 26), fill=(80, 200, 100), anchor='lm')
        return im
    return f
SCREENS = dict(l1=leak("CLASSIFIED", "EVERY MAJOR CITY HAS A FREQUENCY FENCE."), l2=leak("CLASSIFIED", "IT'S NOT THE AIR. IT'S THE FENCE."),
               l3=leak("SCHEMATIC", "7.4 GHz FIELD. 14 Hz PULSE. FEAR ON TAP."), l4=leak("NYC-DOWN", "TUESDAY 3 AM. ALLIANCE SIGNAL TEAMS."),
               l5=leak("33-REMAINING", "60 DAYS. ONE CITY AT A TIME. SHARE THIS."),
               a1=sign('SAME LEASH.', 'NEW STORY'), a2=sign('WE HOLD THE SWITCH.', 'YOUR FEAR HAS ONE'),
               a3=sign('CONSUME. OBEY.', 'AFRAID PEOPLE DO BOTH'), a4=sign('STAY SEATED.', 'SOMEONE ELSE WILL SAVE YOU'),
               a5=sign('DO NOTHING.', 'TRUST THE PLAN. WAIT FOR THE NEXT DROP'), end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 2.7, "EVERY MAJOR CITY HAS A FREQUENCY FENCE."), (2.7, 4.9, "THEY JUST TURNED OFF NEW YORK'S.")], .3), jessie=[(0, N + '01'), (4.0, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(AM + '14', 0)], pad=0.3, min=2.8,
      caps=sh_([(0, 1.2, "NEW STORY."), (1.2, 2.5, "SAME LEASH.")], .1), jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 2.0, "YOU FEEL DIFFERENT WHEN YOU LEAVE THE CITY."), (2.0, 3.3, "IT'S NOT THE AIR."), (3.3, 4.8, "IT'S THE FREQUENCY FENCE.")], .1),
      jessie=[(0, N + '05'), (3.9, L + '04')]),
 dict(mode='on', screen='a2', audio=[('a2', .1)], figs=[(AM + '09', 0)], pad=0.3,
      caps=sh_([(0, 2.0, "YOUR FEAR HAS A SWITCH."), (2.0, 4.0, "WE HOLD IT.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.6, "A 14 HERTZ PULSE"), (1.6, 4.2, "KEEPS YOUR FEAR CENTER PRODUCING CORTISOL."), (4.2, 5.4, "WITHOUT CAUSE."), (5.4, 6.6, "WITHOUT THREAT."), (6.6, 7.6, "WITHOUT REASON.")], .1),
      jessie=[(0, N + '07'), (6.6, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(AM + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.8, "AFRAID PEOPLE CONSUME."), (1.8, 3.4, "AFRAID PEOPLE OBEY.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 2.4, "NEW YORK'S FENCE WAS SHUT DOWN TUESDAY AT 3 AM,"), (2.4, 4.5, "BY ALLIANCE SIGNAL TEAMS.")], .1),
      jessie=[(0, N + '02'), (3.6, L + '07')]),
 dict(mode='on', screen='a4', audio=[('a4', .1)], figs=[(AM + '14', 0)], pad=0.3, min=3.2,
      caps=sh_([(0, 1.6, "SOMEONE ELSE WILL SAVE YOU."), (1.6, 3.1, "STAY SEATED.")], .1), jessie=[(0, C + '02')]),
 dict(mode='off', screen='l5', audio=[('l5', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.9, "33 CITIES REMAIN."), (1.9, 5.8, "EACH ONE SCHEDULED FOR DEACTIVATION OVER THE NEXT 60 DAYS."), (5.8, 7.1, "SHARE THIS.")], .1),
      jessie=[(0, N + '03'), (6.0, L + '03')]),
 dict(mode='on', screen='a5', audio=[('a5', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0, 1.9, "WAIT FOR THE NEXT DROP."), (1.9, 3.3, "TRUST THE PLAN."), (3.3, 5.8, "DO NOTHING.")], .1), jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "NOBODY'S COMING.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "CODE: URBAN-HIVE  \u2022  14HZ-FENCE  \u2022  NYC-DOWN  \u2022  33-REMAINING  \u2022  FEEL THE DIFFERENCE  \u2022  "
TICK_ON = "SAME LEASH  \u2022  WE HOLD THE SWITCH  \u2022  CONSUME  \u2022  OBEY  \u2022  STAY SEATED  \u2022  DO NOTHING  \u2022  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
