from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


WORDS = {1: "one", 2: "two", 3: "three"}


def spoken_ratio(r):
    return " to ".join(WORDS[v] for v in r)


class Priors(SoundScene):
    def construct(self):
        chapter(self, 5, r"Priors revealed by iteration", r"How do you see what a listener expects?")
        self.method()
        self.quiz()
        self.triangle()
        self.two()
        self.theorem()

    # ------------------------------------------------------------------
    def method(self):
        items = [
            (r"Nori Jacoby and Josh McDermott \ (2017): \ a loop of three intervals, \ chosen at random", WHITE),
            (r"the listener taps it back; \ the tapping is played back to the same listener, \ who taps again", WHITE),
            (r"after a few rounds, \ the rhythm no longer depends on where it started", WHITE),
            (r"it settles where the listener's expectations, \ the prior, \ put it", TUNE),
            (r"the same idea as a game of telephone: \ the message drifts toward what the players expect", GREY_A),
        ]
        rows_scene(self, r"tapping it back", items,
                   "How can you see what a listener expects, when the expectation is in their head? <bookmark mark='b'/> Nori "
                   "Jacoby and Josh McDermott, in 2017, played people a loop of three intervals chosen at random. "
                   "<bookmark mark='c'/> The listener tapped it back; the tapping was played to the same listener, who tapped "
                   "again, and so on. <bookmark mark='d'/> After a few rounds the rhythm no longer depends on where it started. "
                   "<bookmark mark='e'/> It settles where the listener's expectations, the prior, put it. "
                   "<bookmark mark='f'/> It is a game of telephone: the message drifts toward what the players expect.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("rhythm")
        c = clip("rhythm.two")
        card = listen_card(r"A random rhythm, \ looped four times. \ Then what a simulated listener tapped after five rounds "
                           r"of hearing its own tapping. \ Which could you clap along to?", width=10.4)
        with self.voiceover(
            "Listen. A random rhythm, looped four times. Then what a simulated listener tapped after five rounds of hearing "
            "its own tapping. Which could you clap along to?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ex = d["example"]
        def strip_(x, color):
            W = 9.0
            on = [0.0, x[0], x[0] + x[1]]
            fr = Line(LEFT * W / 2, RIGHT * W / 2, color=GREY_B, stroke_width=2)
            ticks = VGroup(*[Line(fr.get_left() + RIGHT * W * o + DOWN * 0.3, fr.get_left() + RIGHT * W * o + UP * 0.3, color=color, stroke_width=6) for o in on])
            return VGroup(fr, ticks)
        a = strip_(ex["start"], GREY_A)
        b = strip_(ex["end"], TUNE)
        g = VGroup(VGroup(label(r"first", font_size=20, color=GREY_A), a).arrange(DOWN, buff=0.3),
                   VGroup(label(r"second", font_size=20, color=TUNE), b).arrange(DOWN, buff=0.3)).arrange(DOWN, buff=0.9).move_to(UP * 0.4)
        cap = label(r"one cycle, \ two seconds long: \ each tick a tap", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        self.play(FadeOut(card), FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"before, \ and after five rounds", kind="synthesized", detail=r"struck-wood taps", corner=DL, tag_corner=DR)
            for name, strip, x in (("start", a, ex["start"]), ("end", b, ex["end"])):
                playhead = VGroup(Line(DOWN * 0.4, UP * 0.4, color=WHITE, stroke_width=3), Dot(radius=0.08, color=WHITE))
                def sweep(m, now, fr=strip[0], start=st[name]):
                    elapsed = now - start
                    m.set_opacity(1.0 if 0.0 <= elapsed < 8.0 else 0.0)
                    m.move_to(fr.get_left() + RIGHT * fr.width * ((elapsed % 2.0) / 2.0))
                snd.show(playhead)
                snd.drive(playhead, sweep)
                on = [0.0, x[0], x[0] + x[1]]
                for k in range(4):
                    for i, o in enumerate(on):
                        t = st[name] + (k + o) * 2.0
                        pulse(snd, strip[1][i], t, t + 0.15, buff=0.05)
        s, e = ex["start"], ex["end"]
        def ratio(x):
            m = min(x)
            return " to ".join(say(v / m, 1) for v in x)
        with self.voiceover(
            f"The second. The first loop's intervals stood in the ratio {ratio(s)}: no simple pattern. After five rounds the "
            f"listener tapped {ratio(e)}, close to {spoken_ratio(ex['near'])}. Our model explicitly supplies a prior favoring simple ratios; the iterations reveal and amplify that assumption."
        ):
            self.play(Indicate(g[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def triangle(self):
        d = load("rhythm")
        A = d["A"]
        paths = np.array(A["paths"])
        tri = simplex(side=4.6).move_to(LEFT * 3.0 + DOWN * 0.35)
        verts = tri.tri.get_vertices()
        vl = VGroup(label(r"first interval long", font_size=15, color=GREY_A).next_to(verts[0], DOWN, buff=0.15),
                    label(r"second long", font_size=15, color=GREY_A).next_to(verts[1], DOWN, buff=0.15),
                    label(r"third long", font_size=15, color=GREY_A).next_to(verts[2], UP, buff=0.1))
        pts = VGroup()
        for pat, w in A["weights"].items():
            q = tuple(int(v) for v in pat.split("-"))
            from itertools import permutations
            for o in sorted(set(permutations(q))):
                s = sum(o)
                pts.add(Circle(radius=0.12, stroke_color=EAR, stroke_width=2).move_to(tri.at([v / s for v in o])))
        dots = VGroup(*[Dot(tri.at(p[0]), radius=0.035, color=WHITE, fill_opacity=0.85) for p in paths])
        mass = A["mass"]
        plot = line_plot([mass], width=4.4, height=2.4, ylo=0, yhi=1, xmax=5, colors=[TUNE], xlabel=r"rounds", ylabel=r"share near a ratio of small integers",
                         yticks=(0, 0.5, 1), xticks=(0, 1, 2, 3, 4, 5), size=16).move_to(RIGHT * 3.6 + DOWN * 0.3)
        head = label(r"400 random rhythms, \ tapped back five times by one simulated listener", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the whole experiment, run on a simulated listener. Every three-interval rhythm is a point in this "
            "triangle: each corner is a rhythm whose whole cycle is one interval, and the centre is three equal intervals. "
            "<bookmark mark='a'/> The rings mark rhythms of small whole-number ratios: one to one to one, one to one to two "
            "in its three orders, and so on. <bookmark mark='b'/> Start four hundred chains at random. <bookmark mark='c'/> "
            "Our listener hears each rhythm with timing noise, then taps back a rhythm drawn from what it believes it heard: "
            "its posterior, which blends the noisy evidence with its prior. Round by round, the cloud gathers on the rings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tri), FadeIn(vl), FadeIn(plot[0]))
            vo.wait_until("a")
            self.play(FadeIn(pts))
            vo.wait_until("b")
            self.play(FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(plot[1:]), run_time=0.6)
            for r in range(1, 6):
                self.play(*[dt.animate.move_to(tri.at(p[r])) for dt, p in zip(dots, paths)], run_time=1.2)
        with self.voiceover(
            f"In numbers: at the start, {say(100 * mass[0])} per cent of rhythms lay near a ratio of small integers, which "
            f"is about how much of the triangle the rings cover. After one round, {say(100 * mass[1])} per cent; after three, "
            f"{say(100 * mass[3])}; and there it stays, held back only by the noise of the listener's hand. Three or four "
            "rounds are enough, which is why the real experiment could be run in an afternoon."
        ):
            self.play(Indicate(plot.lines[0], color=WHITE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two(self):
        d = load("rhythm")
        def panel(key, title, color):
            r = d[key]
            pats = list(r["prior_share"])
            land = sum(v for k, v in r["end_share"].items() if k != "none")
            rows_ = VGroup()
            for i, p in enumerate(pats):
                y = -0.6 * i
                pv = r["prior_share"][p] / sum(r["prior_share"].values())
                ev = r["end_share"].get(p, 0.0) / land
                rows_.add(VGroup(label(ratio_tex(p.split("-")), font_size=20, color=WHITE).move_to([-2.2, y, 0]),
                                 Rectangle(width=3.2 * pv, height=0.2, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9).move_to([-1.5 + 1.6 * pv, y + 0.12, 0]),
                                 Rectangle(width=3.2 * ev, height=0.2, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([-1.5 + 1.6 * ev, y - 0.12, 0])))
            return VGroup(label(title, font_size=21, color=color), rows_).arrange(DOWN, buff=0.35)
        pa = panel("A", r"listener A: \ raised on music in 4/4", TUNE)
        pb = panel("B", r"listener B: \ raised on 7/8, \ grouped 2 + 2 + 3", EAR)
        g = VGroup(pa, pb).arrange(RIGHT, buff=1.4).move_to(DOWN * 0.1)
        key = VGroup(VGroup(Rectangle(width=0.4, height=0.2, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9), label(r"its prior", font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.15),
                     VGroup(Rectangle(width=0.4, height=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=0.9), label(r"where its chains ended \ (of those that ended near a pattern)", font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.5)
        head = label(r"two simulated listeners, \ two priors", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        a, b = d["A"], d["B"]
        landA = sum(v for k, v in a["end_share"].items() if k != "none")
        landB = sum(v for k, v in b["end_share"].items() if k != "none")
        with self.voiceover(
            "Now give two simulated listeners different priors. <bookmark mark='a'/> Listener A expects what music in four "
            "four is full of: one to one to two most of all, then even beats. <bookmark mark='b'/> Listener B grew up on "
            "seven eight grouped two plus two plus three, as in much Balkan dance music. Grey bars are each prior; coloured "
            "bars are where the chains ended. "
            f"Listener A's chains ended on one to one to two {say(100 * a['end_share']['1-1-2'] / landA)} per cent of the "
            f"time, against a prior of {say(100 * a['prior_share']['1-1-2'] / sum(a['prior_share'].values()))}; listener B's on "
            f"two to two to three {say(100 * b['end_share']['2-2-3'] / landB)} per cent, against "
            f"{say(100 * b['prior_share']['2-2-3'] / sum(b['prior_share'].values()))}. The same random starts came out as "
            "two different musics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(ghost(g, 0.15)))
            vo.wait_until("a")
            self.play(FadeIn(pa))
            vo.wait_until("b")
            self.play(FadeIn(pb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        items = [
            (r"Thomas Griffiths and Michael Kalish \ (2007): \ matched generative and posterior-sampling assumptions: \\ prior is stationary; convergence needs further conditions", WHITE),
            (r"the data wash out; \ what is left is what learners bring", WHITE),
            (r"Jacoby and McDermott: \ Americans' and Tsimane' chains both settled on ratios of small integers, \ but on different ones", WHITE),
            (r"Jacoby and colleagues \ (2024): \ 39 groups in 15 countries; \ every group favoured small-integer ratios, \ in its own proportions", TUNE),
            (r"a candidate universal of the mind: \ rhythm is heard in categories of simple ratios; \ which ones, \ culture decides", GREY_A),
        ]
        rows_scene(self, r"why the chains find the prior", items,
                   "Why does this work? <bookmark mark='b'/> Thomas Griffiths and Michael Kalish proved in 2007 that if each "
                   "learner in a chain samples its posterior, under matched generative and sampling assumptions, the prior is a stationary distribution; convergence and forgetting require additional conditions: "
                   "<bookmark mark='c'/> the data wash out, and what is left is what the learners bring. "
                   "<bookmark mark='d'/> Jacoby and McDermott found that Americans' and Tsimane' chains both settled on ratios of "
                   "small integers, but on different ones. <bookmark mark='e'/> In 2024 Jacoby and colleagues ran thirty-nine "
                   "groups in fifteen countries: every group favoured small-integer ratios, each in its own proportions. "
                   "<bookmark mark='f'/> That is a candidate universal of the mind: rhythm is heard in categories of simple "
                   "ratios, and which ones, culture decides.", marks="bcdef")
