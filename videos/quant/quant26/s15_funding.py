from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, ask, illustration, load


class Funding(VoiceoverScene):
    def construct(self):
        f = load("funding")
        self.card()
        self.pipeline()
        self.why_ramp()
        self.ramp(f)
        self.claims(f)
        self.question()

    def card(self):
        c = chapter_card(14, r"How a strategy gets capital", r"What happens between a backtest and a trade?",
                         lit=(1982, 1988), part=PART)
        with self.voiceover("Chapter fourteen. What happens between a good backtest and real money."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pipeline(self):
        stages = [(r"idea", r"a reason the edge should exist, written down before the data are touched"),
                  (r"research review", r"the protocol, the data's point-in-time checks, the trial count, the costs"),
                  (r"incubation", r"run live on paper: real data arriving, no capital"),
                  (r"capital ramp", r"a small allocation, raised step by step if the live record holds up"),
                  (r"full allocation", r"sized for its capacity and its correlation with the book"),
                  (r"monitoring, retirement", r"a monitor that can stop it, and a record kept after it dies")]
        boxes = VGroup()
        for k, (a, b) in enumerate(stages):
            box = RoundedRectangle(width=3.8, height=1.35, corner_radius=0.12, stroke_color=QC.HOUSE, stroke_width=2,
                                   fill_color="#141a26", fill_opacity=1)
            t = VGroup(label(a, font_size=21, color=QC.HOUSE), wrapped_label(b, 3.5, 14, GREY_A)).arrange(DOWN, buff=0.08)
            t.move_to(box)
            boxes.add(VGroup(box, t))
        boxes.arrange_in_grid(2, 3, buff=(0.45, 0.6)).move_to(UP * 0.4)
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.08, color=GREY_C, stroke_width=2,
                                max_tip_length_to_length_ratio=0.25) for k in (0, 1, 3, 4)])
        bend = CurvedArrow(boxes[2].get_bottom() + DOWN * 0.05, boxes[3].get_top() + UP * 0.05, angle=-0.6, color=GREY_C,
                           stroke_width=2, tip_length=0.15)
        src = note(r"as commonly described: Lopez de Prado (2018), ch.\ 1, `the meta-strategy paradigm'; Arnott, Harvey and "
                   r"Markowitz (2019), `A backtesting protocol in the era of machine learning'", font_size=15,
                   color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Firms that run many strategies describe a similar path from idea to capital. <bookmark mark='a'/> It "
            "begins with an idea and a reason the edge should exist, written down before the data are touched. Then a "
            "research review: is the protocol sound, are the data point in time, how many trials were run, what will "
            "it cost to trade. <bookmark mark='b'/> Then incubation: the strategy runs live, on data it has never seen, "
            "with no capital at all. <bookmark mark='c'/> Then a capital ramp: a small allocation, raised step by step "
            "while the live record holds up. Full allocation, sized for its capacity and for how it correlates with "
            "everything else. And finally monitoring, with a rule that can stop it, and a record that is kept after "
            "it dies. Marcos Lopez de Prado calls this the meta-strategy paradigm: research run as a production line, "
            "with a check at every station."
        ) as vo:
            self.play(FadeIn(boxes[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]))
            vo.wait_until("c")
            self.play(Create(bend), FadeIn(boxes[3]))
            self.play(GrowArrow(arrows[2]), FadeIn(boxes[4]))
            self.play(GrowArrow(arrows[3]), FadeIn(boxes[5]))
        self.wait(0.4)
        self.clear_scene()

    def why_ramp(self):
        cards = VGroup(
            desk_question(r"the backtest is biased upward", r"by selection, however carefully it was counted: the "
                          r"best of many is, on average, luckier than it is good", width=12.2, font_size=20),
            desk_question(r"the costs are unknown", r"until real orders meet a real market: impact, borrow, fills, "
                          r"capacity are learned only live, and only at size", width=12.2, font_size=20),
            desk_question(r"so capital follows evidence", r"small while little is known, larger as the live record "
                          r"confirms the backtest, and stopped by a rule decided in advance", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why ramp at all? <bookmark mark='a'/> Because a backtest is biased upward by selection, however carefully "
            "the trials were counted: the best of many is, on average, luckier than it is good. <bookmark mark='b'/> "
            "Because the costs are unknown until real orders meet a real market, and impact, borrow and capacity are "
            "learned only live, and only at size. <bookmark mark='c'/> So capital follows evidence: small while little "
            "is known, larger as the live record confirms the backtest, and stopped by a rule decided in advance."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def ramp(self, f):
        a, b = f["real_1"], f["overfit_1"]
        months = np.arange(len(a["mean_cap"]))
        g = axes([0, 60], [0, 1.05], x_length=7.4, y_length=4.0, xlabel=r"months live",
                 ylabel=r"capital, share of the target", xticks=[0, 6, 12, 24, 36, 48, 60], yticks=[0, 0.5, 1.0],
                 font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        ex = VGroup()
        for row, col in ((a["examples"], OOS_C), (b["examples"], BAD)):
            for e in row[:4]:
                ex.add(VMobject(color=col, stroke_width=1.2, stroke_opacity=0.45).set_points_as_corners(
                    [ax.c2p(m_, v) for m_, v in zip(months, e)]))
        la = curve(ax, months, np.asarray(a["mean_cap"]), OOS_C, stroke_width=3.5)
        lb = curve(ax, months, np.asarray(b["mean_cap"]), BAD, stroke_width=3.5)
        paper = Rectangle(width=ax.c2p(6, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 1.05)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=GREY_D, fill_opacity=0.35).move_to(
            [(ax.c2p(0, 0)[0] + ax.c2p(6, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, 1.05)[1]) / 2, 0])
        pl = label(r"paper", font_size=13, color=GREY_A).move_to(paper).shift(UP * 1.4)
        side = VGroup(
            label(r"backtest Sharpe ratio 1.5; the monitor tests `as good as the backtest'", font_size=16, color=GREY_A),
            MathTex(rf"\text{{real (true 1.0)}}:\ \text{{stopped}}\ {100 * a['stopped']:.0f}\%", font_size=24, color=OOS_C),
            MathTex(rf"\text{{overfit (true 0)}}:\ \text{{stopped}}\ {100 * b['stopped']:.0f}\%", font_size=24, color=BAD),
            MathTex(rf"\text{{median stop: month}}\ {b['median_stop']:.0f}", font_size=22, color=BAD),
            wrapped_label(r"six months on paper, then 10\% of the target, raised 15 points a quarter; stopped when the "
                          r"monitor reaches 20. Thick: the average of 1,000 simulated careers; thin: a few of them"
                          .replace("1,000", "1{,}000"), 3.4, 14, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "A simulated ramp. Two strategies with the same backtest, a Sharpe ratio of one and a half. One is real, "
            "with a true Sharpe ratio of one, two thirds of its backtest; the other was overfitted and has none. "
            "<bookmark mark='a'/> Each spends six months on paper, then gets ten percent of its target capital, raised "
            "fifteen points a quarter, while a monitor tests the claim that it is as good as its backtest. "
            "<bookmark mark='b'/> The real strategy is stopped in four percent of its careers, and is almost always at "
            "full size by its third year. <bookmark mark='c'/> The overfitted one is stopped in sixty-two percent of "
            "its five-year careers, at a median of month forty-three. In the meantime it has held less capital, on "
            "average, than the real one, and that is the ramp's real protection: not quick detection, which five years of "
            "data cannot give, but small bets while the evidence is thin."
        ) as vo:
            self.play(FadeIn(g), FadeIn(paper), FadeIn(pl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ex), run_time=2)
            vo.wait_until("b")
            self.play(Create(la), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lb), FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]), run_time=2)
        self.add(illustration(r"simulated: the House's \texttt{martingale.EProcess} as a capital gate"))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, f):
        rows = VGroup(
            MathTex(r"\text{claim tested}", r"\quad", r"\text{overfit stopped}", r"\quad", r"\text{real stopped}",
                    font_size=26, color=GREY_A),
            MathTex(r"\text{as good as the backtest}", r"\quad", rf"{100 * f['overfit_1']['stopped']:.0f}\%", r"\quad",
                    rf"{100 * f['real_1']['stopped']:.0f}\%", font_size=30),
            MathTex(r"\text{at least half the backtest}", r"\quad", rf"{100 * f['overfit_0.5']['stopped']:.0f}\%",
                    r"\quad", rf"{100 * f['real_0.5']['stopped']:.0f}\%", font_size=30),
        ).arrange(DOWN, buff=0.4).shift(UP * 0.6)
        for r_ in rows[1:]:
            for i in (0, 2, 4):
                r_[i].move_to([[-3.2, 1.3, 4.6][i // 2], r_.get_y(), 0])
        for i in (0, 2, 4):
            rows[0][i].move_to([[-3.2, 1.3, 4.6][i // 2], rows[0].get_y(), 0])
        foot = wrapped_label(r"within five years. A monitor stops what it is asked to doubt: ask it whether the strategy is "
                             r"as good as was claimed, which is the claim that justified the capital. Lowering the bar to "
                             r"protect a favourite lets the overfitted strategy run", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "One design choice matters most: which claim the monitor doubts. <bookmark mark='a'/> Tested against the "
            "backtest itself, the overfitted strategy is stopped sixty-two percent of the time within five years. "
            "<bookmark mark='b'/> Tested only against half the backtest, a gentler bar, it is stopped ten percent of "
            "the time, and runs on. The capital was granted because of the backtest's claim, so the monitor should test "
            "that claim. A bar lowered to protect a favourite is how dead strategies keep their capital."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a strategy's capacity is \$200 million, its backtest Sharpe ratio 1.2 after costs at \$50 million. "
                r"The ramp reaches \$150 million and the live Sharpe ratio falls to 0.6. Overfitting, or something else?")
        with self.voiceover(
            "Pause and predict. A strategy's capacity is estimated at two hundred million dollars, and its backtest "
            "Sharpe ratio is one point two after costs at fifty million. The ramp reaches a hundred and fifty million, "
            "and the live Sharpe ratio falls to point six. Overfitting, or something else?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
