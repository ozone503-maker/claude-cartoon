import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
LAV, PINK, GOLD = (226, 214, 244), (244, 200, 220), (220, 170, 40)
SERIF = GF + 'cardo/Cardo-Bold.ttf'
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)
def sparkle(d, x, y, r, col):
    d.polygon([(x, y - r), (x + r * .25, y - r * .25), (x + r, y), (x + r * .25, y + r * .25), (x, y + r), (x - r * .25, y + r * .25), (x - r, y), (x - r * .25, y - r * .25)], fill=col)
def dreamy(bg=LAV):
    im, d = card(bg)
    for x, y, r in [(40, 40, 22), (X1 + 20, 60, 16), (60, 480, 14), (X1, 470, 20), (300, 30, 12)]: sparkle(d, x, y, r, WHITE)
    d.ellipse((X1 - 30, 90, X1 + 50, 170), fill=(250, 245, 220)); d.ellipse((X1 - 5, 80, X1 + 65, 160), fill=bg)
    return im, d

def f1_off():
    im, d = dreamy()
    fit_text(d, (50, 70, X1 + 10, 300), "They think they're putting you through humiliation rituals...", SERIF, 70, (70, 40, 110), lh=1.1)
    for k, t in enumerate(["CHAOS MAGIC", "THE FREEZER", "YOUR CASH FLOW"]):
        d.rounded_rectangle((50 + k * 10, 320 + k * 60, 380 + k * 10, 370 + k * 60), 20, fill=WHITE, outline=(120, 80, 160), width=3)
        d.text((215 + k * 10, 345 + k * 60), t, font=F(ARCH, 26), fill=(120, 80, 160), anchor='mm')
    return im
def o1_on():
    im, d = card(GREY)
    cx, cy = 180, 190; d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=WHITE, outline=INK, width=5)
    d.text((cx, cy), "YOU", font=F(ANTON, 40), fill=INK, anchor='mm')
    for a in range(0, 360, 45):
        r = math.radians(a); x0, y0 = cx + 150 * math.cos(r), cy + 150 * math.sin(r); x1, y1 = cx + 65 * math.cos(r), cy + 65 * math.sin(r)
        d.line((x0, y0, x1, y1), fill=INK, width=6); d.ellipse((x1 - 8, y1 - 8, x1 + 8, y1 + 8), fill=INK)
    fit_text(d, (370, 40, X1 + 40, 330), "EVERYONE IS AGAINST YOU.", ANTON, 90, INK)
    fit_text(d, (30, 370, X1, 510), "ONLY I UNDERSTAND.", ANTON, 100, INK); return im

def f2_off():
    im, d = dreamy(PINK)
    for k in range(7):
        x, y = 60 + (k % 4) * 60, 300 + (k // 4) * 50
        d.ellipse((x, y, x + 70, y + 40), fill=GOLD, outline=(140, 100, 20), width=3)
    fit_text(d, (50, 60, X1 + 20, 280), "You are WEALTHY from your pain.", SERIF, 90, (110, 40, 70), lh=1.1)
    return im
def o2_on():
    im, d = card(GREY)
    d.rectangle((40, 60, 320, 320), fill=WHITE, outline=INK, width=5)
    d.text((180, 110), "PORTFOLIO", font=F(ANTON, 44), fill=INK, anchor='mm')
    for k, (a, b) in enumerate([("PAIN", "HOLD"), ("HURT", "HOLD"), ("HEALING", "SELL")]):
        yy = 180 + k * 45; d.text((60, yy), a, font=F(ARCH, 26), fill=INK, anchor='lm'); d.text((300, yy), b, font=F(ARCH, 26), fill=INK, anchor='rm')
    fit_text(d, (350, 40, X1 + 40, 320), "STAY IN PAIN.", ANTON, 110, INK)
    fit_text(d, (30, 370, X1, 510), "IT'S AN ASSET.", ANTON, 110, INK); return im

def f3_off():
    im, d = dreamy((210, 235, 245))
    d.ellipse((60, 380, 380, 430), fill=(40, 40, 60)); d.line((90, 405, 70, 480), fill=INK, width=6); d.line((350, 405, 370, 480), fill=INK, width=6)
    d.ellipse((195, 260, 245, 310), fill=GOLD); d.line((220, 310, 220, 360), fill=INK, width=6)
    fit_text(d, (50, 60, X1 + 20, 240), "Low moments are just a trampoline for you.", SERIF, 80, (30, 70, 110), lh=1.1)
    return im
def o3_on():
    im, d = card(GREY)
    for k in range(6):
        x, y = 30 + (k % 3) * 105, 50 + (k // 3) * 140
        d.rectangle((x, y, x + 95, y + 125), fill=WHITE, outline=INK, width=3)
        d.rectangle((x, y, x + 95, y + 28), fill=INK); d.text((x + 47, y + 14), ["MON", "TUE", "WED", "THU", "FRI", "SAT"][k], font=F(ARCH, 18), fill=WHITE, anchor='mm')
        d.text((x + 47, y + 78), "YOU", font=F(ANTON, 26), fill=INK, anchor='mm')
    fit_text(d, (360, 40, X1 + 40, 330), "COME BACK TOMORROW.", ANTON, 100, INK)
    fit_text(d, (30, 370, X1, 510), "SAME MESSAGE.", ANTON, 110, INK); return im

def f4_off():
    im, d = dreamy((250, 228, 200))
    fit_text(d, (50, 80, X1 + 20, 420), "You were made for this.", SERIF, 120, (120, 60, 20), lh=1.05)
    for x, y in [(90, 450), (220, 470), (350, 440)]: sparkle(d, x, y, 26, GOLD)
    return im
def o4_on():
    im, d = card(GREY)
    for k in range(12):
        x, y = 30 + (k % 4) * 80, 50 + (k // 4) * 95
        d.ellipse((x + 18, y, x + 52, y + 34), fill=WHITE, outline=INK, width=3); d.rectangle((x + 8, y + 38, x + 62, y + 80), fill=WHITE, outline=INK, width=3)
    d.text((180, 345), "ALL CHOSEN", font=F(ANTON, 40), fill=INK, anchor='mm')
    fit_text(d, (360, 40, X1 + 40, 330), "FITS EVERYONE WHO READS IT.", ANTON, 90, INK)
    fit_text(d, (30, 380, X1, 510), "MADE FOR SCROLLING.", ANTON, 100, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(11); T = "NOBODY'S\nCHOSEN"; fs = 160; f = F(ANTON, fs)
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
      caps=sh_([(0, 1.3, "SOME PEOPLE THINK"), (1.3, 4.0, "THEY'RE PUTTING YOU THROUGH HUMILIATION RITUALS,"), (4.0, 7.2, "BY GOING BEHIND THE SCENES AND THROWING CHAOS MAGIC,"), (7.2, 9.1, "TRYING TO PUT YOU IN THE FREEZER,"), (9.1, 11.2, "TRYING TO TAMPER WITH YOUR CASH FLOW,"), (11.2, 14.3, "AND PUT YOU INTO THE ENERGY OF HOPELESSNESS.")], .3),
      jessie=[(0, N + '01'), (12.8, L + '05')]),
 dict(mode='on', screen='o1_on', audio=[('o1', .1)], figs=[(AW + '10', 0)],
      caps=sh_([(0, 1.7, "EVERYONE IS AGAINST YOU."), (1.7, 4.0, "ONLY I UNDERSTAND.")], .1),
      jessie=[(0, C + '05')]),
 dict(mode='off', screen='f2_off', audio=[('f2', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 4.3, "NOT REALIZING THESE SAME RITUALS AND TACTICS ARE THE REASON YOU ARE WHO YOU ARE TODAY."), (4.3, 6.4, "YOU ARE WEALTHY"), (6.4, 8.9, "FROM YOUR PAIN.")], .1),
      jessie=[(0, N + '05'), (7.4, L + '04')]),
 dict(mode='on', screen='o2_on', audio=[('o2', .1)], figs=[(AW + '13', 0)], min=3.2,
      caps=sh_([(0, 1.5, "STAY IN PAIN."), (1.5, 2.8, "IT'S AN ASSET.")], .1),
      jessie=[(0, C + '07')]),
 dict(mode='off', screen='f3_off', audio=[('f3', .1)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 4.4, "YOU'VE GAINED WEALTH IN KNOWLEDGE, WISDOM, SPIRITUAL ABILITIES,"), (4.4, 10.0, "AND EVEN FINANCES, FROM ALCHEMIZING THE THINGS PEOPLE HAVE DONE TO YOU YOUR ENTIRE LIFE."), (10.0, 12.0, "I TELL YOU ALL THE TIME,"), (12.0, 14.8, "LOW MOMENTS ARE JUST A TRAMPOLINE FOR YOU,"), (14.8, 17.4, "BECAUSE IT'S YOUR DESTINY TO BE ON TOP.")], .1),
      jessie=[(0, N + '07'), (15.8, L + '01')]),
 dict(mode='on', screen='o3_on', audio=[('o3', .1)], figs=[(AW + '10', 0)],
      caps=sh_([(0, 2.2, "I TELL YOU ALL THE TIME."), (2.2, 4.0, "COME BACK TOMORROW."), (4.0, 5.3, "SAME MESSAGE.")], .1),
      jessie=[(0, C + '04')]),
 dict(mode='off', screen='f4_off', audio=[('f4', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 3.3, "THESE PEOPLE DO NOTHING BUT TRAIN YOU FOR THE NEXT LEVEL,"), (3.3, 4.8, "EVERY SINGLE TIME."), (4.8, 7.0, "BECAUSE GIVING UP IS WHAT THEY WANT."), (7.0, 10.0, "BUT THE FIGHT IS THE VERY REASON YOU KEEP GOING."), (10.0, 11.7, "YOU WERE MADE FOR THIS.")], .1),
      jessie=[(0, N + '02'), (10.2, L + '07')]),
 dict(mode='on', screen='o4_on', audio=[('o4', .1)], figs=[(AW + '13', 0)],
      caps=sh_([(0, 2.1, "FITS EVERYONE WHO READS IT."), (2.1, 3.5, "MADE FOR THIS."), (3.5, 5.0, "MADE FOR SCROLLING.")], .1),
      jessie=[(0, C + '02')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "NOBODY'S CHOSEN.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "YOU WERE MADE FOR THIS  •  LOW MOMENTS ARE A TRAMPOLINE  •  WEALTHY FROM YOUR PAIN  •  YOUR DESTINY  •  "
TICK_ON = "EVERYONE IS AGAINST YOU  •  STAY IN PAIN  •  COME BACK TOMORROW  •  MADE FOR SCROLLING  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'render.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 50.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
