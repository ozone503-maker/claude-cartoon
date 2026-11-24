import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
SPACE = (12, 16, 36); NASA_B = (20, 50, 140)
FIRA = GF + 'firasans/FiraSans-Regular.ttf'; SERIF = GF + 'cardo/Cardo-Bold.ttf'
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def stars(d, n=70, seed=2, col=(230, 230, 255)):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x, y, r = rng.uniform(0, sw), rng.uniform(0, sh), rng.uniform(1, 3); d.ellipse((x - r, y - r, x + r, y + r), fill=col)
def moon(d, cx, cy, r, col, crater):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=INK, width=5)
    for dx, dy, cr in [(-.4, -.3, .18), (.3, -.1, .12), (-.1, .35, .15), (.45, .4, .09), (.05, -.55, .08)]:
        d.ellipse((cx + dx * r - cr * r, cy + dy * r - cr * r, cx + dx * r + cr * r, cy + dy * r + cr * r), fill=crater)
def base(d, cx, by, col, line):
    for k, (w, h) in enumerate([(90, 60), (60, 45), (90, 60)]):
        x = cx - 120 + k * 90; d.chord((x, by - h, x + w, by + h), 180, 360, fill=col, outline=line, width=4)
    d.line((cx + 60, by - 50, cx + 60, by - 110), fill=line, width=4); d.polygon([(cx + 60, by - 110), (cx + 100, by - 98), (cx + 60, by - 86)], fill=RED if line != INK or col != (200, 200, 200) else INK)

def p1_off():
    im, d = card(SPACE); stars(d); moon(d, 190, 270, 160, (210, 210, 205), (180, 180, 175))
    base(d, 190, 400, WHITE, INK)
    d.rectangle((370, 60, sw - 30, 160), fill=NASA_B); d.text(((370 + sw - 30) / 2, 110), "MOON BASE", font=F(ANTON, 70), fill=WHITE, anchor='mm')
    fit_text(d, (370, 190, sw - 30, 330), "$20,000,000,000", ANTON, 80, (255, 220, 90))
    fit_text(d, (370, 340, sw - 30, 440), "7 YEARS • LUNAR SOUTH POLE", ARCH, 34, WHITE); return im
def invoice(d, x, y, w, h):
    d.rectangle((x, y, x + w, y + h), fill=WHITE, outline=INK, width=5)
    d.text((x + w / 2, y + 40), "INVOICE", font=F(ANTON, 50), fill=INK, anchor='mm')
    rows = [("1969 TRIP", "PAID"), ("1972 TRIP", "PAID"), ("2026 TRIP", "$20B")]
    for k, (a, b) in enumerate(rows):
        yy = y + 110 + k * 50; d.text((x + 20, yy), a, font=F(ARCH, 28), fill=INK, anchor='lm'); d.text((x + w - 20, yy), b, font=F(ARCH, 28), fill=INK, anchor='rm')
    d.line((x + 15, y + h - 60, x + w - 15, y + h - 60), fill=INK, width=4)
def p1_on():
    im, d = card(GREY); invoice(d, 30, 30, 330, 320)
    fit_text(d, (380, 40, X1 + 40, 340), "SAME TRIP. NEW INVOICE.", ANTON, 100, INK)
    fit_text(d, (30, 380, X1, 500), "FIFTY YEARS LATER.", ANTON, 90, INK); return im

def rover(d, x, y, col, line):
    d.rounded_rectangle((x, y, x + 150, y + 60), 10, fill=col, outline=line, width=4)
    for k in range(3): d.ellipse((x + 5 + k * 50, y + 45, x + 45 + k * 50, y + 85), fill=line)
    d.line((x + 120, y, x + 130, y - 50), fill=line, width=4); d.ellipse((x + 118, y - 70, x + 142, y - 46), fill=col, outline=line, width=4)
def drone(d, x, y, col, line):
    d.rectangle((x - 30, y - 10, x + 30, y + 10), fill=col, outline=line, width=3)
    for dx in (-50, 50): d.line((x, y, x + dx, y - 15), fill=line, width=4); d.ellipse((x + dx - 22, y - 22, x + dx + 22, y - 10), outline=line, width=3)
def p2_off():
    im, d = card(SPACE); stars(d, 40); d.rectangle((0, 380, sw, sh), fill=(150, 150, 145))
    rover(d, 60, 300, WHITE, INK); rover(d, 280, 330, (230, 210, 120), INK); drone(d, 220, 120, WHITE, INK); drone(d, 420, 190, WHITE, INK)
    fit_text(d, (30, 420, X1 + 40, 520), "ROBOTS FIRST. HUMANS LATER.", ANTON, 60, INK); return im
def p2_on():
    im, d = card(GREY); rover(d, 50, 180, (210, 210, 210), INK)
    d.rectangle((40, 120, 230, 170), fill=INK); d.text((135, 145), "NO COMMENT", font=F(ANTON, 32), fill=GREY, anchor='mm')
    fit_text(d, (260, 40, X1 + 40, 330), "ROBOTS GO FIRST.", ANTON, 100, INK)
    fit_text(d, (30, 380, X1, 500), "ROBOTS DON'T TALK.", ANTON, 100, INK); return im

def p3_off():
    im, d = card(SPACE); stars(d, 50)
    d.ellipse((60, 120, sw - 60, 480), fill=(110, 110, 110), outline=INK, width=5); d.ellipse((120, 200, sw - 120, 470), fill=(15, 15, 25))
    for k in range(6):
        x = 220 + k * 50; d.polygon([(x, 400), (x + 20, 360), (x + 40, 400)], fill=(170, 220, 255), outline=WHITE)
    d.text((sw / 2, 60), "PERMANENT SHADOW", font=F(ARCH, 40), fill=WHITE, anchor='mm')
    d.text((sw / 2, 515), "WATER ICE?", font=F(ANTON, 40), fill=(170, 220, 255), anchor='mm'); return im
def p3_on():
    im, d = card(GREY)
    for k in range(5):
        x = 50 + k * 60; d.polygon([(x, 300), (x + 25, 220), (x + 50, 300)], fill=WHITE, outline=INK, width=4)
    d.line((40, 120, 330, 120), fill=INK, width=8); d.polygon([(330, 100), (370, 120), (330, 140)], fill=INK)
    d.text((185, 80), "MINE", font=F(ANTON, 60), fill=INK, anchor='mm')
    fit_text(d, (380, 40, X1 + 40, 320), "WHOEVER HOLDS THE ICE,", ANTON, 90, INK)
    fit_text(d, (30, 350, X1, 500), "HOLDS THE MOON.", ANTON, 110, INK); return im

def p4_off():
    im, d = card((250, 248, 240)); d.text((60, 90), "“", font=F(SERIF, 200), fill=(150, 160, 200), anchor='lm')
    fit_text(d, (60, 120, sw - 40, 380), "America will never again give up the moon.", SERIF, 80, INK, lh=1.15)
    d.text((sw - 40, 450), "NASA Administrator Jared Isaacman", font=F(ARCH, 28), fill=(90, 90, 90), anchor='rm'); return im
def p4_on():
    im, d = card(GREY); moon(d, 160, 170, 120, (210, 210, 210), (180, 180, 180))
    d.text((160, 330), "1972 → ????", font=F(ANTON, 54), fill=INK, anchor='mm')
    fit_text(d, (310, 40, X1 + 40, 330), "NEVER GIVE IT UP AGAIN.", ANTON, 90, INK)
    fit_text(d, (30, 380, X1, 500), "NEVER ASK WHY WE LEFT.", ANTON, 90, INK); return im

def p5_off():
    im, d = card(WHITE); d.rectangle((0, 0, sw, 90), fill=NASA_B); d.text((sw / 2, 45), "PARTNERS", font=F(ARCH, 44), fill=WHITE, anchor='mm')
    for k in range(6):
        x = 40 + (k % 3) * 210; y = 130 + (k // 3) * 130
        d.rounded_rectangle((x, y, x + 180, y + 100), 14, fill=(230, 232, 240), outline=INK, width=3)
        d.text((x + 90, y + 50), ["COMMERCIAL", "INTERNATIONAL", "COMMERCIAL", "INTERNATIONAL", "COMMERCIAL", "???"][k], font=F(ARCH, 18), fill=INK, anchor='mm')
    d.text((sw / 2, 450), "NEXT STOP: MARS", font=F(ANTON, 60), fill=RED, anchor='mm'); return im
def p5_on():
    im, d = card(GREY)
    for k in range(3):
        x = 30 + k * 60; d.rectangle((x, 60 + k * 30, x + 150, 250 + k * 30), fill=WHITE, outline=INK, width=4); d.text((x + 75, 90 + k * 30), "INVOICE", font=F(ANTON, 28), fill=INK, anchor='mm')
    fit_text(d, (310, 40, X1 + 40, 330), "PARTNERS MEANS CONTRACTORS.", ANTON, 80, INK)
    fit_text(d, (30, 380, X1, 500), "MARS MEANS MORE INVOICES.", ANTON, 90, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3); fs = 175; T = "LOOK UP"
    while ld.textlength(T, font=F(ANTON, fs)) > sw - 90: fs -= 5
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .35; L = rng.uniform(30, 150)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(p1_off=p1_off, p1_on=p1_on, p2_off=p2_off, p2_on=p2_on, p3_off=p3_off, p3_on=p3_on, p4_off=p4_off, p4_on=p4_on,
               p5_off=p5_off, p5_on=p5_on, end=end, end_g=end_g)

C = 'jessie-cool-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='p1_off', audio=[('p1', .3)], figs=[(RM + '14', 0)],
      caps=sh_([(0, 3.4, "NASA WILL SPEND TWENTY BILLION DOLLARS OVER SEVEN YEARS,"), (3.4, 6.9, "TO BUILD A PERMANENT MOON BASE NEAR THE LUNAR SOUTH POLE.")], .3),
      jessie=[(0, C + 'no-glasses-01'), (5.2, C + 'glasses-lowered-05')]),
 dict(mode='on', screen='p1_on', audio=[('o1', .1)], figs=[(AM + '14', 0)],
      caps=sh_([(0, 1.6, "FIFTY YEARS LATER."), (1.6, 2.9, "SAME TRIP."), (2.9, 4.2, "NEW INVOICE.")], .1),
      jessie=[(0, C + 'glasses-worn-05')]),
 dict(mode='off', screen='p2_off', audio=[('p2', .1)], figs=[(RM + '09', 0)],
      caps=sh_([(0.3, 3.6, "ROBOTS, AUTONOMOUS ROVERS, AND DRONES"), (3.6, 6.8, "WILL EXPLORE THE SOUTH POLE FIRST, BEFORE ANY HUMANS ARRIVE.")], .1),
      jessie=[(0, C + 'no-glasses-05'), (5.0, C + 'glasses-lowered-04')]),
 dict(mode='on', screen='p2_on', audio=[('o2', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0.3, 1.9, "ROBOTS GO FIRST."), (1.9, 3.6, "ROBOTS DON'T TALK.")], .1),
      jessie=[(0, C + 'glasses-worn-07')]),
 dict(mode='off', screen='p3_off', audio=[('p3', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 3.8, "SCIENTISTS BELIEVE THE SOUTH POLE MAY HOLD WATER ICE,"), (3.8, 6.7, "PRESERVED IN CRATERS OF PERMANENT DARKNESS.")], .1),
      jessie=[(0, C + 'no-glasses-07'), (5.0, C + 'glasses-lowered-01')]),
 dict(mode='on', screen='p3_on', audio=[('o3', .1)], figs=[(AW + '13', 0)],
      caps=sh_([(0.3, 1.9, "WHOEVER HOLDS THE ICE,"), (1.9, 3.4, "HOLDS THE MOON.")], .1),
      jessie=[(0, C + 'glasses-worn-04')]),
 dict(mode='off', screen='p4_off', audio=[('p4', .1)], figs=[(RM + '14', 0)], min=3.4,
      caps=sh_([(0, 3.0, "AMERICA WILL NEVER AGAIN GIVE UP THE MOON.")], .1),
      jessie=[(0, C + 'no-glasses-02'), (1.8, C + 'glasses-lowered-03')]),
 dict(mode='on', screen='p4_on', audio=[('o4', .1)], figs=[(AM + '14', 0)],
      caps=sh_([(0, 2.3, "NEVER GIVE IT UP AGAIN."), (2.3, 4.3, "NEVER ASK WHY WE LEFT.")], .1),
      jessie=[(0, C + 'glasses-worn-02')]),
 dict(mode='off', screen='p5_off', audio=[('p5', .1)], figs=[(RM + '10', 0)],
      caps=sh_([(0, 2.6, "IT WILL BE BUILT WITH COMMERCIAL AND INTERNATIONAL PARTNERS,"), (2.6, 4.3, "TO PREPARE FOR MARS.")], .1),
      jessie=[(0, C + 'no-glasses-03'), (3.0, C + 'glasses-lowered-07')]),
 dict(mode='on', screen='p5_on', audio=[('o5', .1)], figs=[(AM + '10', 0)],
      caps=sh_([(0, 2.0, "PARTNERS MEANS CONTRACTORS."), (2.0, 5.0, "MARS MEANS MORE INVOICES.")], .1),
      jessie=[(0, C + 'glasses-worn-01')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "LOOK UP.")], brand=3.2, jessie=[(0, C + 'glasses-lowered-08')]),
]
TICK_OFF = "NASA UNVEILS $20B MOON BASE  •  LUNAR SOUTH POLE  •  ROBOTS FIRST, HUMANS LATER  •  NEXT STOP MARS  •  "
TICK_ON = "NEW INVOICE  •  HOLD THE ICE  •  NEVER ASK WHY  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'mon evening they news moon invoice.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 26.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
