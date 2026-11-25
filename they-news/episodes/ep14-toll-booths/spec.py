import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
NAVY, TEAL = (25, 45, 90), (40, 140, 150)
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)
def header(d, t, col=NAVY):
    d.rectangle((0, 0, sw, 80), fill=col); d.text((sw / 2, 40), t, font=F(ANTON, 48), fill=WHITE, anchor='mm')
def house(d, x, y, s, col, line):
    d.rectangle((x, y, x + 120 * s, y + 90 * s), fill=col, outline=line, width=4)
    d.polygon([(x - 15 * s, y), (x + 60 * s, y - 60 * s), (x + 135 * s, y)], fill=line)
    d.rectangle((x + 45 * s, y + 40 * s, x + 75 * s, y + 90 * s), fill=line)
def bars(d, x0, y0, x1, y1, col, w=8, n=6):
    d.rectangle((x0, y0, x1, y1), outline=col, width=w)
    for k in range(1, n): xx = x0 + (x1 - x0) * k / n; d.line((xx, y0, xx, y1), fill=col, width=w)

def f1_off():
    im, d = card(WHITE); header(d, "GENERATION ANGRY", RED)
    d.text((40, 130), "RENT", font=F(ANTON, 50), fill=INK, anchor='lm'); d.rectangle((170, 110, X1 + 20, 150), outline=INK, width=4); d.rectangle((170, 110, 170 + (X1 - 150) * .5, 150), fill=RED)
    d.text((X1 + 30, 130), "50%", font=F(ANTON, 36), fill=INK, anchor='lm')
    house(d, 80, 260, 1.2, (240, 220, 180), INK); d.text((120, 400), "FANTASY", font=F(ANTON, 40), fill=RED, anchor='mm')
    fit_text(d, (260, 200, X1 + 40, 420), "EXPERTS AGREE: CAPITALISM IS THE PROBLEM", ANTON, 70, INK); return im
def o1_on():
    im, d = card(GREY)
    for k in range(7): d.line((70, 60 + k * 55, 150, 60 + k * 55), fill=INK, width=6)
    d.line((70, 40, 70, 420), fill=INK, width=8); d.line((150, 40, 150, 420), fill=INK, width=8)
    d.line((40, 60, 180, 420), fill=RED, width=10)
    for r in range(6):
        for c in range(3): d.rectangle((200 + c * 50 + (r % 2) * 25, 60 + r * 60, 245 + c * 50 + (r % 2) * 25, 115 + r * 60), fill=WHITE, outline=INK, width=3)
    fit_text(d, (380, 40, X1 + 40, 300), "HATE THE LADDER.", ANTON, 100, INK)
    fit_text(d, (30, 430, X1, 520), "LOVE THE WALL.", ANTON, 100, INK); return im

def f2_off():
    im, d = card((240, 240, 230)); header(d, "CITY PLANNING COMMISSION")
    for k in range(9): d.rectangle((60 + k * 6, 380 - k * 28, 260 + k * 6, 400 - k * 28), fill=WHITE, outline=INK, width=2)
    d.text((170, 440), "PERMITS", font=F(ANTON, 40), fill=INK, anchor='mm')
    fit_text(d, (320, 130, X1 + 40, 420), "REVIEW TIME: 7 YEARS", ANTON, 90, NAVY); return im
def o2_on():
    im, d = card(GREY); house(d, 90, 180, 1.6, WHITE, INK)
    bars(d, 50, 330, 330, 440, INK, 6, 7); d.text((190, 470), "OWNERS ONLY", font=F(ANTON, 36), fill=INK, anchor='mm')
    fit_text(d, (370, 40, X1 + 40, 330), "THE PEOPLE INSIDE", ANTON, 100, INK)
    fit_text(d, (370, 340, X1 + 40, 520), "VOTE TO LOCK THE DOOR.", ANTON, 80, INK); return im

def f3_off():
    im, d = card(WHITE); header(d, "PHARMA PRESS BRIEFING", TEAL)
    d.rounded_rectangle((70, 200, 290, 290), 45, fill=(250, 120, 120), outline=INK, width=4); d.rectangle((180, 200, 290, 290), fill=WHITE); d.rounded_rectangle((70, 200, 290, 290), 45, outline=INK, width=4)
    d.text((180, 340), "$1,200", font=F(ANTON, 60), fill=RED, anchor='mm')
    fit_text(d, (320, 140, X1 + 40, 420), "PATENT EXTENDED. AGAIN.", ANTON, 90, TEAL); return im
def o3_on():
    im, d = card(GREY)
    d.rounded_rectangle((80, 200, 290, 280), 40, fill=WHITE, outline=INK, width=5)
    bars(d, 50, 120, 320, 360, INK, 7, 6)
    fit_text(d, (360, 40, X1 + 40, 330), "NO COMPETITOR. NO CHEAP PILL.", ANTON, 90, INK)
    fit_text(d, (30, 400, X1, 520), "NO CHOICE.", ANTON, 110, INK); return im

def f4_off():
    im, d = card((235, 238, 245)); header(d, "SENATE HEARING: AI SAFETY")
    d.rectangle((60, 140, 330, 320), fill=WHITE, outline=INK, width=4)
    d.text((195, 190), "AI LICENSE", font=F(ANTON, 44), fill=NAVY, anchor='mm'); d.text((195, 245), "ACT", font=F(ANTON, 44), fill=NAVY, anchor='mm')
    d.text((195, 300), "for your safety", font=F(ARCH, 22), fill=INK, anchor='mm')
    fit_text(d, (350, 120, X1 - 10, 440), "BIG TECH WELCOMES REGULATION", ANTON, 70, NAVY); return im
def o4_on():
    im, d = card(GREY)
    d.rectangle((90, 200, 280, 320), fill=WHITE, outline=INK, width=5); d.polygon([(60, 320), (310, 320), (330, 350), (40, 350)], fill=INK)
    d.text((185, 260), "AI", font=F(ANTON, 60), fill=INK, anchor='mm')
    bars(d, 30, 150, 340, 380, INK, 7, 7)
    fit_text(d, (370, 40, X1 + 40, 300), "LICENSES FOR US.", ANTON, 100, INK)
    fit_text(d, (30, 410, X1, 520), "LOCKS FOR YOU.", ANTON, 110, INK); return im

def f5_off():
    im, d = card((245, 240, 225)); header(d, "GLOBAL INEQUALITY SUMMIT", (120, 80, 40))
    for k, t in enumerate(["FOUNDATION", "THINK TANK", "NGO", "STUDY"]):
        x, y = 50 + (k % 2) * 170, 130 + (k // 2) * 110
        d.rounded_rectangle((x, y, x + 150, y + 85), 16, fill=WHITE, outline=(120, 80, 40), width=4)
        d.text((x + 75, y + 42), t, font=F(ARCH, 17), fill=(120, 80, 40), anchor='mm')
    fit_text(d, (40, 380, X1 + 40, 500), "“BECAUSE WE CARE”", ANTON, 70, (120, 80, 40)); return im
def o5_on():
    im, d = card(GREY)
    d.text((180, 70), "$", font=F(ANTON, 90), fill=INK, anchor='mm')
    for k, t in enumerate(["RULES", "ANGER"]):
        x = 60 + k * 170; d.line((180, 110, x + 60, 300), fill=INK, width=4)
        d.rectangle((x, 300, x + 120, 370), fill=WHITE, outline=INK, width=5); d.text((x + 60, 335), t, font=F(ANTON, 36), fill=INK, anchor='mm')
    fit_text(d, (370, 40, X1 + 40, 300), "WE WROTE THE RULES.", ANTON, 100, INK)
    fit_text(d, (30, 400, X1, 520), "THEN WE SOLD YOU THE ANGER.", ANTON, 90, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(14); T = "WHO WROTE\nTHE RULE?"; fs = 150; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(f1_off=f1_off, o1_on=o1_on, f2_off=f2_off, o2_on=o2_on, f3_off=f3_off, o3_on=o3_on, f4_off=f4_off, o4_on=o4_on, f5_off=f5_off, o5_on=o5_on, end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='f1_off', audio=[('f1', .3)], figs=[(RW + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.6, "YOUNG PEOPLE ARE ANGRY."), (1.6, 5.3, "RENT EATS HALF THEIR PAYCHECK, AND A HOUSE IS A FANTASY."), (5.3, 6.6, "EXPERTS AGREE."), (6.6, 8.5, "CAPITALISM IS THE PROBLEM.")], .3),
      jessie=[(0, N + '01'), (7.4, L + '05')]),
 dict(mode='on', screen='o1_on', audio=[('o1', .1)], figs=[(AW + '10', 0)], min=2.8, pad=0.3,
      caps=sh_([(0, 1.1, "HATE THE LADDER."), (1.1, 2.4, "LOVE THE WALL.")], .1),
      jessie=[(0, C + '05')]),
 dict(mode='off', screen='f2_off', audio=[('f2', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.6, "TO PROTECT OUR NEIGHBORHOOD,"), (1.6, 4.3, "EVERY NEW BUILDING NEEDS YEARS OF PERMITS AND REVIEW.")], .1),
      jessie=[(0, N + '05'), (3.4, L + '04')]),
 dict(mode='on', screen='o2_on', audio=[('o2', .1)], figs=[(AM + '14', 0)], min=3.1, pad=0.3,
      caps=sh_([(0, 2.8, "THE PEOPLE INSIDE VOTE TO LOCK THE DOOR.")], .1),
      jessie=[(0, C + '07')]),
 dict(mode='off', screen='f3_off', audio=[('f3', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 2.6, "OUR PATENT EXTENSIONS PROTECT INNOVATION,"), (2.6, 4.0, "AND PATIENT SAFETY.")], .1),
      jessie=[(0, N + '07'), (3.1, L + '01')]),
 dict(mode='on', screen='o3_on', audio=[('o3', .1)], figs=[(AM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.2, "NO COMPETITOR."), (1.2, 2.9, "NO CHEAP PILL."), (2.9, 4.2, "NO CHOICE.")], .1),
      jessie=[(0, C + '04')]),
 dict(mode='off', screen='f4_off', audio=[('f4', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 4.3, "WE WELCOME A GOVERNMENT LICENSING REGIME FOR ADVANCED AI."), (4.3, 6.0, "FOR YOUR SAFETY.")], .1),
      jessie=[(0, N + '02'), (5.0, L + '07')]),
 dict(mode='on', screen='o4_on', audio=[('o4', .1)], figs=[(AM + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.4, "LICENSES FOR US."), (1.4, 2.9, "LOCKS FOR YOU."), (2.9, 6.4, "THE ONE TOOL THAT LETS YOU COMPETE, BEHIND A GATE.")], .1),
      jessie=[(0, C + '02')]),
 dict(mode='off', screen='f5_off', audio=[('f5', .1)], figs=[(RM + '07', 0)], pad=0.3,
      caps=sh_([(0, 1.7, "WE FUND THE FOUNDATIONS,"), (1.7, 3.6, "THE STUDIES, AND THE SUMMITS."), (3.6, 6.2, "BECAUSE WE CARE ABOUT INEQUALITY.")], .1),
      jessie=[(0, N + '03'), (5.2, L + '03')]),
 dict(mode='on', screen='o5_on', audio=[('o5', .1)], figs=[(AM + '07', 0)],
      caps=sh_([(0, 1.6, "WE WROTE THE RULES."), (1.6, 3.9, "THEN WE SOLD YOU THE ANGER.")], .1),
      jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "WHO WROTE THE RULE?")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "CAPITALISM IS THE PROBLEM  •  PERMITS PROTECT NEIGHBORHOODS  •  PATENTS PROTECT PATIENTS  •  AI NEEDS A LICENSE  •  WE CARE  •  "
TICK_ON = "HATE THE LADDER  •  LOVE THE WALL  •  LOCK THE DOOR  •  LICENSES FOR US  •  LOCKS FOR YOU  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 30.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
