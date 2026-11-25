import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
DUSK, ROSE, SAGE = (60, 50, 90), (250, 215, 215), (215, 235, 215)
SERIF = GF + 'cardo/Cardo-Bold.ttf'
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)
def person(d, x, y, s, col):
    d.ellipse((x - 14 * s, y, x + 14 * s, y + 28 * s), fill=col); d.rounded_rectangle((x - 20 * s, y + 32 * s, x + 20 * s, y + 90 * s), 10, fill=col)

def f1_off():
    im, d = card(DUSK)
    d.ellipse((X1 - 60, 40, X1 + 30, 130), fill=(250, 230, 180))
    d.rectangle((0, 400, sw, sh), fill=(35, 30, 55)); person(d, 200, 300, 1.1, (20, 15, 30))
    fit_text(d, (40, 40, X1 - 70, 250), "They left you for dead when you were at your lowest.", SERIF, 70, (240, 225, 250), align='left', lh=1.1)
    return im
def o1_on():
    im, d = card(GREY)
    d.rounded_rectangle((60, 40, 300, 460), 30, fill=WHITE, outline=INK, width=6)
    for k in range(5):
        y = 80 + k * 72; d.ellipse((80, y, 120, y + 40), fill=INK); d.rectangle((130, y + 12, 210, y + 28), fill=(170, 170, 170))
        d.rounded_rectangle((215, y + 5, 290, y + 35), 10, fill=INK); d.text((252, y + 20), "BLOCK", font=F(ARCH, 16), fill=WHITE, anchor='mm')
    fit_text(d, (330, 40, X1 + 40, 300), "EVERYONE LEFT YOU.", ANTON, 100, INK)
    fit_text(d, (330, 310, X1 + 40, 510), "CUT THEM OFF FIRST.", ANTON, 90, INK); return im

def f2_off():
    im, d = card(ROSE)
    d.rectangle((150, 300, 250, 440), fill=(200, 230, 240), outline=INK, width=4)
    d.line((200, 300, 200, 180), fill=(60, 130, 60), width=8)
    for a in range(0, 360, 60):
        r = math.radians(a); d.ellipse((200 + 40 * math.cos(r) - 28, 160 + 40 * math.sin(r) - 28, 200 + 40 * math.cos(r) + 28, 160 + 40 * math.sin(r) + 28), fill=(240, 120, 150))
    d.ellipse((180, 140, 220, 180), fill=(250, 210, 80))
    fit_text(d, (290, 60, X1 + 30, 300), "You bloomed in isolation.", SERIF, 90, (130, 40, 70), align='left', lh=1.05)
    return im
def o2_on():
    im, d = card(GREY)
    d.rectangle((40, 60, 320, 330), fill=WHITE, outline=INK, width=5)
    d.text((180, 100), "SCREEN TIME", font=F(ANTON, 40), fill=INK, anchor='mm')
    d.text((180, 190), "14h 22m", font=F(ANTON, 80), fill=INK, anchor='mm')
    d.text((180, 280), "FRIENDS: 0", font=F(ARCH, 30), fill=INK, anchor='mm')
    fit_text(d, (350, 40, X1 + 40, 330), "ISOLATED PEOPLE SCROLL LONGER.", ANTON, 90, INK)
    fit_text(d, (30, 370, X1, 510), "BLOOM ALONE.", ANTON, 110, INK); return im

def f3_off():
    im, d = card(SAGE)
    d.ellipse((60, 60, 330, 420), fill=(230, 240, 245), outline=(120, 140, 120), width=10)
    hx, hy = 195, 230
    d.ellipse((hx - 60, hy - 50, hx, hy + 10), fill=(220, 90, 110)); d.ellipse((hx, hy - 50, hx + 60, hy + 10), fill=(220, 90, 110))
    d.polygon([(hx - 58, hy - 10), (hx + 58, hy - 10), (hx, hy + 70)], fill=(220, 90, 110))
    fit_text(d, (350, 60, X1 + 30, 380), "You learned to love yourself in isolation.", SERIF, 80, (40, 80, 50), align='left', lh=1.05)
    return im
def o3_on():
    im, d = card(GREY)
    d.rectangle((40, 200, 320, 240), fill=WHITE, outline=INK, width=4)
    for k in range(4):
        x = 60 + k * 70; d.rectangle((x, 130, x + 40, 200), outline=INK, width=4); d.line((x + 5, 240, x + 5, 300), fill=INK, width=4); d.line((x + 35, 240, x + 35, 300), fill=INK, width=4)
    d.text((180, 340), "TABLE FOR ONE", font=F(ANTON, 40), fill=INK, anchor='mm')
    fit_text(d, (350, 40, X1 + 40, 330), "NO FRIENDS. NO FAMILY.", ANTON, 100, INK)
    fit_text(d, (30, 380, X1, 510), "JUST THE FEED.", ANTON, 110, INK); return im

def f4_off():
    im, d = card(DUSK)
    fit_text(d, (40, 25, X1 + 40, 115), "Permanently. Forevermore.", SERIF, 70, (240, 225, 250))
    d.rectangle((80, 140, 400, 470), fill=(30, 25, 45), outline=(240, 200, 120), width=8)
    for k in range(7): d.line((110 + k * 45, 140, 110 + k * 45, 470), fill=(240, 200, 120), width=6)
    d.rectangle((50, 270, 430, 345), fill=(200, 40, 60)); d.text((240, 307), "ACCESS DENIED", font=F(ANTON, 52), fill=WHITE, anchor='mm')
    return im
def o4_on():
    im, d = card(GREY)
    for k in range(6):
        x, y = 40 + (k % 3) * 100, 50 + (k // 3) * 150
        d.rectangle((x, y, x + 85, y + 130), outline=INK, width=5); person(d, x + 42, y + 25, .9, INK)
    d.text((180, 360), "DIVIDE & CONQUER", font=F(ANTON, 36), fill=INK, anchor='mm')
    fit_text(d, (370, 40, X1 + 40, 330), "DIVIDED. ISOLATED. CONQUERED.", ANTON, 90, INK)
    fit_text(d, (30, 390, X1, 510), "TRUST NO ONE. EXCEPT THIS ACCOUNT.", ANTON, 80, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(13); T = "CALL YOUR\nPEOPLE"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(f1_off=f1_off, o1_on=o1_on, f2_off=f2_off, o2_on=o2_on, f3_off=f3_off, o3_on=o3_on, f4_off=f4_off, o4_on=o4_on, end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='f1_off', audio=[('f1', .3)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 3.0, "THEY LEFT YOU FOR DEAD WHEN YOU WERE AT YOUR LOWEST."), (3.0, 7.6, "AND THEN ON TOP OF THAT, THEY HOPED AND WISHED THAT ISOLATION WOULD FINISH THE JOB."), (7.6, 9.2, "THAT YOU'D CRASH OUT."), (9.2, 11.2, "YOU'D BREAK."), (11.2, 15.8, "YOU'D COME CRAWLING BACK, DESPERATELY NEEDING THEM.")], .3),
      jessie=[(0, N + '01'), (14.2, L + '05')]),
 dict(mode='on', screen='o1_on', audio=[('o1', .1)], figs=[(AW + '10', 0)], min=3.4,
      caps=sh_([(0, 1.2, "EVERYONE LEFT YOU."), (1.2, 3.0, "CUT THEM OFF FIRST.")], .1),
      jessie=[(0, C + '05')]),
 dict(mode='off', screen='f2_off', audio=[('f2', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 1.9, "BUT THAT'S NOT WHAT HAPPENED."), (1.9, 4.4, "IT ACTUALLY WENT QUITE THE OPPOSITE."), (4.4, 6.8, "YOU FOUND YOURSELF IN ISOLATION."), (6.8, 9.3, "YOU BLOOMED IN ISOLATION."), (9.3, 11.8, "YOU THRIVED IN ISOLATION."), (11.8, 14.5, "YOU HEALED IN ISOLATION."), (14.5, 17.2, "YOU FOUND PEACE IN ISOLATION.")], .1),
      jessie=[(0, N + '05'), (15.6, L + '04')]),
 dict(mode='on', screen='o2_on', audio=[('o2', .1)], figs=[(AW + '13', 0)],
      caps=sh_([(0, 2.3, "ISOLATED PEOPLE SCROLL LONGER."), (2.3, 3.6, "BLOOM ALONE.")], .1),
      jessie=[(0, C + '07')]),
 dict(mode='off', screen='f3_off', audio=[('f3', .1)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 3.3, "YOU LEARNED TO LOVE YOURSELF IN ISOLATION."), (3.3, 7.3, "YOU LEARNED TO DEEPLY UNDERSTAND YOURSELF IN ISOLATION."), (7.3, 11.1, "YOU FELL IN LOVE WITH BEING CONTENT WITH YOUR OWN ENERGY."), (11.1, 17.3, "YOU LOVED ISOLATION SO MUCH THAT YOU BECAME QUITE STINGY ABOUT WHO GETS ANY OF YOUR ENERGY.")], .1),
      jessie=[(0, N + '07'), (15.8, L + '01')]),
 dict(mode='on', screen='o3_on', audio=[('o3', .1)], figs=[(AW + '10', 0)], min=3.6,
      caps=sh_([(0, 1.0, "NO FRIENDS."), (1.0, 2.4, "NO FAMILY."), (2.4, 3.5, "JUST THE FEED.")], .1),
      jessie=[(0, C + '04')]),
 dict(mode='off', screen='f4_off', audio=[('f4', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 4.2, "NOW THEIR ACCESS TO YOU IS PERMANENTLY DENIED."), (4.2, 8.5, "AND MOST IMPORTANTLY, YOU'VE LEARNED TO TRUST YOUR INTUITION"), (8.5, 11.0, "ABOUT WHO GETS ANY OF YOUR ENERGY."), (11.0, 12.3, "FOREVERMORE.")], .1),
      jessie=[(0, N + '02'), (10.8, L + '07')]),
 dict(mode='on', screen='o4_on', audio=[('o4', .1)], figs=[(AW + '13', 0)],
      caps=sh_([(0, 0.9, "DIVIDED."), (0.9, 2.1, "ISOLATED."), (2.1, 3.1, "CONQUERED."), (3.1, 4.8, "TRUST NO ONE."), (4.8, 6.4, "EXCEPT THIS ACCOUNT.")], .1),
      jessie=[(0, C + '02')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "CALL YOUR PEOPLE.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "YOU BLOOMED IN ISOLATION  •  PROTECT YOUR ENERGY  •  ACCESS DENIED  •  TRUST YOUR INTUITION  •  "
TICK_ON = "CUT THEM OFF  •  SCROLL LONGER  •  JUST THE FEED  •  DIVIDED  •  CONQUERED  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 18.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
