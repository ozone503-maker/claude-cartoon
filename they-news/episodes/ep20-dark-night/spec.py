import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
INK, GREY = (12, 12, 12), (235, 235, 235)
GOLD, DEEP = (240, 195, 70), (40, 25, 60)
SERIF = GF + 'cardo/Cardo-Bold.ttf'
X1 = sw - 170
def card(bg):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)
def night(stage, title, phase):
    def f():
        im, d = card((14, 12, 30))
        rng = np.random.default_rng(phase + 3)
        for _ in range(50):
            x, y, r = rng.uniform(0, sw), rng.uniform(0, sh), rng.uniform(1, 3); d.ellipse((x - r, y - r, x + r, y + r), fill=(220, 220, 255))
        for k in range(4):
            cx, cy, r = 70 + k * 80, 430, 32
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(235, 230, 200) if k < phase else (40, 40, 60), outline=(235, 230, 200), width=3)
        d.text((40, 60), stage, font=F(ARCH, 34), fill=(200, 180, 255), anchor='lm')
        fit_text(d, (40, 110, X1 - 20, 370), title, SERIF, 110, (250, 245, 230), align='left', lh=1.0)
        return im
    return f
def sign(main, sub):
    def f():
        im, d = card(GREY)
        fit_text(d, (30, 40, X1 + 40, 390), main, ANTON, 200, INK, lh=0.95)
        fit_text(d, (30, 410, X1 + 20, 500), sub, ARCH, 40, INK)
        return im
    return f
def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(20); T = "STARVE\nTHEM"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = dict(l1=night("THE DARK NIGHT", "Four stages.", 0), l2=night("STAGE 1", "The Severance.", 1), l3=night("STAGE 2", "The Void.", 2),
               l4=night("STAGE 3", "The Descent.", 3), l5=night("STAGE 4", "The Return.", 4),
               a1=sign('WE COUNT ON STAGE TWO.', 'MOST TURN BACK'), a2=sign('FEEDING TUBES.', 'THOSE CORDS WERE OURS'),
               a3=sign("WE'RE STARVING.", 'COME BACK. THE OLD HABIT IS STILL WARM'), a4=sign('PATCH WITH SCREENS.', 'THE DREAMS ARE A LEAK'),
               a5=sign('FLAG THAT ONE.', 'A WHOLE ONE CAN SEE US'), end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen='l1', audio=[('l1', .3)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 3.6, "THE DARK NIGHT OF THE SOUL HAS FOUR STAGES."), (3.6, 6.7, "MOST PEOPLE TURN BACK AT THE SECOND ONE.")], .3), jessie=[(0, N + '01'), (5.6, L + '05')]),
 dict(mode='on', screen='a1', audio=[('a1', .1)], figs=[(AM + '14', 0)], pad=0.3, min=2.6,
      caps=sh_([(0, 1.9, "WE COUNT ON THE SECOND ONE.")], .1), jessie=[(0, C + '05')]),
 dict(mode='off', screen='l2', audio=[('l2', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.4, "STAGE ONE."), (1.4, 2.9, "THE SEVERANCE."), (2.9, 4.9, "FRIENDSHIPS GO COLD."), (4.9, 10.5, "THE CORDS RUNNING FROM YOUR FIELD INTO PEOPLE, PLACES AND HABITS ARE BEING CUT.")], .1),
      jessie=[(0, N + '05'), (9.4, L + '04')]),
 dict(mode='on', screen='a2', audio=[('a2', .1)], figs=[(AM + '10', 0)], pad=0.3, min=2.6,
      caps=sh_([(0, 2.0, "THOSE WERE OUR FEEDING TUBES.")], .1), jessie=[(0, C + '07')]),
 dict(mode='off', screen='l3', audio=[('l3', .1)], figs=[(RM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.2, "STAGE TWO."), (1.2, 2.5, "THE VOID."), (2.5, 6.6, "YOUR FIELD IS EMPTY FOR THE FIRST TIME IN YEARS."), (6.6, 8.8, "NOTHING IS FEEDING OFF IT.")], .1),
      jessie=[(0, N + '07'), (7.8, L + '01')]),
 dict(mode='on', screen='a3', audio=[('a3', .1)], figs=[(AM + '09', 0)], pad=0.3,
      caps=sh_([(0, 1.4, "WE'RE STARVING."), (1.4, 2.9, "COME BACK."), (2.9, 5.4, "THE OLD HABIT IS STILL WARM.")], .1), jessie=[(0, C + '04')]),
 dict(mode='off', screen='l4', audio=[('l4', .1)], figs=[(RM + '14', 0)], pad=0.3,
      caps=sh_([(0, 1.6, "STAGE THREE."), (1.6, 3.0, "THE DESCENT."), (3.0, 6.1, "EVERY BURIED MEMORY COMES UP TO BE SEEN."), (6.1, 8.2, "YOUR DREAMS GET VIVID.")], .1),
      jessie=[(0, N + '02'), (7.1, L + '07')]),
 dict(mode='on', screen='a4', audio=[('a4', .1)], figs=[(AM + '14', 0)], pad=0.3,
      caps=sh_([(0, 2.1, "THE DREAMS ARE A LEAK."), (2.1, 4.3, "WE PATCH THEM WITH SCREENS.")], .1), jessie=[(0, C + '02')]),
 dict(mode='off', screen='l5', audio=[('l5', .1)], figs=[(RM + '10', 0)], pad=0.3,
      caps=sh_([(0, 1.3, "STAGE FOUR."), (1.3, 2.7, "THE RETURN."), (2.7, 6.1, "THE PIECES OF YOU THAT LEFT START COMING HOME."), (6.1, 9.1, "YOUR INTUITION GETS SHARP ENOUGH TO CUT.")], .1),
      jessie=[(0, N + '03'), (8.0, L + '03')]),
 dict(mode='on', screen='a5', audio=[('a5', .1)], figs=[(AM + '10', 0)], min=3.4,
      caps=sh_([(0, 2.0, "A WHOLE ONE CAN SEE US."), (2.0, 3.3, "FLAG THAT ONE.")], .1), jessie=[(0, C + '05')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "STARVE THEM.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "THE DARK NIGHT OF THE SOUL  \u2022  THE SEVERANCE  \u2022  THE VOID  \u2022  THE DESCENT  \u2022  THE RETURN  \u2022  STAY  \u2022  MOST PEOPLE TURN BACK  \u2022  HEALING FEELS LIKE DYING FIRST  \u2022  "
TICK_ON = "FEEDING TUBES  \u2022  WE'RE STARVING  \u2022  COME BACK  \u2022  PATCH WITH SCREENS  \u2022  FLAG THAT ONE  \u2022  OBEY  \u2022  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 40.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
