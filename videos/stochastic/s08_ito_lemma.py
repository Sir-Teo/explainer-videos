from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (boxed, hero, label, load, mtex, mult_table, note, num, num_table, part_card,
                                      path_curve, polyline, tw_axes)


class ItoLemma(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain_rule_fails()
        self.taylor()
        self.lemma()
        self.check_on_path()
        self.convexity()
        self.general()

    def card(self):
        c = part_card(3, r"It\^o's lemma", r"the chain rule, corrected for noise")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def chain_rule_fails(self):
        cr = MathTex(r"\frac{d}{dt} f(x(t))", r"=", r"f'(x)\,\frac{dx}{dt}", font_size=42)
        cr2 = MathTex(r"df", r"=", r"f'(x)\,dx", font_size=42)
        guess = MathTex(r"d\big(W^2\big)", r"\overset{?}{=}", r"2W\,dW", font_size=42)
        truth = MathTex(r"d\big(W^2\big)", r"=", r"2W\,dW", r"+", r"dt", font_size=42)
        truth[4].set_color(C.QV)
        for m in (cr, cr2):
            m.to_edge(UP, buff=0.8)
        guess.next_to(cr2, DOWN, buff=0.7)
        truth.move_to(guess)
        src = label(r"from the missing half: \ $W_T^2 = 2\int_0^T W\,dW + T$", font_size=28, color=GREY_A)
        src.next_to(truth, DOWN, buff=0.45)
        with self.voiceover(
            "In ordinary calculus, the chain rule tells you how a function of a changing quantity changes: "
            "<bookmark mark='a'/> d f equals f prime times d x. <bookmark mark='g'/> Applied to W squared, it would say "
            "the change in W squared is two W d W. <bookmark mark='t'/> But we've already found the truth: W squared at "
            "time T is twice the integral of W d W, plus T. So the change in W squared has an extra piece: plus d t. "
            "Where does it come from, and what is it for a general function?"
        ) as vo:
            self.play(Write(cr))
            vo.wait_until("a")
            self.play(TransformMatchingTex(cr, cr2))
            vo.wait_until("g")
            self.play(Write(guess))
            vo.wait_until("t")
            self.play(FadeIn(src), TransformMatchingTex(guess, truth))
            self.play(Circumscribe(truth[4], color=C.QV))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def taylor(self):
        tay = MathTex(r"\Delta f", r"=", r"f'(W)\,\Delta W", r"+", r"\tfrac12 f''(W)\,(\Delta W)^2", r"+",
                      r"\tfrac16 f'''(W)\,(\Delta W)^3", r"+", r"\cdots", font_size=40).to_edge(UP, buff=0.45)
        tay[2].set_color(C.BROWNIAN)
        tay[4].set_color(C.QV)
        tay[6].set_color(GREY_B)
        sizes = VGroup(
            MathTex(r"\sim \Delta t^{1/2}", font_size=30, color=C.BROWNIAN).next_to(tay[2], DOWN, buff=0.3),
            MathTex(r"\sim \Delta t", font_size=30, color=C.QV).next_to(tay[4], DOWN, buff=0.3),
            MathTex(r"\sim \Delta t^{3/2}", font_size=30, color=GREY_B).next_to(tay[6], DOWN, buff=0.3),
        )
        fates = VGroup(
            label(r"sum: random signs,\\an It\^o integral", font_size=24, color=C.BROWNIAN).next_to(sizes[0], DOWN, buff=0.2),
            label(r"sum: $n\cdot\Delta t$ stays finite\\$\to \int \tfrac12 f''\,dt$", font_size=24, color=C.QV).next_to(sizes[1], DOWN, buff=0.2),
            label(r"sum: $n\cdot\Delta t^{3/2} \to 0$", font_size=24, color=GREY_B).next_to(sizes[2], DOWN, buff=0.2),
        )
        with self.voiceover(
            "Go back to basics: Taylor's theorem. <bookmark mark='t'/> Over one small step, the change in f is f prime "
            "times delta W, plus one half f double prime times delta W squared, plus a cubic term, and so on. "
            "<bookmark mark='s'/> In ordinary calculus, only the first term matters, because the others are too small to "
            "survive being added up. But now delta W is the size of root delta t. <bookmark mark='a'/> So the first term "
            "is of order root delta t, <bookmark mark='b'/> the second of order delta t, <bookmark mark='c'/> and the "
            "third of order delta t to the three halves."
        ) as vo:
            self.play(Write(tay), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(sizes[0], shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(sizes[1], shift=DOWN * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(sizes[2], shift=DOWN * 0.1))
        with self.voiceover(
            "Now add up n of them, one per step, where n is T over delta t. <bookmark mark='a'/> The first terms have "
            "random signs, and their sum is an Itô integral. <bookmark mark='b'/> The second terms are n times something of "
            "order delta t: that stays finite. In fact, by our rule, delta W squared adds up like delta t, so this sum "
            "becomes an ordinary integral of one half f double prime. <bookmark mark='c'/> The third terms add up to n "
            "times delta t to the three halves, which goes to zero. So do all the rest."
        ) as vo:
            for m, f in zip("abc", fates):
                vo.wait_until(m)
                self.play(FadeIn(f, shift=DOWN * 0.1))

        h = load("hero")
        idx = [list(h["n"]).index(n) for n in (16, 256, 4096, 65536, 4194304)]
        WT = float(hero()[-1])
        rows = []
        for i in idx:
            rows.append([f"{int(h['n'][i]):,}".replace(",", "{,}"), num(h["cube1"][i], 3), num(h["cube2"][i], 3),
                         num(h["cube3"][i], 4), num(h["cube1"][i] + h["cube2"][i] + h["cube3"][i], 4)])
        tab = num_table([r"n", r"\sum 3W^2\,\Delta W", r"\sum 3W\,(\Delta W)^2", r"\sum (\Delta W)^3", r"\text{total}"],
                        rows, font_size=28, col_colors=[C.CLOCK, C.BROWNIAN, C.QV, GREY_B, WHITE])
        tab.to_edge(DOWN, buff=0.75).set_x(0)
        ftitle = label(r"exact for $f(x) = x^3$, on our path:", font_size=28).next_to(tab, UP, buff=0.25)
        target = MathTex(r"3\int_0^1 W\,dt = " + num(3 * float(h["int_W"][0]), 3), font_size=28, color=C.QV)
        target.next_to(tab.cols[2], DOWN, buff=0.2)
        w3 = MathTex(r"W_1^3 = " + num(WT**3, 4), font_size=28).next_to(tab.cols[4], DOWN, buff=0.2)
        assert np.allclose(h["cube1"] + h["cube2"] + h["cube3"], WT**3)
        with self.voiceover(
            "Let's watch it happen. For f equals x cubed, Taylor's expansion stops after three terms, so it's exact: "
            "<bookmark mark='t'/> W cubed at time one is exactly the sum of these three columns, at every resolution. "
            "<bookmark mark='c'/> As the steps shrink, the cubic column dies away to nothing. <bookmark mark='q'/> The "
            "middle column settles to 0.338, which is three times the integral of W d t, just as predicted. "
            "<bookmark mark='w'/> And the totals never change: always W cubed, 1.966."
        ) as vo:
            self.play(FadeOut(fates), FadeOut(sizes), FadeIn(ftitle))
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(tab.cols[3], color=GREY_A))
            vo.wait_until("q")
            self.play(FadeIn(target), Indicate(tab.cols[2], color=C.QV))
            vo.wait_until("w")
            self.play(FadeIn(w3), Indicate(tab.cols[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lemma(self):
        lem = MathTex(r"df(W_t)", r"=", r"f'(W_t)\,dW_t", r"+", r"\tfrac12 f''(W_t)\,dt", font_size=54)
        lem[2].set_color(C.BROWNIAN)
        lem[4].set_color(C.QV)
        lb = boxed(lem, color=C.QV, buff=0.3).move_to(UP * 1.4)
        name = label(r"It\^o's lemma (It\^o, 1951)", font_size=30, color=GREY_A).next_to(lb, UP, buff=0.2)
        b = Brace(lem[4], DOWN, buff=0.15, color=C.QV)
        bl = label(r"new: from $(dW)^2 = dt$", font_size=28, color=C.QV).next_to(b, DOWN, buff=0.1)
        ex = VGroup(
            MathTex(r"f = x^2:", r"\quad d(W^2)", r"=", r"2W\,dW", r"+", r"dt", font_size=40),
            MathTex(r"f = x^3:", r"\quad d(W^3)", r"=", r"3W^2\,dW", r"+", r"3W\,dt", font_size=40),
            MathTex(r"f = e^x:", r"\quad d(e^W)", r"=", r"e^W\,dW", r"+", r"\tfrac12 e^W\,dt", font_size=40),
        )
        for e in ex:
            e[3].set_color(C.BROWNIAN)
            e[5].set_color(C.QV)
            e.shift(-e[2].get_center()[0] * RIGHT)
        ex.arrange(DOWN, buff=0.3).next_to(bl, DOWN, buff=0.45)
        for e in ex:
            e.shift((0.4 - e[2].get_center()[0]) * RIGHT)
        with self.voiceover(
            "So here's the corrected chain rule. <bookmark mark='l'/> The change in f of W is f prime d W, the term you'd "
            "expect, <bookmark mark='n'/> plus one half f double prime d t: a new term that comes straight from d W "
            "squared equals d t. This is Itô's lemma."
        ) as vo:
            vo.wait_until("l")
            self.play(Write(lem[:3]), FadeIn(name))
            vo.wait_until("n")
            self.play(Write(lem[3:]), Create(lb[0]))
            self.play(GrowFromCenter(b), FadeIn(bl))
        with self.voiceover(
            "Check it on W squared: <bookmark mark='a'/> f double prime is two, so the change is two W d W plus d t. "
            "Exactly what the telescoping sum told us, by a completely different route. <bookmark mark='b'/> For W "
            "cubed, three W squared d W plus three W d t: the two columns in the table. <bookmark mark='c'/> And for e "
            "to the W, the correction is one half e to the W d t."
        ) as vo:
            for m, e in zip("abc", ex):
                vo.wait_until(m)
                self.play(FadeIn(e, shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check_on_path(self):
        n = 4096
        w = hero(n)
        ts = np.linspace(0, 1, n + 1)
        naive = np.concatenate([[0], np.cumsum(2 * w[:-1] * np.diff(w))])
        ito = naive + ts
        truth = w**2
        assert np.max(np.abs(naive + np.concatenate([[0], np.cumsum(np.diff(w) ** 2)]) - truth)) < 1e-9
        assert np.max(np.abs(ito - truth)) < 0.06
        ax = tw_axes(x_length=10.5, y_range=(-0.8, 2.0, 0.5), y_length=4.8).move_to(DOWN * 0.7)
        c_truth = path_curve(ax, truth, color=WHITE, stroke_width=7).set_stroke(opacity=0.35)
        c_naive = path_curve(ax, naive, color=C.RIGHT_PT, stroke_width=2.5)
        c_ito = path_curve(ax, ito, color=C.QV, stroke_width=2.5)
        leg = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=WHITE, stroke_width=7).set_stroke(opacity=0.35),
                   MathTex(r"W_t^2", font_size=30)),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C.RIGHT_PT, stroke_width=3),
                   MathTex(r"\int_0^t 2W\,dW", r"\quad\text{(ordinary chain rule)}", font_size=30, color=C.RIGHT_PT)),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C.QV, stroke_width=3),
                   MathTex(r"\int_0^t 2W\,dW + t", r"\quad\text{(It\^o)}", font_size=30, color=C.QV)),
        )
        for g in leg:
            g.arrange(RIGHT, buff=0.2)
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.45)
        gap = DoubleArrow(ax.c2p(1, naive[-1]), ax.c2p(1, truth[-1]), buff=0, color=C.QV, stroke_width=3,
                          tip_length=0.15)
        gap_l = MathTex(r"\text{gap} \approx t", font_size=30, color=C.QV).next_to(gap, RIGHT, buff=0.1)
        sim = note(r"our path, $4{,}096$ steps").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's the lemma at work on our path. <bookmark mark='w'/> The faint thick curve is W squared itself. "
            "<bookmark mark='n'/> The red curve integrates the ordinary chain rule, two W d W, step by step: it falls "
            "further and further behind. <bookmark mark='i'/> Add Itô's correction, plus t, and it lands right on top."
        ) as vo:
            self.play(Create(ax), FadeIn(ax.x_labels), FadeIn(sim))
            vo.wait_until("w")
            self.play(Create(c_truth), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("n")
            self.play(Create(c_naive), FadeIn(leg[1]), run_time=2)
            self.play(GrowFromCenter(gap), FadeIn(gap_l))
            vo.wait_until("i")
            self.play(Create(c_ito), FadeIn(leg[2]), run_time=2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def convexity(self):
        ax = Axes(x_range=[-1.6, 1.6, 0.5], y_range=[0, 2.4, 0.5], x_length=6.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_edge(LEFT, buff=0.6).shift(DOWN * 0.5)
        bowl = ax.plot(lambda x: x * x, x_range=[-1.5, 1.5], color=C.DRIFT, stroke_width=3.5)
        bl = MathTex(r"f(x) = x^2", font_size=30, color=C.DRIFT).next_to(ax.c2p(1.5, 2.25), RIGHT, buff=0.1)
        x0, h = 0.35, 0.75
        p0 = ax.c2p(x0, x0**2)
        pm, pp = ax.c2p(x0 - h, (x0 - h) ** 2), ax.c2p(x0 + h, (x0 + h) ** 2)
        dot = Dot(p0, radius=0.08, color=WHITE)
        dm, dp = Dot(pm, radius=0.07, color=C.BROWNIAN), Dot(pp, radius=0.07, color=C.BROWNIAN)
        am = Arrow(ax.c2p(x0, 0), ax.c2p(x0 - h, 0), buff=0, color=C.BROWNIAN, stroke_width=3)
        ap = Arrow(ax.c2p(x0, 0), ax.c2p(x0 + h, 0), buff=0, color=C.BROWNIAN, stroke_width=3)
        lab = VGroup(MathTex(r"x - h", font_size=26).next_to(ax.c2p(x0 - h, 0), DOWN, buff=0.1),
                     MathTex(r"x", font_size=26).next_to(ax.c2p(x0, 0), DOWN, buff=0.1),
                     MathTex(r"x + h", font_size=26).next_to(ax.c2p(x0 + h, 0), DOWN, buff=0.1))
        chord = Line(pm, pp, color=C.BROWNIAN, stroke_width=2.5)
        mid = (pm + pp) / 2
        dmid = Dot(mid, radius=0.07, color=C.QV)
        lift = Line(p0, mid, color=C.QV, stroke_width=5)
        lift_l = MathTex(r"\tfrac12 f''(x)\,h^2", font_size=30, color=C.QV).next_to(lift, LEFT, buff=0.15)
        avg = MathTex(r"\frac{f(x+h) + f(x-h)}{2}", r"=", r"f(x)", r"+", r"\tfrac12 f''(x)\,h^2", r"+ \cdots", font_size=36)
        avg[4].set_color(C.QV)
        avg.to_edge(UP, buff=0.4).shift(RIGHT * 1.5)

        # right: average of W_t^2 over 200 paths rises like t, while the average of W_t stays at 0
        f = load("fan")["paths"]
        rax = tw_axes(x_length=4.6, y_range=(-0.6, 1.4, 0.5), y_length=3.6).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.7)
        ts = np.linspace(0, 1, f.shape[1])
        mw = polyline(rax, ts, f.mean(axis=0), color=C.BROWNIAN, stroke_width=3)
        mw2 = polyline(rax, ts, (f**2).mean(axis=0), color=C.QV, stroke_width=3)
        line = DashedLine(rax.c2p(0, 0), rax.c2p(1, 1), color=C.CLOCK, stroke_width=2)
        rl = VGroup(MathTex(r"\text{avg } W_t", font_size=26, color=C.BROWNIAN).next_to(rax.c2p(1, 0), RIGHT, buff=0.1),
                    MathTex(r"\text{avg } W_t^2", font_size=26, color=C.QV).next_to(rax.c2p(1, 1), RIGHT, buff=0.1))
        rnote = note(r"200 simulated paths").next_to(rax, DOWN, buff=0.35)
        with self.voiceover(
            "Here's the intuition. <bookmark mark='a'/> Picture a curved bowl, f, and a point at x. <bookmark mark='b'/> "
            "The noise pushes x to the left or right by the same amount, h, with equal odds. On average, x hasn't moved. "
            "<bookmark mark='c'/> But f has: the average of the two outcomes is the midpoint of this chord, and on a convex "
            "curve, the chord lies above the curve. <bookmark mark='d'/> It sits higher by one half f double prime h "
            "squared. And h squared is delta t."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), Create(bowl), FadeIn(bl), FadeIn(dot), FadeIn(lab[1]))
            vo.wait_until("b")
            self.play(GrowArrow(am), GrowArrow(ap), FadeIn(lab[0]), FadeIn(lab[2]))
            vo.wait_until("c")
            self.play(FadeIn(dm), FadeIn(dp), Create(chord))
            self.play(FadeIn(dmid))
            vo.wait_until("d")
            self.play(Create(lift), FadeIn(lift_l), Write(avg))
        with self.voiceover(
            "So noise, plus curvature, makes drift. <bookmark mark='r'/> Across two hundred paths, the average of W stays at "
            "zero, but the average of W squared climbs steadily: one unit of height per unit of time. That climb is the "
            "Itô term, one half f double prime d t."
        ) as vo:
            vo.wait_until("r")
            self.play(Create(rax), Create(line), FadeIn(rnote))
            self.play(Create(mw), Create(mw2), FadeIn(rl), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def general(self):
        proc = MathTex(r"dX", r"=", r"\mu\,dt", r"+", r"\sigma\,dW", font_size=42)
        proc[2].set_color(C.DRIFT)
        proc[4].set_color(C.BROWNIAN)
        proc.to_edge(UP, buff=0.4)
        pl = label(r"an It\^o process: drift plus noise", font_size=26, color=GREY_A).next_to(proc, DOWN, buff=0.12)
        s1 = MathTex(r"df", r"=", r"f_t\,dt", r"+", r"f_x\,dX", r"+", r"\tfrac12 f_{xx}\,(dX)^2", font_size=40)
        s1[6].set_color(C.QV)
        s2 = MathTex(r"(dX)^2", r"=", r"\mu^2\,dt^2", r"+", r"2\mu\sigma\,dt\,dW", r"+", r"\sigma^2\,dW^2", font_size=40)
        s2[0].set_color(C.QV)
        s3 = MathTex(r"(dX)^2", r"=", r"\sigma^2\,dt", font_size=40)
        s3[0].set_color(C.QV)
        col = VGroup(s1, s2).arrange(DOWN, buff=0.5).next_to(pl, DOWN, buff=0.5)
        for m in (s2,):
            m.shift((s1[1].get_center()[0] - m[1].get_center()[0]) * RIGHT)
        s3.shift(s2[1].get_center() - s3[1].get_center())
        crosses = VGroup(Cross(s2[2], stroke_color=C.RIGHT_PT, stroke_width=4),
                         Cross(s2[4], stroke_color=C.RIGHT_PT, stroke_width=4))
        final = MathTex(r"df", r"=", r"\Big(f_t + \mu f_x + \tfrac12\sigma^2 f_{xx}\Big)", r"dt", r"+", r"\sigma f_x",
                        r"\,dW", font_size=46)
        final[2].set_color(C.DRIFT)
        final[5:].set_color(C.BROWNIAN)
        fb = boxed(final, color=C.QV, buff=0.25).to_edge(DOWN, buff=0.7)
        sub = label(r"the drift term carries It\^o's correction $\tfrac12\sigma^2 f_{xx}$", font_size=26, color=C.QV)
        sub.next_to(fb, DOWN, buff=0.15)
        table = mult_table(30).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)

        with self.voiceover(
            "The same argument works for anything driven by noise. <bookmark mark='p'/> Suppose X moves with a drift mu "
            "and a noise amplitude sigma: d X equals mu d t plus sigma d W. <bookmark mark='f'/> For a function of time and "
            "X, Taylor's theorem gives three terms that might survive: the time derivative, the slope times d X, and one "
            "half the curvature times d X squared."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(proc), FadeIn(pl))
            vo.wait_until("f")
            self.play(Write(s1))
        with self.voiceover(
            "Use the multiplication table on d X squared. <bookmark mark='e'/> It expands into three products. "
            "<bookmark mark='x'/> d t squared is zero, d t d W is zero, <bookmark mark='s'/> and d W squared is d t. So d X "
            "squared is just sigma squared d t."
        ) as vo:
            self.play(FadeIn(table))
            vo.wait_until("e")
            self.play(Write(s2))
            vo.wait_until("x")
            self.play(Create(crosses))
            vo.wait_until("s")
            self.play(FadeOut(crosses), TransformMatchingTex(s2, s3))
        with self.voiceover(
            "Collect the terms: <bookmark mark='r'/> d f has a drift part, f t plus mu f x plus one half sigma squared f x "
            "x, all times d t, and a noise part, sigma f x d W. This is Itô's lemma in its general form, and it's the "
            "workhorse of everything that follows."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(final), Create(fb[0]))
            self.play(FadeIn(sub))
        self.wait(0.5)
        self.clear_scene()
