from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class MVPF(VoiceoverScene):
    def construct(self):
        card(self, 13, r"One yardstick", r"How can a pension, a tax credit and a health programme be compared?",
             "Chapter thirteen. One yardstick.", lit={2020: r"Hendren and Sprung-Keyser"},
             scale=("nation",), horizon=("a year", "a lifetime"))
        self.definition()
        self.island()
        self.findings()

    def definition(self):
        lines = VGroup(
            MathTex(r"\text{MVPF} \;=\; \frac{\text{what recipients would pay for it}}{\text{net cost to the "
                    r"government}}", font_size=40),
            MathTex(r"\text{net cost} \;=\; \text{cost} \;-\; \text{taxes it brings back} \;+\; "
                    r"\text{other spending it causes}", font_size=32),
        ).arrange(DOWN, buff=0.55).move_to(UP * 1.2)
        notes = VGroup(
            label(r"above 1: \ each net dollar delivers more than a dollar of value", font_size=21, color=GAIN),
            label(r"below 1: \ some of each dollar leaks away in changed behaviour", font_size=21, color=LOSS),
            label(r"infinite: \ the policy pays for itself", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.MVPF_2020.tag, corner=DR, font_size=10)
        with self.voiceover(
            "This part has met pensions, unemployment benefits, health insurance, disability insurance and tax "
            "credits. How can they be compared? In 2020 Nathaniel Hendren and Ben Sprung-Keyser proposed one "
            "yardstick, the marginal value of public funds. <bookmark mark='a'/> For a small expansion of a "
            "policy, divide what its beneficiaries would be willing to pay for it by its net cost to the "
            "government. <bookmark mark='b'/> The net cost counts the policy's effects on the rest of the budget: "
            "taxes it brings back when people work or earn more, and other spending it causes or saves. "
            "<bookmark mark='c'/> Above one, each net dollar delivers more than a dollar of value. "
            "<bookmark mark='d'/> Below one, some of each dollar leaks away in changed behaviour. "
            "<bookmark mark='e'/> And if the policy raises more in later taxes than it costs, the value is infinite: "
            "it pays for itself."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(lines[1]))
            for mk, n_ in zip("cde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        M = load("mvpf")
        B = load("baily")
        b = np.array(B["b"])
        ax = plane([0, 0.6], [0, 2.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.5, 1.0, 1.5, 2.0],
                   xlabel=r"unemployment benefit, \ share of the wage", ylabel=r"MVPF of a little more",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.1f}", font_size=14)
        ln = path(ax, b, B["mvpf"], UNEMP, 3.4, yr=(0, 2.0))
        one = seg(ax, 0, 1, 0.6, 1, GREY_B, 1.6, dashed=True)
        P = M["points"]
        star = VGroup(vline(ax, P["ui_best"]["b"], 0, 2.0, GAIN), dot(ax, P["ui_best"]["b"], 1.0, GAIN, 0.09))
        side = VGroup(
            label(rf"at 20\%: \ {P['ui_low']['mvpf']:.2f}", font_size=19, color=UNEMP),
            label(rf"at 50\%: \ {P['ui_high']['mvpf']:.2f}", font_size=19, color=UNEMP),
            label(rf"at the best benefit, \\ {100 * P['ui_best']['b']:.0f}\%: \ exactly 1", font_size=19,
                  color=GAIN),
            label(rf"the Island's EITC: \ {P['eitc']['mvpf']:.2f}", font_size=19, color=PENSION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island, compute the value of a little more unemployment insurance at each benefit level. "
            "<bookmark mark='a'/> At a fifth of the wage, a little more is worth "
            f"{P['ui_low']['mvpf']:.2f} dollars per net dollar, because the consumption it protects is valuable. "
            f"<bookmark mark='b'/> At half the wage, only {P['ui_high']['mvpf']:.2f}, because longer unemployment "
            "eats into the budget. <bookmark mark='c'/> At the best benefit of chapter two, exactly one: the "
            "Baily-Chetty formula is the condition that the last dollar is worth a dollar. "
            f"<bookmark mark='d'/> The Island's earned income tax credit scores {P['eitc']['mvpf']:.2f}, because "
            "the parents it draws into work pay taxes and leave welfare. Now programmes as different as these can "
            "be ranked: spend the next dollar where the value per dollar is highest."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(one), Create(ln), run_time=2.0)
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                anims = [FadeIn(side[k])]
                if k == 2:
                    anims.append(FadeIn(star))
                self.play(*anims)
        self.clear_scene()

    def findings(self):
        H = tables.MVPF_2020.data
        ax_line = NumberLine(x_range=[0, 4, 1], length=9.0, include_numbers=True, font_size=24,
                             color=GREY_B).move_to(DOWN * 0.4 + LEFT * 0.6)
        band_ = Rectangle(width=ax_line.n2p(H["adult_hi"])[0] - ax_line.n2p(H["adult_lo"])[0], height=0.7,
                          stroke_width=0, fill_color=UNEMP, fill_opacity=0.3).move_to(
            (ax_line.n2p(H["adult_lo"]) + ax_line.n2p(H["adult_hi"])) / 2)
        bl = label(r"most policies for adults", font_size=19, color=UNEMP).next_to(band_, UP, buff=0.2)
        inf = VGroup(Arrow(ax_line.n2p(3.3), ax_line.n2p(4.0) + RIGHT * 0.8, buff=0, color=GAIN, stroke_width=4),
                     label(r"$\infty$", font_size=40, color=GAIN))
        inf[1].next_to(inf[0], RIGHT, buff=0.1)
        il = label(r"health and education \\ for children: \ the \\ highest, \ some pay \\ for themselves",
                   font_size=19, color=GAIN).next_to(inf, UP, buff=0.3)
        head = label(rf"{H['policies']} American policies on one scale", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        foot = label(r"the MVPF of a tax, \ the inverse of Part 41's cost of public funds, \ is the bar each policy "
                     r"must clear", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.MVPF_2020.tag, corner=DR, font_size=10)
        with self.voiceover(
            f"Hendren and Sprung-Keyser applied the yardstick to {H['policies']} American policies from the past "
            "half century. <bookmark mark='a'/> Most policies for adults, from unemployment insurance to tax "
            "credits and job training, scored between about a half and two. <bookmark mark='b'/> The highest "
            "scores went to health and education policies for children, and some of them paid for themselves: the "
            "children grew up to earn more and pay more tax than the programmes cost. <bookmark mark='c'/> The "
            "yardstick also links back to Part forty-one. Raising a dollar of tax costs taxpayers more than a "
            "dollar; a policy is worth paying for with a tax when its value per dollar beats the tax's. That is how "
            "the two sides of the budget meet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(ax_line), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(band_), FadeIn(bl))
            vo.wait_until("b")
            self.play(GrowArrow(inf[0]), FadeIn(inf[1]), FadeIn(il))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
