from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import FORMULA, HURDLE, PART, RL_C, TRAIN_C, VALID_C, fit_right, illustration, load, tt


class RL(VoiceoverScene):
    def construct(self):
        r = load("rl")
        self.card()
        self.paper()
        self.tokens()
        self.reward()
        self.gradient()
        self.training(r)
        self.pool(r)
        self.question()

    def card(self):
        c = chapter_card(5, r"Reinforcement learning: AlphaGen", r"What if the miner is rewarded not for a good formula, "
                         r"but for a formula that adds something new?", part=PART)
        with self.voiceover("Chapter five. Random search and evolution reward a formula for being good on its own. But a "
                            "desk does not trade one formula; it trades a combination, and a formula that copies what the "
                            "desk already has adds nothing. What if the miner were rewarded for what a formula adds?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def paper(self):
        card = firm_card(r"AlphaGen (Yu, Xue, Ao, Pan, He, Tu and He, 2023)", r"`Generating synergistic formulaic alpha "
                         r"collections via reinforcement learning': a policy network writes formulas token by token; "
                         r"its reward is the improvement in the IC of a linear combination of a pool of formulas when "
                         r"the new one joins it",
                         numbers=((r"\text{KDD}", r"published at the ACM SIGKDD conference, 2023"),
                                  (r"\text{PPO}", r"the policy is trained by proximal policy optimisation; we use the "
                                                  r"simpler REINFORCE")),
                         source=r"arXiv 2306.12964", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "AlphaGen's June2023 version1 studies synergistic factor collections using policy gradients. <bookmark mark='a'/> Its PPO policy writes symbolic factors and is rewarded for the fitted pool's performance. Its Chinese-stock setting uses a20-day price-return target, training2009-2018, validation2019 and testing2020-2021. <bookmark mark='b'/> Our unchanged original uses a small GRU with REINFORCE, a next-day target and a different coin archive. It is inspired by the mechanism, not a reproduction of the paper's architecture, data, metrics or results."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def tokens(self):
        seq = [(r"\texttt{close}", FORMULA, ["close"]),
               (r"\texttt{close}", FORMULA, ["close", "close"]),
               (r"\texttt{ts\_mean\_5}", QC.OPTION, ["close", "ts_mean(close, 5)"]),
               (r"\texttt{sub}", RL_C, ["(close - ts_mean(close, 5))"]),
               (r"\texttt{rank}", RL_C, ["rank(close - ts_mean(close, 5))"]),
               (r"\texttt{END}", GREY_B, ["rank(close - ts_mean(close, 5))"])]
        toks = VGroup(*[VGroup(RoundedRectangle(width=1.9, height=0.6, corner_radius=0.1, stroke_color=c, fill_color=c,
                                                fill_opacity=0.15), label(t, font_size=18, color=c))
                        for t, c, _ in seq])
        for b in toks:
            b[1].move_to(b[0])
        toks.arrange(RIGHT, buff=0.18).move_to(UP * 2.2)
        head = label(r"the policy writes, left to right (reverse Polish notation)", font_size=20, color=GREY_B
                     ).next_to(toks, UP, buff=0.3)
        stack_t = label(r"the stack after each token", font_size=20, color=GREY_B).move_to(UP * 0.9)
        stacks = []
        for _, _, st in seq:
            g = VGroup(*[label(tt(s, 60), font_size=17, color=GREY_A) for s in st]).arrange(DOWN, buff=0.12)
            g.next_to(stack_t, DOWN, buff=0.35)
            stacks.append(g)
        note_ = wrapped_label(r"a mask forbids any token that would leave the stack unable to close into one formula: "
                              r"this illustrates syntax; it does not guarantee finite values, economic meaning or predictability", 11.0, 17, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How does a network write a formula? <bookmark mark='a'/> In reverse Polish notation, the way old calculators "
            "worked. Close; close again; the five-day mean of the top item; subtract; rank. <bookmark mark='b'/> A stack "
            "keeps track, and at the end it holds a single formula: the rank of the price's gap above its five-day "
            "mean. <bookmark mark='c'/> At each step, the network outputs a probability for every token, and a mask "
            "removes the ones that could never close into a valid formula."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stack_t), FadeIn(illustration()))
            vo.wait_until("a")
            cur = None
            for k in range(len(seq)):
                anims = [FadeIn(toks[k], shift=DOWN * 0.1)]
                anims.append(FadeIn(stacks[k]) if cur is None else ReplacementTransform(cur, stacks[k]))
                cur = stacks[k]
                self.play(*anims, run_time=0.55)
            vo.wait_until("b")
            self.play(Indicate(cur, color=RL_C))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def reward(self):
        rows = [cmath(r"\pi_\theta(a_k \mid a_{<k})", r"", r"\text{: a recurrent network over } 6 + 28 + 5 + 4 \text{ tokens}",
                      font_size=30, colors={r"\pi_\theta(a_k \mid a_{<k})": RL_C}),
                cmath(r"R(f)", r"=", r"IC\big(\text{pool} \cup \{f\}\big) - IC(\text{pool})", font_size=32,
                      colors={r"R(f)": HURDLE}),
                cmath(r"\nabla_\theta J", r"=", r"\mathbb E\Big[R(f)\textstyle\sum_k \nabla_\theta\log\pi_\theta(a_k \mid a_{<k})"
                      r"\Big]", font_size=32, colors={r"\nabla_\theta J": RL_C}),
                cmath(r"\text{pool}", r":", r"\text{keep new } f \text{ if } R(f) > 0.0005;\ \text{at 10, drop the least useful}",
                      font_size=30)]
        whys = [why(r"a GRU reads the tokens so far and outputs a probability for the next: six fields, seven time-series "
                    r"operators at four windows, five unary and four binary operators"),
                why(r"the synergy reward: the gain in training IC of the pool's least-squares combination when $f$ joins"),
                why(r"REINFORCE (Williams 1992): raise the log-probability of every token of a formula in proportion to its "
                    r"reward"),
                why(r"the pool is the miner's library; its combination is what is scored")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The local miner is inspired by AlphaGen, with a smaller REINFORCE implementation. <bookmark mark='a'/> A GRU chooses tokens under a stack-validity mask. <bookmark mark='b'/> Reward is the marginal training IC of a least-squares pool when the proposed formula joins. The fit zero-fills missing future returns, while IC scoring filters finite outcomes, so the two missingness conventions differ. <bookmark mark='c'/> REINFORCE credits sampled log probabilities with this marginal reward, scaled by one hundred; invalid formulas receive minus0.01. <bookmark mark='d'/> A new string joins only above0.0005 gain. Above ten members, the removal with the best remaining training score is chosen. This is adaptive training selection, not independent evidence of complementary out-of-sample alpha."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def gradient(self):
        rows = [cmath(r"J(\theta)", r"=", r"\mathbb E_{f \sim \pi_\theta}[R(f)] = \textstyle\sum_f \pi_\theta(f)\,R(f)",
                      font_size=32, colors={r"J(\theta)": RL_C}),
                cmath(r"\nabla_\theta J", r"=", r"\textstyle\sum_f \pi_\theta(f)\,\nabla_\theta\log\pi_\theta(f)\,R(f)",
                      font_size=32, colors={r"\nabla_\theta J": RL_C}),
                cmath(r"\log\pi_\theta(f)", r"=", r"\textstyle\sum_k \log\pi_\theta(a_k \mid a_{<k})", font_size=32),
                cmath(r"\mathbb E[\nabla_\theta\log\pi_\theta(f)\, b]", r"=", r"b\,\nabla_\theta \textstyle\sum_f"
                      r"\pi_\theta(f) = 0", font_size=30, colors={r"\mathbb E[\nabla_\theta\log\pi_\theta(f)\, b]": HURDLE})]
        whys = [why(r"the objective: the expected reward of a formula drawn from the policy"),
                why(r"the log-derivative trick, $\nabla\pi = \pi\,\nabla\log\pi$: the gradient is itself an expectation, "
                    r"so a sampled formula gives an unbiased estimate"),
                why(r"a formula's probability is the product of its tokens' probabilities: the reward is credited to every "
                    r"token"),
                why(r"an action-independent baseline conditional on state has zero expected score contribution: "
                    r"a suitable choice may reduce variance")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Condition on a fixed current pool and reward mapping. <bookmark mark='a'/> The objective is expected reward under the token policy. <bookmark mark='b'/> The log-derivative identity gives an unbiased sampled score-function gradient for that fixed conditional objective. It does not make the backtest score unbiased or the changing pool stationary. <bookmark mark='c'/> Sequence log probability sums the token log probabilities. <bookmark mark='d'/> A baseline independent of the sampled action, conditional on the available state, has zero score-function expectation. A suitable baseline can reduce variance, but an arbitrary one need not. The current pool score is part of the marginal reward definition here; no separate learned value-function baseline is fitted. Updating policy and pool supplies no guarantee of global optimisation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def training(self, r):
        h = r["hist"]
        ep = np.array([x["ep"] for x in h], float)
        ic = np.array([x["pool_ic"] for x in h], float)
        n = np.array([x["pool"] for x in h], float)
        top = float(np.ceil(max(ic.max(), 0.01) * 100 + 0.5) / 100)
        g = axes([0, ep[-1]], [0, top], x_length=7.2, y_length=4.4, xlabel=r"episodes (formulas written)",
                 ylabel=r"the pool's training IC", xticks=[0, ep[-1] / 2, ep[-1]], yticks=[0, top / 2, top], font_size=15,
                 xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.2f}").move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, ep, ic, RL_C, stroke_width=3)
        side = VGroup(MathTex(rf"{r['evaluated']:,}".replace(",", "{,}") + r"\ \text{distinct formulas}", font_size=24),
                      MathTex(rf"\text{{pool of}}\ {int(n[-1])}", font_size=24, color=RL_C),
                      wrapped_label(r"the step pattern: a formula that adds to the pool lifts its IC at once; between "
                                    r"lifts the policy explores", 3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"""The single-seed original run samples {r['episodes']:,} episodes; repeated strings can recur. A penalty for failed decoding is defined, but the stored result does not report a failed-decode count. <bookmark mark='a'/> The current pool's fitted training score ends at {r['train']['ic']:.3f}. Admission and removal use that same training objective. <bookmark mark='b'/> Its cache evaluates {r['evaluated']:,} distinct valid strings. This is a computational count within one adaptive search, not independent tests. The stored histories describe pool score and size; they do not preserve a policy checkpoint or establish how token probabilities changed."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def pool(self, r):
        kept = 100 * r["valid"]["ic"] / r["train"]["ic"]
        rows = VGroup(*[label(tt(f, 80), font_size=20, color=GREY_A) for f in r["pool"][:10]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14)
        head = label(r"the final pool: truncated formula previews", font_size=24, color=RL_C)
        res = MathTex(rf"\text{{the pool's combination: IC}}\ {r['train']['ic']:.3f}\ \text{{on 2018--19}}\ \to\ "
                      rf"{r['valid']['ic']:+.3f}\ \text{{on 2020}}\ (t = {r['valid']['t']:+.1f})", font_size=26)
        g = VGroup(head, rows, res).arrange(DOWN, buff=0.35)
        if g.width > 12.8:
            g.scale_to_fit_width(12.8)
        g.move_to(ORIGIN)
        with self.voiceover(
            f"""The final pool contains {len(r['pool'])} formulas. <bookmark mark='a'/> Volume and recent-price terms recur, but visual resemblance does not identify independent economic risks. These formulas were chosen to help the fitted training combination, with training-based signs and weights. <bookmark mark='b'/> Its mean IC is {r['train']['ic']:.3f} in training and {r['valid']['ic']:+.3f} in validation, with an IID-day descriptive t-statistic of {r['valid']['t']:.1f}. The validation-to-training ratio is about {kept:.0f} percent. Dependence, adaptive selection, missingness and costs remain unresolved by that ratio; synergy reward does not guarantee durable diversification."""
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the synergy reward uses the training IC of the pool's combination. What happens to the reward "
                       r"of a formula that is pure noise but uncorrelated with the pool?")
        with self.voiceover(
            "Pause and predict. The reward is the gain in the pool's training score. What reward does a formula earn "
            "that is pure noise, but uncorrelated with everything in the pool?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
