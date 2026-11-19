from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403

KIND_COLOR = {"exponential": LATER, "hyperbolic": FAN, "beta-delta": BIAS}
KIND_NAME = {"exponential": r"exponential: \ $e^{-0.1t}$", "hyperbolic": r"hyperbolic: \ $1/(1+t)$",
             "beta-delta": r"beta--delta: \ $1$, then $0.7\,\delta^{t}$"}


class Discount(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Discounting", r"How do economists add up pay-offs that arrive at different times, and why "
             r"that way?", "Chapter two. Discounting.", lit={1937: r"Samuelson's discounted utility"},
             horizon=("a year", "a decade"))
        self.present_value()
        self.samuelson()
        self.consistency()

    def present_value(self):
        d = load("discount")
        years = np.array(d["years"])
        ax = plane([0, 30], [0, 100], center=LEFT * 3.3 + DOWN * 0.4, x_length=6.4, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, 25, 50, 75, 100], xlabel=r"years away",
                   ylabel=r"worth today, \ \$", font_size=18)
        a = ax.ax
        bars = {}
        for r, col, dx in (("0.03", LATER, -0.08), ("0.1", RISKY, 0.08)):
            pv = np.array(d["pv"][r])
            g = VGroup()
            for t in years[::2]:
                v = pv[t]
                g.add(Rectangle(width=0.14, height=max(1e-3, a.c2p(0, v)[1] - a.c2p(0, 0)[1]), stroke_width=0,
                                fill_color=col, fill_opacity=0.85).move_to(a.c2p(t, 0) + RIGHT * dx, aligned_edge=DOWN))
            bars[r] = g
        side = VGroup(
            MathTex(r"U \;=\; \sum_{t} \beta^{t}\, u(c_t), \qquad \beta = \frac{1}{1+\rho}", font_size=36),
            label(r"\$100, \ 30 years from now, \ is worth today:", font_size=24),
            label(rf"at 3\% a year: \ \${d['pv']['0.03'][-1]:.2f}", font_size=27, color=LATER),
            label(rf"at 10\% a year: \ \${d['pv']['0.1'][-1]:.2f}", font_size=27, color=RISKY),
            label(r"the rate decides what the future counts for: \\ a pension, \ a dam, \ the climate", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Two seasons become many. The standard way to add up a life's consumption is to discount: <bookmark "
            "mark='a'/> utility in each period, weighted by a discount factor beta raised to the number of periods "
            "away. Beta is one over one plus rho, the rate of time preference. <bookmark mark='b'/> The same "
            "arithmetic prices money in time. A hundred dollars thirty years from now is worth, today, <bookmark "
            "mark='c'/> forty-one dollars twenty at three percent a year, <bookmark mark='d'/> and five dollars "
            "seventy-three at ten percent. <bookmark mark='e'/> Small differences in the rate compound into large "
            "differences in what the future counts for: a pension, a dam that lasts a century, the climate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(side[0], color=E.ACCENT, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars["0.03"]], lag_ratio=0.08), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars["0.1"]], lag_ratio=0.08), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def samuelson(self):
        s = tables.SAMUELSON_1937.data
        head = label(r"Samuelson, \ 1937: \ ``A Note on Measurement of Utility''", font_size=32,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        q1 = quote_card(s["arbitrary"], r"p.\ 159", width=10.8, font_size=25, color=LATER)
        q2 = quote_card(s["disavowed"], r"p.\ 161", width=10.8, font_size=25, color=GREY_A)
        VGroup(q1, q2).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.45)
        k = label(r"Koopmans (1960): \ stationary, impatient preferences \ $\Rightarrow$ \ discounted utility",
                  font_size=25, color=EUL).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"as quoted by Frederick, Loewenstein and O'Donoghue, JEL (2002), pp.\ 355--356",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The formula is Paul Samuelson's, from a seven-page note of 1937, written while he was a graduate student. It "
            "became the standard model of choice over time almost at once, and its author warned against exactly "
            "that. <bookmark mark='a'/> It is completely arbitrary, he wrote, to assume that the individual behaves "
            "so as to maximize an integral of the form envisaged. <bookmark mark='b'/> And any connection between "
            "this utility and welfare, he disavowed. <bookmark mark='c'/> A better reason came in 1960, when Tjalling "
            "Koopmans showed that discounting follows from a few axioms about preferences, the most important being "
            "stationarity: how you rank two streams doesn't change if both are pushed one period into the future."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(k))
        self.clear_scene()

    def consistency(self):
        d = load("discount")
        tt = np.array(d["tt"])
        ax = plane([0, 30], [0, 1], center=LEFT * 3.6 + UP * 0.2, x_length=5.2, y_length=4.0,
                   xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1], xlabel=r"years away", ylabel=r"discount factor $D(t)$",
                   font_size=16)
        bx = plane([0, 20], [0.4, 1], center=RIGHT * 2.9 + UP * 0.2, x_length=5.2, y_length=4.0,
                   xticks=[0, 5, 10, 15, 20], yticks=[0.4, 0.6, 0.8, 1.0], xlabel=r"starting year $t$",
                   ylabel=r"$D(t+1)/D(t)$: \ waiting one more year", font_size=16)
        cv, rv, names = VGroup(), VGroup(), VGroup()
        for k, c in KIND_COLOR.items():
            ys = np.array(d["curves"][k])
            if k == "beta-delta":
                cv.add(VGroup(Dot(ax.ax.c2p(0, 1), radius=0.06, color=c),
                              path(ax, tt[1:], ys[1:], color=c, width=3)))
            else:
                cv.add(path(ax, tt, ys, color=c, width=3))
            r = np.array(d["ratio"][k])
            rv.add(VMobject(stroke_color=c, stroke_width=3).set_points_as_corners(
                [bx.ax.c2p(t, v) for t, v in zip(range(20), r)]))
            names.add(label(KIND_NAME[k], font_size=22, color=c))
        names.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=1.05)
        msg = label(r"only exponential discounting prices a year's wait the same whenever it comes: \\ the plan you "
                    r"make today is the plan you will want to follow tomorrow", font_size=23,
                    color=LATER).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Stationarity has a consequence that matters a great deal. Compare three ways the future might be "
            "discounted. <bookmark mark='a'/> Exponential, which is Samuelson's: the weight falls by the same "
            "proportion every year. Hyperbolic, one over one plus t, which falls steeply at first and slowly later. "
            "And beta-delta, which treats now as special: full weight today, then a sudden drop to seven tenths, then "
            "exponential. <bookmark mark='b'/> On the right is what each says about waiting one more year: the ratio "
            "of the weight a year later to the weight now. For exponential discounting the ratio is the same at "
            "every date. For the others it rises: waiting a year seems expensive when the year starts today, and "
            "cheap when it starts in ten years. <bookmark mark='c'/> So only exponential discounting is time "
            "consistent: the plan you make today is the plan you'll still want tomorrow. With the others, today's "
            "self and tomorrow's disagree. Chapter eleven is about that disagreement."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(bx))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cv], lag_ratio=0.5), FadeIn(names), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rv], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(msg))
        self.clear_scene()
