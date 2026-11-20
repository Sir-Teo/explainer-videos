from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ trade ministries and customs", r"Who does this for a living?",
             "Chapter fourteen. In practice: trade ministries and customs.", lit={1953: r"Leontief"},
             scale=("market", "nation"), horizon=("a day", "a year"))
        self.jobs()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"trade ministries: \ negotiators and their economists, \ who model what each concession is worth",
                  font_size=21, color=GAIN),
            label(r"customs: \ classifying goods by tariff line, \ valuing them, \ rules of origin", font_size=21,
                  color=TARIFF),
            label(r"trade-remedy agencies: \ anti-dumping and safeguard cases, \ injury to an industry measured",
                  font_size=21, color=CAPITAL),
            label(r"at the WTO and in law firms: \ disputes, \ and the counterfactuals they need", font_size=21,
                  color=FISH),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"WTO, \ \emph{World Tariff Profiles}; \ USITC", corner=DR, font_size=12)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Trade ministries employ negotiators and the "
            "economists who model what each concession is worth, sector by sector, with the computable models of "
            "Part thirty-six. <bookmark mark='b'/> Customs services classify every import into one of thousands of "
            "tariff lines, value it, and decide where it was made, which under a trade agreement can decide the duty. "
            "<bookmark mark='c'/> Agencies like America's International Trade Commission judge anti-dumping and "
            "safeguard cases, which turn on whether imports have injured a domestic industry. "
            "<bookmark mark='d'/> And at the World Trade Organization and in the law firms around it, economists "
            "estimate what trade would have been without a disputed measure."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["heckscher_ohlin_us"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17).move_to(UP * 0.3)
        tag = published_tag(r"Ohlin (1933); \ Leontief (1953); \ Leamer, \ \emph{JPE} 88(3) (1980); \ Trefler (1995)",
                            corner=DR, font_size=12)
        foot = label(r"a theory that needed a second ingredient: \ technology differs", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Heckscher and Ohlin's theory, read for the United States after 1945, "
            "said that the country best endowed with capital should export capital-intensive goods. "
            "<bookmark mark='b'/> Leontief's table found the reverse. Leamer later showed that the table was the "
            "wrong test, and by the right one America was rich in capital after all; but Trefler found the theory's "
            "predicted trade in factors far larger than the real thing. <bookmark mark='c'/> The verdict: partly "
            "right. <bookmark mark='d'/> The theory's logic survives, but it predicts trade well only once Ricardo's "
            "differences in technology are added back."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
