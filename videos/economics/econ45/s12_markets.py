from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Markets(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Do markets cure it?", r"Does competition remove biases, or feed on them?",
             "Chapter ten. Do markets cure it?",
             lit={1997: r"Shleifer and Vishny", 2004: r"DellaVigna and Malmendier", 2006: r"Gabaix and Laibson"},
             scale=("market",), horizon=("a year",))
        self.three()
        self.ledger()
        self.verdict()

    def three(self):
        cards = point_cards([
            (r"learning", r"people who trade \\ often learn: \\ the dealers of \\ chapter three", GAIN),
            (r"arbitrage", r"the rational profit \\ from others' errors, \\ and push prices back", PLAN),
            (r"selection", r"biased firms \\ lose money \\ and leave", SOPH),
            (r"but", r"each has limits, \\ and firms can \\ profit from biases \\ that remain", LOSS),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"three reasons to hope markets cure biases", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.WELFARE_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "An old reply to behavioural economics is that markets will fix it. There are three versions. "
            "<bookmark mark='a'/> Learning: people who trade often learn, like the experienced card dealers of "
            "chapter three. <bookmark mark='b'/> Arbitrage: rational traders profit from others' mistakes and, by "
            "doing so, push prices back to where they belong. <bookmark mark='c'/> Selection: biased firms make "
            "losses and leave. <bookmark mark='d'/> Each has limits. Learning needs frequent decisions with clear "
            "feedback, which pensions, mortgages and health plans do not give. Andrei Shleifer and Robert Vishny "
            "showed that arbitrage needs capital and patience, and can be too risky to finish the job. And "
            "selection works on firms, not on their customers, whose biases a firm may profit from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def ledger(self):
        K = load("contract")
        S = load("shrouded")
        X = load("experience")
        rows = VGroup()
        spec = [
            (r"mugs, \ traded often", rf"trade rises from {100 * X['share_traded'][0]:.0f}\% to "
                                      rf"{100 * X['share_traded'][-1]:.0f}\% with experience", r"cured", GAIN),
            (r"the gym, \ monopoly", rf"naifs lose {dollars(-K['naif_monopoly']['realized_surplus'])} a month "
                                    r"by joining", r"exploited", LOSS),
            (r"the gym, \ competition", rf"fees fall to {dollars(K['naif_competition']['F'])}; \ visits still "
                                       r"priced below cost", r"passed back", SOPH),
            (r"printers, \ competition", rf"myopes pay {dollars(S['myope_pays'])}, \ sophisticates "
                                         rf"{dollars(S['soph_pays'])}", r"cross-subsidy", HOLD),
            (r"printers, \ honesty", r"the firm that unshrouds \\ gains no customers", r"no cure", LOSS),
        ]
        for nm, what, verdict, col in spec:
            a = label(nm, font_size=20, color=WHITE)
            b = label(what, font_size=18, color=GREY_A)
            c = label(verdict, font_size=20, color=col)
            row = VGroup(a, b, c)
            rows.add(row)
        for row in rows:
            row[0].move_to(np.array([-4.6, 0, 0]))
            row[1].move_to(np.array([0.3, 0, 0]))
            row[2].move_to(np.array([4.9, 0, 0]))
        rows.arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)
        for row in rows:
            row[0].set_x(-4.6)
            row[1].set_x(0.3)
            row[2].set_x(4.9)
        head = label(r"the Island's ledger", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island's markets give a mixed ledger. <bookmark mark='a'/> Where people trade the same good "
            "often, experience cures the endowment effect. <bookmark mark='b'/> A monopoly gym designs its contract "
            "around naive members and leaves them worse off for joining. <bookmark mark='c'/> Competition between "
            "gyms passes the money back through lower fees, though the contract is still shaped around the bias. "
            "<bookmark mark='d'/> Competition between printer makers does not stop the shroud. It turns it into a "
            "transfer from the inattentive to the attentive. <bookmark mark='e'/> And honesty does not pay, the "
            "curse of debiasing. Markets cure some biases and feed on others; which, depends on how often people "
            "decide, how fast they learn, and whether a firm gains by teaching them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0][:2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][2]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def verdict(self):
        steps = flow_chain([(r"the bias", NAIF), (r"a firm designs \\ for it", FIRM), (r"competition \\ "
                                                                                       r"shares the spoils", SOPH),
                            (r"the bias \\ remains", LOSS)],
                           notes=[r"present bias, \\ inattention, \\ loss aversion", r"fees, \ add-ons, \\ defaults, \ "
                                  r"renewals", r"lower base prices, \\ not better choices", r"a case for \\ policy?"],
                           box_w=2.7, font_size=20, note_size=16).move_to(UP * 0.4)
        foot = label(r"the question of chapter eleven: \ if not markets, \ who, \ and by what standard?",
                     font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.PRESENT_BIAS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The general pattern. <bookmark mark='a'/> A bias creates a profit opportunity. A firm designs its "
            "prices, add-ons, defaults and automatic renewals around it. <bookmark mark='b'/> Competition does not "
            "remove the design; it competes away the profit, often through a lower headline price. "
            "<bookmark mark='c'/> And the bias remains. That is not proof that policy can do better, but it is why "
            "the next question matters: if the market will not fix it, should anyone, and by what standard of "
            "better off?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("a")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]), FadeIn(foot))
        self.clear_scene()
