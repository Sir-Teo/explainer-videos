from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403

WHO = ("friday", "chidi", "dara", "bo", "ana")      # poorest to richest, as the bars stand


def bars(ax, incomes, width=0.56):
    g = VGroup()
    for k, (y, w) in enumerate(zip(incomes, WHO)):
        x = k + 1
        r = Polygon(ax.ax.c2p(x - width / 2, 0), ax.ax.c2p(x + width / 2, 0), ax.ax.c2p(x + width / 2, y),
                    ax.ax.c2p(x - width / 2, y), stroke_width=0, fill_color=color_of(w), fill_opacity=0.85)
        v = label(rf"{y:.0f}", font_size=20, color=WHITE).next_to(r, UP, buff=0.08)
        g.add(VGroup(r, v, islander(w, 0.45).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.12)))
    return g


class Welfare(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Welfare functions: \ Bentham, \ Rawls and Atkinson", r"How much should a society care about "
             r"how its income is shared, \ not only how much there is?",
             "Chapter seven. Welfare functions: Bentham, Rawls and Atkinson.",
             lit={1789: r"Bentham", 1970: r"Atkinson", 1971: r"Rawls", 1975: r"Okun"}, scale=("person", "nation"),
             horizon=("a year",))
        self.two_ends()
        self.family()
        self.bucket()

    def two_ends(self):
        w = load("welfare")
        ax = plane([0, 6], [0, 90], center=LEFT * 3.8 + DOWN * 0.2, x_length=5.4, y_length=5.0,
                   yticks=[0, 20, 40, 60, 80], ylabel=r"income, \ baskets a week")
        bs = bars(ax, w["incomes"])
        mean = VGroup(seg(ax, 0.3, w["mean"], 5.7, w["mean"], color=HARS, width=3, dashed=True),
                      label(rf"mean {w['mean']:.0f}", font_size=18, color=HARS).next_to(ax.ax.c2p(5.7, w["mean"]),
                                                                                       RIGHT, buff=0.08))
        low = VGroup(seg(ax, 0.3, w["min"], 5.7, w["min"], color=RAWLS, width=3, dashed=True),
                     label(rf"minimum {w['min']:.0f}", font_size=18, color=RAWLS).next_to(ax.ax.c2p(5.7, w["min"]),
                                                                                         RIGHT, buff=0.08))
        rows = VGroup(
            label(r"Bentham: \ add up everyone's utility", font_size=23, color=HARS),
            label(r"if utility were income, \ only the total would count: \ the mean", font_size=21, color=GREY_A),
            label(r"Rawls: \ judge a society by its worst-off member", font_size=23, color=RAWLS),
            label(r"only the minimum counts", font_size=21, color=GREY_A),
            label(r"between them: \ utility that grows ever more slowly with income", font_size=23, color=WELF),
            MathTex(r"u(y) = \frac{y^{\,1-\varepsilon}}{1-\varepsilon}, \qquad \varepsilon = 1:\ u = \log y",
                    font_size=32, color=WELF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r in rows:
            if r.width > 5.9:
                r.width = 5.9
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35).shift(UP * 0.2)
        head = label(r"five islanders' incomes", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.3).to_edge(LEFT,
                                                                                                           buff=0.6)
        with self.voiceover(
            "To go further, a welfare function must say how to weigh people against each other. Here are five "
            "islanders' incomes, from five baskets a week to eighty. <bookmark mark='a'/> Jeremy Bentham's answer "
            "was to add up everyone's happiness. <bookmark mark='b'/> If happiness rose in step with income, only "
            "the total would matter, and this island would score its mean, thirty-one, however the baskets were "
            "shared. <bookmark mark='c'/> John Rawls's answer, for the basic structure of a society, was to judge "
            "it by how its worst-off member fares. <bookmark mark='d'/> Then only the minimum, five, counts. "
            "<bookmark mark='e'/> Between them lies a family. Let each person's utility grow ever more slowly as "
            "income rises, <bookmark mark='f'/> at a rate set by one number, epsilon. At epsilon zero this is "
            "Bentham with income; at epsilon one, utility is the logarithm of income; and as epsilon grows without "
            "limit, the sum behaves like Rawls's minimum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bs], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(mean[0]), FadeIn(mean[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(low[0]), FadeIn(low[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def family(self):
        w = load("welfare")
        eps, ede = np.array(w["eps"]), np.array(w["ede"])
        ax = plane([0, 6], [0, 90], center=LEFT * 3.4 + DOWN * 0.2, x_length=5.6, y_length=5.0,
                   yticks=[0, 20, 40, 60, 80], ylabel=r"income")
        bs = bars(ax, w["incomes"])
        e = ValueTracker(0.0)

        def line():
            v = float(np.interp(e.get_value(), eps, ede))
            return VGroup(seg(ax, 0.3, v, 5.7, v, color=WELF, width=4),
                          label(rf"{v:.1f}", font_size=20, color=WELF).next_to(ax.ax.c2p(5.7, v), RIGHT, buff=0.1))

        ln = always_redraw(line)
        ea = plane([0, 6], [0, 35], center=RIGHT * 3.3 + DOWN * 0.2, x_length=5.6, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 5, 10, 20, 31], xlabel=r"inequality aversion \ $\varepsilon$",
                   ylabel=r"equally distributed equivalent")
        curve = path(ea, eps, ede, color=WELF, width=4)
        floor = VGroup(seg(ea, 0, w["min"], 6, w["min"], color=RAWLS, width=2, dashed=True),
                       label(r"the minimum", font_size=16, color=RAWLS).next_to(ea.ax.c2p(6, w["min"]), UP, buff=0.06,
                                                                               aligned_edge=RIGHT))
        dot = always_redraw(lambda: Dot(ea.ax.c2p(e.get_value(), float(np.interp(e.get_value(), eps, ede))),
                                        radius=0.08, color=WHITE))
        eval_ = always_redraw(lambda: MathTex(rf"\varepsilon = {e.get_value():.1f}", font_size=30,
                                              color=WHITE).next_to(ea, UP, buff=0.1).align_to(ea, RIGHT))
        t, idx = w["table"], w["index"]
        rows = VGroup(*[label(rf"$\varepsilon = {k}$: \ {t[k]:.1f}, \ Atkinson index {idx[k]:.2f}", font_size=20,
                              color=c) for k, c in (("0.0", HARS), ("1.0", WELF), ("2.0", WELF), ("5.0", RAWLS))])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ea).shift(UP * 1.45 + RIGHT * 1.3)
        box = SurroundingRectangle(rows, buff=0.12, color=GREY_D, fill_color=BACKGROUND, fill_opacity=0.9,
                                   stroke_width=1)
        head = label(r"the equally distributed equivalent: \ the equal income society values as highly", font_size=23,
                     color=E.ACCENT).to_edge(UP, buff=0.25)
        tag = published_tag(r"Atkinson, JET 2(3) (1970)", corner=DR, font_size=13)
        with self.voiceover(
            "Anthony Atkinson, in 1970, turned the family into a measure. <bookmark mark='a'/> Ask: what income, "
            "if everyone had the same, would this welfare function value exactly as highly as the island's real "
            "incomes? He called it the equally distributed equivalent. <bookmark mark='b'/> At epsilon zero it is "
            "the mean, thirty-one. Now raise epsilon. <bookmark mark='c'/> At one it is twenty, the geometric mean; "
            "at two, about thirteen; and it sinks toward the minimum, five. <bookmark mark='d'/> One minus its ratio "
            "to the mean is Atkinson's index of inequality. At epsilon one it is nought point three five: a society "
            "that cared this much about equality would give up thirty-five percent of its income, if the rest could "
            "be shared equally, and count itself no worse off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(bs), FadeIn(tag))
            vo.wait_until("a")
            self.add(ln)
            self.play(FadeIn(ea), FadeIn(floor), FadeIn(eval_))
            vo.wait_until("b")
            self.add(dot)
            self.play(Create(curve), e.animate.set_value(1.0), run_time=3, rate_func=linear)
            vo.wait_until("c")
            self.play(e.animate.set_value(6.0), run_time=6, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(box), FadeIn(rows))
        self.remove(ln, dot, eval_)
        self.clear_scene()

    def bucket(self):
        w = load("welfare")
        lk = w["leak"]
        head = label(r"Okun's leaky bucket: \ carry one basket from the richest islander to the poorest", font_size=25,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        rich, poor = islander("ana", 0.9), islander("friday", 0.9)
        rich.move_to(LEFT * 4.6 + UP * 1.3)
        poor.move_to(RIGHT * 4.6 + UP * 1.3)
        lab = VGroup(label(r"income 80", font_size=19, color=GREY_A).next_to(rich, DOWN, buff=0.12),
                     label(r"income 5", font_size=19, color=GREY_A).next_to(poor, DOWN, buff=0.12))
        bucket = VGroup(Polygon([-0.35, 0.3, 0], [0.35, 0.3, 0], [0.26, -0.3, 0], [-0.26, -0.3, 0],
                                stroke_color=MONEY, stroke_width=3, fill_color=MONEY, fill_opacity=0.25))
        bucket.move_to(rich.get_right() + RIGHT * 0.8)
        x0_, x1_ = rich.get_right()[0] + 0.8, poor.get_left()[0] - 0.8
        drops = VGroup(*[Dot([x, rich.get_center()[1] - 0.55, 0], radius=0.045, color=MONEY)
                         for x in np.linspace(x0_ + 0.6, x1_ - 0.6, 9)])
        rows = VGroup(
            label(r"$\varepsilon = 0$: \ none of it may leak: \ a basket is a basket", font_size=22, color=HARS),
            *[label(rf"$\varepsilon = {e}$: \ up to {say} of it may leak, \ and the move still helps", font_size=22,
                    color=c)
              for e, say, c in ((r"\tfrac12", rf"{lk['0.5'] * 100:.0f}\%", WELF),
                                ("1", rf"{lk['1.0'] * 100:.0f}\%", WELF),
                                ("2", rf"{lk['2.0'] * 100:.1f}\%", RAWLS))])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 1.2)
        foot = label(r"every measure of inequality, \ the Gini coefficient too, \ holds a judgment like this one",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Okun, \emph{Equality and Efficiency: The Big Tradeoff} (1975)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Arthur Okun gave epsilon a picture in 1975: a leaky bucket. <bookmark mark='a'/> Carry one basket "
            "from the richest islander, with eighty, to the poorest, with five. Taxes and administration make the "
            "bucket leak. How much may leak before the transfer makes society worse off? "
            "<bookmark mark='b'/> At epsilon zero, none: a basket is a basket. <bookmark mark='c'/> At epsilon a "
            f"half, {say_pct(lk['0.5'], 0)} of it may leak. At epsilon one, {say_pct(lk['1.0'], 0)}. At epsilon two, "
            "almost all of it. <bookmark mark='d'/> Atkinson's lesson was that every measure of inequality, the Gini "
            "coefficient included, holds a judgment like this one, whether or not it says so. His made it a number "
            "you have to choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rich), FadeIn(poor), FadeIn(lab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bucket))
            self.play(bucket.animate.move_to(poor.get_left() + LEFT * 0.8),
                      LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in drops], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            for r in rows[1:]:
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
