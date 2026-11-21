from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Deficits(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Bilateral deficits and the current account", r"What does a bilateral trade deficit measure, "
             r"\ and can a tariff close the overall one?", "Chapter five. Bilateral deficits and the current account.",
             scale=("nation", "world"), horizon=("a year",))
        self.identity()
        self.triangle()
        self.chains()

    def identity(self):
        eqs = VGroup(
            MathTex(r"Y = C + I + G + (X - M)", font_size=44),
            MathTex(r"X - M", r"=", r"(Y - C - G)", r"-", r"I", font_size=44),
            MathTex(r"\text{net exports}", r"=", r"\text{national saving}", r"-", r"\text{investment}",
                    font_size=40),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.9)
        eqs[1][2].set_color(FREE)
        eqs[1][4].set_color(US)
        eqs[2][2].set_color(FREE)
        eqs[2][4].set_color(US)
        rows = VGroup(
            label(r"a tariff closes the overall deficit only if it raises saving or lowers investment", font_size=21,
                  color=E.ACCENT),
            label(r"if imports fall, \ the dollar tends to rise, \ and exports fall too", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eqs, DOWN, buff=0.55)
        tag = published_tag(r"Part 34", corner=DL, font_size=12)
        with self.voiceover(
            "Start with the identity of Part thirty-four. <bookmark mark='a'/> Output is spent on consumption, "
            "investment, government purchases and net exports. <bookmark mark='b'/> Rearrange: net exports equal "
            "output less consumption and government purchases, which is national saving, minus investment. "
            "<bookmark mark='c'/> A country runs a trade deficit when it invests more than it saves. <bookmark "
            "mark='d'/> So a tariff closes the overall deficit only if it raises saving or lowers investment. "
            "<bookmark mark='e'/> If it only cuts imports, the dollar tends to rise and exports fall with them. The "
            "model of chapter four held each deficit fixed for exactly this reason: tariffs move the deficit only "
            "through saving and investment."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def triangle(self):
        T = load("triangle")
        pos = {"A": UP * 1.6 + LEFT * 3.0, "B": DOWN * 1.6 + LEFT * 0.4, "C": UP * 1.6 + RIGHT * 2.2}
        nodes = VGroup()
        for c, p in pos.items():
            nodes.add(VGroup(Circle(radius=0.5, stroke_color=US, stroke_width=2.5, fill_color=US, fill_opacity=0.2),
                             label(c, font_size=30, color=WHITE)).move_to(p))
        arrows = VGroup()
        for key, v in T["flows"].items():
            o, d = key[0], key[1]
            start, end = pos[o], pos[d]
            direction = (end - start) / np.linalg.norm(end - start)
            normal = np.array([-direction[1], direction[0], 0])
            off = normal * (0.26 if v > 50 else -0.26)
            a = Arrow(start + direction * 0.6 + off, end - direction * 0.6 + off, buff=0,
                      stroke_width=2 + v / 25, color=FREE if v > 50 else GREY_B, max_tip_length_to_length_ratio=0.08)
            lab = label(f"{v:.0f}", font_size=18, color=FREE if v > 50 else GREY_B).move_to(
                (start + end) / 2 + off * 2.0)
            arrows.add(VGroup(a, lab))
        side = VGroup(
            label(r"each sells 100 to the next, \ 40 back", font_size=19, color=GREY_A),
            label(rf"overall: \ A {T['total']['A']:+.0f}, \ B {T['total']['B']:+.0f}, \ C {T['total']['C']:+.0f}",
                  font_size=19, color=FREE),
            label(r"bilaterally: \ every pair has a deficit of 60 one way", font_size=19, color=TARIFF),
            label(r"balancing every pair means shrinking trade", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)
        with self.voiceover(
            "Bilateral deficits are a different matter. <bookmark mark='a'/> Three countries, each selling a "
            "hundred to the next and forty back. <bookmark mark='b'/> Each country's trade is exactly balanced "
            "overall: it sells a hundred and forty and buys a hundred and forty. <bookmark mark='c'/> Yet every pair "
            "has a deficit of sixty one way. A buys from C more than it sells to C; it makes up the difference with "
            "B. <bookmark mark='d'/> A formula that set tariffs to balance every pair would treat a balanced country "
            "as cheated by its partners, and could balance each pair only by shrinking trade. Bilateral balances "
            "reflect what each country is good at making and what it wants to buy, not fairness."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(nodes), LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.2), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def chains(self):
        ch = flow_chain([(r"designed in California", US), (r"chips from Taiwan and Korea", STATE),
                         (r"assembled in China", ROW), (r"bought in America", PRICE)], box_w=2.7, box_h=1.0,
                        font_size=18).move_to(UP * 1.4)
        rows = VGroup(
            label(r"gross trade counts the whole phone as an import from the last country to touch it", font_size=20,
                  color=GREY_A),
            label(r"value-added trade counts each country's part \ (Part 36)", font_size=20, color=FREE),
            label(r"measured in value added, \ the deficit with the assembler shrinks \ and others' grow",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ch, DOWN, buff=0.8)
        tag = published_tag(r"Johnson and Noguera, \ JIE 86(2) (2012); \ Part 36", corner=DL, font_size=12)
        with self.voiceover(
            "And bilateral numbers are distorted by supply chains. <bookmark mark='a'/> A phone designed in "
            "California, with chips from Taiwan and Korea, assembled in China and sold in America, enters the "
            "statistics as a Chinese export of its whole value. <bookmark mark='b'/> Gross trade counts the whole "
            "phone as an import from the last country to touch it. <bookmark mark='c'/> Trade in value added, the "
            "measure of Part thirty-six, counts each country's own contribution. <bookmark mark='d'/> Measured that "
            "way, the deficit with the assembler shrinks and the deficits with the countries that made the parts "
            "grow. A tariff aimed at the last country in the chain hits the whole chain."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in ch.boxes], lag_ratio=0.3),
                      LaggedStart(*[Create(a) for a in ch.arrows], lag_ratio=0.3), run_time=2.0)
            for mk, r_ in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
