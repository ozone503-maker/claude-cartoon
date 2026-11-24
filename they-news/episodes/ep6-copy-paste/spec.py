import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
FIRA = GF + 'firasans/FiraSans-Regular.ttf'; FB = (24, 119, 242)
X1 = sw - 170
MEME = "What is the mental illness called when people generate AI pictures of themselves and thank everybody that is complementing how good they look?"
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def gradient(w, h, on):
    a = np.linspace(0, 1, w)[None, :] * .6 + np.linspace(0, 1, h)[:, None] * .4
    c1, c2 = (np.array([200, 140, 180]), np.array([120, 160, 210])) if not on else (np.array([200, 200, 200]), np.array([150, 150, 150]))
    img = (c1 * (1 - a[..., None]) + c2 * a[..., None]).astype(np.uint8); return Image.fromarray(img)
def fbpost(im, d, x, y, w, h, on, scale=1.0):
    d.rectangle((x, y, x + w, y + h), fill=(255, 255, 255), outline=(180, 180, 180), width=max(1, int(2 * scale)))
    r = int(26 * scale); d.ellipse((x + 12 * scale, y + 12 * scale, x + 12 * scale + 2 * r, y + 12 * scale + 2 * r), fill=(160, 160, 160))
    d.rectangle((x + 80 * scale, y + 18 * scale, x + 80 * scale + 150 * scale, y + 34 * scale), fill=(60, 60, 60) if not on else (40, 40, 40))
    d.text((x + 80 * scale, y + 52 * scale), "Suggested for you", font=F(FIRA, max(8, int(22 * scale))), fill=(120, 120, 120), anchor='lm')
    gy = int(y + 80 * scale); gh = h - int(80 * scale) - int(8 * scale)
    g = gradient(w - int(16 * scale), gh, on); im.paste(g, (int(x + 8 * scale), gy))
    fit_text(d, (x + 20 * scale, gy + 10 * scale, x + w - 20 * scale, gy + gh - 10 * scale), MEME, ARCH, max(10, int(34 * scale)), (255, 255, 255), minsize=6)

def p1_off():
    im, d = card((230, 232, 236)); fbpost(im, d, 30, 20, sw - 60, sh - 40, False); return im
def p1_on():
    im, d = card((215, 215, 215)); cw, ch = 165, 135
    for j in range(4):
        for i in range(4):
            fbpost(im, d, 10 + i * (cw + 6), 10 + j * (ch + 4), cw, ch, True, scale=.3)
    lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rectangle((60, 190, sw - 60, 360), fill=(255, 255, 255, 235), outline=INK, width=10)
    ld.text((sw / 2, 275), "COPY / PASTE", font=F(ANTON, 120), fill=INK, anchor='mm')
    lay = lay.rotate(-8, resample=Image.BICUBIC); im.paste(lay, (0, 0), lay); return im

def p2_off():
    im, d = card(WHITE)
    d.rectangle((0, 0, sw, 90), fill=FB); d.text((30, 45), "SUGGESTED FOR YOU", font=F(ARCH, 40), fill=WHITE, anchor='lm')
    for i, (lab, num) in enumerate([("REACTIONS", "64"), ("COMMENTS", "18"), ("SHARES", "7")]):
        y = 150 + i * 130; d.text((60, y), num, font=F(ANTON, 100), fill=INK, anchor='lm'); d.text((250, y), lab, font=F(ARCH, 44), fill=(90, 90, 90), anchor='lm')
    return im
def eye(d, cx, cy, s, col):
    d.ellipse((cx - s, cy - s * .55, cx + s, cy + s * .55), outline=col, width=12)
    d.ellipse((cx - s * .35, cy - s * .35, cx + s * .35, cy + s * .35), fill=col)
def p2_on():
    im, d = card(GREY); eye(d, 200, 150, 140, INK)
    fit_text(d, (30, 280, X1, 520), "WE CHOSE YOUR OUTRAGE.", ANTON, 110, INK); return im

COMS = ["Narcissist", "Severe attention-seeking \U0001F644", "Denial", "Insanity"]
def p3(on):
    im, d = card((242, 242, 245) if not on else GREY)
    for i, t in enumerate(COMS):
        y = 20 + i * 130
        d.ellipse((25, y + 20, 95, y + 90), fill=(170, 170, 170))
        d.rounded_rectangle((110, y, X1 + 80, y + 110), 26, fill=(228, 230, 235) if not on else WHITE)
        tt = t.replace(" \U0001F644", "") if True else t
        tx = tt if not on else "POINT."; fp = ARCH if not on else ANTON; sz = 44
        while d.textlength(tx, font=F(fp, sz)) > X1 - 50: sz -= 2
        d.text((135, y + 55), tx, font=F(fp, sz), fill=INK, anchor='lm')
    return im
def mirror_on():
    im, d = card(GREY)
    d.ellipse((60, 40, 330, 330), outline=INK, width=14); d.ellipse((90, 70, 300, 300), fill=(215, 215, 215))
    d.text((195, 185), "YOU", font=F(ANTON, 80), fill=INK, anchor='mm')
    fit_text(d, (350, 60, X1, 300), "NEVER AT THE FILTER ON YOUR OWN FACE.", ANTON, 70, INK)
    fit_text(d, (30, 360, X1, 520), "POINT AT THEM.", ANTON, 120, INK); return im

def p4_off():
    im, d = card((242, 242, 245))
    d.ellipse((25, 40, 105, 120), fill=(170, 170, 170))
    d.rounded_rectangle((120, 20, sw - 30, 320), 30, fill=(228, 230, 235))
    fit_text(d, (150, 40, sw - 60, 300), "Is it really that much different than using filters, or putting on makeup? Just saying.", FIRA, 46, INK, align='left', lh=1.2)
    d.text((150, 360), "Like  ·  Reply", font=F(ARCH, 30), fill=(110, 110, 110), anchor='lm'); return im
def phone_on():
    im, d = card(GREY)
    d.rounded_rectangle((40, 30, 200, 330), 22, fill=INK); d.rounded_rectangle((52, 50, 188, 310), 12, fill=(200, 200, 200))
    d.ellipse((90, 95, 150, 165), fill=(150, 150, 150)); d.chord((75, 160, 165, 240), 180, 360, fill=(150, 150, 150))
    for k in range(3):
        y = 255 + k * 18; d.line((65, y, 175, y), fill=INK, width=3); d.ellipse((150, y - 6, 162, y + 6), fill=INK)
    fit_text(d, (220, 40, X1, 320), "EVERY FACE ONLINE IS EDITED.", ANTON, 90, INK)
    d.rectangle((30, 360, X1, 510), fill=INK); fit_text(d, (45, 370, X1 - 15, 500), "INCLUDING YOURS.", ANTON, 100, GREY); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3); fs = 175; T = "OWN YOUR FACE"
    while ld.textlength(T, font=F(ANTON, fs)) > sw - 90: fs -= 5
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .35; L = rng.uniform(30, 150)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(p1_off=p1_off, p1_on=p1_on, p2_off=p2_off, p2_on=p2_on, p3_off=lambda: p3(False), p3_on=mirror_on,
               p4_off=p4_off, p4_on=phone_on, end=end, end_g=end_g)

C = 'jessie-cool-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='p1_off', audio=[('p1_off', .3)], figs=[(RW + '12', 0)],
      caps=sh_([(0, 2.1, "WHAT IS THE MENTAL ILLNESS CALLED,"), (2.1, 4.9, "WHEN PEOPLE POST AI PICTURES OF THEMSELVES,"), (4.9, 8.0, "AND THANK EVERYONE WHO TELLS THEM HOW GOOD THEY LOOK?")], .3),
      jessie=[(0, C + 'no-glasses-06'), (6.0, C + 'glasses-lowered-05')]),
 dict(mode='on', screen='p1_on', audio=[('o1', .1)], figs=[(AW + '12', 0)],
      caps=sh_([(0, 0.9, "COPY."), (0.9, 1.8, "PASTE."), (1.8, 2.8, "REPOST."), (2.8, 4.1, "SAME WORDS."), (4.1, 6.5, "TENS OF THOUSANDS OF ACCOUNTS.")], .1),
      jessie=[(0, C + 'glasses-worn-04')]),
 dict(mode='off', screen='p2_off', audio=[('p2_off', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 1.9, "THIS POST WAS SUGGESTED FOR YOU."), (1.9, 5.2, "SIXTY-FOUR REACTIONS. SEVEN SHARES.")], .1),
      jessie=[(0, C + 'no-glasses-05'), (3.6, C + 'glasses-lowered-01')]),
 dict(mode='on', screen='p2_on', audio=[('o2', .1)], figs=[(AW + '13', 0)],
      caps=sh_([(0, 2.5, "WE CHOSE YOUR OUTRAGE."), (2.5, 4.7, "YOU CHOSE NOTHING.")], .1),
      jessie=[(0, C + 'glasses-worn-05')]),
 dict(mode='off', screen='p3_off', audio=[('c1', .1), ('c2', 1.2), ('c3', 3.4), ('c4', 4.6)], figs=[(RW + '09', 0, .78), (RM + '09', -235, .78)],
      caps=[(.1, 1.2, "NARCISSIST!"), (1.2, 3.4, "SEVERE ATTENTION SEEKING."), (3.4, 4.6, "DENIAL!"), (4.6, 6.0, "INSANITY.")],
      jessie=[(0, C + 'no-glasses-02'), (4.4, C + 'glasses-lowered-03')], pad=0.3),
 dict(mode='on', screen='p3_on', audio=[('o3', .1)], figs=[(AW + '09', 0, .78), (AM + '09', -235, .78)],
      caps=sh_([(0, 1.2, "POINT AT THEM."), (1.2, 4.4, "NEVER AT THE FILTER ON YOUR OWN FACE.")], .1),
      jessie=[(0, C + 'glasses-worn-07')]),
 dict(mode='off', screen='p4_off', audio=[('p4_off', .1)], figs=[(RM + '10', 0)],
      caps=sh_([(0, 3.7, "IS IT REALLY THAT MUCH DIFFERENT THAN USING FILTERS, OR PUTTING ON MAKEUP?"), (3.7, 5.6, "JUST SAYING.")], .1),
      jessie=[(0, C + 'no-glasses-03'), (4.0, C + 'glasses-lowered-04')]),
 dict(mode='on', screen='p4_on', audio=[('o4', .1)], figs=[(AM + '10', 0)],
      caps=sh_([(0, 2.9, "EVERY FACE ONLINE IS EDITED."), (2.9, 5.4, "INCLUDING YOURS.")], .1),
      jessie=[(0, C + 'glasses-worn-02'), (3.2, C + 'glasses-lowered-08')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "OWN YOUR FACE.")], brand=3.2, jessie=[(0, C + 'glasses-lowered-08')]),
]
TICK_OFF = "WHAT IS THE MENTAL ILLNESS CALLED  •  SUGGESTED FOR YOU  •  64 REACTIONS  •  7 SHARES  •  "
TICK_ON = "COPY  •  PASTE  •  REPOST  •  POINT AT THEM  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'mon afternoon they news copy paste.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
