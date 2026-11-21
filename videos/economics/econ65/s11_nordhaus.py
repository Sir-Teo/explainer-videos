from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class Nordhaus(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Nordhaus's tests", r"If growth were about to explode, \ what would we see in the data first?",
             "Chapter nine. Nordhaus's tests.", lit={2021: "Nordhaus"}, scale=("nation",), horizon=("a decade",))
        self.logic()
        self.tests()
        self.verdict()

    def logic(self):
        cards = point_cards([
            (r"the condition", r"a singularity needs information capital to substitute for people well enough: "
             r"\ an elasticity of substitution above one, \ in production or in what we buy", IDEA),
            (r"the signatures", r"then, \ as computing gets cheap: \ productivity growth accelerates, \ capital's "
             r"share of income rises, \ information capital's share of capital rises", GDP),
            (r"the method", r"look for the signatures in the data, \ and project how long they would take to get "
             r"there", MACH),
        ], width=12.6, cols=1, font_size=21).move_to(DOWN * 0.1)
        tag = published_tag(r"Nordhaus, \ \emph{Are We Approaching an Economic Singularity?}, \ AEJ: Macro 13(1) "
                            r"(2021)", corner=DL, font_size=12)
        with self.voiceover(
            "William Nordhaus asked how we would know. <bookmark mark='a'/> For growth to explode, he showed, "
            "information capital, computers and software and now AI, must substitute for people well enough: the "
            "elasticity of substitution between them must be above one, either in production or in what people "
            "buy. <bookmark mark='b'/> If it is, then as computing gets cheaper, it leaves signatures in the data: "
            "productivity growth should accelerate, capital's share of income should rise, and information "
            "capital should become a growing share of all capital. <bookmark mark='c'/> So look for the "
            "signatures, and ask how long they would take to get there."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def tests(self):
        N = load("nordhaus")
        D = N["decades"]
        a1 = plane([-0.6, len(D) - 0.4], [0, 3.2], center=LEFT * 4.6 + DOWN * 0.5, x_length=4.0, y_length=3.8,
                   xticks=[], yticks=[0, 1, 2, 3], ylabel=r"output per hour, \ \% a year",
                   yfmt=lambda v: f"{v:.0f}", font_size=12)
        b1 = bars(a1, range(len(D)), [100 * d["growth"] for d in D], [GDP] * len(D), width=0.6)
        n1 = VGroup(*[label(f"{d['from']}s" if d["to"] - d["from"] == 10 else f"{d['from']}--", font_size=11,
                            color=GREY_A).rotate(PI / 4).next_to(a1.ax.c2p(k, 0), DOWN, buff=0.22)
                      for k, d in enumerate(D)])
        C = N["capital"]
        a2 = plane([1950, 2024], [0.3, 0.5], center=DOWN * 0.5, x_length=4.0, y_length=3.8,
                   xticks=[1950, 1980, 2010], yticks=[0.3, 0.35, 0.4, 0.45, 0.5], ylabel=r"capital's share",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=12)
        l2 = path(a2, C["year"], C["capital_share"], MACH, 2.8, smooth=False)
        T = N["transistors"]
        a3 = plane([1970, 2022], [3, 11], center=RIGHT * 4.6 + DOWN * 0.5, x_length=4.0, y_length=3.8,
                   xticks=[1970, 1990, 2010], yticks=[3, 5, 7, 9, 11], ylabel=r"transistors per chip",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"10^{{{v:.0f}}}", font_size=12)
        l3 = path(a3, T["year"], T["log10"], IDEA, 2.8, smooth=False)
        heads = VGroup(label(r"1. \ productivity growth", font_size=19, color=GDP).next_to(a1.ax, UP, buff=0.45),
                       label(r"2. \ capital's share", font_size=19, color=MACH).next_to(a2.ax, UP, buff=0.45),
                       label(r"3. \ the price of computing", font_size=19, color=IDEA).next_to(a3.ax, UP, buff=0.45))
        stamps = VGroup(
            label(r"no acceleration", font_size=17, color=NAIVE).next_to(a1.ax, DOWN, buff=0.75),
            label(rf"rising: \ {100 * N['cap_first']:.0f}\% $\to$ {100 * N['cap_last']:.0f}\%", font_size=17,
                  color=NEWT).next_to(a2.ax, DOWN, buff=0.45),
            label(rf"doubling every {N['doubling']:.1f} years", font_size=17, color=NEWT).next_to(a3.ax, DOWN,
                                                                                                  buff=0.45),
        )
        tag = data_tag(r"BLS via FRED: \ OPHNFB; \ Penn World Table 11.0: \ labsh; \ Rupp via Our World in Data",
                       corner=DL, font_size=12)
        dd = {d["from"]: d for d in D}
        with self.voiceover(
            "Here are three of his signatures, on today's data. <bookmark mark='a'/> First, American productivity "
            f"growth by decade: {100 * dd[1990]['growth']:.1f} percent a year in the nineteen-nineties, "
            f"{100 * dd[2000]['growth']:.1f} in the two-thousands, {100 * dd[2010]['growth']:.1f} in the twenty-tens, "
            f"{100 * D[-1]['growth']:.1f} since 2020. No acceleration. <bookmark mark='b'/> Second, capital's share "
            f"of income: {100 * N['cap_first']:.0f} percent in {N['cap_first_year']}, "
            f"{100 * N['cap_last']:.0f} in {N['cap_last_year']}. Rising, which points the right way. <bookmark "
            "mark='c'/> Third, the price of computing: the number of transistors on a chip has doubled about every "
            f"{N['doubling']:.0f} years for half a century. Computing has never been cheaper, and that is the "
            "fuel. The question is whether it substitutes for people fast enough to show up in the first two."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(heads[0]), FadeIn(n1))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.1), run_time=1.4)
            self.play(FadeIn(stamps[0]))
            vo.wait_until("b")
            self.play(FadeIn(a2), FadeIn(heads[1]), Create(l2), run_time=1.6)
            self.play(FadeIn(stamps[1]))
            vo.wait_until("c")
            self.play(FadeIn(a3), FadeIn(heads[2]), Create(l3), run_time=1.6)
            self.play(FadeIn(stamps[2]))
        self.clear_scene()

    def verdict(self):
        c = calls.CALLS["nordhaus_2021"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18)
        tag = published_tag(r"Nordhaus, \ AEJ: Macro 13(1) (2021)", corner=DL, font_size=12)
        with self.voiceover(
            "Nordhaus's own verdict, on data to the late twenty-tens, was that the singularity is not near. "
            "<bookmark mark='a'/> Most of his tests pointed away from it. A couple pointed towards it, but at their "
            "pace it was many decades off. <bookmark mark='b'/> Since then, productivity growth has picked up a "
            "little, capital's share is high, and generative AI arrived after his data ended. <bookmark mark='c'/> "
            "Called it? His tests are the right ones to run again every year. For now: too early to say."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cc.left))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.4))
        self.clear_scene()
