import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
FIRA = GF + 'firasans/FiraSans-Regular.ttf'; COMIC = GF + 'comicrelief/ComicRelief-Bold.ttf'
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def fish(d, cx, cy, s, col, eye):
    d.ellipse((cx - s, cy - s * .5, cx + s * .7, cy + s * .5), fill=col, outline=INK, width=4)
    d.polygon([(cx + s * .6, cy), (cx + s * 1.15, cy - s * .45), (cx + s * 1.15, cy + s * .45)], fill=col, outline=INK)
    d.ellipse((cx - s * .65, cy - s * .18, cx - s * .45, cy + s * .02), fill=eye)
def microwave(d, on):
    body = (200, 200, 205) if not on else (215, 215, 215)
    d.rounded_rectangle((40, 90, 470, 420), 20, fill=body, outline=INK, width=6)
    d.rectangle((70, 120, 360, 390), fill=(255, 200, 90) if not on else (170, 170, 170), outline=INK, width=5)
    d.rectangle((380, 130, 450, 380), fill=(150, 150, 155) if not on else (190, 190, 190), outline=INK, width=4)
    for i in range(3): d.ellipse((400, 160 + i * 60, 430, 190 + i * 60), fill=INK)
    fish(d, 210, 300, 80, (150, 170, 190) if not on else (120, 120, 120), INK)
    for k in range(3):  # stink lines
        x = 150 + k * 60
        d.arc((x - 15, 60, x + 15, 120), 90, 270, fill=(120, 150, 60) if not on else INK, width=6)
        d.arc((x - 15, 20, x + 15, 70), 270, 90, fill=(120, 150, 60) if not on else INK, width=6)
def sticky(im, text, on, x=455, y=120):
    lay = Image.new('RGBA', (240, 220), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rectangle((10, 10, 230, 210), fill=(255, 235, 110) if not on else (250, 250, 250), outline=INK, width=4)
    fit_text(ld, (25, 25, 215, 195), text, COMIC if not on else ANTON, 40, INK)
    lay = lay.rotate(6, resample=Image.BICUBIC, expand=True); im.paste(lay, (x, y), lay)

def micro_off():
    im, d = card((70, 110, 120)); microwave(d, False); sticky(im, "please no fish :)", False); return im
def micro_on():
    im, d = card(GREY); microwave(d, True); sticky(im, "YOU WILL STOP.", True)
    return im

CHAT = [("she's so dramatic lol", (60, 130, 200)), ("fish is FOOD", (220, 120, 40)), ("nobody tells me what to eat", (90, 160, 80))]
def chat_off():
    im, d = card((20, 22, 28))
    d.rectangle((0, 0, sw, 70), fill=(40, 44, 56)); d.text((25, 35), "#break-room", font=F(ARCH, 34), fill=WHITE, anchor='lm')
    for i, (t, c) in enumerate(CHAT):
        y = 100 + i * 145
        d.ellipse((25, y + 15, 95, y + 85), fill=c)
        d.rounded_rectangle((115, y, X1 + 120, y + 110), 22, fill=(255, 255, 255))
        sz = 40
        while d.textlength(t, font=F(ARCH, sz)) > X1 - 20: sz -= 2
        d.text((140, y + 55), t, font=F(ARCH, sz), fill=INK, anchor='lm')
    return im
def chat_on():
    im, d = card(GREY)
    fit_text(d, (30, 30, X1, 220), "MOCKERY NOTED.", ANTON, 130, INK)
    d.rectangle((40, 270, X1, 510), outline=INK, width=6)
    for i, (t, done) in enumerate([("PHASE ONE: ASK", True), ("PHASE TWO: SUFFER", False)]):
        y = 330 + i * 110; d.rectangle((60, y - 30, 120, y + 30), outline=INK, width=5)
        if done: d.line((70, y, 88, y + 22, 115, y - 28), fill=INK, width=9)
        d.text((145, y), t, font=F(ANTON, 58), fill=INK, anchor='lm')
    return im

def rain(d, on, rng):
    for k in range(120):
        x = rng.uniform(0, sw); y = rng.uniform(0, sh); d.line((x, y, x - 10, y + 34), fill=(170, 190, 220) if not on else (120, 120, 120), width=3)
def rain_off():
    im, d = card((40, 50, 70)); rng = np.random.default_rng(5)
    d.rectangle((0, 380, sw, sh), fill=(60, 60, 70)); rain(d, False, rng)
    d.rectangle((80, 330, 460, 360), fill=(120, 80, 50), outline=INK, width=4)
    for x in (110, 430): d.rectangle((x - 8, 360, x + 8, 430), fill=(90, 60, 40))
    d.polygon([(200, 330), (330, 330), (310, 290), (220, 290)], fill=(230, 200, 140), outline=INK)  # sandwich
    d.rectangle((215, 300, 315, 312), fill=(100, 170, 80))
    d.text((sw / 2 - 60, 470), "outside the break room", font=F(COMIC, 34), fill=(220, 220, 230), anchor='mm'); return im
def rain_on():
    im, d = card(GREY); rng = np.random.default_rng(5); rain(d, True, rng)
    d.rectangle((40, 40, 300, 200), fill=WHITE, outline=INK, width=5)
    d.text((170, 85), "FORECAST", font=F(ARCH, 30), fill=INK, anchor='mm'); d.text((170, 150), "RAIN 100%", font=F(ANTON, 60), fill=INK, anchor='mm')
    d.ellipse((30, 110, 310, 195), outline=INK, width=5)
    fit_text(d, (30, 230, X1, 520), "WAIT FOR RAIN.\nSIT WHERE THEY CAN SEE YOU.", ANTON, 90, INK); return im

def sob_off():
    im, d = card((245, 225, 230))
    d.text((40, 100), "“", font=F(GF + 'cardo/Cardo-Bold.ttf', 200), fill=(200, 120, 140), anchor='lm')
    fit_text(d, (60, 150, X1, 430), "I've been struggling with severe nausea for weeks...", GF + 'cardo/Cardo-Bold.ttf', 64, INK, lh=1.15)
    for k in range(5): d.text((70 + k * 70, 480), "♥", font=F('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 46), fill=(210, 80, 110), anchor='mm')
    return im
def sob_on():
    im, d = card(GREY); fit_text(d, (30, 40, X1, 520), "I AM NOT SICK.\nI AM STRATEGIC.", ANTON, 150, INK); return im

def ban_off():
    im, d = card(WHITE)
    d.rectangle((0, 0, sw, 100), fill=(30, 50, 110)); d.text((sw / 2, 50), "OFFICE NOTICE", font=F(ARCH, 46), fill=WHITE, anchor='mm')
    fit_text(d, (40, 130, X1 + 100, 330), "NO MICROWAVING FISH IN THE OFFICE", ANTON, 100, INK)
    fish(d, sw / 2 - 60, 430, 70, (150, 170, 190), INK)
    d.line((sw / 2 - 190, 340, sw / 2 + 70, 520), fill=RED, width=16); d.line((sw / 2 + 70, 340, sw / 2 - 190, 520), fill=RED, width=16)
    return im
def ban_on():
    im, d = card(GREY); fit_text(d, (30, 40, X1, 520), "GUILT WORKS.\nFISH BANNED.", ANTON, 150, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3); fs = 175
    while ld.textlength("SHE PLAYED YOU", font=F(ANTON, fs)) > sw - 90: fs -= 5
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.text((sw / 2 + dx, sh / 2 + dy), "SHE PLAYED YOU", font=f, fill=(200, 20, 20, 235), anchor='mm', stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .35; L = rng.uniform(30, 150)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(micro_off=micro_off, micro_on=micro_on, chat_off=chat_off, chat_on=chat_on, rain_off=rain_off, rain_on=rain_on,
               sob_off=sob_off, sob_on=sob_on, ban_off=ban_off, ban_on=ban_on, end=end, end_g=end_g)

C = 'jessie-cool-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='micro_off', audio=[('n1', .3)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 3.4, "MY COWORKER ASKED US NOT TO MICROWAVE FISH IN THE OFFICE,"), (3.4, 5.3, "BECAUSE SHE DIDN'T LIKE IT.")], .3),
      jessie=[(0, C + 'no-glasses-07'), (3.8, C + 'glasses-lowered-01')]),
 dict(mode='on', screen='micro_on', audio=[('o1', .1)], figs=[(AW + '10', 0)],
      caps=sh_([(0, 1.5, "I DON'T LIKE IT."), (1.5, 3.4, "SO YOU WILL STOP.")], .1),
      jessie=[(0, C + 'glasses-worn-05')]),
 dict(mode='off', screen='chat_off', audio=[('n2', .1)], figs=[(RM + '07', 0)],
      caps=sh_([(0, 3.5, "WE LAUGHED, AND TOLD HER SHE COULDN'T DICTATE WHAT OTHER PEOPLE ATE."), (3.5, 5.2, "WE KEPT DOING IT.")], .1),
      jessie=[(0, C + 'no-glasses-02'), (3.8, C + 'glasses-lowered-03')]),
 dict(mode='on', screen='chat_on', audio=[('o2', .1)], figs=[(AW + '03', 0)],
      caps=sh_([(0, 1.3, "MOCKERY NOTED."), (1.3, 3.2, "PROCEED TO PHASE TWO.")], .1),
      jessie=[(0, C + 'glasses-worn-04')]),
 dict(mode='off', screen='rain_off', audio=[('n3', .1)], figs=[(RW + '05', 0)],
      caps=sh_([(0, 1.5, "THEN I FOUND HER OUTSIDE,"), (1.5, 2.5, "IN THE RAIN,"), (2.5, 4.7, "COVERING HER SANDWICH WITH HER JACKET.")], .1),
      jessie=[(0, C + 'no-glasses-05'), (3.4, C + 'glasses-lowered-05')]),
 dict(mode='on', screen='rain_on', audio=[('o3', .1)], figs=[(AW + '05', 0)],
      caps=sh_([(0, 2.0, "WAIT FOR RAIN."), (2.0, 4.0, "SIT WHERE THEY CAN SEE YOU.")], .1),
      jessie=[(0, C + 'glasses-worn-07')]),
 dict(mode='off', screen='sob_off', audio=[('w1', .1)], figs=[(RW + '01', 0)],
      caps=sh_([(0, 3.0, "I'VE BEEN STRUGGLING WITH SEVERE NAUSEA FOR WEEKS."), (3.0, 6.0, "AND I CAN'T AFFORD TO BUY LUNCH EVERY DAY.")], .1),
      jessie=[(0, C + 'no-glasses-06'), (4.8, C + 'glasses-lowered-04')]),
 dict(mode='on', screen='sob_on', audio=[('o4', .1)], figs=lambda r: [(AW + ('01' if r < 1.6 else '15'), 0)],
      caps=sh_([(0, 1.5, "I AM NOT SICK."), (1.5, 3.2, "I AM STRATEGIC.")], .1),
      jessie=[(0, C + 'glasses-worn-02')]),
 dict(mode='off', screen='ban_off', audio=[('n4', .1)], figs=[(RM + '10', 0)],
      caps=sh_([(0, 1.3, "I FELT TERRIBLE."), (1.3, 2.6, "WE ALL AGREED."), (2.6, 4.6, "NO MORE FISH IN THE OFFICE.")], .1),
      jessie=[(0, C + 'no-glasses-03'), (3.2, C + 'glasses-lowered-06')]),
 dict(mode='on', screen='ban_on', audio=[('o5', .1)], figs=[(AW + '07', 0)],
      caps=sh_([(0, 1.2, "GUILT WORKS."), (1.2, 2.3, "FISH BANNED."), (2.3, 3.4, "OBEY.")], .1),
      jessie=[(0, C + 'glasses-worn-08')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "SHE PLAYED YOU.")], brand=3.2, jessie=[(0, C + 'glasses-lowered-08')]),
]
TICK_OFF = "OFFICE BANS MICROWAVED FISH  •  COWORKER BRAVELY EATS IN THE RAIN  •  FAITH IN HUMANITY RESTORED  •  "
TICK_ON = "PITY IS POWER  •  CUE THE RAIN  •  YOU WILL STOP  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'mon afternoon they news fish lady.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 34.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
