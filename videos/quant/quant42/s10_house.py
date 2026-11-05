from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import agents as A
from videos.quant.quant42.common import (BAD, COLL_C, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C,
                                         house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        m, c, cr, r = load("maker"), load("collusion"), load("crowd"), load("research")
        self.answer()
        self.card()
        self.scorecard(m, c, cr, r)
        self.audit()
        self.governance()
        self.registry()
        self.lab()
        self.lab2()
        self.module()
        self.test()

    def answer(self):
        rows = [cmath(r"\text{1. other markets}", r":", r"\text{regimes it never trained in}", font_size=38,
                      colors={r"\text{1. other markets}": SIM_C}),
                cmath(r"\text{2. its own copies}", r":", r"\text{the market if it were imitated}", font_size=38,
                      colors={r"\text{2. its own copies}": SHARE_C}),
                cmath(r"\text{3. a forced deviation}", r":", r"\text{does it punish a rival?}", font_size=38,
                      colors={r"\text{3. a forced deviation}": COLL_C}),
                cmath(r"\text{4. live, not replayed}", r":", r"\text{its own fills, not another's tape}", font_size=36,
                      colors={r"\text{4. live, not replayed}": LEARN_C})]
        whys = [why(r"Chapter 4: an agent trained where few traders are informed, tested where many are"),
                why(r"Chapter 7: what a shared signal does once it is a large part of the flow"),
                why(r"Chapter 6's impulse test: an agent that learns to punish undercutting is colluding, by the "
                    r"economist's definition"),
                why(r"Chapter 4: evaluating a policy on the tape another policy produced overstates it, here threefold")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The answer to the pause: four tests. <bookmark mark='a'/> Against markets unlike the one it trained in. "
            "<bookmark mark='b'/> Against copies of itself: the market it would face if it worked and were imitated. "
            "<bookmark mark='c'/> Against a forced deviation: does it learn to punish a rival who undercuts? If so, it "
            "is colluding. <bookmark mark='d'/> And live, in the simulator, never replayed on another policy's tape."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def card(self):
        c = chapter_card(9, r"Rule 42: test the agent against the market it creates", r"What must a learned agent pass "
                         r"before it trades?", part=PART)
        with self.voiceover("Chapter nine. The House's forty-second rule belongs to its research desk and its market "
                            "makers, with compliance watching. A learned agent is evaluated not only in the market it was "
                            "trained on, but in the market its own success would create."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def scorecard(self, m, c, cr, r):
        cx = m["cross"]
        rp = m["replay"]
        w2 = [x for x in cr["rows"] if x["share"] == 0.2][0]
        d95 = [x for x in c["by_delta"] if x["delta_disc"] == 0.95][0]
        best30 = max(x["mean"] for x in m["fixed"]["0.3"])
        h30 = cx["0.3"]["0.3"]["mean"]
        lines = VGroup(
            label(r"This part's agents, through the four tests", font_size=24, color=QC.HOUSE),
            label(rf"1. maker at 30\% informed: {cx['0.05']['0.3']['mean']:.0f} trained at 5\%, {cx['0.3']['0.3']['mean']:.0f} "
                  rf"trained at 30\%; the best fixed rule {best30:.0f}", font_size=18, color=SIM_C),
            label(rf"2. a fifth of each trade from one model: {100 * w2['common']:.0f}\% of the flow is common; volatility "
                  rf"{w2['vol_ratio']:.1f}$\times$", font_size=18, color=SHARE_C),
            label(rf"3. two Q-learners: collusion index {d95['delta']:.2f}; a forced undercut is punished, then forgiven "
                  rf"within {r['back']} periods", font_size=18, color=COLL_C),
            label(rf"4. a wider quote replayed on a narrow quote's tape: {rp['naive4']:.0f}; live: {rp['live4']:.0f}",
                  font_size=18, color=LEARN_C),
            label(r"verdict: none of these agents would be allowed to trade as it is", font_size=20, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(ORIGIN)
        with self.voiceover(
            "The scorecard for this part's own agents. <bookmark mark='a'/> The market maker earns about "
            f"{h30:.0f} in the hard market wherever it was trained, against {best30:.0f} for the "
            "best fixed rule. <bookmark mark='b'/> A fifth of each trade from a shared model makes "
            f"{100 * w2['common']:.0f} percent of the flow common. <bookmark mark='c'/> The pricing learners collude "
            "and punish. <bookmark mark='d'/> And a replay would have more than tripled a quote rule's apparent profit. "
            "<bookmark mark='e'/> None of them passes."
        ) as vo:
            self.play(FadeIn(lines[0]))
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                self.play(FadeIn(lines[k + 1], shift=RIGHT * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def audit(self):
        rows = [cmath(r"\text{run}", r":", r"\text{the agent against a copy of itself, to convergence}", font_size=36,
                      colors={r"\text{run}": LEARN_C}),
                cmath(r"\text{force}", r":", r"\text{one copy to undercut once}", font_size=38, colors={r"\text{force}": BAD}),
                cmath(r"\text{watch}", r":", r"\text{the other's next prices or quotes}", font_size=38),
                cmath(r"\text{flag}", r":", r"\text{a cut that follows, then a return}", font_size=38,
                      colors={r"\text{flag}": COLL_C})]
        whys = [why(r"in the House's simulator, with the agent's real code"),
                why(r"the impulse test of Chapter 6"),
                why(r"a competitive agent has no reason to respond; a colluding one punishes"),
                why(r"the pattern of a reward-and-punishment scheme: the agent goes back to compliance before it trades")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The collusion audit, which compliance now runs on every pricing or quoting agent. <bookmark mark='a'/> Run "
            "the agent against a copy of itself until both settle. <bookmark mark='b'/> Force one copy to undercut "
            "once. <bookmark mark='c'/> Watch what the other does next. <bookmark mark='d'/> A cut that follows, and a "
            "return to the old level, is the signature of a reward-and-punishment scheme, and the agent goes back "
            "before it trades."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def governance(self):
        cards = VGroup(
            desk_question(r"limits outside the model", r"position, loss and message limits enforced by code the agent "
                          r"cannot see or change, with a kill switch a person controls", width=12.4, font_size=19),
            desk_question(r"diversity on purpose", r"no two of the House's agents share both data and objective; a "
                          r"shared model's weight is capped (Chapter 7)", width=12.4, font_size=19),
            desk_question(r"every trial counted", r"each configuration, seed and retraining is a trial on the counter "
                          r"(Part 26), registered before it is scored", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the governance around it. <bookmark mark='a'/> Limits outside the model, enforced by code the agent "
            "cannot see, with a kill switch a person controls. <bookmark mark='b'/> Diversity on purpose: no two of the "
            "House's agents share both their data and their objective. <bookmark mark='c'/> And every configuration, "
            "seed and retraining counted as a trial, registered before it is scored."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def registry(self):
        rows = [cmath(r"\text{an agent}", r"=", r"(\text{code},\ \text{data},\ \text{seed},\ \text{simulator version})", font_size=36,
                      colors={r"\text{an agent}": LEARN_C}),
                cmath(r"\text{each retraining}", r"\Rightarrow", r"\text{a new agent, a new trial}", font_size=38),
                cmath(r"\text{approval}", r":", r"\text{the four tests, re-run on every new agent}", font_size=38,
                      colors={r"\text{approval}": HURDLE})]
        whys = [why(r"what is registered: enough to rebuild the agent exactly, so its tests can be repeated"),
                why(r"Chapter 8's point: a model that retrains itself is a new model; the House's counter (Part 26) "
                    r"counts each one"),
                why(r"nothing is grandfathered: an agent that passed last month and retrained since has not passed")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And the agent registry. <bookmark mark='a'/> An agent is its code, its data, its seed and the version of "
            "the simulator it learned in: enough to rebuild it exactly. <bookmark mark='b'/> Each retraining makes a new "
            "agent, and a new trial on the House's counter. <bookmark mark='c'/> And approval means the four tests, "
            "re-run on every new agent. An agent that passed last month and has retrained since has not passed."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Two Q-learners, one update each", A._calvano.py_func, "nst = act[0] * k + act[1]", 9, width=10.6)
        with self.voiceover(
            "The House's code for Chapter six. After both firms choose, the new state is the pair of prices. Each firm "
            "takes its profit, adds the discounted value of the best price in the new state, and moves its table entry "
            "a step toward that target. Nothing in it mentions a rival's intentions, or collusion."
        ):
            self.play(FadeIn(card))
        self.wait(0.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"The impulse test", A.impulse, "deviate_to = int(np.argmax(R[:, a2, 0]))", 3,
                         extra=((A.impulse, "for _ in range(periods):", 6),), width=10.6)
        with self.voiceover(
            "And the audit. Force firm one to its best response to firm two's price for one period, then let both play "
            "their learned strategies and record the prices that follow."
        ):
            self.play(FadeIn(card))
        self.wait(0.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research", "mm", "compliance")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{fw\_model}, \texttt{stylized}, \texttt{kirman}, \texttt{betabinom\_pmf}", r"artificial markets, herding"),
            (r"\texttt{DealerEnv}, \texttt{q\_maker}, \texttt{run\_maker}", r"a dealer market and its learner"),
            (r"\texttt{calvano}, \texttt{impulse}, \texttt{grim\_threshold}, \texttt{crowd}", r"collusion, monoculture"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 42: a learned agent trades only after it has been tested in markets it never trained "
                             r"in, against copies of itself, against a forced deviation, and live rather than replayed; "
                             r"its limits sit outside it.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds, in the House's agents module. <bookmark mark='a'/> Artificial markets and "
            "herding; a dealer market and its learner; collusion and monoculture. <bookmark mark='b'/> And the "
            "forty-second rule. A learned agent trades only after it has been tested in markets it never trained in, "
            "against copies of itself, against a forced deviation, and live rather than replayed. And its limits sit "
            "outside it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.5)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"an agent that did well in a simulator", r"ask what the simulator assumed about how others "
                          r"respond to it, and how it did in regimes it never saw (Chapters 3 and 4)", width=12.0,
                          font_size=19),
            desk_question(r"prices that stay high without an agreement", r"ask what happens after one seller cuts: a "
                          r"punishment and a return is collusion in all but law (Chapter 6)", width=12.0, font_size=19),
            desk_question(r"many firms using one model", r"ask what share of the market's flow it drives, and what its "
                          r"one mistake would do (Chapter 7)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three tests to carry away. <bookmark mark='a'/> When an agent did well in a simulator, ask what the "
            "simulator assumed about how others respond, and how the agent did in regimes it never saw. "
            "<bookmark mark='b'/> When prices stay high without an agreement, ask what happens after one seller cuts. "
            "<bookmark mark='c'/> And when many firms use one model, ask what share of the flow it drives, and what one "
            "mistake would do."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
