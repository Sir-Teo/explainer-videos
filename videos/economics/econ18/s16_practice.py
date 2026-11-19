from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ rules for regulators and voters", r"Where do governments actually add people "
             r"up, \ and by what rules?", "Chapter fourteen. In practice: rules for regulators and voters.",
             lit={1981: r"OIRA's review", 2003: r"Circular A-4", 2018: r"Maine's ranked ballots"},
             scale=("city", "nation"), horizon=("a year",))
        self.regulators()
        self.courts()
        self.ballots()

    def regulators(self):
        rows = VGroup(
            label(r"since 1981, \ major American regulations need an analysis of costs and benefits, \ reviewed at "
                  r"the White House", font_size=22),
            label(r"Circular A-4, \ 2003: \ discount at 3\% and at 7\%", font_size=23, color=MONEY),
            label(r"its 2023 revision: \ 2\%, \ and room for distributional weights", font_size=23, color=WELF),
            label(r"January 2025: \ an executive order restores the 2003 version", font_size=23, color=CYCLE),
            label(r"Britain's Green Book: \ 3.5\% for the first thirty years, \ then lower", font_size=23,
                  color=RULE),
            label(r"the parameters of chapters seven and ten, \ set by each administration", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"E.O.\ 12291 (1981), \ 12866 (1993), \ 14192 (2025); \ OMB Circular A-4 (2003, 2023); "
                            r"\ HM Treasury, \emph{The Green Book}", corner=DR, font_size=11)
        with self.voiceover(
            "Governments do this arithmetic every day. <bookmark mark='a'/> Since 1981, every major American "
            "regulation has needed an analysis of its costs and benefits, reviewed by an office at the White House. "
            "<bookmark mark='b'/> The guidance, Circular A-4, told agencies in 2003 to discount future costs and "
            "benefits at three percent and at seven. <bookmark mark='c'/> Its revision in 2023 lowered the default "
            "to two percent and allowed agencies to weight gains to poorer people more heavily. "
            "<bookmark mark='d'/> In January 2025 an executive order directed that the 2003 version be restored. "
            "<bookmark mark='e'/> Britain's Treasury uses three and a half percent for the first thirty years, and "
            "less after that. <bookmark mark='f'/> The epsilon and the discount rate of this part are set, and "
            "reset, by each administration."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def courts(self):
        rows = VGroup(
            label(r"and sometimes the law forbids the arithmetic", font_size=27, color=E.ACCENT),
            label(r"\emph{Whitman v.\ American Trucking}, \ 2001: \ the Clean Air Act bars the EPA from weighing "
                  r"costs when it sets air-quality standards", font_size=22, color=LIFE),
            label(r"\emph{Michigan v.\ EPA}, \ 2015: \ but it must consider cost before regulating power plants' "
                  r"mercury", font_size=22, color=MONEY),
            label(r"a legislature can choose its own welfare function: \ health first, \ or costs and benefits",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        tag = published_tag(r"531 U.S.\ 457 (2001); \ 576 U.S.\ 743 (2015)", corner=DR, font_size=13)
        with self.voiceover(
            "And sometimes the law forbids the arithmetic. <bookmark mark='a'/> In 2001 the Supreme Court held, in "
            "Whitman against American Trucking, that the Clean Air Act bars the Environmental Protection Agency from "
            "weighing costs when it sets the standards for air quality. <bookmark mark='b'/> In 2015, in Michigan "
            "against the EPA, it held that the agency must consider cost before deciding to regulate the mercury "
            "from power plants. <bookmark mark='c'/> A legislature can write its own welfare function into the "
            "statute: health first, or costs against benefits."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ballots(self):
        cards = point_cards([
            (r"Australia", r"the House by instant \\ runoff since 1918", VOTE["B"]),
            (r"Maine", r"ranked ballots from 2018, \\ after a referendum", VOTE["B"]),
            (r"Alaska", r"top four and ranked ballots \\ from 2022; \ kept in 2024 and 2026", VOTE["B"]),
            (r"Fargo", r"approval voting from 2020: \\ tick every candidate you accept", VOTE["E"]),
            (r"North Dakota", r"banned approval and \\ ranked voting in 2025", CYCLE),
            (r"Florida, \ Tennessee", r"the first state bans on \\ ranked voting, \ 2022", CYCLE),
        ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
        head = label(r"voting rules are chosen, \ and fought over", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"each rule picks a different winner from the same ballots: \ chapter one, \ in politics",
                     font_size=21, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Voting rules are chosen too, and fought over. <bookmark mark='a'/> Australia has elected its House of "
            "Representatives by instant runoff since 1918. Maine adopted ranked ballots by referendum and first used "
            "them in 2018. Alaska combined a top-four primary with ranked ballots from 2022; voters kept the system "
            "by fewer than eight hundred votes in 2024, and again in 2026. <bookmark mark='b'/> Fargo, in North "
            "Dakota, adopted approval voting, in which you tick every candidate you find acceptable, and used it from 2020. "
            "<bookmark mark='c'/> In 2025 North Dakota banned approval and ranked voting. Florida and Tennessee had "
            "passed the first state bans on ranked voting in 2022. <bookmark mark='d'/> Since each rule can pick a "
            "different winner from the same ballots, the choice of rule is itself political."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards.cards[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards[1:3]], lag_ratio=0.8),
                      run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(cards.cards[3], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards.cards[4], shift=UP * 0.1), FadeIn(cards.cards[5], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
