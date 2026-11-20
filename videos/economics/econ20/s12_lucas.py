from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Lucas(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Why doesn't capital flow to poor countries?", r"If capital is scarce where people are poor, "
             r"\ why don't investors send it there?", "Chapter ten. Why doesn't capital flow to poor countries?",
             lit={1990: r"Lucas's question", 2007: r"uphill flows"}, scale=("world",), horizon=("decades",))
        self.puzzle()
        self.answers()
        self.redo()

    def puzzle(self):
        lit = load("lucas")["lit"]
        rows = VGroup(
            MathTex(r"y = A\,k^{\alpha} \;\Rightarrow\; r = \alpha A k^{\alpha-1} = \alpha A^{1/\alpha}\, "
                    r"y^{\frac{\alpha-1}{\alpha}}", font_size=40),
            MathTex(r"\frac{r_{\text{India}}}{r_{\text{US}}} = \Big(\frac{y_{\text{US}}}{y_{\text{India}}}\Big)^"
                    r"{\frac{1-\alpha}{\alpha}}", font_size=44),
            MathTex(rf"= {lit['ratio_y']}^{{1.5}} \approx {lit['raw']:.0f}", font_size=56, color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.7)
        notes = VGroup(
            label(r"with the same technology $A$, \ the marginal product of capital falls with income", font_size=21,
                  color=GREY_A),
            label(r"Lucas, \ 1988 data: \ US income per worker 15 times India's; \ $\alpha = 0.4$", font_size=21,
                  color=GREY_A),
            label(r"capital should earn 58 times as much in India: \ all new investment should go there",
                  font_size=23, color=RATE),
        )
        for n_, r in zip(notes, rows):
            n_.next_to(r, DOWN, buff=0.12)
        tag = published_tag(r"Lucas, AER 80(2) (1990): \ 92--96", corner=DR, font_size=12)
        with self.voiceover(
            "In 1990 Robert Lucas asked a question that the Solow model makes hard to answer. "
            "<bookmark mark='a'/> If two countries share a technology, the one with less capital per worker has the "
            "higher marginal product of capital, and the return falls with income in a precise way. "
            "<bookmark mark='b'/> So the ratio of returns depends only on the ratio of incomes. "
            "<bookmark mark='c'/> In his data American income per worker was fifteen times India's. With capital's "
            f"share at 0.4, capital should have earned about {lit['raw']:.0f} times as much in India. Every dollar "
            "of new investment in the world should have gone to India and countries like it. It did not."
        ) as vo:
            self.play(FadeIn(tag), Write(rows[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(notes[2]))
        self.clear_scene()

    def answers(self):
        lit = load("lucas")["lit"]
        steps = VGroup(
            VGroup(label(r"the raw calculation", font_size=22, color=GREY_A),
                   label(rf"{lit['raw']:.0f}", font_size=48, color=RATE)),
            VGroup(label(r"an American worker \\ worth five Indian ones \\ (Krueger's estimates)", font_size=20,
                         color=HUMAN),
                   label(rf"$3^{{1.5}} \approx {lit['with_h']:.1f}$", font_size=44, color=HUMAN)),
            VGroup(label(r"and skills that spill over \\ to everyone's productivity", font_size=20, color=TFP),
                   label(rf"$\approx {lit['spill']:.2f}$", font_size=44, color=TFP)),
        )
        for g_ in steps:
            g_.arrange(DOWN, buff=0.3)
        steps.arrange(RIGHT, buff=1.2).move_to(UP * 0.7)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.2, color=GREY_B)
                          for i in range(2)])
        other = VGroup(
            label(r"Lucas's other candidates: \ risk of default and expropriation, \ capital-market imperfections",
                  font_size=21, color=HOLD),
            label(r"in the 2000s capital often flowed \emph{uphill}, \ from poorer countries to richer \ (Prasad, "
                  r"Rajan and Subramanian, \ 2007)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Lucas offered answers himself. <bookmark mark='a'/> Start from fifty-eight. <bookmark mark='b'/> First, "
            "workers are not equal. Using Anne Krueger's estimates, he supposed an American worker was worth about "
            "five Indian workers in human capital. Then income per effective worker differs only threefold, and "
            f"the ratio of returns falls to about {lit['with_h']:.0f}. <bookmark mark='c'/> Second, if each "
            "worker's productivity also rises with the skills of those around them, as in his own model of 1988, "
            "the gap vanishes: about one. <bookmark mark='d'/> He also named risk: of default, of expropriation, "
            "and the imperfections of capital markets. <bookmark mark='e'/> The puzzle has, if anything, deepened. "
            "In the 2000s, Eswar Prasad, Raghuram Rajan and Arvind Subramanian showed, net capital often flowed "
            "uphill, from poorer countries to richer ones."
        ) as vo:
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(other[0]))
            vo.wait_until("e")
            self.play(FadeIn(other[1]))
        self.clear_scene()

    def redo(self):
        l_ = load("lucas")
        bars = [
            (r"predicted, \ raw", l_["raw"], RATE),
            (r"predicted, \ with schooling", l_["with_human_capital"], HUMAN),
            (r"measured \ (PWT's return)", l_["irr_poor"] / l_["irr_rich"], E.ACCENT),
        ]
        ax = plane([-0.5, 2.5], [0, np.log10(30)], center=LEFT * 1.6 + DOWN * 0.4, x_length=7.4, y_length=4.8,
                   xticks=[], yticks=[0, np.log10(3), np.log10(10), np.log10(30)],
                   ylabel=r"India's return to capital $\div$ America's \ (log)", yfmt=lambda v: f"{10 ** v:.0f}",
                   font_size=15)
        rect = VGroup()
        for i, (name, v, c) in enumerate(bars):
            h = ax.ax.c2p(0, np.log10(v))[1] - ax.ax.c2p(0, 0)[1]
            r = Rectangle(width=1.4, height=max(h, 0.02), stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                ax.ax.c2p(i, 0), aligned_edge=DOWN)
            rect.add(VGroup(r, label(name, font_size=16, color=c).next_to(r, DOWN, buff=0.12),
                            label(f"{v:.1f}", font_size=20, color=WHITE).next_to(r, UP, buff=0.08)))
        side = VGroup(
            label(rf"{l_['year']}: \ US output per worker \\ {l_['ratio_y']:.1f} times India's", font_size=20,
                  color=GREY_A),
            label(rf"schooling: \ {l_['ratio_h']:.2f} times", font_size=20, color=HUMAN),
            label(rf"PWT's internal return: \\ India {pc(l_['irr_poor'])}, \ US {pc(l_['irr_rich'])}", font_size=20,
                  color=E.ACCENT),
            label(r"a gap, \ but nothing like \\ the model's", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        src = data_tag(r"Penn World Table 11.0 \ (rgdpo, emp, hc, irr)", corner=DR, font_size=12)
        with self.voiceover(
            f"Redo the calculation with {l_['year']} data. <bookmark mark='a'/> India has grown fast, and American "
            f"output per worker is now about {l_['ratio_y']:.0f} times India's. With the same technology, capital "
            f"should earn about {l_['raw']:.0f} times as much in India. <bookmark mark='b'/> Allow for schooling, and "
            f"the prediction is about {l_['with_human_capital']:.0f} times. <bookmark mark='c'/> The Penn World "
            "Table also estimates what capital actually earns, from national accounts: about "
            f"{100 * l_['irr_poor']:.0f} percent a year in India and {100 * l_['irr_rich']:.0f} in America. A ratio "
            f"of {l_['irr_poor'] / l_['irr_rich']:.1f}. <bookmark mark='d'/> Returns are higher in India, but nothing "
            "like the model's prediction, which means that the model's premise, the same A, is wrong. The answer to "
            "Lucas's question is the same as the answer to the last chapter's: productivity differs."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(rect[0]))
            vo.wait_until("b")
            self.play(FadeIn(rect[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(rect[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
