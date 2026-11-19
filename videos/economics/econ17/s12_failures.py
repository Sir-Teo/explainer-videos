from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Failures(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Why markets fail to form", r"What must a marketplace do, \ and what happens when it can't?",
             "Chapter ten. Why markets fail to form.",
             lit={2007: r"Roth on repugnance", 2008: r"Roth, \ ``What have we learned''"},
             scale=("market", "nation"), horizon=("a decade",))
        self.three()
        self.unravel()
        self.repugnance()

    def three(self):
        rows = point_cards([
            (r"thick", r"bring enough buyers and \\ sellers together at once", STABLE),
            (r"uncongested", r"time to make offers \\ and consider them", HELD),
            (r"safe and simple", r"no need to game it \\ to do well", PROPOSE),
        ], width=12.6, cols=3, font_size=23).move_to(UP * 0.6)
        fails = VGroup(
            label(r"unravelling: \ offers creep earlier until the market is thin \ (the interns, \ 1940)",
                  font_size=22, color=REJECT),
            label(r"congestion: \ exploding offers; \ New York's waiting lists \ (1950, \ 2003)", font_size=22,
                  color=REJECT),
            label(r"unsafe: \ the Boston rule punished the honest \ (2003)", font_size=22, color=REJECT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(rows, DOWN, buff=0.6)
        head = label(r"what a marketplace must do", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        tag = published_tag(r"Roth, EJ 118(527) (2008); \ Roth, Nobel lecture (2012)", corner=DR, font_size=13)
        with self.voiceover(
            "Looking back over these markets, Roth listed what a marketplace must do. <bookmark mark='a'/> It must "
            "be thick, bringing enough buyers and sellers together at once that each has real options. It must "
            "not be congested: there must be time to make offers and to consider them. And it must be safe and "
            "simple, so that people do well without gaming it. <bookmark mark='b'/> Each failure in this part "
            "breaks one. Unravelling thins the market, as offers creep earlier: the interns of 1940. "
            "<bookmark mark='c'/> Congestion leaves offers unanswered: the exploding offers of 1950, and New York's "
            "waiting lists. <bookmark mark='d'/> And an unsafe rule punishes the honest: Boston's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.7), run_time=5)
            for mk, f in zip("bcd", fails):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=RIGHT * 0.1))
        self.clear_scene()

    def unravel(self):
        rows = VGroup(
            label(r"unravelling is everywhere that a scarce match is decided early", font_size=25, color=E.ACCENT),
            label(r"clerks for American federal judges: \ hired earlier and earlier, \ despite repeated agreements "
                  r"to wait", font_size=22),
            label(r"medical fellowships, \ college football's bowl games, \ new lawyers and economists", font_size=22,
                  color=GREY_A),
            label(r"each employer gains by moving first, \ so an agreement to wait must be enforced, \ or made "
                  r"safe to keep", font_size=22, color=REJECT),
            label(r"a clearinghouse makes waiting safe: \ nothing is lost by joining at the agreed time",
                  font_size=23, color=STABLE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Avery, Jolls, Posner and Roth, U.\ Chicago Law Rev.\ 68 (2001); \ Niederle and Roth "
                            r"(2003)", corner=DR, font_size=12)
        with self.voiceover(
            "Unravelling turns up wherever a scarce match is decided early. <bookmark mark='a'/> American federal "
            "judges have hired their clerks earlier and earlier, despite repeated agreements among the judges to "
            "wait. <bookmark mark='b'/> It has happened in medical fellowships, in college football's bowl games, "
            "and in the markets for new lawyers. <bookmark mark='c'/> Each employer gains by moving first, so an "
            "agreement to wait must be enforced, or made safe to keep. <bookmark mark='d'/> A clearinghouse makes "
            "waiting safe: anyone who joins at the agreed time loses nothing by having waited."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def repugnance(self):
        io = is_ought_card(
            r"a legal market in kidneys would very likely mean more transplants; \ exchange and chains mean more "
            r"without one",
            r"whether to allow payment for kidneys, \ or only gifts and swaps",
            r"how to weigh lives saved against fears of coercion of the poor, \ and against the sense many people have "
            r"that some things should not be sold",
            width=12.2, font_size=23).move_to(UP * 0.4)
        foot = label(r"Roth (2007): \ repugnance is a real constraint on markets; \ design works within it",
                     font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Roth, JEP 21(3) (2007)", corner=DR, font_size=13)
        with self.voiceover(
            "And some markets fail to form because people do not want them. Gary Becker argued that there is no "
            "shortage of kidneys, since everyone has two: the shortage comes from a price set by law at zero. "
            "<bookmark mark='a'/> A paid market would very likely mean more transplants, and exchange and chains "
            "mean more without one. <bookmark mark='b'/> Whether to allow payment needs a judgment: how to weigh "
            "lives saved against fears that the poor would be pressed into selling, and against the sense many "
            "people have that some things should not be sold at all. <bookmark mark='c'/> Roth called that sense "
            "repugnance, and argued that it is as real a constraint on a market as any law of supply and demand. "
            "Kidney exchange is design within it."
        ) as vo:
            self.play(FadeIn(io.card), FadeIn(io.is_row), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(io.judgment), FadeIn(io[1][1]))
            self.play(FadeIn(io.ought), FadeIn(io[1][3]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
