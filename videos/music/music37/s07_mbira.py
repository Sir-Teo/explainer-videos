from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403


class Mbira(SoundScene):
    def construct(self):
        chapter(self, 6, r"The mbira", r"How does a box of metal keys make so many voices?")
        self.instrument()
        self.tine()
        self.hands()
        self.parts()
        self.bira()
        self.travels()

    # ------------------------------------------------------------------
    def instrument(self):
        items = [
            (r"the \textit{mbira dzavadzimba}, \ `mbira of the ancestors', \ of the Shona of Zimbabwe", WHITE),
            (r"22 to 28 metal keys on a wooden board, \ often played inside a gourd resonator \ (\textit{deze})", WHITE),
            (r"bottle caps or shells on the board buzz with every note", WHITE),
            (r"one of a large family of African lamellophones: \ \textit{likembe}, \ \textit{sanza}, \ \textit{kalimba} \ ...", TUNE),
            (r"the physics is Part 9's bar, \ held at one end", GREY_A),
        ]
        rows_scene(self, r"the mbira", items,
                   "The Shona of Zimbabwe play an instrument called the mbira dzavadzimba, the mbira of the ancestors. "
                   "<bookmark mark='b'/> It has twenty-two to twenty-eight metal keys on a wooden board, often played inside a "
                   "large gourd that acts as a resonator. <bookmark mark='c'/> Bottle caps or shells fixed to the board buzz with "
                   "every note. <bookmark mark='d'/> It belongs to a large family of African lamellophones, with names such as "
                   "likembe, sanza and kalimba. <bookmark mark='e'/> And its physics is Part 9's bar, held at one end.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def tine(self):
        d = load("mbira")
        c = clip("mbira.tine")
        board = Rectangle(width=0.5, height=1.2, stroke_width=0, fill_color=GREY_D, fill_opacity=1.0).move_to(LEFT * 5.0 + UP * 1.5)
        x = np.linspace(0, 1, 80)
        shapes = [1.875, 4.694, 7.855]
        rows_ = VGroup()
        for k, b in enumerate(shapes):
            y = (np.cosh(b * x) - np.cos(b * x)) - ((np.cosh(b) + np.cos(b)) / (np.sinh(b) + np.sin(b))) * (np.sinh(b * x) - np.sin(b * x))
            y = y / np.abs(y).max()
            pts = [np.array([-4.75 + 3.4 * xx, 2.5 - 1.25 * k + 0.45 * yy, 0]) for xx, yy in zip(x, y)]
            curve = VMobject(color=[TUNE, BLUE, EAR][k], stroke_width=3).set_points_smoothly(pts)
            rest = DashedLine([-4.75, 2.5 - 1.25 * k, 0], [-1.35, 2.5 - 1.25 * k, 0], color=GREY_D, stroke_width=1.2)
            curve = VGroup(rest, curve)
            lab = label(rf"{d['ratios'][k]:.2f} \ $\times$ \ f", font_size=18, color=[TUNE, BLUE, EAR][k]).next_to(pts[-1], RIGHT, buff=0.3)
            clamp = Rectangle(width=0.25, height=0.6, stroke_width=0, fill_color=GREY_C, fill_opacity=1).move_to([-4.85, 2.5 - 1.25 * k, 0])
            rows_.add(VGroup(clamp, curve, lab))
        left = VGroup(label(r"a tine held at one end: \ its first three shapes", font_size=19, color=GREY_A).move_to(LEFT * 3.0 + UP * 3.25), rows_)
        ax_l, ax_r = 0.9, 6.4
        fmax = 5000.0
        spec = VGroup(Line([ax_l, -0.4, 0], [ax_r, -0.4, 0], color=GREY_B, stroke_width=1.5))
        for k, f in enumerate(d["partials"]):
            if f > fmax:
                continue
            xx = ax_l + (ax_r - ax_l) * f / fmax
            h = [2.2, 1.0, 0.4][k]
            spec.add(Line([xx, -0.4, 0], [xx, -0.4 + h, 0], color=[TUNE, BLUE, EAR][k], stroke_width=6))
            spec.add(label(rf"{f:.0f} Hz", font_size=16, color=[TUNE, BLUE, EAR][k]).move_to([xx, -0.4 + h + 0.25, 0]))
        for k in range(2, 8):
            xx = ax_l + (ax_r - ax_l) * k * d["f"] / fmax
            spec.add(DashedLine([xx, -0.4, 0], [xx, 0.6, 0], color=GREY_D, stroke_width=1.2))
        sl = label(r"partials of a G tine; \ dashed: \ where a string's would be", font_size=17, color=GREY_A).move_to([3.65, -0.95, 0])
        g = VGroup(left, spec, sl)
        g.shift(DOWN * 0.2)
        with self.voiceover(
            "A key held at one end vibrates like a diving board. An ideal uniform cantilever beam, the simplified model used here, has its first three mode frequencies in the ratio one, six point two seven, and seventeen point five five, from the same beam equation as Part 9's free bar, with one end clamped. <bookmark mark='a'/> So the second partial lies more than two and a half octaves above the first, far from where a string's harmonics would be, and it dies quickly. Our decaying model leaves a nearly sinusoidal tail; real shaped tines and resonators have instrument-specific partials, so this is not a universal account of mbira blending. The buzzers add the opposite: a wash of noise that follows each note. Hear one tine, plain and then with its buzz."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(spec), FadeIn(sl))
        with self.listen(c) as snd:
            window(snd, r"one tine, \ plain then buzzing", detail=r"a clamped bar model", corner=DL, tag_corner=DR)
            ev = c.events
            pulse(snd, spec, ev["plain"], ev["buzz"] - 0.3, buff=0.1)
            pulse(snd, rows_, ev["buzz"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hands(self):
        items = [
            (r"two thumbs and the right index finger: \ three fingers, \ two hands", WHITE),
            (r"the left thumb takes the lowest keys; \ the right hand plays above, \ thumb down and finger up", WHITE),
            (r"each hand plays its own repeating pattern; \ the patterns interlock", WHITE),
            (r"a piece is a cycle, \ often 48 pulses in four phrases, \ repeated with variations for a long time", TUNE),
            (r"a single player already makes counterpoint: \ add a second player and it multiplies", GREY_A),
        ]
        rows_scene(self, r"how it is played", items,
                   "How is it played? <bookmark mark='b'/> With two thumbs and the right index finger. <bookmark mark='c'/> The "
                   "left thumb takes the lowest keys, and the right hand plays above, the thumb striking down and the finger "
                   "plucking up. <bookmark mark='d'/> Each hand plays its own repeating pattern, and the patterns interlock. "
                   "<bookmark mark='e'/> A piece is a cycle, often forty-eight pulses long in four phrases, repeated with "
                   "variations for a long time. <bookmark mark='f'/> So a single player already makes counterpoint; add a second "
                   "player and it multiplies.", marks="cdef")

    # ------------------------------------------------------------------
    def parts(self):
        d = load("mbira")
        c = clip("mbira.parts")
        ku = [[m, p, 1.0] for p, m in d["kushaura"]]
        kt = [[m, p, 1.0] for p, m in d["kutsinhira"]]
        roll = voices_roll([ku, kt], width=11.0, height=3.0, colors=[TUNE, BLUE], total=d["cycle"], lo=48, hi=73, bar_h=0.12).move_to(DOWN * 0.1)
        leg = VGroup(label(r"kushaura \ (leading)", font_size=19, color=TUNE), label(r"kutsinhira \ (interweaving)", font_size=19, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(roll, UP, buff=0.35)
        stage = VGroup(*[label(t, font_size=20, color=GREY_A) for t in (r"kushaura", r"kutsinhira", r"both")]).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.7)
        head = label(r"two players, \ one cycle of 24 pulses \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Two mbira players divide a piece into a leading part, kushaura, and an interweaving part, kutsinhira. Ours are "
            "short: a cycle of twenty-four pulses, with low and high notes alternating. The second part plays a pulse later "
            "than the first, a step lower in its upper notes, and fills every gap the first one leaves. Hear the leading part "
            "alone, the interweaving part alone, and both."
        ):
            self.play(FadeIn(head), FadeIn(leg), FadeIn(roll), FadeIn(stage))
        st = d["starts"]
        p = d["pulse"]
        cyc = d["cycle"] * p
        with self.listen(c) as snd:
            window(snd, r"kushaura, \ kutsinhira, \ both", detail=r"tine models", corner=DL, tag_corner=DR)
            for k, which, reps in (("kushaura", (0,), 2), ("kutsinhira", (1,), 2), ("both", (0, 1), 3)):
                for j in which:
                    v = [ku, kt][j]
                    times = [st[k] + r * cyc + n[1] * p for r in range(reps) for n in v]
                    notes = roll.parts[j].notes * reps
                    flash(snd, notes, times, hot=WHITE, base=[TUNE, BLUE][j])
            ks = ["kushaura", "kutsinhira", "both"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, stage[i], st[k], end, buff=0.08)
        ans = label(r"together the parts fill every pulse, \ and new lines appear in the high notes", font_size=21, color=TUNE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Together the parts fill every pulse, at twice the speed of either. And something else happens: listen to the "
            "highest notes, which now come from both players at once and seem to form lines of their own. That is the "
            "subject of the next chapter."
        ):
            self.play(FadeOut(stage), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bira(self):
        items = [
            (r"\textit{bira}: \ an all-night ceremony in which mbira music calls the ancestral spirits", WHITE),
            (r"the music is repetitive by design: \ variations deepen over hours, \ not minutes", WHITE),
            (r"pieces such as \textit{Nyamaropa} and \textit{Nhemamusasa} are shared by players across generations", WHITE),
            (r"singing, \ clapping and hosho \ (gourd shakers) \ join the mbira", TUNE),
            (r"Paul Berliner's \textit{The Soul of Mbira} \ (1978): \ the music as Shona masters taught it", GREY_A),
        ]
        rows_scene(self, r"music for the ancestors", items,
                   "The mbira's home is the bira, an all-night ceremony in which the music calls the ancestral spirits. "
                   "<bookmark mark='b'/> The music is repetitive by design: its variations deepen over hours, not minutes. "
                   "<bookmark mark='c'/> Pieces such as Nyamaropa and Nhemamusasa are shared by players across generations, "
                   "<bookmark mark='d'/> and singing, clapping and gourd shakers called hosho join the mbira. "
                   "<bookmark mark='e'/> Paul Berliner's The Soul of Mbira, from 1978, records the music as Shona master "
                   "players taught it to him.", marks="bcde")

    # ------------------------------------------------------------------
    def travels(self):
        items = [
            (r"Hugh Tracey commercialized a lamellophone \\ using an existing regional name, kalimba", WHITE),
            (r"from the 1970s Thomas Mapfumo's \textit{chimurenga} music moved mbira patterns to electric guitar", WHITE),
            (r"the mbira was discouraged by missionaries and colonial rule, \ and revived as a sign of independence", WHITE),
            (r"Shona teachers have taught mbira in the USA and Europe since the 1970s", TUNE),
            (r"Part 40 follows such patterns into the popular song: \ riffs and loops", GREY_A),
        ]
        rows_scene(self, r"the mbira travels", items,
                   "The mbira has travelled. <bookmark mark='b'/> In the nineteen-fifties Hugh Tracey commercialized a factory-built lamellophone under the name kalimba, drawing on existing regional instrument names and designs. <bookmark mark='c'/> From the nineteen-seventies Thomas Mapfumo's chimurenga music moved mbira patterns onto the electric guitar. <bookmark mark='d'/> The mbira had been discouraged by missionaries and colonial rule, and its revival became a sign of independence. <bookmark mark='e'/> Shona teachers have taught it in the United States and Europe since the nineteen-seventies. <bookmark mark='f'/> Part 40 follows such patterns into the popular song, as riffs and loops.", marks="cdef")
