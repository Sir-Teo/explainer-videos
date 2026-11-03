from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import GOLD, KLC, PART, PENALTY, POLICY, PROXY, REF, REWARD, load, said, ticks


class DPO(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.ours()
        self.displacement()
        self.frontier()
        self.family()

    def card(self):
        card = chapter_card(8, r"Direct preference optimization", r"Do you need the reward model at all?",
                            lit=(2023,), part=PART)
        with self.voiceover("Chapter eight. Direct preference optimization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\pi^*(y \mid x)", r"=", r"\frac{1}{Z(x)}\, \pi_{\mathrm{ref}}(y \mid x)\, e^{r(x, y)/\beta}",
                  font_size=34),
            cmath(r"r(x, y)", r"=", r"\beta \log \frac{\pi^*(y \mid x)}{\pi_{\mathrm{ref}}(y \mid x)} + \beta \log Z(x)",
                  font_size=34),
            cmath(r"P(y_w \succ y_l)", r"=", r"\sigma\Big(\beta \log \frac{\pi^*(y_w \mid x)}{\pi_{\mathrm{ref}}(y_w \mid "
                  r"x)} - \beta \log \frac{\pi^*(y_l \mid x)}{\pi_{\mathrm{ref}}(y_l \mid x)}\Big)", font_size=32),
            cmath(r"\mathcal L_{\mathrm{DPO}}(\theta)", r"=", r"-\,\mathbb E\Big[\log \sigma\Big(\beta \log "
                  r"\frac{\pi_\theta(y_w \mid x)}{\pi_{\mathrm{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid "
                  r"x)}{\pi_{\mathrm{ref}}(y_l \mid x)}\Big)\Big]", font_size=30),
        ]
        rows[3][0].set_color(POLICY)
        whys = [why(r"chapter 6's optimum"), why(r"solve for the reward"),
                why(r"Bradley--Terry, chapter 4: \ $Z(x)$ cancels"),
                why(r"fit $\pi_\theta$ to the comparisons directly")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.2, buff=0.48, edge=6.9)
        imp = label(r"the implicit reward: \ $\beta \log \pi_\theta / \pi_{\mathrm{ref}}$", font_size=28, color=POLICY)
        imp.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2023 Rafael Rafailov, Archit Sharma, Eric Mitchell and colleagues at Stanford noticed that chapter "
            "six's optimum can be run backwards. <bookmark mark='a'/> Take the log and solve for the reward: the "
            "reward is beta times the log of the optimal policy over the reference, plus a term that depends only on "
            "the question. <bookmark mark='b'/> Now put that into the Bradley-Terry model of chapter four. The "
            "comparison depends only on a difference of rewards for the same question, so the awkward normalizer Z "
            "cancels. <bookmark mark='c'/> What's left is a loss on the policy itself: logistic regression whose "
            "score is beta times the log-ratio of policy to reference. No reward model, no sampling, no "
            "reinforcement learning; just a supervised loss on the comparisons. <bookmark mark='d'/> The policy is "
            "its own reward model."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(imp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        d = load("dpo")
        sft = load("sft")
        rl = load("rlhf")
        key = "b" + f"{rl['betas'][0]:g}".replace(".", "_")
        # measured as DPO's is: the trained policy's own lines, scored by gold, and its KL from the fine-tuned model
        rl_gold, rl_kl = float(rl[key + "_final"]["gold"]), float(rl[key + "_final"]["kl"])
        rows = VGroup(
            VGroup(label(r"fine-tuned model", font_size=30, color=REF),
                   label(rf"gold ${sft['sft_line_gold']:+.2f}$", font_size=30, color=GOLD),
                   label(r"KL $0$", font_size=30, color=KLC)),
            VGroup(label(rf"RLHF, \ $\beta = {rl['betas'][0]:g}$", font_size=30, color=POLICY),
                   label(rf"gold ${rl_gold:+.2f}$", font_size=30, color=GOLD),
                   label(rf"KL ${rl_kl:.1f}$", font_size=30, color=KLC)),
            VGroup(label(rf"DPO, \ $\beta = {d['beta']:g}$", font_size=30, color=POLICY),
                   label(rf"gold ${d['gold']:+.2f}$", font_size=30, color=GOLD),
                   label(rf"KL ${d['kl']:.1f}$", font_size=30, color=KLC)),
        )
        for r_ in rows:
            r_[1].move_to([1.0, 0, 0])
            r_[2].move_to([4.0, 0, 0])
            r_[0].move_to([-3.6, 0, 0])
        rows.arrange(DOWN, buff=0.65).move_to(UP * 1.0)
        for r_ in rows:
            r_[0].align_to(rows[0][0], LEFT)
        ex = VGroup(*[said(t, chars=46, font_size=20, max_lines=2) for _, t in d["examples"][:2]])
        ex.arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        tag = note(r"computed: \ the same comparisons; \ estimated KL: $80$ policy draws, nats per line").to_corner(UR, buff=0.25)
        better = d["gold"] > sft["sft_line_gold"]
        said_ = (f"Its lines score {d['gold']:+.2f} with gold, up from {sft['sft_line_gold']:+.2f}, "
                 if better else f"Its lines score {d['gold']:+.2f} with gold, against {sft['sft_line_gold']:+.2f}, ")
        with self.voiceover(
            "We trained DPO on our model, with the same comparisons the reward model learned from. "
            f"<bookmark mark='a'/> {said_}at an estimated divergence of {d['kl']:.1f} nats from where it started. "
            f"<bookmark mark='b'/> RLHF with beta {rl['betas'][0]:g} reached {rl_gold:+.2f} at an estimated {rl_kl:.1f} nats. "
            "The RLHF row is seed zero's separately evaluated final policy. "
            "<bookmark mark='c'/> Two routes to the same kind of objective: one through a reward model and sampling, "
            "the other straight from the comparisons."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def displacement(self):
        d = load("dpo")
        p = np.asarray(d["probe"])
        S = int(p[-1, 0])
        lo, hi = float(min(p[:, 1].min(), p[:, 2].min())), float(max(p[:, 1].max(), p[:, 2].max(), 0.5))
        g = axes([0, S], [np.floor(lo), np.ceil(hi)], x_length=7.0, y_length=3.8, xlabel=r"DPO steps",
                 ylabel=r"$\log \pi_\theta(y) - \log \pi_{\mathrm{ref}}(y)$ \ (mean, nats; $32$ fixed training pairs)",
                 xticks=[0, S], yticks=ticks(np.floor(lo), np.ceil(hi), 3), center=[-1.0, -0.2, 0])
        cw = VMobject().set_points_as_corners([g.ax.c2p(a, b) for a, b in zip(p[:, 0], p[:, 1])]).set_stroke(REWARD, 4)
        cl = VMobject().set_points_as_corners([g.ax.c2p(a, b) for a, b in zip(p[:, 0], p[:, 2])]).set_stroke(PENALTY, 4)
        zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(S, 0), color=GREY_C, dash_length=0.06)
        lg = legend([(REWARD, r"the preferred answers"), (PENALTY, r"the rejected answers")], font_size=20)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        gap_start = float(p[0, 1] - p[0, 2])
        gap_end = float(p[-1, 1] - p[-1, 2])
        gap_change = gap_end - gap_start
        # Avoid interpreting insignificant roundoff near zero as a qualitative pattern.
        observed = p[-1, 1] < -1e-4 and p[-1, 2] < -1e-4 and gap_change > 1e-4
        verdict = ("Both mean log-probabilities end below reference, while their mean gap increased: a pattern "
                   "consistent with likelihood displacement in this probe." if observed else
                   "This probe does not show the specific pattern of both mean log-probabilities ending below "
                   "reference while their mean gap increases.")
        text = (f"At step {S:d}, the preferred answers' mean log-probability relative to reference is "
                f"{p[-1, 1]:+.1f} nats, and the rejected answers' is {p[-1, 2]:+.1f}. Their mean gap has changed "
                f"by {gap_change:+.1f} nats since the start.")
        with self.voiceover(
            "DPO only cares about the gap between the preferred and the rejected answer. Watch what happens to each "
            "separately, for thirty-two fixed training pairs, as it trains. <bookmark mark='a'/> " + text + " The pattern: " + verdict +
            " These averages over fixed training pairs do not measure held-out accuracy or total probability "
            "mass, and do not identify which other answers receive probability."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(lg))
            vo.wait_until("a")
            self.play(Create(cw), Create(cl), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        """Every method trades divergence for gold: best-of-n, RLHF and DPO on one chart, gold gained against sqrt KL."""
        bo, rl, dp, sw = load("bon"), load("rlhf"), load("dpo"), load("dpo_sweep")
        base = load("sft")["sft_line_gold"]
        bo_kl = np.asarray(bo["kl"], dtype=float)
        if not np.isfinite(bo_kl).all() or (bo_kl < 0).any():
            raise ValueError("Invalid best-of-n KL upper-bound coordinate; preserve and review the cached input")
        kx = np.sqrt(bo_kl)
        bon = np.asarray(bo["large_gold"]) - float(bo["large_gold"][0])  # the same prompts' n = 1 average
        pts = [("RLHF", b, rl[f"b{b:g}".replace(".", "_") + "_final"]["gold"] - base,
                rl[f"b{b:g}".replace(".", "_") + "_final"]["kl"]) for b in rl["betas"]]
        pts += [("DPO", b, g_ - base, k_) for b, g_, k_ in sorted([(dp["beta"], dp["gold"], dp["kl"])] +
                                                                [tuple(p_) for p_ in sw["points"]])]
        if not all(np.isfinite([b, gold_gain, kl]).all() for _, b, gold_gain, kl in pts):
            raise ValueError("Nonfinite policy gold/KL coordinate; preserve and review the cached input")
        negative = [(method, beta, kl) for method, beta, _, kl in pts if kl < 0]
        if negative:
            raise ValueError(
                f"Negative Monte Carlo KL estimates cannot be plotted on a square-root axis: {negative}. "
                "Preserve these estimates and review an explicit signed display or a separate evaluation; "
                "do not clip them to zero."
            )
        xmax = max(float(kx[-1]), max(np.sqrt(k_) for *_, k_ in pts)) * 1.08
        ys = [float(bon.min()), float(bon.max())] + [g_ for _, _, g_, _ in pts]
        lo, hi = min(ys + [0.0]), max(ys)
        pad = 0.1 * (hi - lo + 1e-6)
        g = axes([0, xmax], [lo - pad, hi + pad], x_length=8.0, y_length=4.4,
                 xlabel=r"$\sqrt{\mathrm{KL}}$ \ (best-of-$n$: upper bound; \ trained: estimate)",
                 ylabel=r"gold gained over the fine-tuned model", xticks=[0, round(xmax)],
                 yticks=ticks(lo - pad, hi + pad, 3), yfmt=lambda v: rf"{v:+.2f}" if v else "0",
                 center=[-2.3, -0.3, 0])
        zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(xmax, 0), color=GREY_D, dash_length=0.06)
        # what the two directions mean, while the chart is still empty
        up = label(r"$\uparrow$ \ better, by gold", font_size=22, color=GREY_B).move_to(
            g.ax.c2p(0, hi + pad) + RIGHT * 0.3 + DOWN * 0.15, aligned_edge=UL)
        right = label(r"further from where it started \ $\rightarrow$", font_size=22, color=GREY_B).move_to(
            g.ax.c2p(xmax, 0) + LEFT * 0.15 + UP * 0.15, aligned_edge=DR)
        bc = curve(g.ax, kx, bon, PROXY, 5)
        dots = VGroup()
        for meth, b, g_, k_ in pts:
            col = KLC if meth == "RLHF" else POLICY
            d_ = Dot(g.ax.c2p(np.sqrt(k_), g_), radius=0.09, color=col)
            dots.add(VGroup(d_, label(rf"{meth}, \ $\beta = {b:g}$", font_size=20, color=col)))
        # names in a column right of the chart, in the order of their dots' heights, each joined to its dot by a
        # thin leader (RLHF and DPO at beta 0.1 land almost on top of each other)
        X = g.ax.get_right()[0] + 0.5
        order = sorted(range(len(dots)), key=lambda i: -dots[i][0].get_y())
        top_y, bot_y = g.ax.get_top()[1] - 0.2, g.ax.get_bottom()[1] + 0.6
        ys = np.linspace(top_y, bot_y, len(dots)) if len(dots) > 1 else [top_y]
        leaders = VGroup()
        for y, i in zip(ys, order):
            dots[i][1].move_to([X, y, 0], aligned_edge=LEFT)
            leaders.add(Line(dots[i][0].get_center(), dots[i][1].get_left() + LEFT * 0.08, color=GREY_D,
                             stroke_width=1.2))
        for j, i in enumerate(order):
            dots[i].add(leaders[j])
        bl = label(r"best-of-$n$, \ $n = 1 \dots 256$", font_size=20, color=PROXY).move_to(
            [X, top_y + 0.45, 0], aligned_edge=LEFT)
        tag = note(r"exploratory: \ best-of-$n$: $12$ prompts; \ trained gold: $30$; \ trained KL: $10$")
        tag.to_corner(DR, buff=0.2)
        verdict = ("These are exploratory results on different prompt populations: twelve for best-of-n, "
                   "thirty for the trained policies' gold, and ten for their estimated KL.")
        cmp_ = ("Best-of-n uses a KL upper bound, while trained policies use a sample estimate. This chart "
                "does not establish which method is best at equal divergence; that needs a matched evaluation.")
        with self.voiceover(
            "Every method in this part trades divergence from the fine-tuned model for gold. Put them on one chart: "
            "gold gained, against the square root of the KL, as in the last chapter. <bookmark mark='a'/> "
            "Best-of-n with the larger reward model is the yardstick: it trains nothing. <bookmark mark='b'/> "
            "RLHF's seed-zero final policies at two penalties, <bookmark mark='c'/> and DPO at three values of beta. <bookmark mark='d'/> " + verdict
            + " <bookmark mark='e'/> " + cmp_
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(tag))
            self.play(FadeIn(up, shift=UP * 0.1), FadeIn(right, shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Create(bc), FadeIn(bl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(up), FadeOut(right), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_, p_ in zip(dots, pts) if p_[0] == "RLHF"],
                                  lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_, p_ in zip(dots, pts) if p_[0] == "DPO"],
                                  lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        head = label(r"Preference-optimization variants", font_size=30).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(2023, r"IPO \ (Azar et al., DeepMind)", r"a squared loss on the log-ratio margin: \ DPO can "
                         r"push it to infinity when preferences are certain", width=6.2, color=POLICY),
            history_card(2024, r"KTO \ (Ethayarajh et al.)", r"thumbs up or down on single answers, \ no pairs, \ with "
                         r"a loss shaped like prospect theory", width=6.2, color=POLICY),
            history_card(2024, r"SimPO \ (Meng, Xia \& Chen)", r"no reference model: \ the length-normalized "
                         r"log-probability is the reward, \ with a margin", width=6.2, color=POLICY),
            history_card(2024, r"online preference learning", r"fresh answers from the current model, \ judged as "
                         r"training goes: \ advantages in the cited comparisons", width=6.2, color=REWARD),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.1)
        cite_ = cite(r"Azar et al.\ (2023); \ Ethayarajh et al.\ (2024); \ Meng et al.\ (2024); \ Tang et al.\ (2024)")
        with self.voiceover(
            "DPO started a family. <bookmark mark='a'/> IPO replaces the logistic loss with a squared one, because "
            "when one answer always wins, DPO can push the log-ratio margin to infinity and overfit. "
            "<bookmark mark='b'/> KTO learns from single answers marked good or bad, with no pairs, using a loss "
            "shaped like Kahneman and Tversky's prospect theory. <bookmark mark='c'/> SimPO drops the reference "
            "model and uses the length-normalized log-probability as the reward. <bookmark mark='d'/> And a lesson "
            "from comparing them: learning from fresh answers by the current model, judged as training goes, "
            "showed advantages over fixed data from older models in the cited comparisons. New experience is one way "
            "alignment training can improve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
