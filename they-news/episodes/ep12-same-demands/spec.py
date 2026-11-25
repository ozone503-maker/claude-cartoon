import sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
for _w in ('obey.wav', 'tag.wav'): shutil.copy(os.path.join(HERE, '..', '..', 'shared', _w), _w)
from engine import *

sw, sh = SX1 - SX0, SY1 - SY0
WHITE, INK, RED, GREY = (240, 238, 230), (12, 12, 12), (190, 30, 30), (235, 235, 235)
X1 = sw - 170
def card(bg=WHITE):
    im = Image.new('RGB', (sw, sh), bg); return im, ImageDraw.Draw(im)

DEC = [("1960s", "OIL WILL RUN OUT IN 10 YEARS", (250, 215, 120)), ("1970s", "A NEW ICE AGE IS IMMINENT", (200, 230, 250)),
       ("1980s", "ACID RAIN WILL WIPE OUT OUR CROPS", (210, 240, 180)), ("1990s", "THE OZONE LAYER WILL DISAPPEAR", (250, 200, 170)),
       ("2000s", "THE ARCTIC WILL BE ICE-FREE", (190, 220, 250)), ("2010s", "WE HAVE 10 YEARS TO SAVE THE PLANET", (220, 250, 210)),
       ("2020s", "NET ZERO IS OUR LAST CHANCE TO SURVIVE", (250, 210, 210))]
def dec_card(i):
    def f():
        yr, txt, bg = DEC[i]; im, d = card(bg)
        d.rectangle((0, 0, sw, 70), fill=RED); d.text((sw / 2, 35), "BREAKING", font=F(ANTON, 46), fill=WHITE, anchor='mm')
        fit_text(d, (40, 90, X1 + 20, 230), yr, ANTON, 150, INK, align='left')
        fit_text(d, (40, 250, X1 + 20, 500), txt, ANTON, 90, INK, align='left', lh=1.05)
        for k in range(i + 1): d.ellipse((40 + k * 34, sh - 40, 64 + k * 34, sh - 16), fill=INK)
        return im
    return f

def wall(title_top, title_bot, marks):
    def f():
        im, d = card(GREY)
        for k, m in enumerate(marks):
            x, y = 30 + (k % 2) * 160, 40 + (k // 2) * 105
            d.rectangle((x, y, x + 150, y + 95), fill=WHITE, outline=INK, width=4)
            d.text((x + 75, y + 30), m, font=F(ANTON, 34), fill=INK, anchor='mm')
            d.text((x + 75, y + 70), "DEADLINE", font=F(ARCH, 16), fill=INK, anchor='mm'); d.line((x + 20, y + 70, x + 130, y + 70), fill=INK, width=4)
        fit_text(d, (370, 40, X1 + 40, 330), title_top, ANTON, 100, INK)
        fit_text(d, (30, 380, X1, 510), title_bot, ANTON, 100, INK); return im
    return f

def o4_on():
    im, d = card(GREY)
    for k, t in enumerate(["MORE TAXES", "LESS FREEDOM", "MORE CONTROL"]):
        y = 50 + k * 120; d.rectangle((30, y, X1 + 40, y + 100), fill=WHITE, outline=INK, width=6)
        fit_text(d, (50, y + 10, X1 + 20, y + 90), t, ANTON, 90, INK)
    d.text((sw / 2 - 60, 450), "SAME DEMANDS SINCE 1960", font=F(ARCH, 30), fill=INK, anchor='mm'); return im

def end():
    im, d = card(GREY); fit_text(d, (20, 40, sw - 20, sh - 40), "OBEY", ANTON, 330, INK); return im
def end_g():
    im = Image.blend(end(), Image.new('RGB', (sw, sh), GREY), 0.72); lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rng = np.random.default_rng(12); T = "CHECK THE\nDATES"; fs = 160; f = F(ANTON, fs)
    for dx, dy in [(0, 0), (3, 2), (-2, 3)]:
        ld.multiline_text((sw / 2 + dx, sh / 2 + dy), T, font=f, fill=(200, 20, 20, 235), anchor='mm', align='center', spacing=0, stroke_width=4, stroke_fill=(150, 10, 10, 200))
    for k in range(14):
        x = rng.uniform(80, sw - 80); y0 = sh / 2 + fs * .9; L = rng.uniform(30, 120)
        ld.line((x, y0, x, y0 + L), fill=(190, 20, 20, 230), width=int(rng.uniform(5, 10)))
        ld.ellipse((x - 7, y0 + L - 7, x + 7, y0 + L + 7), fill=(190, 20, 20, 230))
    lay = lay.rotate(-7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)); im.paste(lay, (0, 0), lay); return im

SCREENS = {f'd{i}': dec_card(i) for i in range(7)}
SCREENS.update(o1_on=wall("THE DEADLINE MOVES.", "THE BILL DOESN'T.", ["1960s", "1970s"]),
               o2_on=wall("NEW MONSTER EVERY DECADE.", "SAME CURE.", ["1960s", "1970s", "1980s", "1990s"]),
               o3_on=wall("TEN YEARS.", "EVERY TEN YEARS.", ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s"]),
               o4_on=o4_on, end=end, end_g=end_g)

N, L, C = 'jessie-cool-no-glasses-', 'jessie-cool-glasses-lowered-', 'jessie-cool-glasses-worn-'
RM, AM, RW, AW = 'fullbody-regular-man-', 'fullbody-alien-man-', 'fullbody-regular-woman-', 'fullbody-alien-woman-'
def sh_(caps, k): return [(a + k, b + k, t) for a, b, t in caps]
SEGS = [
 dict(mode='off', screen=lambda r: 'd0' if r < 4.1 else 'd1', audio=[('f1', .3)], figs=[(RM + '14', 0)],
      caps=sh_([(0, 3.8, "1960s. OIL WILL RUN OUT IN 10 YEARS."), (3.8, 7.5, "1970s. A NEW ICE AGE IS IMMINENT.")], .3),
      jessie=[(0, N + '01'), (6.2, L + '05')]),
 dict(mode='on', screen='o1_on', audio=[('o1', .1)], figs=[(AM + '14', 0)], min=3.2,
      caps=sh_([(0, 1.4, "THE DEADLINE MOVES."), (1.4, 2.7, "THE BILL DOESN'T.")], .1),
      jessie=[(0, C + '05')]),
 dict(mode='off', screen=lambda r: 'd2' if r < 3.75 else 'd3', audio=[('f2', .1)], figs=[(RW + '10', 0)],
      caps=sh_([(0, 3.65, "1980s. ACID RAIN WILL WIPE OUT OUR CROPS."), (3.65, 6.9, "1990s. THE OZONE LAYER WILL DISAPPEAR.")], .1),
      jessie=[(0, N + '05'), (5.6, L + '04')]),
 dict(mode='on', screen='o2_on', audio=[('o2', .1)], figs=[(AW + '10', 0)],
      caps=sh_([(0, 2.1, "NEW MONSTER EVERY DECADE."), (2.1, 3.5, "SAME CURE.")], .1),
      jessie=[(0, C + '07')]),
 dict(mode='off', screen=lambda r: 'd4' if r < 4.35 else 'd5', audio=[('f3', .1)], figs=[(RW + '13', 0)],
      caps=sh_([(0, 4.25, "2000s. THE ARCTIC WILL BE ICE-FREE."), (4.25, 6.9, "2010s. WE HAVE 10 YEARS TO SAVE THE PLANET.")], .1),
      jessie=[(0, N + '07'), (5.6, L + '01')]),
 dict(mode='on', screen='o3_on', audio=[('o3', .1)], figs=[(AW + '13', 0)], min=3.0,
      caps=sh_([(0, 1.1, "TEN YEARS."), (1.1, 2.7, "EVERY TEN YEARS.")], .1),
      jessie=[(0, C + '04')]),
 dict(mode='off', screen='d6', audio=[('f4', .1)], figs=[(RM + '10', 0)], min=4.6,
      caps=sh_([(0, 1.2, "2020s."), (1.2, 4.3, "NET ZERO IS OUR LAST CHANCE TO SURVIVE.")], .1),
      jessie=[(0, N + '02'), (3.0, L + '07')]),
 dict(mode='on', screen='o4_on', audio=[('o4', .1)], figs=[(AM + '10', 0)],
      caps=sh_([(0, 1.8, "THE APOCALYPSE NEVER CAME."), (1.8, 4.0, "THE DEMANDS STAYED THE SAME."), (4.0, 5.6, "MORE TAXES."), (5.6, 7.0, "LESS FREEDOM."), (7.0, 8.4, "MORE CONTROL.")], .1),
      jessie=[(0, C + '02')]),
 dict(mode='on', screen=lambda r: 'end' if r < 1.6 else 'end_g', audio=[('obey', .3), ('tag', 3.55)], figs=[(AW + '11', 0, .78), (AM + '11', -235, .78)], min=7.2,
      caps=[(.2, 1.6, "OBEY."), (1.6, 3.2, "CHECK THE DATES.")], brand=3.2, jessie=[(0, C + '08')]),
]
TICK_OFF = "OIL RUNS OUT  •  NEW ICE AGE  •  ACID RAIN  •  OZONE HOLE  •  ICE-FREE ARCTIC  •  10 YEARS LEFT  •  NET ZERO  •  "
TICK_ON = "THE DEADLINE MOVES  •  SAME CURE  •  MORE TAXES  •  LESS FREEDOM  •  MORE CONTROL  •  OBEY  •  "

if __name__ == '__main__':
    st = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'still' else None
    segs, flips, total = render(SEGS, '.', SCREENS, TICK_OFF, TICK_ON, 'THEY NEWS', 'THEY LIE', 'render.mp4', MUSIC, 5.0, still=st)
    print('total', round(total, 2))
    for s in segs: print(s['mode'], round(s['start'], 2), round(s['end'], 2))
