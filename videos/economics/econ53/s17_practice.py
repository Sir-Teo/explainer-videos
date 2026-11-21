from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ designing what people learn", r"Where is information designed for a living?",
             "Chapter fifteen. In practice: designing what people learn.",
             lit={1994: r"the first FOMC statement", 2009: r"the first published stress test"},
             scale=("firm", "nation"), horizon=("a decade",))
        self.places()
        self.called()

    def places(self):
        rows = VGroup(
            label(r"ratings: \ a coarse signal, \ designed by agencies, \ paid for by the issuers", font_size=22,
                  color=SENDER),
            label(r"disclosure rules: \ what firms must reveal, \ and when", font_size=22, color=RECEIVER),
            label(r"stress tests: \ bank-by-bank results, \ published since 2009", font_size=22, color=THEORY),
            label(r"central banks: \ decisions announced in statements since 1994; \ projections of their own "
                  r"rate since 2012", font_size=22, color=BELIEF),
            label(r"platforms: \ which reviews to show, \ which badges to award, \ what to recommend", font_size=22,
                  color=SIGNAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        if rows.width > 13.2:
            rows.width = 13.2
        head = label(r"information designers", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who designs information for a living? <bookmark mark='a'/> Rating agencies, whose letter grades are a "
            "deliberately coarse signal, often paid for by the issuers being rated. <bookmark mark='b'/> "
            "Securities regulators, who decide what firms must disclose and when. <bookmark mark='c'/> Bank "
            "supervisors: since 2009 the results of American banks' stress tests have been published bank by bank, "
            "a choice global-game reasoning makes delicate. <bookmark mark='d'/> Central banks: the Federal "
            "Reserve has announced its decisions in a statement since 1994, and published its officials' "
            "projections of its own policy rate since 2012. <bookmark mark='e'/> And platforms, which "
            "choose which reviews to show, which sellers to badge, and what to recommend: Bayesian persuasion at "
            "the scale of millions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["aaa_2006"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 1.0)
        lesson = VGroup(
            label(r"a rating is an investigation designed by someone with a stake in the verdict", font_size=21,
                  color=SENDER),
            label(r"the receivers were not perfect Bayesians: \ many treated triple-A as triple-A", font_size=21,
                  color=BELIEF),
        ).arrange(DOWN, buff=0.3).next_to(cc, DOWN, buff=0.6)
        tag = published_tag(r"Financial Crisis Inquiry Commission (2011); \ US Senate PSI (2011)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? A forecast made in letters. <bookmark mark='a'/> In 2006 the big rating agencies gave "
            "their highest grade, triple-A, to the senior slices of securities built from subprime and other risky "
            "mortgages: as unlikely to default, they said, as the safest bonds. The ratings rested on models "
            "fitted to years of rising house prices, and were paid for by issuers who could choose which agency to "
            "hire. <bookmark mark='b'/> House prices began to fall that year. Within a few years most of the "
            "mortgage securities rated triple-A in 2006 had been downgraded, many to junk, and the downgrades "
            "helped turn falling house prices into a financial crisis. <bookmark mark='c'/> The verdict: wrong. "
            "<bookmark mark='d'/> A rating is an investigation designed by someone with a stake in the verdict, "
            "like the prosecutor's. <bookmark mark='e'/> The difference is that many of its receivers were not "
            "the careful Bayesians of the theory: they treated triple-A as triple-A."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson[0]))
            vo.wait_until("e")
            self.play(FadeIn(lesson[1]))
        self.clear_scene()
