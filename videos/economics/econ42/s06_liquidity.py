from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Liquidity(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Moral hazard or liquidity?", r"Why do benefits lengthen unemployment?",
             "Chapter five. Moral hazard or liquidity?", lit={2008: r"Chetty"},
             scale=("person", "household"), horizon=("a week", "a year"))
        self.split()
        self.share()
        self.chetty()

    def split(self):
        B = load("baily")
        S = B["split"]
        lines = VGroup(
            MathTex(r"\frac{de}{db} \;=\; \underbrace{\frac{de}{dA}}_{\text{liquidity}} \;-\; "
                    r"\underbrace{\frac{de}{dw}}_{\text{moral hazard}}", font_size=40),
            MathTex(r"\frac{u'(c_u) - u'(c_e)}{u'(c_e)} \;=\; \frac{L}{1 - L}, \qquad L = "
                    r"\frac{de/dA}{de/db}", font_size=36, color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 1.6)
        vals = [(r"liquidity: \ cash in both states", abs(S["liquidity"]), LIQ),
                (r"moral hazard: \ a reward for not working", abs(S["moral_hazard"]), HAZARD)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(vals):
            y = -0.9 - 0.85 * k
            w = abs(v) * 30
            r = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-1.0 - w / 2, y, 0]))
            bars.add(VGroup(r, label(nm, font_size=19, color=col).next_to(np.array([-0.9, y, 0]), RIGHT, buff=0.1),
                            label(f"{v:.3f}", font_size=18, color=col).next_to(r, LEFT, buff=0.1)))
        res = label(rf"how much each lowers the chance of finding work; \ at {100 * B['bstar']:.0f}\%: \ liquidity is "
                    rf"{100 * S['share']:.0f}\% of the response", font_size=21, color=E.ACCENT).to_edge(DOWN,
                                                                                                  buff=0.45)
        two = point_cards([
            (r"liquidity", r"cash in hand: \\ no need to take \\ the first job; \\ insurance doing \\ its job", LIQ),
            (r"moral hazard", r"a reward for \\ staying unemployed: \\ a distortion", HAZARD),
        ], width=7.6, cols=2, font_size=19).move_to(DOWN * 1.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Why do benefits lengthen unemployment? In 2008 Raj Chetty separated two reasons. "
            "<bookmark mark='a'/> A higher benefit changes search in two ways. It gives the unemployed more cash, "
            "so they need not grab the first job that comes along: the liquidity effect, the same as giving them "
            "money whether or not they work. And it narrows the gap between working and not working: moral hazard, "
            "a reward for staying unemployed. <bookmark mark='b'/> Only the second is a distortion. The first is "
            "the insurance doing its job, letting people who cannot borrow search as they would if they could. "
            "<bookmark mark='c'/> Chetty showed that the share of the response due to liquidity, L, fixes the "
            "left side of the formula: L over one minus L. <bookmark mark='d'/> On the Island, at its best benefit, "
            "a little more benefit lowers the chance of finding work by "
            f"{abs(S['liquidity']):.3f} through liquidity and {abs(S['moral_hazard']):.3f} through moral hazard: "
            f"liquidity is {say_pct(S['share'], 0)} of the response."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(two.cards[0], shift=UP * 0.1), FadeIn(two.cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(Indicate(two.cards[0], color=LIQ, scale_factor=1.03))
            vo.wait_until("c")
            self.play(Write(lines[1]))
            vo.wait_until("d")
            self.play(FadeOut(two.cards[0]), FadeOut(two.cards[1]))
            self.play(*[FadeIn(b_) for b_ in bars], FadeIn(res))
        self.clear_scene()

    def share(self):
        B = load("baily")
        b = np.array(B["b"])
        ax = plane([0, 0.6], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"benefit, \ share of the wage", ylabel=r"liquidity's share of the response, \ $L$",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, b, B["shares"], LIQ, 3.4)
        S = B["split"]
        star = VGroup(vline(ax, B["bstar"], 0, 1.0, GAIN), dot(ax, B["bstar"], S["share"], GAIN, 0.09))
        ch = seg(ax, 0, 0.6, 0.6, 0.6, DATA, 2.0, dashed=True)
        side = VGroup(
            label(r"low benefits: \ losing a job \\ means a deep fall, \\ so cash matters most", font_size=18,
                  color=LIQ),
            label(rf"at the Island's best \\ benefit: \ {100 * S['share']:.0f}\%", font_size=19, color=GAIN),
            label(r"gold: \ Chetty's 60\% \\ for the United States", font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How large is the liquidity share? <bookmark mark='a'/> On the Island it is largest when benefits are "
            "small, because then losing a job means a deep fall in consumption, and cash in hand matters most. "
            f"<bookmark mark='b'/> At the Island's best benefit it is {say_pct(S['share'], 0)}. "
            "<bookmark mark='c'/> Chetty measured it for American workers in two ways: benefits lengthen spells "
            "much more for households with little savings than for those with plenty, and lump-sum severance pay, "
            "which rewards no one for staying unemployed, lengthens spells for the cash-poor. Combining the two, "
            "about sixty percent of the effect of benefits on durations is liquidity."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(star), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ch), FadeIn(side[2]))
        self.clear_scene()

    def chetty(self):
        F = load("formula")
        cards = point_cards([
            (r"L = 60\%", rf"the gain side: \\ $L/(1 - L)$ = {F['chetty_gain']:.1f}", LIQ),
            (r"the formula", r"far above the cost \\ of longer spells: \\ benefits should rise", GAIN),
            (r"Chetty's verdict", r"an optimal benefit \\ above half \\ of the wage", E.ACCENT),
            (r"two routes", r"the consumption drop \\ says enough; \\ liquidity says more", HOLD),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what sixty percent implies", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.UI_THEORY.tag, corner=DR, font_size=11)
        with self.voiceover(
            f"What does sixty percent imply? <bookmark mark='a'/> The gain side of the formula becomes 0.6 over "
            f"0.4, which is {F['chetty_gain']:.1f}. <bookmark mark='b'/> That is far above any plausible cost of "
            "longer spells, so benefits should rise. <bookmark mark='c'/> Chetty's calculation put the optimal "
            "benefit above half of the wage. <bookmark mark='d'/> Notice the tension. Measured through the "
            "consumption drop, today's benefits look generous enough; measured through liquidity, they look too "
            "low. The two routes rest on different data and different assumptions about how well households can "
            "borrow and save, and the disagreement is not settled."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
