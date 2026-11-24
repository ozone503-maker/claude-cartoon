import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
SAND, SKY = (225, 195, 130), (120, 180, 225)
FIRA = GF + 'firasans/FiraSans-Regular.ttf'; SERIF = GF + 'cardo/Cardo-Bold.ttf'
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def pyramid(d, cx, by, s, col, line=INK, rows=8):
    top = (cx, by - s); l = (cx - s * 1.1, by); r = (cx + s * 1.1, by)
    d.polygon([top, l, r], fill=col, outline=line); d.line([top, l, r, top], fill=line, width=5)
    for k in range(1, rows):
        y = by - s + s * k / rows; half = s * 1.1 * k / rows
        d.line((cx - half, y, cx + half, y), fill=line, width=2)

def p1_off():
    im, d = card((244, 236, 214))
    d.rectangle((0, 0, sw, 80), fill=(120, 60, 30)); d.text((30, 40), "HISTORY  •  CHAPTER 3", font=F(ARCH, 34), fill=WHITE, anchor='lm')
    d.rectangle((30, 110, 330, 400), fill=SKY); d.rectangle((30, 330, 330, 400), fill=SAND)
    pyramid(d, 180, 340, 150, (215, 185, 120))
    fit_text(d, (350, 110, sw - 30, 260), "THE GREAT PYRAMID OF KHUFU", SERIF, 60, INK)
    fit_text(d, (350, 280, sw - 30, 400), "c. 2560 B.C.", SERIF, 80, (150, 40, 20))
    fit_text(d, (30, 430, sw - 30, 520), "Built in about 20 years by the pharaoh Khufu.", SERIF, 40, (70, 60, 50)); return im
def stamp(im, text, cx, cy, size=120, rot=-10, col=INK):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); f = F(ANTON, size)
    w = ld.textlength(text, font=f)
    ld.rectangle((cx - w / 2 - 30, cy - size * .7, cx + w / 2 + 30, cy + size * .7), outline=col + (240,), width=12)
    ld.text((cx, cy), text, font=f, fill=col + (240,), anchor='mm')
    lay = lay.rotate(rot, resample=Image.BICUBIC, center=(cx, cy)); im.paste(lay, (0, 0), lay)
def p1_on():
    im, d = card(GREY); pyramid(d, 180, 300, 170, (200, 200, 200))
    stamp(im, "CASE CLOSED", 260, 230, 100)
    fit_text(d, (30, 400, X1, 520), "DO NOT MEASURE.", ANTON, 110, INK); return im

def blocks(d, on):
    # cross-section: core blocks with casing on part, erosion marks on exposed part
    base = 420; c1 = (205, 180, 125) if not on else (190, 190, 190); c2 = (240, 228, 200) if not on else (225, 225, 225)
    for i in range(5):
        x = 40 + i * 120; d.rectangle((x, base - 220, x + 115, base), fill=c1, outline=INK, width=4)
    # casing over right three blocks (removed now: dashed outline)
    for i in range(2, 5):
        x = 40 + i * 120; d.rectangle((x, base - 260, x + 115, base - 220), fill=c2 if i == 4 else None, outline=INK, width=3)
    # deep erosion on left (exposed since construction), shallow on right
    for i in range(2):
        x = 40 + i * 120
        for k in range(7): d.arc((x + 5 + k * 15, base - 235, x + 25 + k * 15, base - 205), 0, 180, fill=INK, width=4)
    for i in range(2, 4):
        x = 40 + i * 120
        for k in range(7): d.line((x + 8 + k * 15, base - 220, x + 14 + k * 15, base - 215), fill=INK, width=2)
def p2_off():
    im, d = card(WHITE); blocks(d, False)
    d.multiline_text((157, 460), "EXPOSED\nSINCE BUILT", font=F(ARCH, 22), fill=INK, anchor='mm', align='center')
    d.multiline_text((397, 460), "UNCOVERED\nLATER", font=F(ARCH, 22), fill=INK, anchor='mm', align='center')
    fit_text(d, (30, 30, sw - 30, 120), "RELATIVE EROSION METHOD", ANTON, 70, INK)
    d.text((sw / 2, 135), "Preliminary report • not peer reviewed", font=F(FIRA, 26), fill=(110, 110, 110), anchor='mm'); return im
def receipt(d, x, y, w, h):
    d.rectangle((x, y, x + w, y + h), fill=WHITE, outline=INK, width=4)
    for k in range(0, w, 20): d.polygon([(x + k, y + h), (x + k + 10, y + h + 14), (x + k + 20, y + h)], fill=WHITE, outline=INK)
    d.text((x + w / 2, y + 30), "RECEIPT", font=F(ANTON, 34), fill=INK, anchor='mm')
    for k, (a, b) in enumerate([("WIND", "YES"), ("RAIN", "YES"), ("SAND", "YES"), ("TIME", "?????")]):
        yy = y + 80 + k * 38; d.text((x + 20, yy), a, font=F(ARCH, 26), fill=INK, anchor='lm'); d.text((x + w - 20, yy), b, font=F(ARCH, 26), fill=INK, anchor='rm')
def p2_on():
    im, d = card(GREY); receipt(d, 40, 40, 260, 260)
    fit_text(d, (330, 60, X1 + 40, 320), "ROCKS KEEP RECEIPTS.", ANTON, 110, INK)
    fit_text(d, (30, 340, X1, 470), "THE STONE REMEMBERS.", ANTON, 90, INK); return im

def p3_off():
    im, d = card(WHITE)
    fit_text(d, (30, 25, sw - 30, 110), "THE REPORT'S ESTIMATE", ANTON, 66, INK)
    y = 260; x0, x1 = 60, X1 + 20
    d.line((x0, y, x1, y), fill=INK, width=8)
    def xp(bc): return x0 + (37000 - bc) / (37000 - 2000) * (x1 - x0)
    d.rectangle((xp(36878), y - 30, xp(8954), y + 30), fill=(250, 210, 120), outline=INK, width=3)
    for bc, lab, col in [(22900, "~22,900 BC", (190, 40, 20)), (2560, "2560 BC", INK)]:
        X = xp(bc); d.line((X, y - 60, X, y + 60), fill=col, width=8)
        d.text((X, y - 90), lab, font=F(ARCH, 30), fill=col, anchor='mm')
    d.text((xp(22900), y + 100), "range: 36,878 – 8,954 BC", font=F(FIRA, 28), fill=(90, 90, 90), anchor='mm')
    fit_text(d, (30, 400, X1, 500), "Khufu may have renovated a much older structure", SERIF, 44, INK); return im
def p3_on():
    im, d = card(GREY); pyramid(d, 190, 330, 170, (200, 200, 200))
    d.rectangle((90, 180, 290, 240), fill=WHITE, outline=INK, width=5); d.text((190, 210), "KHUFU", font=F(ANTON, 48), fill=INK, anchor='mm')
    d.rectangle((300, 290, 360, 340), fill=(120, 120, 120), outline=INK, width=4)   # paint bucket
    d.line((360, 250, 300, 300), fill=INK, width=6)
    fit_text(d, (380, 60, X1 + 40, 330), "PAINT YOUR NAME ON IT.", ANTON, 90, INK)
    fit_text(d, (30, 390, X1, 520), "CALL IT YOURS.", ANTON, 110, INK); return im

def p4_off():
    im, d = card(WHITE)
    d.rectangle((40, 40, 320, 420), fill=(250, 248, 240), outline=INK, width=5)
    for k in range(9): d.line((70, 90 + k * 34, 290, 90 + k * 34), fill=(150, 150, 150), width=4)
    stamp(im, "NOT PEER REVIEWED", 300, 260, 70, rot=12, col=RED)
    fit_text(d, (350, 360, sw - 30, 520), "“Nothing to see here.”", SERIF, 56, INK); return im
def gate(d, cx, cy, s, col):
    for k in range(7): d.line((cx - s + k * s / 3, cy - s, cx - s + k * s / 3, cy + s), fill=col, width=10)
    d.line((cx - s, cy - s, cx + s, cy - s), fill=col, width=14); d.line((cx - s, cy, cx + s, cy), fill=col, width=10)
    d.rounded_rectangle((cx - 30, cy + 10, cx + 30, cy + 70), 8, fill=col); d.arc((cx - 22, cy - 25, cx + 22, cy + 25), 180, 360, fill=col, width=10)
def p4_on():
    im, d = card(GREY); gate(d, 170, 190, 120, INK)
    fit_text(d, (330, 50, X1 + 40, 330), "PEER REVIEW.", ANTON, 110, INK)
    fit_text(d, (30, 360, X1, 520), "PERMISSION FROM THE PEOPLE WHO WROTE THE TEXTBOOK.", ANTON, 70, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3); fs = 175; T = "MEASURE IT YOURSELF"
    while ld.textlength(T, font=F(ANTON, fs)) > sw - 90: fs -= 5
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .35; L = rng.uniform(30, 150)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(p1_off=p1_off, p1_on=p1_on, p2_off=p2_off, p2_on=p2_on, p3_off=p3_off, p3_on=p3_on, p4_off=p4_off, p4_on=p4_on, end=end, end_g=end_g)

C = 'jessie-cool-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='p1_off', audio=[('p1', .3)], figs=[(RM + '05', 0)],
      caps=sh_([(0, 3.2, "THE GREAT PYRAMID WAS BUILT FOR THE PHARAOH KHUFU,"), (3.2, 6.4, "AROUND 2560 B.C."), (6.4, 8.3, "THE CASE IS CLOSED.")], .3),
      jessie=[(0, C + 'no-glasses-03'), (6.4, C + 'glasses-lowered-05')]),
 dict(mode='on', screen='p1_on', audio=[('o1', .1)], figs=[(AM + '05', 0)],
      caps=sh_([(0, 1.5, "CASE CLOSED."), (1.5, 3.3, "DO NOT MEASURE.")], .1),
      jessie=[(0, C + 'glasses-worn-05')]),
 dict(mode='off', screen='p2_off', audio=[('p2', .1)], figs=[(RM + '09', 0)],
      caps=sh_([(0, 3.6, "IN JANUARY, AN ENGINEER POSTED A PRELIMINARY REPORT."), (3.6, 7.8, "HE COMPARED EROSION ON STONE EXPOSED SINCE CONSTRUCTION,"), (7.8, 11.5, "WITH STONE UNCOVERED ONLY AFTER THE CASING WAS STRIPPED AWAY.")], .1),
      jessie=[(0, C + 'no-glasses-05'), (9.0, C + 'glasses-lowered-04')]),
 dict(mode='on', screen='p2_on', audio=[('o2', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0, 3.3, "ROCKS KEEP RECEIPTS.")], .1),
      jessie=[(0, C + 'glasses-worn-07')]),
 dict(mode='off', screen='p3_off', audio=[('p3', .1)], figs=[(RM + '10', 0)],
      caps=sh_([(0, 3.9, "HIS CALCULATION AVERAGES AROUND 23,000 B.C."), (3.9, 9.4, "AND HE SUGGESTS KHUFU MAY HAVE RENOVATED A MUCH OLDER STRUCTURE.")], .1),
      jessie=[(0, C + 'no-glasses-07'), (7.0, C + 'glasses-lowered-01')]),
 dict(mode='on', screen='p3_on', audio=[('o3', .1)], figs=[(AM + '10', 0)],
      caps=sh_([(0, 1.6, "PAINT YOUR NAME ON IT."), (1.6, 3.4, "CALL IT YOURS.")], .1),
      jessie=[(0, C + 'glasses-worn-04')]),
 dict(mode='off', screen='p4_off', audio=[('p4', .1)], figs=[(RM + '14', 0)],
      caps=sh_([(0, 2.0, "IT'S NOT PEER REVIEWED."), (2.0, 4.3, "THERE'S NOTHING TO SEE HERE.")], .1),
      jessie=[(0, C + 'no-glasses-02'), (2.4, C + 'glasses-lowered-03')]),
 dict(mode='on', screen='p4_on', audio=[('o4', .1)], figs=[(AM + '14', 0)],
      caps=sh_([(0, 1.0, "PEER REVIEW."), (1.0, 3.7, "PERMISSION FROM THE PEOPLE WHO WROTE THE TEXTBOOK.")], .1),
      jessie=[(0, C + 'glasses-worn-02')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "MEASURE IT YOURSELF.")], brand=3.2, jessie=[(0, C + 'glasses-lowered-08')]),
]
TICK_OFF = "GREAT PYRAMID: c. 2560 BC  •  ENGINEER'S REPORT CLAIMS FAR OLDER DATE  •  NOT PEER REVIEWED  •  "
TICK_ON = "CASE CLOSED  •  DO NOT MEASURE  •  ROCKS KEEP RECEIPTS  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'mon afternoon they news pyramid receipts.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 16.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
