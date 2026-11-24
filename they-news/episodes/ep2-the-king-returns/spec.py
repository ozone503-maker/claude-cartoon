import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED = (240, 238, 230), (12, 12, 12), (190, 30, 30)

def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def pr_off():
    im, d = card()
    d.rectangle((0, 0, sw, 90), fill=INK); d.text((30, 45), "PRESS RELEASE", font=F(ARCH, 44), fill=WHITE, anchor='lm')
    d.text((sw - 30, 45), "NOV 23", font=F(ARCH, 34), fill=(200, 200, 200), anchor='rm')
    fit_text(d, (40, 120, sw - 40, 380), "NVIDIA BOARD REINSTATES CEO", ANTON, 130, INK)
    d.rectangle((90, 400, sw - 90, 500), outline=RED, width=8)
    fit_text(d, (110, 410, sw - 110, 490), "EFFECTIVE IMMEDIATELY", ARCH, 46, RED)
    return im

def crown(d, cx, cy, s, col):
    pts = [(-1, .5), (-1, -.4), (-.5, .05), (0, -.6), (.5, .05), (1, -.4), (1, .5)]
    d.polygon([(cx + x * s, cy + y * s) for x, y in pts], fill=col)
    for x, y in [(-1, -.4), (0, -.6), (1, -.4)]: d.ellipse((cx + x * s - 18, cy + y * s - 18, cx + x * s + 18, cy + y * s + 18), fill=col)

def pr_on():
    im, d = card((235, 235, 235)); crown(d, sw / 2, 150, 130, INK)
    fit_text(d, (30, 260, sw - 30, 520), "THE KING RETURNS", ANTON, 170, INK); return im

def check(d, cx, cy, s, col, w):
    d.line((cx - s, cy, cx - s * .3, cy + s * .7, cx + s, cy - s * .8), fill=col, width=w, joint='curve')

def gov_off():
    im, d = card((40, 70, 140))
    d.ellipse((sw / 2 - 110, 40, sw / 2 + 110, 260), fill=(60, 170, 90), outline=WHITE, width=8)
    check(d, sw / 2, 150, 60, WHITE, 26)
    fit_text(d, (30, 290, sw - 30, 520), "NO NATIONAL SECURITY RISK", ANTON, 120, WHITE); return im

def gov_on():
    im, d = card((235, 235, 235)); check(d, sw / 2, 140, 80, INK, 34)
    fit_text(d, (30, 260, sw - 30, 520), "WE CHECKED OURSELVES", ANTON, 140, INK); return im

TWEET = ("There is something profoundly wrong about Jensen Huang having a relationship with a Chinese Communist Spy... "
         "Congress should really dig into this as a national security issue of enormous proportions.")
def tweet(on):
    im, d = card((255, 255, 255) if not on else (235, 235, 235))
    d.ellipse((30, 30, 130, 130), fill=(150, 150, 150) if not on else (120, 120, 120))
    d.ellipse((62, 50, 98, 86), fill=(210, 210, 210)); d.chord((45, 85, 115, 150), 180, 360, fill=(210, 210, 210))
    d.text((150, 62), "Newt Gingrich", font=F(ARCH, 40), fill=INK, anchor='lm')
    d.text((150, 108), "@newtgingrich", font=F(GF + 'firasans/FiraSans-Regular.ttf', 32), fill=(100, 100, 100), anchor='lm')
    if not on:
        fit_text(d, (30, 160, sw - 30, 480), TWEET, GF + 'firasans/FiraSans-Regular.ttf', 44, INK, align='left', lh=1.22)
        d.text((30, 515), "5:52 AM · 23 Nov 26 · 941K Views", font=F(GF + 'firasans/FiraSans-Regular.ttf', 28), fill=(110, 110, 110), anchor='lm')
    else:
        fit_text(d, (30, 170, sw - 30, 420), "HEARINGS.\nBEHIND CLOSED DOORS.", ANTON, 110, INK)
        lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rectangle((150, 430, sw - 150, 520), outline=INK, width=8); ld.text((sw / 2, 475), "CLASSIFIED", font=F(ANTON, 70), fill=INK, anchor='mm')
        lay = lay.rotate(-6, resample=Image.BICUBIC); im.paste(lay, (0, 0), lay)
    return im

REPLIES = [((220, 120, 40), "She wasn't a spy!"), ((60, 130, 200), "Cite your sources!"),
           ((200, 50, 60), "Republicans won't do anything!"), ((90, 160, 80), "This is on Trump!")]
def replies(on):
    im, d = card((20, 22, 28) if not on else (235, 235, 235))
    for i, (col, txt) in enumerate(REPLIES):
        y = 20 + i * 132
        d.rounded_rectangle((20, y, sw - 20, y + 118), 18, fill=(255, 255, 255) if not on else (255, 255, 255), outline=INK, width=4)
        d.ellipse((38, y + 24, 108, y + 94), fill=col if not on else INK)
        t = txt if not on else ["STAY DIVIDED.", "KEEP FIGHTING.", "DO NOT LOOK AT US.", "CONSUME."][i]
        fp = ANTON if on else ARCH; sz = 52 if on else 40
        while d.textlength(t, font=F(fp, sz)) > sw - 175: sz -= 2
        d.text((130, y + 59), t, font=F(fp, sz), fill=INK, anchor='lm')
    return im

def end():
    im, d = card((235, 235, 235)); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im

SCREENS = dict(pr_off=pr_off, pr_on=pr_on, gov_off=gov_off, gov_on=gov_on, tweet_off=lambda: tweet(False), tweet_on=lambda: tweet(True),
               rep_off=lambda: replies(False), rep_on=lambda: replies(True), end=end)

J1, J2 = 'jessie-sheet1-', 'jessie-sheet2-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='pr_off', audio=[('a_off', .3)], figs=[(RM + '14', 0)],
      caps=sh_([(0, 1.45, "NVIDIA TODAY ANNOUNCED"), (1.45, 4.2, "JENSEN HUANG HAS BEEN REINSTATED"), (4.2, 7.6, "AS PRESIDENT AND CHIEF EXECUTIVE OFFICER."), (7.6, 9.6, "EFFECTIVE IMMEDIATELY.")], .3),
      jessie=[(0, 'jessie-cool-no-glasses-01'), (7.4, 'jessie-cool-glasses-lowered-04')]),
 dict(mode='on', screen='pr_on', audio=[('a_on', .2)], figs=[(AM + '14', 0)],
      caps=sh_([(0, 1.6, "ELEVEN DAYS."), (1.6, 3.3, "THE KING RETURNS."), (3.3, 5.0, "NOBODY BLINKED.")], .2),
      jessie=[(0, 'jessie-cool-glasses-worn-01')]),
 dict(mode='off', screen='gov_off', audio=[('b_off', .1)], figs=lambda r: [(RM + ('10' if r < 4.5 else '09'), 0)],
      caps=sh_([(0, 4.4, "THE BOARD RECEIVED INPUT FROM SENIOR LEVELS OF THE UNITED STATES GOVERNMENT,"), (4.4, 8.6, "AND IS CONFIDENT HIS REINSTATEMENT POSES NO NATIONAL SECURITY RISK.")], .1),
      jessie=[(0, 'jessie-cool-no-glasses-03'), (6.6, 'jessie-cool-glasses-lowered-05')]),
 dict(mode='on', screen='gov_on', audio=[('b_on', .2)], figs=lambda r: [(AM + ('10' if r < 2.0 else '11'), 0)],
      caps=sh_([(0, 1.6, "WE MADE A PHONE CALL."), (1.6, 3.2, "WE CHECKED OURSELVES."), (3.2, 4.6, "WE PASSED.")], .2),
      jessie=[(0, 'jessie-cool-glasses-worn-05')]),
 dict(mode='off', screen='tweet_off', audio=[('c_off', .2)], figs=[(RM + '05', 0)],
      caps=sh_([(0, 3.4, "THERE IS SOMETHING PROFOUNDLY WRONG ABOUT THIS."), (3.4, 6.1, "CONGRESS SHOULD REALLY DIG INTO THIS,"), (6.1, 8.1, "AS A NATIONAL SECURITY ISSUE"), (8.1, 10.3, "OF ENORMOUS PROPORTIONS.")], .2),
      jessie=[(0, 'jessie-cool-no-glasses-05'), (8.4, 'jessie-cool-glasses-lowered-07')]),
 dict(mode='on', screen='tweet_on', audio=[('c_on', .1)], figs=[(AM + '05', 0)],
      caps=sh_([(0, 1.4, "HEARINGS."), (1.4, 3.4, "BEHIND CLOSED DOORS."), (3.4, 5.0, "STAY ASLEEP.")], .1),
      jessie=[(0, 'jessie-cool-glasses-worn-07')]),
 dict(mode='off', screen='rep_off', audio=[('r1', .1), ('r2', 1.5), ('r3', 3.1), ('r4', 4.4)], figs=[(RW + '12', 0, .78), (RM + '07', -235, .78)],
      caps=[(.1, 1.5, "SHE WASN'T A SPY!"), (1.5, 3.1, "CITE YOUR SOURCES!"), (3.1, 4.4, "REPUBLICANS WON'T DO ANYTHING!"), (4.4, 6.4, "THIS IS ON TRUMP!")],
      jessie=[(0, 'jessie-cool-no-glasses-06'), (4.4, 'jessie-cool-glasses-lowered-02')], pad=0.2),
 dict(mode='on', screen='rep_on', audio=[('d_on', .1)], figs=[(AW + '12', 0, .78), (AM + '07', -235, .78)],
      caps=sh_([(0, 1.0, "LEFT."), (1.0, 2.0, "RIGHT."), (2.0, 3.1, "SPY."), (3.1, 4.6, "NO SPY."), (4.6, 5.9, "KEEP FIGHTING."), (5.9, 7.8, "STAY DIVIDED.")], .1),
      jessie=[(0, 'jessie-cool-glasses-worn-02')]),
 dict(mode='on', screen='end', audio=[('obey', .4), ('tag', 3.95)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.6,
      caps=[(.3, 3.6, "OBEY.")], brand=3.6, jessie=[(0, 'jessie-cool-glasses-lowered-08')]),
]
TICK_OFF = "NVIDIA REINSTATES CEO  •  BOARD: NO NATIONAL SECURITY RISK  •  HOUSE HEARINGS DEC 1 AND 2  •  "
TICK_ON = "THE KING RETURNS  •  STAY DIVIDED  •  DO NOT QUESTION AUTHORITY  •  CONSUME  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'mon midday they news the king returns.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 6.0, still=st)
    print('total', round(total, 2)); [print(s['mode'], s['screen'], round(s['start'], 2), round(s['end'], 2)) for s in segs]
