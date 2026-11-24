import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
UN = (0, 140, 200); HOT = (230, 90, 30)
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def stamp(im, txt, cx, cy, size=90, col=(200, 25, 25), ang=14):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); f = F(ANTON, size)
    w = ld.textlength(txt, font=f)
    ld.rectangle((cx - w / 2 - 20, cy - size * .62, cx + w / 2 + 20, cy + size * .62), outline=col + (230,), width=8)
    ld.text((cx, cy), txt, font=f, fill=col + (230,), anchor='mm')
    lay = lay.rotate(ang, center=(cx, cy), resample=Image.BICUBIC); im.paste(lay, (0, 0), lay)

def thermo(d, x, y, h, frac, col, line):
    d.rounded_rectangle((x, y, x + 50, y + h), 25, fill=WHITE, outline=line, width=5)
    d.ellipse((x - 20, y + h - 30, x + 70, y + h + 60), fill=col, outline=line, width=5)
    d.rectangle((x + 12, y + h - h * frac, x + 38, y + h + 10), fill=col)

def f1_off():
    im, d = card((255, 240, 225))
    thermo(d, 70, 60, 330, .92, HOT, INK)
    d.text((300, 90), "WORST CASE", font=F(ARCH, 40), fill=INK, anchor='lm')
    fit_text(d, (300, 130, sw - 30, 290), "+4.5°C", ANTON, 150, HOT, align='left')
    d.text((300, 320), "BY 2100  •  RCP8.5", font=F(ARCH, 32), fill=INK, anchor='lm')
    stamp(im, "RETIRED", 430, 430, 80); return im
def o1_on():
    im, d = card(GREY)
    heads = ["DOOM BY 2100", "BUSINESS AS USUAL", "+4.5°C"]
    for k, h in enumerate(heads):
        x, y = 30 + k * 20, 40 + k * 70
        d.rectangle((x, y, x + 300, y + 150), fill=WHITE, outline=INK, width=4)
        fit_text(d, (x + 12, y + 10, x + 288, y + 70), h, ANTON, 50, INK)
    d.text((70, 330), "*retired", font=F(ARCH, 16), fill=INK, anchor='lm')
    fit_text(d, (370, 40, X1 + 40, 320), "15 YEARS OF HEADLINES.", ANTON, 100, INK)
    fit_text(d, (30, 380, X1, 510), "RETIRED IN A FOOTNOTE.", ANTON, 100, INK); return im

def f2_off():
    im, d = card(WHITE); d.rectangle((0, 0, sw, 90), fill=UN)
    d.text((sw / 2, 45), "SCENARIO MODELING", font=F(ARCH, 40), fill=WHITE, anchor='mm')
    d.line((80, 440, 80, 140), fill=INK, width=5); d.line((80, 440, X1 + 40, 440), fill=INK, width=5)
    pts = [(80, 430), (200, 400), (320, 340), (440, 240), X1 + 30 > 540 and (540, 150) or (X1 + 30, 150)]
    d.line(pts, fill=HOT, width=8)
    d.text((300, 170), "STRESS TEST", font=F(ANTON, 60), fill=INK, anchor='mm')
    d.text((300, 500), "NOT A FORECAST", font=F(ARCH, 40), fill=UN, anchor='mm'); return im
def o2_on():
    im, d = card(GREY)
    for k in range(6):
        x = 30 + (k % 3) * 105; y = 40 + (k // 3) * 150
        d.rectangle((x, y, x + 95, y + 135), fill=WHITE, outline=INK, width=3)
        d.rectangle((x + 8, y + 10, x + 87, y + 30), fill=INK); d.text((x + 47, y + 70), "8.5", font=F(ANTON, 40), fill=INK, anchor='mm')
    fit_text(d, (370, 40, X1 + 40, 330), "THEN WHY WAS IT", ANTON, 100, INK)
    fit_text(d, (30, 360, X1, 510), "ON EVERY FRONT PAGE?", ANTON, 100, INK); return im

def f3_off():
    im, d = card((220, 240, 255))
    d.ellipse((50, 50, 190, 190), fill=(255, 210, 60), outline=INK, width=4)
    for k in range(4):
        x = 60 + k * 70; d.polygon([(x, 380), (x + 60, 380), (x + 80, 300), (x + 20, 300)], fill=(40, 70, 140), outline=INK)
    tx = 420; d.line((tx, 420, tx, 180), fill=INK, width=8)
    for a in (90, 210, 330):
        r = math.radians(a); d.line((tx, 180, tx + 110 * math.cos(r), 180 - 110 * math.sin(r)), fill=INK, width=10)
    d.rectangle((0, 420, sw, sh), fill=(120, 180, 90))
    fit_text(d, (30, 440, X1 + 40, 530), "CLEAN ENERGY GREW FASTER", ANTON, 60, INK); return im
def o3_on():
    im, d = card(GREY)
    d.rectangle((40, 50, 320, 330), fill=WHITE, outline=INK, width=5)
    d.text((180, 100), "PROPHECY", font=F(ANTON, 50), fill=INK, anchor='mm')
    d.text((180, 170), "+4.5°C", font=F(ANTON, 60), fill=INK, anchor='mm')
    d.line((60, 70, 300, 310), fill=INK, width=10); d.line((300, 70, 60, 310), fill=INK, width=10)
    fit_text(d, (350, 40, X1 + 40, 330), "THE PROPHECY FAILED.", ANTON, 100, INK)
    fit_text(d, (30, 370, X1, 510), "THE PROPHETS TOOK CREDIT.", ANTON, 90, INK); return im

def f4_off():
    im, d = card(WHITE); d.rectangle((0, 0, sw, 90), fill=UN)
    d.text((sw / 2, 45), "UN PROJECTION", font=F(ARCH, 40), fill=WHITE, anchor='mm')
    cx, cy, r = 260, 420, 150
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(240, 240, 240), outline=INK, width=5)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 290, 320, fill=HOT)
    a = math.radians(-55); d.line((cx, cy, cx + 130 * math.cos(a), cy + 150 * math.sin(a)), fill=INK, width=8)
    fit_text(d, (40, 100, X1 + 40, 250), "2.6\u20132.8\u00b0C", ANTON, 120, HOT)
    d.text((260, 470), "UNDER CURRENT POLICIES", font=F(ARCH, 32), fill=INK, anchor='mm'); return im
def o4_on():
    im, d = card(GREY)
    d.rectangle((30, 40, 330, 340), fill=WHITE, outline=INK, width=5)
    d.text((180, 85), "INVOICE", font=F(ANTON, 50), fill=INK, anchor='mm')
    for k, (a, b) in enumerate([("4.5°C FEAR", "PAID"), ("2.7°C FEAR", "DUE"), ("MANDATES", "DUE")]):
        yy = 160 + k * 50; d.text((45, yy), a, font=F(ARCH, 26), fill=INK, anchor='lm'); d.text((315, yy), b, font=F(ARCH, 26), fill=INK, anchor='rm')
    fit_text(d, (360, 40, X1 + 40, 330), "NEW NUMBER. SAME FEAR.", ANTON, 100, INK)
    fit_text(d, (30, 380, X1, 510), "SAME INVOICE.", ANTON, 110, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(7); fs = 175; T = "READ THE\nFOOTNOTES"; fs = 150
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 150)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(f1_off=f1_off, o1_on=o1_on, f2_off=f2_off, o2_on=o2_on, f3_off=f3_off, o3_on=o3_on, f4_off=f4_off, o4_on=o4_on, end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='f1_off', audio=[('f1', .3)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 4.3, "CLIMATE RESEARCHERS HAVE RETIRED RCP8.5,"), (4.3, 10.0, "THE WORST-CASE SCENARIO THAT PROJECTED ABOUT 4.5 DEGREES OF WARMING BY 2100.")], .3),
      jessie=[(0, N + '01'), (8.6, L + '05')]),
 dict(mode='on', screen='o1_on', audio=[('o1', .1)], figs=[(AW + '10', 0)],
      caps=sh_([(0, 2.2, "FIFTEEN YEARS OF HEADLINES."), (2.2, 4.2, "RETIRED IN A FOOTNOTE.")], .1),
      jessie=[(0, C + '05')]),
 dict(mode='off', screen='f2_off', audio=[('f2', .1)], figs=[(RM + '14', 0)],
      caps=sh_([(0, 3.0, "RESEARCHERS SAY IT WAS ALWAYS A STRESS TEST."), (3.0, 4.3, "NEVER A FORECAST.")], .1),
      jessie=[(0, N + '05'), (3.0, L + '04')]),
 dict(mode='on', screen='o2_on', audio=[('o2', .1)], figs=[(AM + '14', 0)], min=3.8,
      caps=sh_([(0, 3.3, "THEN WHY WAS IT ON EVERY FRONT PAGE?")], .1),
      jessie=[(0, C + '07')]),
 dict(mode='off', screen='f3_off', audio=[('f3', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 3.5, "SCIENTISTS SAY THE WORST CASE BECAME IMPLAUSIBLE,"), (3.5, 6.6, "BECAUSE CLEAN ENERGY GREW FASTER THAN EXPECTED.")], .1),
      jessie=[(0, N + '07'), (5.2, L + '01')]),
 dict(mode='on', screen='o3_on', audio=[('o3', .1)], figs=[(AW + '13', 0)],
      caps=sh_([(0, 1.8, "THE PROPHECY FAILED."), (1.8, 3.8, "THE PROPHETS TOOK CREDIT.")], .1),
      jessie=[(0, C + '04')]),
 dict(mode='off', screen='f4_off', audio=[('f4', .1)], figs=[(RM + '10', 0)],
      caps=sh_([(0, 3.3, "THE UN STILL PROJECTS 2.6 TO 2.8 DEGREES OF WARMING"), (3.3, 6.6, "UNDER CURRENT POLICIES.")], .1),
      jessie=[(0, N + '02'), (5.2, L + '07')]),
 dict(mode='on', screen='o4_on', audio=[('o4', .1)], figs=[(AM + '10', 0)], min=4.4,
      caps=sh_([(0, 1.1, "NEW NUMBER."), (1.1, 2.5, "SAME FEAR."), (2.5, 3.9, "SAME INVOICE.")], .1),
      jessie=[(0, C + '02')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "READ THE FOOTNOTES.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "WORST-CASE CLIMATE SCENARIO RETIRED  •  RCP8.5  •  STRESS TEST, NOT A FORECAST  •  2.6–2.8°C  •  "
TICK_ON = "RETIRED IN A FOOTNOTE  •  EVERY FRONT PAGE  •  SAME FEAR  •  SAME INVOICE  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'tue morning they news worst case.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 12.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
