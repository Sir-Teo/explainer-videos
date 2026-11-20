from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Levels(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Development accounting: \ why levels differ", r"How much of the gap between rich and poor "
             r"countries is capital and schooling, \ and how much is neither?",
             "Chapter nine. Development accounting: why levels differ.",
             lit={1997: r"Klenow and Rodr\'iguez-Clare", 1999: r"Hall and Jones", 2005: r"Caselli"},
             scale=("world",), horizon=("a year",))
        self.form()
        self.hall_jones()
        self.today()
        self.countries()

    def form(self):
        rows = VGroup(
            MathTex(r"y = \frac{Y}{L} = A\,k^{\alpha}\,h^{1-\alpha}", font_size=46),
            MathTex(r"y = \Big(\frac{K}{Y}\Big)^{\frac{\alpha}{1-\alpha}}\; h \;\; A^{\frac{1}{1-\alpha}}",
                    font_size=50, color=E.ACCENT),
        ).arrange(DOWN, buff=0.7).move_to(UP * 0.9)
        notes = VGroup(
            label(r"capital intensity", font_size=22, color=CAPITAL),
            label(r"schooling", font_size=22, color=HUMAN),
            label(r"productivity", font_size=22, color=TFP),
        )
        b = rows[1]
        notes[0].next_to(b, DOWN, buff=0.3).align_to(b, LEFT).shift(RIGHT * 0.6)
        notes[1].next_to(b, DOWN, buff=0.3).shift(RIGHT * 0.55)
        notes[2].next_to(b, DOWN, buff=0.3).align_to(b, RIGHT)
        why = label(r"a richer country, \ with higher $A$, \ builds more capital: \ the ratio $K/Y$ does not, \ so "
                    r"credit for that capital goes to $A$", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Growth accounting splits growth over time. Development accounting splits levels across countries. "
            "<bookmark mark='a'/> Income per worker is productivity times capital per worker to the alpha, times "
            "human capital per worker to the one minus alpha. <bookmark mark='b'/> Robert Hall and Charles Jones "
            "rewrote it with the capital-output ratio instead of capital per worker. <bookmark mark='c'/> Then income "
            "is the product of three factors: capital intensity, schooling and productivity. "
            "<bookmark mark='d'/> Why the rewrite? In the Solow model a country with higher productivity also builds "
            "more capital, so capital per worker partly reflects productivity. The ratio of capital to output does "
            "not, so the extra capital that productivity induces is credited to productivity."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.clear_scene()

    def hall_jones(self):
        d = load("development")
        hj = d["lit"]["hj_1988"]
        row = VGroup(
            label(rf"{hj['y']}", font_size=56, color=OUTPUT),
            MathTex(r"=", font_size=56),
            label(rf"{hj['ky']}", font_size=56, color=CAPITAL),
            MathTex(r"\times", font_size=56),
            label(rf"{hj['h']}", font_size=56, color=HUMAN),
            MathTex(r"\times", font_size=56),
            label(rf"{hj['A']}", font_size=56, color=TFP),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        names = VGroup(
            label(r"output per worker, \\ five richest $\div$ five poorest", font_size=18, color=OUTPUT),
            label(r"capital \\ intensity", font_size=18, color=CAPITAL),
            label(r"schooling", font_size=18, color=HUMAN),
            label(r"productivity", font_size=18, color=TFP),
        )
        for n_, m in zip(names, (row[0], row[2], row[4], row[6])):
            n_.next_to(m, DOWN, buff=0.3)
        head = label(r"Hall and Jones, \ 1999: \ 127 countries in 1988", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.7)
        kicker = label(r"without the productivity gap, \ the richest would be only about four times richer",
                       font_size=23, color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Hall and Jones, QJE 114(1) (1999): \ 83--116", corner=DR, font_size=12)
        with self.voiceover(
            "Hall and Jones did it for a hundred and twenty-seven countries in 1988. <bookmark mark='a'/> Output per "
            f"worker in the five richest countries was {hj['y']} times that in the five poorest. "
            f"<bookmark mark='b'/> Capital intensity accounts for a factor of {hj['ky']}. <bookmark mark='c'/> "
            f"Schooling, a factor of {hj['h']}. <bookmark mark='d'/> Productivity, a factor of {hj['A']}. "
            "<bookmark mark='e'/> With no differences in productivity, the richest countries would have been only "
            "about four times richer than the poorest, not thirty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(row[0]), FadeIn(row[1]), FadeIn(names[0]))
            for mk, k in zip("bcd", (2, 4, 6)):
                vo.wait_until(mk)
                self.play(FadeIn(row[k - 1]), FadeIn(row[k]), FadeIn(names[k // 2]))
            vo.wait_until("e")
            self.play(FadeIn(kicker))
        self.clear_scene()

    def today(self):
        d = load("development")
        y = np.log10(np.array(d["y_rel"]))
        A = np.log10(np.array(d["A_rel"]))
        kh = np.log10(np.array(d["ky_rel"]) * np.array(d["h_rel"]))
        ax = plane([-1.8, 0.5], [-1.8, 0.5], center=LEFT * 2.6 + DOWN * 0.45, x_length=5.6, y_length=5.2,
                   xticks=[np.log10(v) for v in (0.03, 0.1, 0.3, 1.0)], yticks=[np.log10(v) for v in (0.03, 0.1,
                                                                                                      0.3, 1.0)],
                   xlabel=r"output per worker, \ US $= 1$", ylabel=r"factor, \ US $= 1$",
                   xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{10 ** v:g}", font_size=14)
        diag = DashedLine(ax.ax.c2p(-1.8, -1.8), ax.ax.c2p(0.5, 0.5), color=GREY_C, stroke_width=1.5)
        dA = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.04, color=TFP).set_opacity(0.85)
                      for a, b in zip(y, A) if -1.8 <= b <= 0.5 and -1.8 <= a <= 0.5])
        dK = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.04, color=CAPITAL).set_opacity(0.85)
                      for a, b in zip(y, kh) if -1.8 <= b <= 0.5 and -1.8 <= a <= 0.5])
        lit = d["lit"]["caselli_1996"]
        side = VGroup(
            label(rf"Penn World Table 11.0, \ {d['year']}, \ {d['n']} countries", font_size=20, color=GREY_A),
            label(r"90th $\div$ 10th percentile:", font_size=20, color=GREY_A),
            label(rf"output per worker: \ {d['ratio_y']:.1f}", font_size=22, color=OUTPUT),
            label(rf"capital intensity $\times$ schooling: \ {d['ratio_kh']:.1f}", font_size=22, color=CAPITAL),
            label(rf"productivity: \ {d['ratio_A']:.1f}", font_size=22, color=TFP),
            label(r"share of the variance of log income \\ explained by the factors:", font_size=20, color=GREY_A),
            label(rf"Hall--Jones form {d['share_factors']:.2f}, \ Caselli's {d['success']:.2f}", font_size=22,
                  color=E.ACCENT),
            label(rf"(Caselli, 1996 data: \ {lit['hj_form']:.2f} and {lit['success1']:.2f})", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        leg = VGroup(VGroup(Dot(radius=0.06, color=CAPITAL), label(r"capital $\times$ schooling", font_size=15,
                                                                    color=CAPITAL)).arrange(RIGHT, buff=0.08),
                     VGroup(Dot(radius=0.06, color=TFP), label(r"productivity", font_size=15, color=TFP)).arrange(
                         RIGHT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(
            ax.ax.c2p(-1.15, 0.25))
        src = data_tag(r"Penn World Table 11.0; \ $\alpha = 1/3$; \ countries of a million people or more", corner=DR,
                       font_size=11)
        tag = published_tag(r"Caselli, \emph{Handbook of Economic Growth} 1A (2005), \ ch.\ 9, \ section 2.2",
                            corner=UR, font_size=11)
        with self.voiceover(
            f"Here is the same accounting for {d['year']}, on the newest Penn World Table. Each country is placed by "
            "its output per worker, relative to the United States. <bookmark mark='a'/> In gold, its capital "
            "intensity times schooling. They rise with income, but gently: the gold cloud is flat. "
            "<bookmark mark='b'/> In pink, productivity. It rises almost one for one with income. "
            f"<bookmark mark='c'/> Between the ninetieth and tenth percentiles, output per worker differs "
            f"{d['ratio_y']:.0f} times; capital and schooling together, about {d['ratio_kh']:.0f} times; productivity "
            f"about {d['ratio_A']:.0f} times. <bookmark mark='d'/> Francesco Caselli's summary is the share of the "
            "variance of log income that the factors alone would produce if every country had America's "
            f"productivity. In 1996 data he found between {lit['hj_form']:.2f} and {lit['success1']:.2f}, depending "
            f"on the form. In 2019 it is lower still: {d['share_factors']:.2f} and {d['success']:.2f}. Capital and "
            "schooling explain well under half of why some countries are rich."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(src), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in dK], lag_ratio=0.01), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in dA], lag_ratio=0.01), FadeIn(leg[1]), run_time=2)
            vo.wait_until("c")
            self.play(*[FadeIn(m) for m in side[1:5]])
            vo.wait_until("d")
            self.play(*[FadeIn(m) for m in side[5:]])
        self.clear_scene()

    def countries(self):
        d = load("development")
        lab = d["labels"]
        rows = VGroup()
        head = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"relative to the US, \ 2019", GREY_A), (r"output per worker", OUTPUT), (r"capital intensity", CAPITAL),
            (r"schooling", HUMAN), (r"productivity", TFP))])
        xs = [-4.6, -1.3, 1.1, 3.2, 5.2]
        for m, x in zip(head, xs):
            m.move_to([x, 2.4, 0])
        for i, c in enumerate(("KOR", "CHN", "BRA", "IND", "NGA", "ETH")):
            if c not in lab:
                continue
            v = lab[c]
            y = 1.6 - i * 0.62
            cells = VGroup(label(COUNTRY[c][0], font_size=22, color=COUNTRY[c][1]).move_to([xs[0], y, 0]),
                           label(f"{v['y']:.2f}", font_size=22, color=OUTPUT).move_to([xs[1], y, 0]),
                           label(f"{v['ky']:.2f}", font_size=22, color=CAPITAL).move_to([xs[2], y, 0]),
                           label(f"{v['h']:.2f}", font_size=22, color=HUMAN).move_to([xs[3], y, 0]),
                           label(f"{v['A']:.2f}", font_size=22, color=TFP).move_to([xs[4], y, 0]))
            rows.add(cells)
        kicker = label(r"poor countries are not short of capital relative to their output: \ they use everything less "
                       r"productively", font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.5)
        ind = lab["IND"]
        with self.voiceover(
            "Six countries, each relative to the United States. <bookmark mark='a'/> Read across India's row. Its "
            f"output per worker is {ind['y']:.2f} of America's. Its capital intensity is {ind['ky']:.2f}: India has "
            "about as much capital per unit of output as America. <bookmark mark='b'/> Its schooling factor is "
            f"{ind['h']:.2f}. <bookmark mark='c'/> And its productivity is {ind['A']:.2f}. Multiply the three and "
            "you get its income. <bookmark mark='d'/> The pattern holds down the table: capital intensity close to "
            "one everywhere, schooling lower, and productivity lowest of all. Poor countries are not mainly short of "
            "capital. They get less out of everything they have. Why, is the subject of the next part."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.2), run_time=2)
            ii = [i for i, c in enumerate(("KOR", "CHN", "BRA", "IND", "NGA", "ETH")) if c in lab].index(3)
            vo.wait_until("a")
            self.play(Indicate(rows[ii][1]), Indicate(rows[ii][2]))
            vo.wait_until("b")
            self.play(Indicate(rows[ii][3]))
            vo.wait_until("c")
            self.play(Indicate(rows[ii][4]))
            vo.wait_until("d")
            self.play(FadeIn(kicker))
        self.clear_scene()
