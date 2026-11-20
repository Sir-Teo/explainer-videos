from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.peninsula()
        self.saving()
        self.question()
        self.solow()
        self.title()
        self.objectives()

    def peninsula(self):
        h = load("hook")
        ax = plane([1905, 2028], [np.log10(600), np.log10(60000)], center=DOWN * 0.35 + LEFT * 0.2, x_length=11.2,
                   y_length=5.2, xticks=[1920, 1940, 1960, 1980, 2000, 2020],
                   yticks=[np.log10(v) for v in (1000, 3000, 10000, 30000)],
                   ylabel=r"GDP per head, \ 2011 dollars \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: commas(10 ** v), font_size=17)
        ky, kv = h["KOR"]["years"], h["KOR"]["gdppc"]
        py, pv = h["PRK"]["years"], h["PRK"]["gdppc"]
        cut = py.index(1943)
        south = log_path(ax, ky, kv, SOUTH, width=4)
        north_a = log_path(ax, py[:cut + 1], pv[:cut + 1], NORTH, width=4)
        north_b = log_path(ax, py[cut + 1:], pv[cut + 1:], NORTH, width=4)
        gap = DashedLine(ax.ax.c2p(1943, np.log10(pv[cut])), ax.ax.c2p(1990, np.log10(pv[cut + 1])), color=NORTH,
                         stroke_width=2, dash_length=0.08).set_opacity(0.5)
        gap_l = label(r"no estimates, \ 1944--1989", font_size=17, color=NORTH).move_to(ax.ax.c2p(1953,
                                                                                               np.log10(3700)))
        k, p = h["kor"], h["prk"]
        l40 = label(rf"1940: \ north {commas(p['1940'])}, \ south {commas(k['1940'])}", font_size=19,
                    color=GREY_A).move_to(ax.ax.c2p(1928, np.log10(6500)))
        l22 = VGroup(label(rf"South Korea, \ 2022: \ {commas(k['2022'])}", font_size=20, color=SOUTH),
                     label(rf"North Korea, \ 2022: \ {commas(p['2022'])}", font_size=20, color=NORTH),
                     label(rf"a ratio of {h['ratio_2022']:.0f} to 1", font_size=24, color=E.ACCENT)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.12).move_to(ax.ax.c2p(1993, np.log10(1100)))
        for m in (l40, *l22):
            m.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.05)
        src = data_tag(r"Maddison Project Database 2023 \ (Bolt and van Zanden); \ the north's figures are "
                       r"reconstructions", corner=DR, font_size=12)
        with self.voiceover(
            "Seen from space at night, the Korean peninsula is one of the strangest sights on Earth. The south is a "
            "web of light. The north is almost dark, with one bright point where Pyongyang is. "
            "<bookmark mark='a'/> Here are the two halves' incomes per head, from the Maddison Project, on a log "
            "scale. Before the Second World War the peninsula was one Japanese colony, <bookmark mark='b'/> and in "
            f"1940 the north, with its mines, dams and heavy industry, was the richer half: about {commas(p['1940'])} "
            f"dollars a head, against {commas(k['1940'])} in the south. <bookmark mark='c'/> After the division, the "
            "north stopped publishing figures that anyone could check, and there are no estimates for it from 1944 to "
            "1989. <bookmark mark='d'/> By 1990 the south was more than five times richer. By 2022, "
            f"{commas(k['2022'])} dollars against {commas(p['2022'])}: a ratio of about {h['ratio_2022']:.0f} to one, "
            "between people who share a language, a history and, until 1945, a country."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(south), Create(north_a), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(l40))
            vo.wait_until("c")
            self.play(Create(gap), FadeIn(gap_l))
            vo.wait_until("d")
            self.play(Create(north_b), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in l22], lag_ratio=0.4))
        self.clear_scene()

    def saving(self):
        h = load("hook")
        ax = plane([1950, 2026], [0, 0.5], center=DOWN * 0.4 + RIGHT * 2.6, x_length=6.6, y_length=4.4,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                   ylabel=r"South Korea: \ investment, \ share of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        line = path(ax, h["inv_years"], h["inv"], color=SAVE, width=4, smooth=False)
        rows = VGroup(
            label(r"two halves, \ two systems", font_size=28, color=E.ACCENT),
            label(r"the north: \ central planning \\ on the Soviet model", font_size=22, color=NORTH),
            label(r"the south: \ markets, \ exports, \\ and a state that pushed saving", font_size=22, color=SOUTH),
            label(rf"investment: \ {pc(h['inv_1960'], 0)} of GDP in 1960, \\ {pc(h['inv_1990'], 0)} by 1990",
                  font_size=22, color=SAVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        src = data_tag(r"Penn World Table 11.0 \ (csh\_i, \ at current PPPs)", corner=DR, font_size=12)
        with self.voiceover(
            "Economists have argued for seventy years about what made the difference. <bookmark mark='a'/> The two "
            "halves chose different systems. The north planned its economy on the Soviet model. "
            "<bookmark mark='b'/> The south, after a poor decade, chose markets and exports, and a government that "
            "pushed its people to save. <bookmark mark='c'/> South Korea's investment rose from about "
            f"{100 * h['inv_1960']:.0f} percent of its output in 1960 to about {100 * h['inv_1990']:.0f} percent by "
            "1990: four of every ten won produced went into factories, machines, roads and houses. "
            "<bookmark mark='d'/> So did the south get rich by saving? Or is saving what a country does once it is "
            "getting rich for other reasons?"
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(ax), FadeIn(src), Create(line), run_time=2.5)
            self.play(FadeIn(rows[3], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(Indicate(line, color=WHITE))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how much of growth comes from capital, \ and how much from something else?", font_size=28,
                  color=CAPITAL),
            label(r"do poor countries catch up with rich ones?", font_size=28, color=OUTPUT),
            label(r"if capital is scarce in poor countries, \ why doesn't it flow there?", font_size=28,
                  color=RATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: can a country save its way to being rich? <bookmark mark='a'/> How much of "
            "growth comes from piling up capital, and how much from something else? <bookmark mark='b'/> Do poor "
            "countries, which have little capital, catch up with rich ones? <bookmark mark='c'/> And if capital is "
            "scarce where people are poor, and so should earn more there, why doesn't it flow to them?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def solow(self):
        hc = history_card(1956, r"Robert Solow, \ MIT", r"\emph{A Contribution to the Theory of Economic Growth}, \ "
                          r"Quarterly Journal of Economics", color=CAPITAL, width=11.0, font_size=24).to_edge(
            UP, buff=0.5)
        eq = MathTex(r"\dot k \;=\; s\,f(k)\;-\;(n+g+\delta)\,k", font_size=64).next_to(hc, DOWN, buff=0.8)
        rows = VGroup(
            label(r"one equation for what saving can do, \ and what it cannot", font_size=26, color=GREY_A),
            label(r"its answer, \ a year later: \ most growth comes from something the model leaves out",
                  font_size=26, color=TFP),
        ).arrange(DOWN, buff=0.35).next_to(eq, DOWN, buff=0.7)
        tag = published_tag(r"Solow, QJE 70(1) (1956); \ Solow, REStat 39(3) (1957)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1956 Robert Solow, at MIT, wrote down one equation for what capital can and cannot do. "
            "<bookmark mark='a'/> It says how capital per worker changes: by what is saved, less what is needed just "
            "to keep up. <bookmark mark='b'/> Its answer was uncomfortable. Saving can make a country richer, but not "
            "keep it growing. <bookmark mark='c'/> And a year later, when Solow measured America's growth with it, "
            "most of the growth came from something the model leaves out."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
        self.clear_scene()

    def title(self):
        s = load("solow")
        k = np.array(s["k"])
        mini = plane([0, float(k[-1])], [0, float(np.max(s["sf"])) * 1.3], x_length=4.2, y_length=1.6)
        logo = VGroup(path(mini, k, s["sf"], color=SAVE, width=4),
                      path(mini, k, s["break"], color=BREAK, width=4, yr=(0, float(np.max(s["sf"])) * 1.3)))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 20 \ $\cdot$ \ Growth I: \ Capital", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty: growth, part one. Capital."):
            self.play(Create(logo), run_time=1.4)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act V \ $\cdot$ \ The Long Run", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"Kaldor's facts on the data; \ Harrod and Domar's knife edge",
            r"the Solow model derived; \ Play it with a saving rate; \ the golden rule",
            r"convergence: \ its speed in theory, \ and whether it happens",
            r"growth and development accounting; \ East Asia; \ Lucas's puzzle",
            r"Ramsey's choice of saving; \ China; \ dials, \ practice, \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Five, the long run. <bookmark mark='a'/> You'll check Kaldor's facts of growth "
            "against the data, and see the knife edge that the first growth models stood on. "
            "<bookmark mark='b'/> Then you'll derive Solow's model, give the island a saving rate, and find the "
            "golden rule. <bookmark mark='c'/> You'll work out how fast an economy should converge, and ask whether "
            "poor countries do. <bookmark mark='d'/> You'll take growth apart into capital, labour and the residual, "
            "across time and across countries, and settle the argument over East Asia. <bookmark mark='e'/> And you'll "
            "let the island choose how much to save, put China in the model, and end with two dials, how forecasters "
            "use all this, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
