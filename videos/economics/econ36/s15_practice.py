from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 13, r"In practice: \ modelling trade policy", r"Who does this for a living?",
             "Chapter thirteen. In practice: modelling trade policy.", lit={1995: r"Krugman"},
             scale=("firm", "nation"), horizon=("a year",))
        self.jobs()
        self.agreement()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"trade-policy modellers: \ quantitative models with real trade shares, \ at ministries and "
                  r"the ITC", font_size=21, color=GAIN),
            label(r"supply-chain strategists: \ where to source, \ how much to stock, \ what a tariff costs",
                  font_size=21, color=ARCH),
            label(r"trade economists at firms and banks: \ gravity, \ pass-through, \ exposure", font_size=21,
                  color=FISH),
            label(r"local and regional analysts: \ which places a shock will hit", font_size=21, color=CHINA),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"USITC; \ OECD TiVA; \ CEPII", corner=DR, font_size=12)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Trade ministries and agencies like America's "
            "International Trade Commission run quantitative models built on real trade shares, the hat algebra of "
            "chapter eight, to estimate what an agreement or a tariff will do. <bookmark mark='b'/> Firms employ "
            "supply-chain strategists who decide where to source, how much to stock, and what a tariff will cost. "
            "<bookmark mark='c'/> Banks and consultancies employ trade economists who run gravity equations and "
            "measure pass-through. <bookmark mark='d'/> And regional economists now map which places a shock will "
            "hit, the lesson of the China shock."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["krugman_1995"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17).move_to(UP * 0.3)
        tag = published_tag(tables.KRUGMAN_1995.tag + r"; \ Autor, \ Dorn and Hanson (2013)", corner=DR,
                            font_size=12)
        foot = label(r"averages can be right while particular places are devastated", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1995 Paul Krugman estimated that trade with low-wage countries had "
            "raised the ratio of skilled to unskilled wages in America by about three percentage points, a modest "
            "effect, in line with most estimates of the decade. <bookmark mark='b'/> For the years he studied, the "
            "estimate has held up. But after 2000 imports from China grew far faster, and the China shock's "
            "losses were concentrated in particular places, which national averages had smoothed away. "
            "<bookmark mark='c'/> The verdict: partly right. <bookmark mark='d'/> Averages can be right while "
            "particular places are devastated."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def agreement(self):
        F = load("fit")
        rows = [(r"a trade agreement", F["fta_pct"], GAIN), (r"a shared border", F["border"], ARCH),
                (r"twice the distance", -F["dist_double"], TARIFF)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 1.0 - 1.2 * k
            w = abs(v) * 7.0
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.4 + (w / 2 if v > 0 else -w / 2), y, 0]))
            nm_ = label(nm, font_size=21, color=WHITE)
            if v > 0:
                nm_.next_to(np.array([-0.5, y, 0]), LEFT, buff=0.15)
                val = label(f"{100 * v:+.0f}\\%", font_size=21, color=col).next_to(r, RIGHT, buff=0.15)
            else:
                nm_.next_to(np.array([-0.4 - w, y, 0]), LEFT, buff=0.15)
                val = label(f"{100 * v:+.0f}\\%", font_size=21, color=col).next_to(np.array([-0.3, y, 0]), RIGHT,
                                                                                  buff=0.1)
            bars.add(VGroup(r, nm_, val))
        axis = Line(np.array([-0.4, 1.6, 0]), np.array([-0.4, -2.0, 0]), color=GREY_B, stroke_width=2)
        head = label(r"a worked example: \ what would an agreement do to trade between its members?", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"partial effects, \ holding each country's other trade fixed; \ the general equilibrium "
                     r"(chapter 8) adds diversion", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = data_tag(r"CEPII Gravity database (BACI), \ 2019; \ PPML with fixed effects, \ computed", corner=DR,
                       font_size=12)
        with self.voiceover(
            "A typical first assignment for a trade analyst: what would a new agreement do to trade between its "
            "members? Read it off the gravity equation, estimated with each country's fixed effect. "
            f"<bookmark mark='a'/> Pairs with an agreement trade about {100 * F['fta_pct']:.0f} percent more than "
            "otherwise similar pairs. <bookmark mark='b'/> Sharing a border adds about "
            f"{100 * F['border']:.0f} percent; <bookmark mark='c'/> doubling the distance removes about "
            f"{100 * F['dist_double']:.0f} percent. <bookmark mark='d'/> These are partial effects: they hold "
            "fixed everything else each country trades. A real agreement also diverts trade from outsiders and "
            "shifts prices, which is why the analyst's second step is the general-equilibrium calculation of "
            "chapter eight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(tag), *[FadeIn(b_[1]) for b_ in bars])
            for mk, b_ in zip("abc", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b_[0], LEFT if rows[list(bars).index(b_)][1] > 0 else RIGHT), FadeIn(b_[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
