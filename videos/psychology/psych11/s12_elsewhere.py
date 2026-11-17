from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Elsewhere(VoiceoverScene):
    def construct(self):
        self.card()
        self.number()
        self.time()
        self.money()

    def card(self):
        card = chapter_card(11, r"Weber's law elsewhere", r"Is a constant fraction special to the senses?", lit=(), part=PART,
                            scale=("mind", "person"), marr=("what",))
        with self.voiceover(
            "Chapter eleven. Weber's law elsewhere."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def number(self):
        d = load("elsewhere")
        h = archive.HALBERDA_2008.data
        head = heading(r"Number: \ which has more dots?")
        g = np.random.default_rng(4)

        def cloud(n, col, center):
            pts = g.uniform(-0.9, 0.9, size=(n, 2))
            return VGroup(*[Dot([center[0] + x, center[1] + y, 0], radius=0.06, color=col) for x, y in pts])
        c1, c2 = cloud(16, YOU, [2.4, 1.85]), cloud(20, YOU, [4.7, 1.85])
        frame = SurroundingRectangle(VGroup(c1, c2), color=GREY_D, buff=0.25, corner_radius=0.1)
        A = axes([1, 2], [0.45, 1.02], x_length=6.0, y_length=4.0, xticks=[1, 1.25, 1.5, 1.75, 2], yticks=[0.5, 0.75, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"the ratio of the two numbers", ylabel=r"share right",
                 center=[-3.3, -0.2, 0])
        ax = A.ax
        r = d["ratios"]
        small = curve(ax, r, d["p_small"], MODEL, stroke_width=5)
        large = DashedVMobject(curve(ax, r, d["p_large"], WHITE, stroke_width=3), num_dashes=30)
        kids = VGroup(curve(ax, r, d["p_age3"], STEVC, stroke_width=3), curve(ax, r, d["p_age6"], WEBERC, stroke_width=3))
        rows = rows_of([
            (r"too quick to count: \ the answer comes from an approximate sense of number", WHITE),
            (r"8 against 10 is as hard as 16 against 20: \ only the ratio matters. \ Weber's law", MODEL),
            (rf"adults: \ a Weber fraction of about ${h['adult_w']:.2f}$", MODEL),
            (rf"at three, \ children need a ratio of about {h['age3_ratio']}; \ at six, \ {h['age6_ratio']}", STEVC),
        ], 5.6, 28, 0.25).move_to([3.6, -1.15, 0])
        keep_in_frame(rows)
        src = published_tag(archive.HALBERDA_2008.cite)
        tag = psyche_tag(r"computed: the curves the published fractions imply")
        with self.voiceover(
            "Weber's law isn't only about lights and weights. Flash two clouds of dots, too briefly to "
            "count, and ask which has more. <bookmark mark='a'/> People answer from an approximate sense "
            "of number, and it follows Weber's law. Eight dots against ten is as hard as sixteen against "
            "twenty: only the ratio matters. The green curve and the dashed one lie on top of each other. "
            f"<bookmark mark='b'/> For adults the Weber fraction is about {h['adult_w']:.2f}. "
            "<bookmark mark='c'/> And it sharpens through childhood. At three, children need a ratio of "
            "about three to four to be reliably right; at six, about five to six. Number sense, and "
            "whether it matters for learning mathematics, is Part 30."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(frame), FadeIn(c1), FadeIn(c2), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(small), Create(large), FadeIn(rows[0]), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Create(kids), FadeIn(rows[3]), run_time=2.0)
        self.clear_scene()

    def time(self):
        d = load("elsewhere")
        head = heading(r"Time: \ the longer the interval, \ the wider the guesses")
        targets = d["time_targets"]
        cols = [WEBERC, MODEL, STEVC, YOU]
        A = axes([0, 26], [0, 1.1], x_length=5.6, y_length=2.6, xticks=[0, 4, 8, 16, 24], yticks=[], xlabel=r"seconds produced",
                 ylabel=r"", center=[-3.4, 1.0, 0])
        B = axes([0.4, 1.6], [0, 1.1], x_length=4.6, y_length=2.6, xticks=[0.5, 1, 1.5], yticks=[], xfmt=lambda v: f"{v:g}",
                 xlabel=r"produced, \ as a share of the target", ylabel=r"", center=[3.5, 1.0, 0])
        cv = d["time_cv"]
        bells, scaled = VGroup(), VGroup()
        x = np.linspace(0.01, 26, 400)
        xs = np.linspace(0.4, 1.6, 200)
        for t, c in zip(targets, cols):
            bells.add(curve(A.ax, x, np.exp(-0.5 * ((x - t) / (cv * t)) ** 2), c, stroke_width=3))
            scaled.add(curve(B.ax, xs, np.exp(-0.5 * ((xs - 1) / cv) ** 2), c, stroke_width=4 if t == targets[0] else 2))
        rows = rows_of([
            (r"produce 2, 4, 8 or 16 seconds without counting: \ the spread grows with the interval", WHITE),
            (rf"divide by the target, \ and the four curves become one: \ a constant coefficient of variation, \ here "
             rf"{100 * cv:.0f}\%", THRESH),
            (r"Weber's law for time: \ ``scalar timing'' (Gibbon 1977); \ it fails for very short intervals", DATA),
        ], 12.6, 29, 0.22).to_edge(DOWN, buff=0.75)
        src = published_tag(archive.GIBBON_1977.cite)
        tag = note(r"the curves: \ an illustration with a 15\% spread").to_corner(DR, buff=0.3)
        with self.voiceover(
            "And time. Ask people, or rats or pigeons, to wait two, four, eight or sixteen seconds without "
            "counting. <bookmark mark='a'/> The guesses spread out more for longer intervals. "
            "<bookmark mark='b'/> Divide each guess by its target, and the four spreads become one curve. "
            "The error is a constant share of the interval. That is Weber's law for time, which the "
            "timing literature calls the scalar property, after John Gibbon's theory of 1977. It holds "
            "over seconds to minutes and fails for very short intervals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bells], lag_ratio=0.5), FadeIn(rows[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in scaled], lag_ratio=0.3), FadeIn(rows[1]), FadeIn(rows[2]), run_time=3.0)
        self.clear_scene()

    def money(self):
        d = load("money")
        src = archive.BERNOULLI_1738
        head = heading(r"Money: \ Bernoulli's logarithm, \ 1738")
        A = axes([0, 1050], [0, 7.5], x_length=6.2, y_length=4.2, xticks=[0, 250, 500, 750, 1000], yticks=[0, 2, 4, 6],
                 xlabel=r"wealth, \ in ducats", ylabel=r"its value to the owner", center=[-3.2, -0.45, 0])
        ax = A.ax
        line = curve(ax, d["wealth"], d["value"], FECHC, stroke_width=6)

        def step(w, col):
            a, b = ax.c2p(w, np.log(w)), ax.c2p(w + 10, np.log(w))
            c = ax.c2p(w + 10, np.log(w + 10))
            return VGroup(Line(a, b, color=col, stroke_width=4), Line(b, c, color=col, stroke_width=6),
                          Dot(a, radius=0.06, color=col))

        poor, rich = step(10, YOU), step(1000, YOU)
        bars = VGroup()
        top = d["gain_at_10"]
        for v, txt in ((10, r"10"), (100, r"100"), (1000, r"1{,}000")):
            g = d[f"gain_at_{v}"]
            name = label(rf"+10 at {txt}", font_size=23, color=YOU)
            bar = Rectangle(width=max(2.4 * g / top, 0.02), height=0.22, stroke_width=0, fill_color=YOU, fill_opacity=0.85)
            val = label(rf"{g:.2f}", font_size=22, color=YOU)
            bars.add(VGroup(name, bar, val))
        name_w = max(b[0].width for b in bars)
        for r, b in enumerate(bars):
            y = -0.4 * r
            b[0].move_to([0, y, 0], aligned_edge=RIGHT)
            b[1].move_to([0.15, y, 0], aligned_edge=LEFT)
            b[2].next_to(b[1], RIGHT, buff=0.1)
        bars.shift(RIGHT * name_w)
        head_b = label(r"the value of ten more ducats", font_size=23, color=GREY_A)
        gains = VGroup(head_b, bars).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(ax.c2p(640, 1.75))
        rows = rows_of([
            (r"Daniel Bernoulli, \ 1738: \ the value of a small gain is inversely proportional to the wealth already "
             r"held", FECHC),
            (r"add up the gains, \ and value is the logarithm of wealth: \ Fechner's law, \ 122 years before Fechner", WHITE),
            (rf"ten ducats to someone with ten are worth about {d['ratio_10_1000']:.0f} times as much as to someone with a "
             rf"thousand", YOU),
            (r"he used it to explain insurance, \ and why no one pays much for a gamble whose average payout is infinite",
             GREY_A),
            (r"whether people's choices follow it: \ Part 26. \ They judge gains and losses from where they stand", THRESH),
        ], 5.0, 27, 0.24).move_to([4.35, -0.25, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(src.cite), note(r"the curve: \ Bernoulli's rule, \ drawn").to_corner(DR, buff=0.3))
        with self.voiceover(
            "And money, where the idea is older than Fechner. <bookmark mark='a'/> In 1738 the "
            "mathematician Daniel Bernoulli proposed that the value of a small gain to its owner is "
            "inversely proportional to the wealth its owner already holds. <bookmark mark='b'/> Add up those small "
            "gains, and value is the logarithm of wealth. It is Fechner's law, written down a hundred and "
            "twenty-two years before Fechner, for ducats instead of lights. <bookmark mark='c'/> On this "
            "rule, ten ducats to someone who has ten are worth about "
            f"{d['ratio_10_1000']:.0f} times as much as to someone who has a thousand. "
            "<bookmark mark='d'/> Bernoulli used it to explain why merchants insure their cargo, and why no "
            "one will pay much to play a game whose average payout is infinite, the puzzle called the "
            "Saint Petersburg paradox. <bookmark mark='e'/> Whether people's choices actually follow his "
            "curve is a question for Part 26. The short answer is: not quite, because people judge gains "
            "and losses from where they stand, not from their total wealth. Lights, weights, numbers, "
            "durations and money: a constant fraction, and the logarithm it leads to, is one of the most "
            "general ideas about minds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(poor), FadeIn(rich), FadeIn(gains[0]),
                      LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.4), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

