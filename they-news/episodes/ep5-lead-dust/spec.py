import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
OLIVE = (70, 80, 50); FIRA = GF + 'firasans/FiraSans-Regular.ttf'
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def army_off():
    im, d = card(WHITE)
    d.rectangle((0, 0, sw, 100), fill=OLIVE); d.text((sw / 2, 50), "U.S. ARMY PUBLIC ADVISORY", font=F(ARCH, 40), fill=WHITE, anchor='mm')
    fit_text(d, (40, 130, sw - 40, 290), "CONTROLLED DETONATION", ANTON, 110, INK)
    fit_text(d, (40, 300, sw - 40, 360), "IOWA ARMY AMMUNITION PLANT", ARCH, 36, (80, 80, 80))
    d.rectangle((60, 400, sw - 60, 500), fill=OLIVE)
    fit_text(d, (80, 410, sw - 80, 490), "SAFE • CONTROLLED • RESPONSIBLE", ARCH, 40, WHITE); return im
def army_on():
    im, d = card(GREY)
    d.rectangle((50, 60, 330, 220), fill=(200, 200, 200), outline=INK, width=6)   # bunker
    d.chord((50, -40, 330, 160), 180, 360, fill=(160, 160, 160), outline=INK, width=6)
    for i in range(4): d.rectangle((80 + i * 60, 150, 120 + i * 60, 210), fill=(90, 90, 90), outline=INK, width=3)
    d.text((190, 250), "20 YEARS", font=F(ANTON, 52), fill=INK, anchor='mm')
    fit_text(d, (30, 290, X1, 520), "NOW IT'S URGENT.", ANTON, 150, INK); return im

def plume_map(d, on):
    fg = (110, 160, 90) if not on else (200, 200, 200); d.rectangle((0, 0, sw, sh), fill=fg)
    for i in range(0, sw, 70): d.line((i, 0, i - 120, sh), fill=(100, 145, 80) if not on else (185, 185, 185), width=6)
    d.line((0, 330, sw, 300), fill=(60, 60, 60), width=10)
    cx, cy = 230, 330
    for r, c in [(230, (255, 230, 120)), (160, (255, 190, 80)), (90, (240, 120, 60))]:
        col = c if not on else tuple([int(sum(c) / 3 * .8)] * 3)
        lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r * .6, cx + r * 1.4, cy + r * .6), fill=col + (110,))
        return_lay = lay
        d._image.paste(lay, (0, 0), lay)
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=INK)
def plume_off():
    im, d = card(); plume_map(d, False)
    d.rectangle((20, 20, sw - 160, 140), fill=WHITE, outline=INK, width=4)
    fit_text(d, (35, 25, sw - 175, 135), "PLUME LINGERS UP TO 1 HOUR\nTHEN: CLEAN YOUR WINDOWSILLS", ARCH, 34, INK, lh=1.25, minsize=14); return im
def plume_on():
    im, d = card(GREY)
    d.rectangle((40, 40, 250, 260), fill=WHITE, outline=INK, width=8); d.line((145, 40, 145, 260), fill=INK, width=6); d.line((40, 150, 250, 150), fill=INK, width=6)
    d.rectangle((25, 260, 265, 290), fill=(150, 150, 150), outline=INK, width=4)
    for k in range(6): d.ellipse((40 + k * 35, 266, 52 + k * 35, 278), fill=INK)   # dust on sill
    fit_text(d, (280, 40, X1 + 150, 280), "WE MAKE THE DUST.", ANTON, 90, INK)
    fit_text(d, (30, 310, X1, 520), "YOU WIPE THE WINDOWSILLS.", ANTON, 110, INK); return im

TWEET = ("Tomorrow there is a planned detonation... of approximately 5 tons of lead azide... "
         "this blast could contaminate hundreds of miles of homes, farmland, livestock, and water resources... I'm praying for everyone in harms way.")
def tweet(on):
    im, d = card((255, 255, 255) if not on else GREY)
    d.ellipse((30, 30, 130, 130), fill=(150, 150, 150)); d.ellipse((62, 50, 98, 86), fill=(210, 210, 210)); d.chord((45, 85, 115, 150), 180, 360, fill=(210, 210, 210))
    d.text((150, 62), "Marjorie Taylor Greene", font=F(ARCH, 36), fill=INK, anchor='lm')
    d.text((150, 108), "Former Congresswoman", font=F(FIRA, 30), fill=(100, 100, 100), anchor='lm')
    if not on:
        fit_text(d, (30, 160, sw - 30, 470), TWEET, FIRA, 40, INK, align='left', lh=1.2)
        d.text((30, 515), "14K likes · 793K views", font=F(FIRA, 28), fill=(110, 110, 110), anchor='lm')
    else:
        fit_text(d, (30, 160, X1, 400), "THE PLUME FADES IN AN HOUR.", ANTON, 100, INK)
        d.rectangle((30, 420, X1, 520), fill=INK); fit_text(d, (40, 425, X1 - 10, 515), "THE OUTRAGE NEVER DOES.", ANTON, 70, GREY)
    return im

REPLIES = [((220, 120, 40), "Just get a ROBOT to add the chemical!"), ((200, 50, 60), "This is an act of war!"),
           ((60, 130, 200), "It's controlled, you moron!"), ((90, 160, 80), "Leaving out a few critical details...")]
def replies(on):
    im, d = card((20, 22, 28) if not on else GREY)
    for i, (col, txt) in enumerate(REPLIES):
        y = 20 + i * 132
        d.rounded_rectangle((20, y, sw - 20, y + 118), 18, fill=(255, 255, 255), outline=INK, width=4)
        d.ellipse((38, y + 24, 108, y + 94), fill=col if not on else INK)
        t = txt if not on else ["PANIC.", "MOCK.", "PANIC.", "MOCK."][i]; fp = ANTON if on else ARCH; sz = 60 if on else 40
        while d.textlength(t, font=F(fp, sz)) > sw - 175: sz -= 2
        d.text((130, y + 59), t, font=F(fp, sz), fill=INK, anchor='lm')
    return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3); fs = 175; T = "READ IT YOURSELF"
    while ld.textlength(T, font=F(ANTON, fs)) > sw - 90: fs -= 5
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .35; L = rng.uniform(30, 150)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(army_off=army_off, army_on=army_on, plume_off=plume_off, plume_on=plume_on, tw_off=lambda: tweet(False), tw_on=lambda: tweet(True),
               rep_off=lambda: replies(False), rep_on=lambda: replies(True), end=end, end_g=end_g)

C = 'jessie-cool-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='army_off', audio=[('a1_off', .3)], figs=[(RM + '14', 0)],
      caps=sh_([(0, 4.5, "THE U.S. ARMY WILL CONDUCT TWO CONTROLLED DETONATIONS OF DEGRADED LEAD AZIDE,"), (4.5, 8.8, "TO SAFELY DISPOSE OF UNSTABLE MATERIAL.")], .3),
      jessie=[(0, C + 'no-glasses-01'), (6.6, C + 'glasses-lowered-05')]),
 dict(mode='on', screen='army_on', audio=[('a1_on', .1)], figs=[(AM + '14', 0)],
      caps=sh_([(0, 1.5, "TWENTY YEARS IN A BUNKER."), (1.5, 3.4, "NOW IT'S URGENT.")], .1),
      jessie=[(0, C + 'glasses-worn-05')]),
 dict(mode='off', screen='plume_off', audio=[('a2_off', .1)], figs=[(RM + '09', 0)],
      caps=sh_([(0, 3.8, "THE ARMY HAS TAKEN EXTRAORDINARY MEASURES TO MITIGATE THE PLUME."), (3.8, 8.2, "AFTERWARD, RESIDENTS SHOULD CLEAN PLAY SURFACES AND WINDOWSILLS.")], .1),
      jessie=[(0, C + 'no-glasses-03'), (6.2, C + 'glasses-lowered-04')]),
 dict(mode='on', screen='plume_on', audio=[('a2_on', .1)], figs=[(AM + '09', 0)],
      caps=sh_([(0, 2.2, "WE MAKE THE DUST."), (2.2, 4.8, "YOU WIPE THE WINDOWSILLS.")], .1),
      jessie=[(0, C + 'glasses-worn-07')]),
 dict(mode='off', screen='tw_off', audio=[('a3_off', .1)], figs=[(RW + '12', 0)],
      caps=sh_([(0, 4.2, "THIS BLAST COULD CONTAMINATE HUNDREDS OF MILES"), (4.2, 7.0, "OF HOMES, FARMLAND, LIVESTOCK, AND WATER."), (7.0, 8.9, "IT'S TRULY AWFUL."), (8.9, 11.5, "I'M PRAYING FOR EVERYONE IN HARM'S WAY.")], .1),
      jessie=[(0, C + 'no-glasses-06'), (9.0, C + 'glasses-lowered-07')]),
 dict(mode='on', screen='tw_on', audio=[('a3_on', .1)], figs=[(AW + '12', 0)],
      caps=sh_([(0, 1.9, "THE PLUME FADES IN AN HOUR."), (1.9, 4.2, "THE OUTRAGE NEVER DOES.")], .1),
      jessie=[(0, C + 'glasses-worn-02')]),
 dict(mode='off', screen='rep_off', audio=[('r1', .1), ('r2', 2.9), ('r3', 6.4)], figs=[(RW + '12', 0, .78), (RM + '07', -235, .78)],
      caps=[(.1, 2.9, "JUST GET A ROBOT TO ADD THE CHEMICAL!"), (2.9, 6.4, "THIS IS AN ACT OF WAR!"), (6.4, 8.2, "IT'S CONTROLLED, YOU MORON!")],
      jessie=[(0, C + 'no-glasses-02'), (6.4, C + 'glasses-lowered-02')], pad=0.2),
 dict(mode='on', screen='rep_on', audio=[('a4_on', .1)], figs=[(AW + '12', 0, .78), (AM + '07', -235, .78)],
      caps=sh_([(0, 0.9, "PANIC."), (0.9, 1.9, "MOCK."), (1.9, 2.9, "PANIC."), (2.9, 3.6, "MOCK."), (3.6, 5.5, "NOBODY READS THE PERMIT.")], .1),
      jessie=[(0, C + 'glasses-worn-04')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "READ IT YOURSELF.")], brand=3.2, jessie=[(0, C + 'glasses-lowered-08')]),
]
TICK_OFF = "ARMY TO DETONATE LEAD AZIDE IN MIDDLETOWN, IOWA  •  RESIDENTS ADVISED TO STAY INDOORS  •  EXTRAORDINARY MEASURES TAKEN  •  "
TICK_ON = "WIPE THE WINDOWSILLS  •  PANIC  •  MOCK  •  NOBODY READS THE PERMIT  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'mon afternoon they news lead dust.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 12.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
