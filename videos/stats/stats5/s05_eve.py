from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Eve(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.galton()
        self.world()
        self.eta()
        self.on_average()

    def card(self):
        card = chapter_card(4, r"Eve's law", r"Total variance $=$ within $+$ between", lit=(), part=PART)
        with self.voiceover("Chapter four. Eve's law."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"Y - EY", r"=", r"\big(Y - E[Y \mid X]\big)", r"+", r"\big(E[Y \mid X] - EY\big)", font_size=34),
            cmath(r"\mathrm{Var}\,Y", r"=", r"E\big[(Y - E[Y\mid X])^2\big]", r"+", r"E\big[(E[Y\mid X] - EY)^2\big]", font_size=32),
            cmath(r"\mathrm{Var}\,Y", r"=", r"E\big[\mathrm{Var}(Y \mid X)\big]", r"+", r"\mathrm{Var}\big(E[Y \mid X]\big)", font_size=36),
        ]
        for r in rows:
            r[2].set_color(S.RESID)
            r[4].set_color(COND)
        whys = [why(r"the error, \ plus the prediction's deviation"), why(r"Pythagoras: \ the two are $\perp$ (chapter 3)"),
                why(r"tower property")]
        names = VGroup(label(r"within: \ noise around the conditional mean", font_size=24, color=S.RESID),
                       label(r"between: \ how much the conditional mean moves", font_size=24, color=COND))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.9)
        eve = label(r"``Eve'' $= EV + VE$ \ (Blitzstein \& Hwang); \ also the law of total variance; \ Part 3 met it for mixtures",
                    font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The projection picture gives another law for free. <bookmark mark='a'/> Split Y's deviation from its "
            "mean into the prediction error and the prediction's own deviation. <bookmark mark='b'/> The two pieces "
            "are perpendicular, so their squared lengths add. <bookmark mark='c'/> By the tower property, that says "
            "the variance of Y is the expected conditional variance plus the variance of the conditional mean. "
            "<bookmark mark='d'/> Noise within groups, plus variation between them. Blitzstein and Hwang's textbook "
            "calls it Eve's law, for E V plus V E; it's also called the law of total variance, and Part 3 met it as the "
            "variance of a mixture."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=k > 0)
            vo.wait_until("d")
            self.play(FadeIn(names), FadeIn(eve))
        self.clear_scene()

    def galton(self):
        e = load("eve")["galton"]
        tot = e["total"]
        A = axes([0, 1], [0, 1], x_length=8.0, y_length=1.0, center=[0, 0.6, 0])
        A.set_opacity(0)
        wbar = Rectangle(width=8.0 * e["within"] / tot, height=0.8, stroke_width=0, fill_color=S.RESID, fill_opacity=0.8)
        bbar = Rectangle(width=8.0 * e["between"] / tot, height=0.8, stroke_width=0, fill_color=COND, fill_opacity=0.8)
        wbar.move_to([-4.0 + wbar.width / 2, 0.6, 0])
        bbar.next_to(wbar, RIGHT, buff=0)
        lw = MathTex(rf"{e['within']:.2f}", font_size=30, color=S.RESID).next_to(wbar, DOWN, buff=0.2)
        lb = MathTex(rf"{e['between']:.2f}", font_size=30, color=COND).next_to(bbar, DOWN, buff=0.2)
        head = MathTex(rf"\mathrm{{Var}}(\text{{child}}) = {tot:.2f}\ \text{{in}}^2", font_size=34).next_to(VGroup(wbar, bbar), UP, buff=0.4)
        r2 = VGroup(MathTex(rf"\frac{{\mathrm{{Var}}\,E[Y\mid X]}}{{\mathrm{{Var}}\,Y}} = {e['between'] / tot:.3f}", font_size=34, color=COND),
                    MathTex(rf"r^2 = {e['r2']:.3f}", font_size=30, color=GREY_A),
                    label(r"the share of variance explained: \ the true $R^2$; \ it equals $r^2$ when the conditional means lie on a "
                          r"line", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.25).move_to([0, -1.9, 0])
        if r2[2].width > 12.6:
            r2[2].width = 12.6
        src = historical_tag(r"Galton (1886): \ child height within and between mid-parent rows")
        with self.voiceover(
            "Galton's table splits cleanly. <bookmark mark='a'/> The children's heights vary with a variance of "
            f"about {tot:.1f} square inches. <bookmark mark='b'/> Most of it, {e['within']:.1f}, is spread within each "
            f"mid-parent row: brothers and sisters differ. <bookmark mark='c'/> Only {e['between']:.1f} is between rows, "
            "the part that parents' heights account for. <bookmark mark='d'/> The ratio, the share of variance "
            f"explained, is {e['between'] / tot:.2f}. It's the honest version of R squared, and because Galton's row "
            "means lie close to a straight line, it almost equals the squared correlation."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(GrowFromEdge(wbar, LEFT), FadeIn(lw))
            vo.wait_until("c")
            self.play(GrowFromEdge(bbar, LEFT), FadeIn(lb))
            vo.wait_until("d")
            self.play(FadeIn(r2))
        self.clear_scene()

    def world(self):
        e = load("eve")
        la = e["logage"]
        rows = VGroup(
            label(r"the World's log incomes, \ grouped by age band:", font_size=26),
            MathTex(rf"{la['total']:.3f}", r"=", rf"{la['within']:.3f}", r"+", rf"{la['between']:.3f}", font_size=36),
            label(rf"age explains {100 * la['between'] / la['total']:.0f}\% of the variance; \ region, \ "
                  rf"{100 * e['region']['share']:.3f}\% \ (the World gave regions no income effect)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to([0, 0.8, 0])
        rows[1][2].set_color(S.RESID)
        rows[1][4].set_color(COND)
        use = label(r"within $+$ between: \ the analysis of variance (Part 13), \ random effects (Part 25)", font_size=26,
                    color=S.ACCENT).to_edge(DOWN, buff=0.8)
        tag = simulated_tag()
        with self.voiceover(
            "In the World it works the same way. <bookmark mark='a'/> Group the log incomes by age band: within plus "
            "between. <bookmark mark='b'/> Age explains about ten percent of the variance, the career curve. "
            "Region explains essentially none, which is correct, because the World was built with no regional income "
            "effect. <bookmark mark='c'/> Within plus between is the skeleton of the analysis of variance in Part 13, "
            "and of the random-effects models of Part 25, where the between part is itself a parameter to estimate."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(use))
        self.clear_scene()

    def eta(self):
        d = load("predictor")
        rows = VGroup(
            MathTex(r"\eta^2", r"=", r"\frac{\mathrm{Var}\,E[Y \mid X]}{\mathrm{Var}\,Y}", r"\quad\text{(Pearson's correlation ratio, 1903)}",
                    font_size=32),
            MathTex(rf"\text{{World, log income on age: }}\ r^2 = {d['r2_line']:.3f},\quad \eta^2 = {d['r2_cond']:.3f}", font_size=30),
            label(r"$r^2$ measures the best \emph{line}; \ $\eta^2$ the best \emph{function}: \ $r^2 \le \eta^2$, \ equal iff "
                  r"$E[Y \mid X]$ is linear", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to([0, 0.6, 0])
        rows[0][0].set_color(COND)
        rows[0][3].set_color(GREY_B)
        rows[1].set_color(COND)
        take = label(r"a small $r^2$ does not mean a weak relationship", font_size=28, color=S.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Eve's law also exposes a common mistake. <bookmark mark='a'/> The share of variance explained by the "
            "conditional mean has a name, Karl Pearson's correlation ratio, eta squared. <bookmark mark='b'/> For the "
            f"World's log incomes, the squared correlation with age is {d['r2_line']:.3f}, almost nothing, but eta "
            f"squared is {d['r2_cond']:.2f}: age explains about sixteen times as much as the straight line can. "
            "<bookmark mark='c'/> The squared correlation measures how well the best line does; eta squared, how "
            "well the best function does. They agree only when the conditional mean is linear, as it is for the "
            "bivariate normal. <bookmark mark='d'/> A small r squared does not mean a weak relationship."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def on_average(self):
        rows = [
            cmath(r"X \sim \mathrm{Bernoulli}(0.1)", r",\quad", r"Y = X \cdot Z,\ \ Z \sim N(0, 10^2)", font_size=32),
            cmath(r"\mathrm{Var}\,Y", r"=", r"0.1 \times 100 = 10", font_size=34),
            cmath(r"\mathrm{Var}(Y \mid X = 1)", r"=", r"100", r"\ >\ ", r"10", font_size=34),
            cmath(r"E\,\mathrm{Var}(Y \mid X)", r"=", r"0.9 \times 0 + 0.1 \times 100 = 10", r"\ \le\ ", r"\mathrm{Var}\,Y", font_size=32),
        ]
        rows[2][2].set_color(S.RESID)
        rows[3][2].set_color(COND)
        whys = [why(r"a rare switch that turns on a lot of noise"), why(r"Eve's law, \ or directly"),
                why(r"learning $X = 1$ made us \emph{less} certain"), why(r"but on average, \ conditioning never adds variance")]
        take = label(r"information reduces uncertainty on average, \ not in every case", font_size=26, color=S.ACCENT)
        take.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Eve's law says conditioning reduces variance. Be careful what that means. <bookmark mark='a'/> Let X be a "
            "rare switch, on one time in ten, and let Y be zero when the switch is off and a wide normal, standard "
            "deviation ten, when it's on. <bookmark mark='b'/> The variance of Y is ten. <bookmark mark='c'/> Now "
            "learn that the switch is on. The conditional variance is a hundred, ten times larger: this piece of "
            "information made us less certain. <bookmark mark='d'/> Eve's law only promises the average: the "
            "expected conditional variance is at most the variance. Information reduces uncertainty on average, not "
            "in every case, a fact Part 15 meets again when a single surprising observation widens a posterior."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
            self.play(FadeIn(take))
        self.clear_scene()
