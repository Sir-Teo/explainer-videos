from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403

TAG = S.ACCENT
FISH = "#5C7A99"


class Capture(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.lake()
        self.hypergeometric()
        self.estimate()
        self.repeat()
        self.tree_update(4, "The fourth arrow: <bookmark mark='t'/> sampling without replacement from a population "
                            "much larger than the sample is almost the same as sampling with replacement, so the "
                            "hypergeometric becomes the binomial.")

    def card(self):
        card = chapter_card(4, r"Without replacement", r"How many fish are in the lake?", lit=(1898,), part=PART)
        with self.voiceover("Chapter four. Without replacement."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lake(self):
        d = load("capture")
        g = np.random.Generator(np.random.PCG64(3))
        shape = Ellipse(width=7.4, height=4.6, stroke_color=S.WORLD, stroke_width=2, fill_color="#0F2030",
                        fill_opacity=1).move_to([-2.6, -0.4, 0])
        pts = []
        while len(pts) < 420:
            x, y = g.uniform(-3.5, 3.5), g.uniform(-2.2, 2.2)
            if (x / 3.5) ** 2 + (y / 2.2) ** 2 < 0.92:
                pts.append((x - 2.6, y - 0.4))
        fish = VGroup(*[Dot([x, y, 0], radius=0.035, color=FISH) for x, y in pts])
        tagged_idx = g.choice(len(pts), 26, replace=False)
        steps = VGroup(
            label(rf"1. \ catch {d['n1']}, \ tag them, \ let them go", font_size=26, color=TAG),
            label(rf"2. \ later, \ catch {d['n2']}", font_size=26),
            label(rf"3. \ count the tagged: \ $m = {d['m']}$", font_size=26, color=TAG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 1.0, 0])
        q = label(r"how many fish, $N$?", font_size=32, color=S.ACCENT).move_to([4.2, -1.2, 0])
        tag = simulated_tag(r"simulated: the World's lake")
        recap = VGroup(*[Circle(radius=0.09, stroke_color=WHITE, stroke_width=1.5).move_to(fish[i])
                         for i in g.choice(len(pts), 20, replace=False)])
        with self.voiceover(
            "The World has a lake, and the lake has fish. How many? You can't count them; they won't hold still. "
            "<bookmark mark='a'/> So catch some, five hundred, tag them, and let them go. <bookmark mark='b'/> Wait "
            "for them to mix back in, then catch another sample, four hundred. <bookmark mark='c'/> Count how many of "
            f"the second catch carry tags: {d['m']}. <bookmark mark='d'/> From those three numbers, estimate the size "
            "of the whole population. The method is called capture–recapture, and it's how ecologists count "
            "everything from fish to whales; Laplace used the same ratio in 1802 to estimate the population of "
            "France."
        ) as vo:
            self.play(FadeIn(shape), FadeIn(fish, lag_ratio=0.002), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), *[fish[i].animate.set_color(TAG).scale(1.6) for i in tagged_idx])
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), LaggedStart(*[Create(c) for c in recap], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.clear_scene()

    def hypergeometric(self):
        d = load("capture")
        kk = np.asarray(d["kk"])
        A = axes([-0.6, 60.6], [0, 0.09], x_length=8.0, y_length=4.0, xlabel=r"tagged fish in the second catch, $m$",
                 xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[0, 0.04, 0.08], center=[-2.0, -0.8, 0])
        ax = A.ax
        bars = pmf_bars(ax, kk, d["hyp"], DISC, width=0.7)
        dots = pmf_dots(ax, kk, d["bino"], EXACT, radius=0.045)
        f = MathTex(r"P(m)", r"=", r"\frac{\binom{n_1}{m} \binom{N - n_1}{n_2 - m}}{\binom{N}{n_2}}", font_size=36)
        f.move_to([4.2, 2.4, 0])
        f[0].set_color(DISC)
        fw = label(r"choose $m$ tagged and $n_2 - m$ untagged \ of all $\binom{N}{n_2}$ catches", font_size=22,
                   color=GREY_B).next_to(f, DOWN, buff=0.2)
        if fw.width > 5.8:
            fw.width = 5.8
        leg = legend([(DISC, r"hypergeometric"), (EXACT, rf"binomial$({d['n2']}, n_1/N)$")], font_size=22)
        leg.move_to([4.4, 0.4, 0])
        nt = label(r"without replacement \ $\approx$ \ with, \ when $N \gg n_2$", font_size=24, color=GREY_A)
        nt.move_to([4.4, -0.6, 0])
        with self.voiceover(
            "First, what should the number of tagged fish look like, if there are N fish in all? "
            "<bookmark mark='a'/> The second catch is four hundred fish drawn without replacement. The chance of "
            "exactly m tagged is the number of ways to pick m of the tagged fish and the rest from the untagged, "
            "over the number of possible catches. That's the hypergeometric distribution. "
            "<bookmark mark='b'/> With the World's true N, it's centred near twenty-five. <bookmark mark='c'/> And "
            "it's almost exactly a binomial: when the lake is much bigger than the catch, taking a fish out barely "
            "changes the chances for the next one, so sampling without replacement is nearly sampling with it."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fw))
            vo.wait_until("b")
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(leg), FadeIn(nt))
        self.clear_scene()

    def estimate(self):
        d = load("capture")
        rows = [
            cmath(r"\frac{n_1}{N}", r"\approx", r"\frac{m}{n_2}", font_size=42),
            cmath(r"\hat N", r"=", r"\frac{n_1 n_2}{m}", r"=", rf"\frac{{{d['n1']} \cdot {d['n2']}}}{{{d['m']}}}", r"=",
                  rf"{money(d['estimate'])}", font_size=40),
        ]
        rows[1][0].set_color(S.EST)
        rows[1][6].set_color(S.EST)
        whys = [why(r"the tagged share of the lake, \ seen in the catch"), why(r"Petersen 1896; \ Lincoln 1930")]
        truth = MathTex(r"N", r"=", rf"{money(d['N'])}", font_size=40, color=S.TRUTH).move_to([0, -1.6, 0])
        tl = label(r"the World knows the truth", font_size=24, color=S.TRUTH).next_to(truth, DOWN, buff=0.2)
        with self.voiceover(
            "Now estimate. <bookmark mark='a'/> The share of the lake that's tagged, five hundred over N, should be "
            "about the share of the catch that's tagged, m over four hundred. <bookmark mark='b'/> Solve for N: five "
            f"hundred times four hundred, over {d['m']}, about {money(round(d['estimate'], -1))} fish. It's called the "
            "Lincoln–Petersen estimate. <bookmark mark='c'/> And because this is the World, we can check it. The "
            f"lake actually holds {money(d['N'])} fish. Our estimate is off by a fifth. Was the method wrong, or "
            "were we unlucky?"
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.4, x=0.0, buff=0.7)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(truth), FadeIn(tl))
        self.clear_scene()

    def repeat(self):
        d = load("capture")
        lp, chap = np.asarray(d["lp"]), np.asarray(d["chap"])
        A = axes([3000, 16000], [0, 0.00032], x_length=8.6, y_length=4.2, xlabel=r"estimated number of fish",
                 xticks=[4000, 8000, 12000, 16000], xfmt=lambda v: fmt_int(v), center=[-1.4, -0.4, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        edges = np.linspace(3000, 16000, 53)
        h = hist_bars(ax, edges, np.histogram(lp, edges)[0] / (len(lp) * np.diff(edges)), color=SIM)
        tl = Line(ax.c2p(d["N"], 0), ax.c2p(d["N"], 0.00032), color=S.TRUTH, stroke_width=4)
        tlab = MathTex(rf"N = {money(d['N'])}", font_size=28, color=S.TRUTH).next_to(tl, UP, buff=0.08)
        ours = Line(ax.c2p(d["estimate"], 0), ax.c2p(d["estimate"], 0.0001), color=S.ACCENT, stroke_width=4)
        ol = label(r"ours", font_size=22, color=S.ACCENT).next_to(ours, UP, buff=0.05)
        stats_ = VGroup(
            MathTex(rf"\text{{Lincoln--Petersen: mean }} {money(d['lp_mean'])}", font_size=26, color=SIM),
            MathTex(rf"\text{{Chapman: mean }} {money(d['chap_mean'])}", font_size=26, color=S.LIK),
            MathTex(r"\hat N_C = \frac{(n_1 + 1)(n_2 + 1)}{m + 1} - 1", font_size=28, color=S.LIK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, 1.6, 0])
        why_ = label(r"$1/m$ is convex: \ Jensen pushes $E[1/m]$ above $1/E m$ \ (Part 9)", font_size=22, color=GREY_B)
        why_.to_edge(DOWN, buff=0.3)
        tag = simulated_tag(r"simulated: 2,000 repetitions in the World's lake")
        with self.voiceover(
            "In the World we can find out, by doing the whole experiment again, two thousand times. "
            "<bookmark mark='a'/> Here are two thousand Lincoln–Petersen estimates. <bookmark mark='b'/> They "
            "spread from about five thousand to fourteen thousand; ours was in the low tail. So partly we were "
            f"unlucky. <bookmark mark='c'/> But their average is {money(d['lp_mean'])}, above the truth: the "
            "estimate is biased upward, because dividing by a random m exaggerates the small values of m. In 1951 "
            "Douglas Chapman proposed adding one to each count, and his version averages "
            f"{money(d['chap_mean'])}, almost exactly right. Bias, and how to remove it, is the subject of Part 9."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h, lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(tl), FadeIn(tlab), Create(ours), FadeIn(ol))
            vo.wait_until("c")
            self.play(FadeIn(stats_), FadeIn(why_))
        self.clear_scene()
