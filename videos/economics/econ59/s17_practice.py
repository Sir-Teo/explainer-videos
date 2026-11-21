from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ agencies, \ consultancies, \ in-house teams", r"Who does this work, \ and "
             r"what does a second request feel like from inside?", "Chapter fifteen. In practice: agencies, "
             "consultancies, in-house teams.", lit={2016: r"AT\&T's bet"}, scale=("firm", "nation"),
             horizon=("a day", "a year"))
        self.jobs()
        self.week()
        self.called()

    def jobs(self):
        cards = point_cards([
            (r"the agencies", r"the FTC's Bureau of Economics, \ the Justice Department's economists, \ the "
             r"European Commission's chief economist team, \ the CMA", GOV),
            (r"consultancies", r"teams of economists and data scientists who work for the merging firms, \ or for "
             r"their opponents", DEF),
            (r"academic experts", r"professors who testify, \ and whose papers are cited against them", E.ACCENT),
            (r"in-house teams", r"economists at large firms: \ pricing, \ competition risk, \ the documents they "
             r"write", ALDER),
        ], width=12.4, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"where merger economics is done", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Merger economics is a profession. <bookmark mark='a'/> The agencies employ economists who review "
            "deals: the Federal Trade Commission's Bureau of Economics, the Justice Department's economists, the "
            "European Commission's chief economist team, Britain's Competition and Markets Authority. <bookmark "
            "mark='b'/> Consulting firms employ many more, with data scientists, working for the merging firms or "
            "for customers and rivals who oppose them. <bookmark mark='c'/> Professors serve as testifying experts, "
            "and their own published work is read back to them under oath. <bookmark mark='d'/> And large firms "
            "keep economists in-house, for pricing and for competition risk, because the firm's own documents, "
            "its emails, strategy decks and win-loss reports, will one day be evidence."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def week(self):
        steps = flow_chain([(r"data requests: \\ prices, \\ costs, \\ win-loss", ALDER),
                            (r"clean, \\ match, \\ document", SHOPS), (r"diversion, \\ margins, \\ GUPPIs", GOV),
                            (r"the simulation \\ and its \\ alternatives", SIM),
                            (r"a white paper, \\ then a report", E.ACCENT)], box_w=2.2, box_h=1.4, buff=0.4,
                           font_size=18).move_to(UP * 0.8)
        rule = label(r"the rule of the trade: \ the other side will rerun everything, \ so rerun it first",
                     font_size=22, color=DEF).next_to(steps, DOWN, buff=0.8)
        with self.voiceover(
            "What does the work look like? <bookmark mark='a'/> A second request brings in millions of records: "
            "transaction prices, costs, and the firms' records of which deals they won and lost, and to whom. "
            "<bookmark mark='b'/> Most of the time goes into cleaning and matching them, and documenting every step. "
            "<bookmark mark='c'/> Then come diversion ratios, margins and pricing-pressure screens, <bookmark "
            "mark='d'/> a simulation with its alternatives, <bookmark mark='e'/> and a white paper for the agency, "
            "and, if the case goes to court, an expert report and a deposition. <bookmark mark='f'/> The rule of "
            "the trade is the one from chapter ten: the other side will rerun everything, so rerun it first."
        ) as vo:
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                anims = [FadeIn(steps.boxes[k], shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(steps.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(rule))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["att_2016"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 0.9)
        lesson = VGroup(
            label(r"the court asked whether the merger would harm competition, \ and found it would not", font_size=20,
                  color=GOV),
            label(r"whether it was a good business was never the law's question", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(cc, DOWN, buff=0.55)
        tag = published_tag(r"AT\&T, \ press releases of 22 October 2016 and April 2022", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In October 2016 AT&T's chief executive, Randall Stephenson, announced "
            "the purchase of Time Warner for eighty-five billion dollars with a line: the future of video is "
            "mobile, and the future of mobile is video. The deal would join content to distribution, and save "
            "about a billion dollars a year. <bookmark mark='b'/> AT&T beat the government in court and closed the "
            "purchase in June 2018. In May 2021 it agreed to spin WarnerMedia off and combine it with Discovery, "
            "and that closed in April 2022, less than four years after the purchase. <bookmark mark='c'/> The "
            "verdict: wrong. <bookmark mark='d'/> Note what the court did and did not decide. It asked whether the "
            "merger would harm competition, and found it would not. <bookmark mark='e'/> Whether it was a good "
            "business was never the law's question, and the market answered that one separately."
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
