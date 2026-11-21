from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Bayesian(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Bayesian games", r"How do you play against someone you cannot see?",
             "Chapter two. Bayesian games.", lit={1967: r"Harsanyi"}, scale=("firm", "market"), horizon=("a year",))
        self.harsanyi()
        self.cournot()
        self.value()

    def harsanyi(self):
        steps = flow_chain([(r"nature draws each player's type", BELIEF),
                            (r"each sees only their own type", SIGNAL),
                            (r"a strategy says what each type does", SENDER),
                            (r"each type best-responds, on average over the others' types", RECEIVER)],
                           box_w=2.9, box_h=1.35, font_size=19, buff=0.45).move_to(UP * 1.0)
        foot = VGroup(
            label(r"incomplete information becomes imperfect information about a move of nature", font_size=21,
                  color=WHITE),
            label(r"a common prior over types: \ the same probabilities, \ known to all", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.8)
        tag = published_tag(r"Harsanyi, \ Management Science 14 (1967--68)", corner=DR, font_size=12)
        hc = history_card(1967, r"John Harsanyi", r"``Games with incomplete information played by `Bayesian' "
                          r"players'', \ in three parts", color=E.ACCENT, width=10.0, font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "How do you play a game against someone whose payoffs you do not know? In three papers in 1967 and "
            "1968, John Harsanyi gave the answer economics still uses. <bookmark mark='a'/> Imagine that nature "
            "moves first and draws each player's type: a firm's cost, a buyer's value, a defendant's guilt. "
            "<bookmark mark='b'/> Each player sees only their own type. <bookmark mark='c'/> A strategy says what "
            "every type would do. <bookmark mark='d'/> And in equilibrium, each type's action is a best response, "
            "on average over the types the others might be, using probabilities everyone shares. <bookmark "
            "mark='e'/> Incomplete information about payoffs becomes imperfect information about a move of nature, "
            "and ordinary game theory applies. This is a Bayes-Nash equilibrium."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(FadeOut(hc))
                an = [FadeIn(steps.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
            vo.wait_until("e")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
        self.clear_scene()

    def cournot(self):
        B = load("bayes")
        a, c1, ch, cl = B["a"], B["c1"], B["c_high"], B["c_low"]
        ax = plane([0, 5], [0, 5], center=LEFT * 2.3 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 1, 2, 3, 4, 5], xlabel=r"firm 1's output",
                   ylabel=r"firm 2's output", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        q = np.linspace(0, 5, 101)
        br2h = path(ax, q, (a - ch - q) / 2, WEAK, 2.6, xr=(0, 5), yr=(0, 5))
        br2l = path(ax, q, (a - cl - q) / 2, STRONG, 2.6, xr=(0, 5), yr=(0, 5))
        qs = np.linspace(0, 5, 101)
        br1 = path(ax, (a - c1 - qs) / 2, qs, SENDER, 2.6, xr=(0, 5), yr=(0, 5))
        fh = dot(ax, B["full"]["high"]["q1"], B["full"]["high"]["q2"], WEAK, 0.08)
        fl = dot(ax, B["full"]["low"]["q1"], B["full"]["low"]["q2"], STRONG, 0.08)
        bh = dot(ax, B["q1"], B["q2"]["high"], WEAK, 0.12)
        bl = dot(ax, B["q1"], B["q2"]["low"], STRONG, 0.12)
        q1line = DashedLine(ax.ax.c2p(B["q1"], 0), ax.ax.c2p(B["q1"], 5), color=SENDER, stroke_width=1.6)
        side = VGroup(
            label(rf"firm 2's cost: \ {ch:.0f} or {cl:.0f}, \\ equally likely; \ firm 1's: \ {c1:.0f}", font_size=18,
                  color=WHITE),
            label(r"orange, \ blue: \ firm 2's best \\ response if its cost is high, \ low", font_size=18,
                  color=GREY_A),
            label(r"gold: \ firm 1's best response \\ to what it knows", font_size=18, color=SENDER),
            label(rf"firm 1 makes {B['q1']:.2f}: \\ between {B['full']['low']['q1']:.2f} and "
                  rf"{B['full']['high']['q1']:.2f}, \\ what it would make if it knew", font_size=19, color=SENDER),
            label(rf"firm 2 makes {B['q2']['high']:.2f} or {B['q2']['low']:.2f}", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(rf"demand $P = {a:.0f} - Q$ \ (illustrative)", corner=DL, font_size=12)
        with self.voiceover(
            "An example: two firms competing in quantities, as in Part twelve, except that firm 1 does not know "
            f"firm 2's cost. It is {ch:.0f} or {cl:.0f}, equally likely; firm 1's own cost is {c1:.0f}. <bookmark "
            "mark='a'/> Firm 2 knows its cost, so it has two best-response lines: the orange one if its cost is "
            "high, the blue one if it is low. <bookmark mark='b'/> Firm 1 must choose one quantity that is best "
            "against the average of what the two types of firm 2 will do: the gold line. <bookmark mark='c'/> In "
            f"equilibrium firm 1 makes {B['q1']:.2f}, and firm 2 makes {B['q2']['high']:.2f} if its cost is high "
            f"and {B['q2']['low']:.2f} if it is low. <bookmark mark='d'/> If firm 1 knew the cost, it would make "
            f"{B['full']['high']['q1']:.2f} against a high-cost rival and {B['full']['low']['q1']:.2f} against a "
            "low-cost one. Not knowing, it hedges in between, and each type of firm 2 adjusts to that hedge."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(br2h), Create(br2l), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(br1), FadeIn(side[2]), run_time=1.4)
            vo.wait_until("c")
            self.play(Create(q1line), FadeIn(bh, scale=1.4), FadeIn(bl, scale=1.4), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(fh), FadeIn(fl), FadeIn(side[3]))
        self.clear_scene()

    def value(self):
        B = load("bayes")
        rows = VGroup(
            label(rf"firm 1's expected profit, \ not knowing: \ {B['profit1']:.2f}", font_size=24, color=SENDER),
            label(rf"if it could learn firm 2's cost first: \ {B['full_profit1']:.2f}", font_size=24, color=WHITE),
            label(r"information has value only because it changes what you do", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.4)
        with self.voiceover(
            "How much is the missing information worth to firm 1? <bookmark mark='a'/> Not knowing, it expects a "
            f"profit of {B['profit1']:.2f}. <bookmark mark='b'/> If it could learn firm 2's cost before choosing, "
            f"{B['full_profit1']:.2f}. <bookmark mark='c'/> The difference is small here because firm 1's best "
            "choice moves only a little with what it learns; information is worth something only when it would "
            "change what you do. That idea returns in chapter seven, with Blackwell."
        ) as vo:
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
