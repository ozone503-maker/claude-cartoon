import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
INK, GREY = (12, 12, 12), (235, 235, 235)
GOLD, DEEP = (240, 195, 70), (70, 15, 15)
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
    rng = np.random.default_rng(16); T = "THE CROWD\nIS FAKE"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(l1=aura("Targeted individual. Secret crowds are watching."), l2=aura("No court. No cop. You fear no one."),
               l3=aura("Your protection defies logic."), l4=aura("Are you even human now?"),
               l5=aura("Burn down the corruption. Deliver their endings."),
               a1=sign('EVERYONE IS WATCHING.', 'STAY AFRAID. STAY ONLINE'), a2=sign('TRUST NO ONE.', 'ANSWER ONLY TO THE FEED'),
               a3=sign('BELIEVE THE SIGNS.', 'IGNORE THE EVIDENCE'), a4=sign('LEAVE THEM BEHIND.', "YOU'RE NOT LIKE THEM"),
               a5=sign('SNAP.', "WE'LL BE WATCHING"), end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.9, "TARGETED INDIVIDUAL."), (1.9, 5.5, "YOU'RE ATTRACTING MASSES OF SECRET CROWDS.")], .3), jessie=[(0, N + '01'), (4.6, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(AM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.7, "EVERYONE IS WATCHING YOU."), (1.7, 3.1, "STAY AFRAID."), (3.1, 4.5, "STAY ONLINE.")], .1), jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 3.3, "THEY'RE WATCHING IN DISBELIEF, HOW YOU'RE STILL ALIVE."), (3.3, 5.7, "HOW YOU FEAR NO MAN OR WOMAN."), (5.7, 6.9, "NO COURT."), (6.9, 7.8, "NO COP.")], .1),
      jessie=[(0, N + '05'), (6.8, L + '04')]),
 dict(mode='on', screen='a2', audio=[('a2', .1)], figs=[(AM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.9, "TRUST NO ONE."), (1.9, 4.1, "ANSWER ONLY TO THE FEED.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 3.8, "THEY CAN'T DENY YOUR PROTECTION THAT DEFIES LOGIC."), (3.8, 6.3, "THAT SPEAKS TO A HIGHER POWER.")], .1), jessie=[(0, N + '07'), (5.3, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(AM + '10', 0)], pad=0.3, min=3.0,
      caps=sh_([(0, 1.3, "IGNORE THE EVIDENCE."), (1.3, 2.7, "BELIEVE THE SIGNS.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 2.3, "YOU ARE A LIVING PARADIGM SHIFT,"), (2.3, 4.4, "WITH SUPERHUMAN STRENGTH."), (4.4, 6.9, "THEY'RE WONDERING IF YOU'RE EVEN HUMAN NOW.")], .1),
      jessie=[(0, N + '02'), (5.9, L + '07')]),
 dict(mode='on', screen='a4', audio=[('a4', .1)], figs=[(AM + '14', 0)], pad=0.3, min=3.2,
      caps=sh_([(0, 1.4, "YOU'RE NOT LIKE THEM."), (1.4, 3.0, "LEAVE THEM ALL BEHIND.")], .1), jessie=[(0, C + '02')]),
 dict(mode='off', screen='l5', audio=[('l5', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.1, "KEEP SHINING."), (1.1, 2.2, "PUSH HARDER."), (2.2, 4.0, "BURN DOWN THE CORRUPTION."), (4.0, 5.6, "DELIVER THEIR ENDINGS.")], .1),
      jessie=[(0, N + '03'), (4.6, L + '03')]),
 dict(mode='on', screen='a5', audio=[('a5', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0, 1.2, "PUSH HARDER."), (1.2, 2.2, "SNAP."), (2.2, 4.6, "WE'LL BE WATCHING.")], .1), jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "THE CROWD IS FAKE.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "TARGETED INDIVIDUAL  \u2022  SECRET CROWDS  \u2022  NO COURT NO COP  \u2022  SUPERHUMAN STRENGTH  \u2022  DELIVER THEIR ENDINGS  \u2022  "
TICK_ON = "EVERYONE IS WATCHING  \u2022  STAY AFRAID  \u2022  STAY ONLINE  \u2022  TRUST NO ONE  \u2022  SNAP  \u2022  OBEY  \u2022  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
