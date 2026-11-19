from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403


def journal_card(name: str, verdict: str, color, width=3.9, font_size=21) -> VGroup:
    box = RoundedRectangle(width=width, height=1.55, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                           fill_color=BACKGROUND, fill_opacity=1)
    t = label(name, font_size=font_size, color=color)
    v = label(verdict, font_size=font_size - 2, color=GREY_A)
    VGroup(t, v).arrange(DOWN, buff=0.18).move_to(box)
    stamp = label(r"rejected", font_size=font_size + 2, color=E.MISS).rotate(0.18).move_to(box.get_corner(UR) +
                                                                                         LEFT * 0.75 + DOWN * 0.3)
    g = VGroup(box, t, v, stamp)
    g.stamp = stamp
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.rejections()
        self.paper()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def rejections(self):
        ak = load("lemons")["ak"]
        hc = history_card(1967, r"George Akerlof, \ a young assistant professor at Berkeley", r"a paper about used cars: \ why a market "
                          r"can shrink, \ or vanish, \\ when sellers know more than buyers", color=LEMON, width=11.4,
                          font_size=24).to_edge(UP, buff=0.45)
        cards = VGroup(
            journal_card(r"American Economic Review", r"too trivial to publish", SIGNAL),
            journal_card(r"Review of Economic Studies", r"too trivial to publish", POOL),
            journal_card(r"Journal of Political Economy", r"wrong: \ if it were right, \\ no goods could be traded",
                         LOSS),
        ).arrange(RIGHT, buff=0.35).next_to(hc, DOWN, buff=0.55)
        foot = label(r"``If this is correct, \ economics would be different''", font_size=26, color=E.ACCENT
                     ).next_to(cards, DOWN, buff=0.5)
        tag = published_tag(r"Akerlof, ``Writing `The Market for Lemons''' (2003), \ as excerpted", corner=DR,
                            font_size=13)
        del ak
        with self.voiceover(
            "In the late 1960s a young economist at Berkeley, George Akerlof, wrote a short paper about used cars. "
            "It asked why a market can shrink, or vanish altogether, when sellers know more than buyers. "
            "<bookmark mark='a'/> The American Economic Review turned it down: the journal, its editor explained, did "
            "not publish papers on subjects of such triviality. <bookmark mark='b'/> The Review of Economic Studies "
            "turned it down for the same reason. <bookmark mark='c'/> The Journal of Political Economy's referees "
            "argued that it was simply wrong: if the paper were correct, no goods could be traded. "
            "<bookmark mark='d'/> As Akerlof later recalled it, the editor's verdict came to this: if this is "
            "correct, economics would be different."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c[:3], shift=UP * 0.1))
                self.play(FadeIn(c.stamp, scale=1.4), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def paper(self):
        ak = load("lemons")["ak"]
        hc = history_card(1970, r"``The Market for `Lemons': \ Quality Uncertainty and the Market Mechanism''",
                          rf"thirteen pages in the \emph{{Quarterly Journal of Economics}}, \ pp.\ {ak['pages'][0]}"
                          rf"--{ak['pages'][1]}", color=LEMON, width=11.4, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"it was correct, \ and economics was different", font_size=27, color=EQ),
            label(r"the start of the economics of information: \ used cars, \ insurance, \ credit, \ jobs",
                  font_size=24),
            label(rf"in {ak['nobel']}, \ Akerlof shared the Nobel prize with Michael Spence and Joseph Stiglitz",
                  font_size=24, color=GREY_A),
            label(r"``lemon'': \ American slang for a car that turns out to be bad", font_size=23, color=LEMON),
        ).arrange(DOWN, buff=0.38).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"Akerlof, QJE 84(3) (1970); \ the Nobel Foundation (2001)", corner=DR, font_size=13)
        with self.voiceover(
            "The Quarterly Journal of Economics published it in 1970, thirteen pages under the title The Market for "
            "Lemons. <bookmark mark='a'/> It was correct, and economics was different. <bookmark mark='b'/> It "
            "started the economics of information, which now explains much of how insurance, credit and hiring "
            "work. <bookmark mark='c'/> In 2001 Akerlof shared the Nobel prize with Michael Spence and Joseph "
            "Stiglitz, whose ideas fill the second half of this part. <bookmark mark='d'/> A lemon, in American "
            "slang, is a car that turns out to be bad once you have bought it."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"used cars", r"the seller has \\ driven it", USED),
            (r"health insurance", r"you know your \\ own health", GOOD),
            (r"loans", r"the borrower knows \\ the project", SIGNAL),
            (r"hiring", r"the applicant knows \\ how good they are", POOL),
            (r"online sellers", r"a stranger, \\ a photo, \ a promise", LEMON),
            (r"art and antiques", r"is it real?", LOSS),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"one side knows something the other can't see", font_size=32, color=E.ACCENT
                     ).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Private information is everywhere once you look for it. <bookmark mark='a'/> The seller of a used car "
            "has driven it for years. You know your own health better than any insurer. A borrower knows the "
            "project far better than the bank. A job applicant knows how good they are. An online seller is a "
            "stranger with a photograph and a promise. And is that painting real? <bookmark mark='b'/> In every case "
            "one side knows something the other cannot see, and that changes what trades, at what price, and "
            "whether the market survives."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(Indicate(head, color=WHITE))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why can good goods be driven out by bad ones?", font_size=29, color=LEMON),
            label(r"how do the informed prove what they know, \ and the uninformed find out?", font_size=29,
                  color=SIGNAL),
            label(r"how much does it cost, \ and what should policy do about it?", font_size=29, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Act Four of this series is about markets that fail and markets that are designed. It opens with a "
            "question: what happens to a market when one side knows more than the other? <bookmark mark='a'/> Why "
            "can good goods be driven out of a market by bad ones? <bookmark mark='b'/> How do the informed prove what "
            "they know, and how do the uninformed find out? <bookmark mark='c'/> And how much does all this cost, "
            "and what, if anything, should policy do about it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = pair(height=1.0)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 13 \ $\cdot$ \ Lemons and Signals", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirteen: lemons and signals."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IV \ $\cdot$ \ Failure and Design", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"buy a boat you cannot inspect; \ Akerlof's market, \ and how it unravels",
            r"guarantees, \ reputations, \ inspectors; \ Spence's signals, \ and whether school is one",
            r"Rothschild and Stiglitz's screening; \ Harvard's death spiral; \ selection drawn as two curves",
            r"testing for private information; \ credit rationing; \ mandates, \ subsidies, \ feedback",
            r"a dial for the cost of adverse selection; \ selection on moral hazard, \ and the end of pooling",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part opens Act Four, on failure and design. <bookmark mark='a'/> You'll buy a boat you cannot "
            "inspect, and we'll use it to build Akerlof's market and watch it unravel. <bookmark mark='b'/> Then the "
            "fixes: guarantees, reputations and inspectors; Spence's signals, and whether school is one. "
            "<bookmark mark='c'/> Rothschild and Stiglitz's screening; the death of Harvard's most generous health "
            "plan; and selection drawn as two curves, measured. <bookmark mark='d'/> How economists test for private "
            "information; why banks ration credit; and what mandates, subsidies and online feedback can do. "
            "<bookmark mark='e'/> And a dial for what adverse selection costs, with a frontier on selection on moral "
            "hazard and the end of pooling."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
