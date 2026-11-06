from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class Waiting(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.geometric()
        self.memoryless()
        self.first_step()
        self.negbin()
        self.tree_voiceover("Two more arrows: <bookmark mark='t'/> waiting for the first success turns Bernoulli "
                            "trials into a geometric, and adding r independent geometric waits gives a negative "
                            "binomial.", 3)

    def card(self):
        card = chapter_card(3, r"Waiting", r"How long until the first six?", lit=(1654,), part=PART)
        with self.voiceover("Chapter three. Waiting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def geometric(self):
        d = load("waiting")
        ks, geo = np.asarray(d["ks"]), np.asarray(d["geo"])
        A = axes([0.4, 30.6], [0, 0.18], x_length=8.6, y_length=4.2, xlabel=r"throws until the first six, $T$",
                 xticks=[1, 5, 10, 15, 20, 25, 30], yticks=[0, 0.1], center=[-1.6, -0.6, 0])
        bars = pmf_bars(A.ax, ks, geo, DISC, width=0.7)
        f = MathTex(r"P(T = k)", r"=", r"(1-p)^{k-1}\, p", font_size=38).move_to([4.2, 2.6, 0])
        f[0].set_color(DISC)
        fw = label(r"$k - 1$ failures, \ then a success", font_size=22, color=GREY_B).next_to(f, DOWN, buff=0.15)
        m = MathTex(r"E T", r"=", r"\frac1p", r"= 6", font_size=36).move_to([4.6, 1.0, 0])
        m[3].set_color(EXACT)
        sim = MathTex(rf"\text{{simulated}}\ {d['mean_wait']:.3f}", font_size=26, color=SIM).next_to(m, DOWN, buff=0.2)
        why_ = label(r"layer cake: \ $E T = \sum_{k \ge 0} P(T > k) = \sum (1-p)^k = 1/p$", font_size=22, color=GREY_B)
        why_.to_edge(DOWN, buff=0.3)
        intro = label('Waiting for the first success', font_size=36)
        with self.voiceover(
            "Instead of counting successes in a fixed number of trials, wait for the first one. <bookmark mark='a'/> "
            "Throw a die until it shows a six. The wait T is k throws if the first k minus one fail and the k-th "
            "succeeds: probability one minus p to the k minus one, times p. That's the geometric distribution. "
            "<bookmark mark='b'/> Each extra throw multiplies the chance by five sixths, so the bars decay "
            "geometrically, which is the name. <bookmark mark='c'/> On average you wait one over p throws: six for "
            "a die. The layer-cake formula of Part 2 gives it in one line, and fifty thousand simulated waits "
            "agree."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(f), FadeIn(fw))
            vo.wait_until("b")
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("c")
            self.play(Write(m), FadeIn(sim), FadeIn(why_))
        self.clear_scene()

    def memoryless(self):
        d = load("waiting")
        ks, geo = np.asarray(d["ks"]), np.asarray(d["geo"])
        s_, t_ = d["s"], d["t"]
        A = axes([0.4, 30.6], [0, 0.18], x_length=8.6, y_length=3.6, xticks=[1, 5, 10, 15, 20, 25, 30],
                 yticks=[0, 0.1], center=[-1.6, 0.4, 0])
        ax = A.ax
        bars = pmf_bars(ax, ks, geo, DISC, width=0.7)
        cut = DashedLine(ax.c2p(s_ + 0.5, 0), ax.c2p(s_ + 0.5, 0.18), color=S.ACCENT, stroke_width=2)
        cl = label(rf"already waited {s_}", font_size=22, color=S.ACCENT).next_to(cut, UP, buff=0.1)
        tail = VGroup(*[b for k, b in zip(ks, bars) if k > s_])
        head_bars = VGroup(*[b for k, b in zip(ks, bars) if k <= s_])
        rescaled = pmf_bars(ax, ks[: len(tail)], geo[s_:] / (5 / 6) ** s_, S.ACCENT, width=0.7, opacity=0.6)
        eq = MathTex(r"P(T > s + t \mid T > s)", r"=", r"P(T > t)", font_size=36).to_edge(DOWN, buff=1.2)
        chk = MathTex(rf"\text{{simulated: }}{d['lhs']:.3f} \ \text{{vs}}\ {d['rhs']:.3f};\ \ \text{{exact }} "
                      rf"(5/6)^3 = {d['exact_ml']:.3f}", font_size=26, color=SIM).next_to(eq, DOWN, buff=0.2)
        with self.voiceover(
            "The geometric has a remarkable property. <bookmark mark='a'/> Suppose you've already thrown five times "
            "without a six. <bookmark mark='b'/> Throw away the first five bars, rescale the rest so they add to "
            "one, and slide them back to the start. <bookmark mark='c'/> They match the original exactly. Having "
            "waited tells you nothing about how much longer you'll wait: the die has no memory. "
            "<bookmark mark='d'/> In symbols, the chance of waiting t more, given that you've waited s, is the "
            "chance of waiting t from scratch. The gambler who thinks a six is overdue is wrong, and this is why."
        ) as vo:
            self.play(FadeIn(A), FadeIn(bars))
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cl))
            vo.wait_until("b")
            self.play(head_bars.animate.set_opacity(0.2))
            self.play(ReplacementTransform(tail.copy(), rescaled), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(rescaled, color=S.ACCENT, scale_factor=1.03))
            vo.wait_until("d")
            self.play(Write(eq), FadeIn(chk))
        self.clear_scene()

    def first_step(self):
        lv = ["", "", WHITE, [(r"\text{six}", r"p", S.ACCENT, []), (r"\text{not}", r"1 - p", GREY_B, [])]]
        tree = prob_tree(lv, x0=-6.0, dx=3.0, height=3.0, font_size=30).move_to([-4.0, 1.2, 0])
        done = label(r"done: \ $1$ throw", font_size=24, color=S.ACCENT).next_to(tree.nodes[(0,)], RIGHT, buff=0.3)
        again = label(r"start over: \ $1 + T'$", font_size=24, color=GREY_B).next_to(tree.nodes[(1,)], RIGHT, buff=0.3)
        rows = [
            cmath(r"E T", r"=", r"p \cdot 1 + (1 - p)(1 + E T)", font_size=38),
            cmath(r"p\, E T", r"=", r"1", font_size=38),
            cmath(r"E T", r"=", r"\frac1p", font_size=42),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"condition on the first throw; \ no memory: \ $T'$ is a fresh $T$"), why(r"rearrange"), None]
        pas = label(r"Pascal's method from Part 2: \ value now $=$ average of the values next", font_size=24,
                    color=GREY_B).to_edge(DOWN, buff=0.4)
        intro = label('Condition on the first throw', font_size=36)
        with self.voiceover(
            "Memorylessness gives a second, slicker way to the mean, and it's Pascal's method from Part 2. "
            "<bookmark mark='a'/> Condition on the first throw. With probability p it's a six, and you're done in "
            "one throw. <bookmark mark='b'/> Otherwise you've used one throw, and because the die has no memory, "
            "you're back where you started: the rest of the wait is a fresh copy of T. <bookmark mark='c'/> So the "
            "expected wait satisfies an equation involving itself: p times one, plus one minus p times one plus the "
            "expected wait. <bookmark mark='d'/> Solve it, and the expected wait is one over p. This first-step "
            "analysis solves waiting problems far harder than this one, from the gambler's ruin to Markov chains "
            "in Part 7."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tree), FadeIn(done))
            vo.wait_until("b")
            self.play(FadeIn(again))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=2.6, buff=0.55, edge=6.9)
            vo.wait_until("c")
            step(0, transform=False)
            vo.wait_until("d")
            step(1)
            step(2)
            self.play(FadeIn(pas))
        self.clear_scene()

    def negbin(self):
        d = load("waiting")
        ks, nb = np.asarray(d["ks"]), np.asarray(d["nb"])
        A = axes([0.4, 30.6], [0, 0.08], x_length=7.6, y_length=3.8, xlabel=r"throws until the third six",
                 xticks=[3, 10, 20, 30], yticks=[0, 0.04, 0.08], center=[-2.2, -0.6, 0])
        bars = pmf_bars(A.ax, ks, nb, DISC, width=0.7)
        f = MathTex(r"P(T_3 = k)", r"=", r"\binom{k-1}{2} p^3 (1-p)^{k-3}", font_size=34).move_to([3.8, 2.6, 0])
        f[0].set_color(DISC)
        fw = label(r"the $k$-th throw is the third six; \ two sixes among the first $k-1$", font_size=22,
                   color=GREY_B).next_to(f, DOWN, buff=0.15)
        if fw.width > 6.0:
            fw.width = 6.0
        m = MathTex(r"T_r = G_1 + \cdots + G_r", r",\quad E T_r = \frac{r}{p} = 18", font_size=32).move_to([4.0, 0.6, 0])
        nxt = label(r"failures $T_r-r$: \ a gamma--Poisson mixture \ (chapter 12)", font_size=24, color=GREY_A)
        nxt.move_to([4.0, -0.6, 0])
        if nxt.width > 6.0:
            nxt.width = 6.0
        intro = label('Waiting for the third success', font_size=36)
        with self.voiceover(
            "Wait for more than one success and you get the negative binomial. <bookmark mark='a'/> The wait for the "
            "third six is k throws if the k-th throw is a six and exactly two of the first k minus one were: k minus "
            "one choose two, times p cubed, times the failures. <bookmark mark='b'/> It's also a sum: the wait for "
            "the first six, plus the further wait for the second, plus the wait for the third, three independent "
            "geometric waits, because the die has no memory. So the mean is r over p, eighteen. "
            "<bookmark mark='c'/> Count failures instead of total trials, subtracting r, and the negative binomial has a second life as a Poisson count whose rate is itself "
            "random, and in that guise it's the workhorse for counts more variable than a Poisson allows. We'll "
            "derive that in chapter twelve."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(f), FadeIn(fw), FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                                                    lag_ratio=0.03), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(m))
            vo.wait_until("c")
            self.play(FadeIn(nxt))
        self.clear_scene()
