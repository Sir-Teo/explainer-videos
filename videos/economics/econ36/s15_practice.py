from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 13, r"In practice: \ modelling trade policy", r"Who does this for a living?",
             "Chapter thirteen. In practice: modelling trade policy.", lit={1995: r"Krugman"},
             scale=("firm", "nation"), horizon=("a year",))
        self.jobs()
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
