import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
FB = (24, 119, 242); DARK = (28, 28, 28)
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

def post_off():
    im, d = card(DARK)
    fit_text(d, (40, 40, X1 + 30, sh - 40), "I don't know who Coldplay is but if you've ever made a post about them or the Island Boys you are an NPC. I do not make the rules", ARCH, 64, WHITE, lh=1.1)
    return im
def post_on():
    im, d = card(GREY)
    d.rounded_rectangle((30, 40, 330, 250), 18, fill=WHITE, outline=INK, width=6)
    d.text((180, 85), "MEMBER", font=F(ANTON, 44), fill=INK, anchor='mm')
    d.text((180, 150), "“THEY SUCK”", font=F(ANTON, 50), fill=INK, anchor='mm')
    d.text((180, 215), "NO THOUGHT REQUIRED", font=F(ARCH, 20), fill=INK, anchor='mm')
    fit_text(d, (350, 40, X1 + 40, 320), "PICK A SAFE TARGET.", ANTON, 100, INK)
    fit_text(d, (30, 340, X1, 500), "SAY IT SUCKS. YOU BELONG.", ANTON, 100, INK); return im

def bubble(d, box, who, txt, col=(240, 242, 245)):
    x0, y0, x1, y1 = box
    d.ellipse((x0, y0, x0 + 70, y0 + 70), fill=(160, 160, 170))
    d.rounded_rectangle((x0 + 85, y0, x1, y1), 26, fill=col)
    d.text((x0 + 110, y0 + 30), who, font=F(ARCH, 26), fill=INK, anchor='lm')
    fit_text(d, (x0 + 110, y0 + 60, x1 - 20, y1 - 15), txt, FIRA_R, 44, INK, align='left', lh=1.15)
def comment_off():
    im, d = card(WHITE)
    bubble(d, (25, 60, sw - 25, 300), "A COMMENTER", "Wait, do you know who the Island Boys are? Also, does this post not count?")
    d.text((140, 360), "Like    Reply", font=F(ARCH, 26), fill=(100, 100, 100), anchor='lm'); return im
def comment_on():
    im, d = card(GREY)
    for k in range(7):
        x = 40 + (k % 4) * 75; y = 70 + (k // 4) * 95
        d.ellipse((x, y, x + 55, y + 40), fill=WHITE, outline=INK, width=4); d.ellipse((x + 40, y + 5, x + 65, y + 30), fill=INK)
    d.text((170, 300), "THE HERD", font=F(ANTON, 50), fill=INK, anchor='mm')
    fit_text(d, (350, 40, X1 + 40, 330), "PRETEND NOT TO UNDERSTAND.", ANTON, 90, INK)
    fit_text(d, (30, 360, X1, 500), "PULL HIM BACK IN.", ANTON, 100, INK); return im

def reply_off():
    im, d = card(WHITE)
    bubble(d, (25, 30, X1 + 50, 190), "JESSIE SPONBERG", "I def know who the Island Boys are but I don't know their names \U0001F602".replace(" \U0001F602", " lol"))
    bubble(d, (25, 210, X1 + 50, 350), "JESSIE SPONBERG", "This post isn't about the Island Boys.")
    bubble(d, (25, 370, X1 + 50, 530), "JESSIE SPONBERG", "Gonna make you an easy to understand cartoon real quick")
    return im
def reply_on():
    im, d = card(GREY)
    d.rectangle((30, 40, 330, 300), fill=WHITE, outline=INK, width=6)
    d.text((180, 100), "THE POST", font=F(ANTON, 50), fill=INK, anchor='mm')
    d.line((60, 150, 300, 280), fill=INK, width=10); d.line((300, 150, 60, 280), fill=INK, width=10)
    d.text((180, 330), "UNREAD", font=F(ANTON, 40), fill=INK, anchor='mm')
    fit_text(d, (350, 40, X1 + 40, 320), "NPCs DON'T READ THE POST.", ANTON, 90, INK)
    fit_text(d, (30, 380, X1, 510), "THEY READ THE ROOM.", ANTON, 100, INK); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(5); fs = 175; T = "NOT AN NPC"
    while ld.textlength(T, font=F(ANTON, fs)) > sw - 90: fs -= 5
    f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .35; L = rng.uniform(30, 150)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

FIRA_R = GF + 'firasans/FiraSans-Regular.ttf'
SCREENS = dict(post_off=post_off, post_on=post_on, comment_off=comment_off, comment_on=comment_on, reply_off=reply_off, reply_on=reply_on, end=end, end_g=end_g)

C = 'jessie-cool-glasses-worn-'; N = 'jessie-cool-no-glasses-'; L = 'jessie-cool-glasses-lowered-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='post_off', audio=[('n1', .3)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 1.8, "I DON'T KNOW WHO COLDPLAY IS."), (1.8, 3.8, "BUT IF YOU'VE EVER MADE A POST ABOUT THEM,"), (3.8, 5.3, "OR THE ISLAND BOYS,"), (5.3, 6.9, "YOU ARE AN NPC."), (7.0, 8.7, "I DO NOT MAKE THE RULES.")], .3),
      jessie=[(0, N + '01'), (7.6, L + '05')]),
 dict(mode='on', screen='post_on', audio=[('o1', .1)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 2.1, "PICK A SAFE TARGET."), (2.1, 4.2, "EVERYONE ALREADY AGREES."), (4.2, 5.5, "SAY IT SUCKS."), (5.5, 6.5, "YOU BELONG.")], .1),
      jessie=[(0, C + '05')]),
 dict(mode='off', screen='comment_off', audio=[('a1', .1)], figs=[(RM + '07', 0)],
      caps=sh_([(0, 0.9, "WAIT."), (0.9, 3.4, "DO YOU KNOW WHO THE ISLAND BOYS ARE?"), (3.4, 6.3, "ALSO, DOES THIS POST NOT COUNT?")], .1),
      jessie=[(0, N + '05'), (5.0, L + '04')]),
 dict(mode='on', screen='comment_on', audio=[('o2', .1)], figs=[(AM + '07', 0)],
      caps=sh_([(0, 2.2, "PRETEND NOT TO UNDERSTAND."), (2.2, 4.4, "MAKE HIM EXPLAIN."), (4.4, 6.1, "PULL HIM BACK INTO THE HERD.")], .1),
      jessie=[(0, C + '07')]),
 dict(mode='off', screen='reply_off', audio=[('n2', .1), ('n3', 4.6)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 2.7, "I DEFINITELY KNOW WHO THE ISLAND BOYS ARE."), (2.7, 4.4, "I JUST DON'T KNOW THEIR NAMES."), (4.5, 7.3, "THIS POST ISN'T ABOUT THE ISLAND BOYS."), (7.3, 10.6, "I'M GONNA MAKE YOU AN EASY TO UNDERSTAND CARTOON."), (10.6, 11.6, "HOLD ON.")], .1),
      jessie=[(0, N + '07'), (10.4, L + '01')]),
 dict(mode='on', screen='reply_on', audio=[('o3', .1)], figs=[(RW + '13', 60, .85), (AM + '07', -150, .85), (AW + '13', -330, .85)], min=4.4,
      caps=sh_([(0, 1.9, "NPCs DON'T READ THE POST."), (1.9, 3.8, "THEY READ THE ROOM.")], .1),
      jessie=[(0, C + '08')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "NOT AN NPC.")], brand=3.2, jessie=[(0, C + '01')]),
]
TICK_OFF = "WHO IS COLDPLAY?  •  ISLAND BOYS  •  YOU ARE AN NPC  •  I DO NOT MAKE THE RULES  •  "
TICK_ON = "SAFE TARGET  •  YOU BELONG  •  BACK TO THE HERD  •  READ THE ROOM  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    out = 'tue morning they news npc check.mp4'
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', out, MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
