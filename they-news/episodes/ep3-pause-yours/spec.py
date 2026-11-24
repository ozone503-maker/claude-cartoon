import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
FIRA = GF + 'firasans/FiraSans-Regular.ttf'; FIRAB = GF + 'firasans/FiraSans-Black.ttf'
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def avatar(d, on):
    d.ellipse((30, 30, 130, 130), fill=(150, 150, 150) if not on else (120, 120, 120))
    d.ellipse((62, 50, 98, 86), fill=(210, 210, 210)); d.chord((45, 85, 115, 150), 180, 360, fill=(210, 210, 210))
    d.text((150, 62), "Bernie Sanders", font=F(ARCH, 40), fill=INK, anchor='lm')
    d.text((150, 108), "@BernieSanders", font=F(FIRA, 32), fill=(100, 100, 100), anchor='lm')

def tw1_off():
    im, d = card((255, 255, 255)); avatar(d, False)
    fit_text(d, (30, 170, sw - 30, 470), "PAUSE ADVANCED AI DEVELOPMENT BEFORE IT’S TOO LATE", FIRAB, 70, INK, align='left', lh=1.15)
    d.text((30, 515), "Posted on X", font=F(FIRA, 28), fill=(110, 110, 110), anchor='lm'); return im
def tw1_on():
    im, d = card(GREY); avatar(d, True)
    fit_text(d, (30, 170, sw - 30, 520), "PAUSE YOURS.\nNOT OURS.", ANTON, 150, INK); return im

def robot(d, cx, cy, s, col, bg):
    d.rounded_rectangle((cx - s, cy - s * .8, cx + s, cy + s * .8), 20, fill=col)
    d.line((cx, cy - s * .8, cx, cy - s * 1.2), fill=col, width=10); d.ellipse((cx - 16, cy - s * 1.2 - 16, cx + 16, cy - s * 1.2 + 16), fill=col)
    for ex in (-.45, .45): d.ellipse((cx + ex * s - 22, cy - 30, cx + ex * s + 22, cy + 14), fill=bg)
    d.rectangle((cx - s * .5, cy + s * .35, cx + s * .5, cy + s * .5), fill=bg)
def sci_off():
    im, d = card((40, 70, 140)); robot(d, sw / 2, 150, 90, WHITE, (40, 70, 140))
    fit_text(d, (30, 290, sw - 170, 520), "SCIENTISTS WARN: AI INDEPENDENT OF HUMAN CONTROL", ANTON, 90, WHITE); return im
def sci_on():
    im, d = card(GREY); robot(d, sw / 2, 150, 90, INK, GREY)
    fit_text(d, (30, 290, sw - 170, 520), "INDEPENDENT OF OUR CONTROL", ANTON, 120, INK); return im

def num_off():
    im, d = card((120, 20, 25)); X1 = sw - 170; L = (255, 220, 200)
    fit_text(d, (30, 30, X1, 200), "10\u201320%", ANTON, 170, WHITE)
    fit_text(d, (30, 205, X1, 260), "CHANCE OF WIPING OUT HUMANITY", ARCH, 30, L)
    d.line((60, 290, X1 - 30, 290), fill=L, width=3)
    fit_text(d, (30, 310, X1, 450), "COIN FLIP", ANTON, 130, WHITE)
    fit_text(d, (30, 455, X1, 515), "LOSS OF HUMAN CONTROL IN 3 YEARS", ARCH, 30, L); return im
def num_on():
    im, d = card(GREY)
    fit_text(d, (30, 40, sw - 170, 260), "BE AFRAID.", ANTON, 170, INK)
    fit_text(d, (30, 280, sw - 170, 520), "FRIGHTENED PEOPLE ASK FOR LEASHES", ANTON, 90, INK); return im

BANS = ["NATIONAL DATA CENTER MORATORIUM", "PAUSE ADVANCED AI", "BAN SUPERINTELLIGENCE"]
def ban_off():
    im, d = card(WHITE)
    d.rectangle((0, 0, sw, 90), fill=(30, 50, 110)); d.text((30, 45), "THE PLAN", font=F(ARCH, 44), fill=WHITE, anchor='lm')
    for i, b in enumerate(BANS):
        y = 150 + i * 135; d.rectangle((40, y - 40, 120, y + 40), outline=INK, width=6)
        d.line((52, y, 75, y + 25, 110, y - 32), fill=(60, 150, 80), width=12)
        sz = 52
        while d.textlength(b, font=F(ANTON, sz)) > sw - 180: sz -= 2
        d.text((150, y), b, font=F(ANTON, sz), fill=INK, anchor='lm')
    return im
def ban_on():
    im, d = card(GREY); fit_text(d, (30, 40, sw - 170, 520), "ONE MIND ALLOWED.\nOURS.", ANTON, 150, INK); return im

REPLIES = [((220, 120, 40), "Gonna have China pause too?"), ((60, 130, 200), "Define advanced AI."),
           ((90, 90, 90), "It's too late, Bernie."), ((90, 160, 80), "I'd rather pause Bernie than AI.")]
ON_REP = ["FEAR THE MACHINE.", "FEAR CHINA.", "FEAR EACH OTHER.", "WHO HOLDS THE OFF SWITCH?"]
def replies(on):
    im, d = card((20, 22, 28) if not on else GREY)
    for i, (col, txt) in enumerate(REPLIES):
        y = 20 + i * 132
        d.rounded_rectangle((20, y, sw - 20, y + 118), 18, fill=(255, 255, 255), outline=INK, width=4)
        d.ellipse((38, y + 24, 108, y + 94), fill=col if not on else INK)
        t = txt if not on else ON_REP[i]; fp = ANTON if on else ARCH; sz = 52 if on else 40
        while d.textlength(t, font=F(fp, sz)) > sw - 175: sz -= 2
        d.text((130, y + 59), t, font=F(fp, sz), fill=INK, anchor='lm')
    return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3); fs = 175
    while ld.textlength("OWN YOUR AI", font=F(ANTON, fs)) > sw - 90: fs -= 5
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.text((sw / 2 + dx, sh / 2 + dy), "OWN YOUR AI", font=f, fill=(200, 20, 20, 235), anchor='mm', stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):  # drips
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + 55; L = rng.uniform(30, 160)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC); lay = lay.filter(ImageFilter.GaussianBlur(0.8))
    im.paste(lay, (0, 0), lay); return im

SCREENS = dict(tw1_off=tw1_off, tw1_on=tw1_on, sci_off=sci_off, sci_on=sci_on, num_off=num_off, num_on=num_on, ban_off=ban_off, ban_on=ban_on,
               rep_off=lambda: replies(False), rep_on=lambda: replies(True), end=end, end_g=end_g)

C = 'jessie-cool-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='tw1_off', audio=[('s1_off', .3)], figs=[(RM + '14', 0)], min=3.4,
      caps=sh_([(0, 3.6, "PAUSE ADVANCED AI DEVELOPMENT BEFORE IT'S TOO LATE.")], .3),
      jessie=[(0, C + 'no-glasses-01'), (2.4, C + 'glasses-lowered-03')]),
 dict(mode='on', screen='tw1_on', audio=[('s1_on', .1)], figs=[(AM + '14', 0)],
      caps=sh_([(0, 1.4, "PAUSE YOURS."), (1.4, 3.0, "NOT OURS.")], .1),
      jessie=[(0, C + 'glasses-worn-01')]),
 dict(mode='off', screen='sci_off', audio=[('s2_off', .1)], figs=[(RM + '10', 0)],
      caps=sh_([(0, 2.6, "LEADING SCIENTISTS ARE CONCERNED"), (2.6, 6.0, "ABOUT AI BECOMING INDEPENDENT OF HUMAN CONTROL.")], .1),
      jessie=[(0, C + 'no-glasses-03'), (4.6, C + 'glasses-lowered-05')]),
 dict(mode='on', screen='sci_on', audio=[('s2_on', .1)], figs=[(AM + '10', 0)],
      caps=sh_([(0, 2.2, "INDEPENDENT OF OUR CONTROL."), (2.2, 4.8, "THAT IS THE PROBLEM.")], .1),
      jessie=[(0, C + 'glasses-worn-05')]),
 dict(mode='off', screen='num_off', audio=[('s3_off', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 5.0, "A 10 TO 20 PERCENT CHANCE OF WIPING OUT HUMANITY."), (5.0, 7.9, "A COIN FLIP ON LOSING HUMAN CONTROL.")], .1),
      jessie=[(0, C + 'no-glasses-06'), (6.4, C + 'glasses-lowered-04')]),
 dict(mode='on', screen='num_on', audio=[('s3_on', .1)], figs=[(AW + '13', 0)],
      caps=sh_([(0, 1.3, "BE AFRAID."), (1.3, 4.1, "FRIGHTENED PEOPLE ASK FOR LEASHES.")], .1),
      jessie=[(0, C + 'glasses-worn-04')]),
 dict(mode='off', screen='ban_off', audio=[('s4_off', .1)], figs=[(RM + '09', 0)],
      caps=sh_([(0, 3.0, "PASS A NATIONAL DATA CENTER MORATORIUM."), (3.0, 4.5, "PAUSE ADVANCED AI."), (4.5, 8.5, "BAN THE DEVELOPMENT OF SUPERINTELLIGENCE.")], .1),
      jessie=[(0, C + 'no-glasses-05'), (7.0, C + 'glasses-lowered-07')]),
 dict(mode='on', screen='ban_on', audio=[('s4_on', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0, 1.5, "ONE MIND ALLOWED."), (1.5, 2.8, "OURS."), (2.8, 5.6, "DO NOT BUILD YOUR OWN.")], .1),
      jessie=[(0, C + 'glasses-worn-07')]),
 dict(mode='off', screen='rep_off', audio=[('r1', .1), ('r2', 3.3), ('r3', 4.5), ('r4', 6.0)], figs=[(RW + '12', 0, .78), (RM + '07', -235, .78)],
      caps=[(.1, 3.3, "GONNA HAVE CHINA PAUSE TOO?"), (3.3, 5.0, "DEFINE ADVANCED AI."), (5.0, 6.4, "IT'S TOO LATE, BERNIE."), (6.4, 9.0, "I'D RATHER PAUSE BERNIE THAN AI!")],
      jessie=[(0, C + 'no-glasses-02'), (6.0, C + 'glasses-lowered-02')], pad=0.2),
 dict(mode='on', screen='rep_on', audio=[('s5_on', .1)], figs=[(AW + '12', 0, .78), (AM + '07', -235, .78)],
      caps=sh_([(0, 1.4, "FEAR THE MACHINE."), (1.4, 2.8, "FEAR CHINA."), (2.8, 4.4, "FEAR EACH OTHER."), (4.4, 7.3, "NEVER ASK WHO HOLDS THE OFF SWITCH.")], .1),
      jessie=[(0, C + 'glasses-worn-02')]),
 dict(mode='on', screen=lambda r: 'end' if r < 2.2 else 'end_g', audio=[('obey', .3), ('tag', 4.15)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.8,
      caps=[(.2, 2.2, "OBEY."), (2.2, 3.8, "OWN YOUR AI.")], brand=3.8, jessie=[(0, C + 'glasses-lowered-08')]),
]
TICK_OFF = "SENATOR: PAUSE ADVANCED AI  •  DATA CENTER MORATORIUM PROPOSED  •  BAN ON SUPERINTELLIGENCE  •  "
TICK_ON = "ONLY WE MAY THINK  •  FEAR THE MACHINE  •  DO NOT BUILD YOUR OWN  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'mon afternoon they news pause yours.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 20.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], s['start'], s['end'])
