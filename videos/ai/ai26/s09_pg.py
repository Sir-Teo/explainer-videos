from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import (AGENT, PART, REWARD, TDERR, VALUE, axes, band, cartpole, curve, legend, load,
                                   node_box)

SCORE = C.SCORE
REINF, BASE, AC, PPO_C = GREY_B, C.MODEL_Q, C.BASELINE, C.TRUE_P


class PolicyGradient(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_policy()
        self.derive()
        self.intuition()
        self.baseline()
        self.cloud()
        self.actor_critic()
        self.curves()

    def card(self):
        card = chapter_card(8, r"Policy gradients", r"Why not improve the policy directly?", lit=(), part=PART)
        with self.voiceover("Chapter eight. Policy gradients."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why_policy(self):
        pol = cmath(r"\pi_\theta(a \mid s)", r"=", r"\operatorname{softmax}\big(f_\theta(s)\big)_a", font_size=40)
        pol[0].set_color(AGENT)
        pol.move_to([2.7, 2.5, 0])
        J = cmath(r"J(\theta)", r"=", r"\mathbb E_{\tau \sim \pi_\theta}\big[\, R(\tau) \,\big]", font_size=40)
        J[0].set_color(REWARD)
        J.next_to(pol, DOWN, buff=0.5)
        # the policy as a picture: a state goes in, a probability for each push comes out
        cp = cartpole(0.3, 0.12, center=[-5.3, 1.0, 0], scale=0.55)
        sl = MathTex(r"s", font_size=30, color=GREY_A).next_to(cp, DOWN, buff=0.15)
        net = node_box(r"$f_\theta$", AGENT, font_size=30, height=1.1).move_to([-2.75, 1.25, 0])
        pb = VGroup(*[Rectangle(width=0.55, height=1.6 * p_, stroke_width=0, fill_color=AGENT, fill_opacity=0.8)
                      for p_ in (0.3, 0.7)]).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([-0.95, 0.95, 0])
        pb.align_to(cp[2], DOWN)
        pv = VGroup(*[MathTex(rf"{p_:.1f}", font_size=24, color=GREY_A).next_to(b_, UP, buff=0.08)
                      for p_, b_ in zip((0.3, 0.7), pb)])
        pt = VGroup(*[label(t_, font_size=20, color=GREY_B).next_to(b_, DOWN, buff=0.12) for t_, b_ in
                      zip((r"left", r"right"), pb)])
        a1 = Arrow([-3.95, 1.25, 0], net.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(net.get_right(), pb.get_left() + UP * 0.3, buff=0.12, color=GREY_B, stroke_width=2.5)
        pic = VGroup(cp, sl, net, pb, pv, pt, a1, a2)
        jl = label(r"$\tau$: \ a whole episode, \ $R(\tau)$: \ its total reward", font_size=22, color=GREY_A)
        jl.next_to(J, DOWN, buff=0.2)
        pros = VGroup(
            label(r"actions can be continuous: \ a torque, \ a steering angle", font_size=24),
            label(r"the best policy may be random: \ rock-paper-scissors, \ bluffing", font_size=24),
            label(r"a small change in $\theta$ is a small change in behaviour", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.8)
        with self.voiceover(
            "Value methods learn how good things are, and act greedily. Policy-gradient methods skip that and adjust "
            "the policy itself. Make it a network with parameters theta that outputs a probability for each action. "
            "<bookmark mark='a'/> The objective is the expected total reward of an episode, J of theta. Climb it by "
            "gradient ascent. <bookmark mark='b'/> This handles continuous actions, like a torque or a steering "
            "angle, where taking a max over actions is a problem in itself. <bookmark mark='c'/> It can learn "
            "policies that are deliberately random, which the best play in rock-paper-scissors, or poker, has to be. "
            "<bookmark mark='d'/> And behaviour changes smoothly with theta, instead of jumping whenever two Q "
            "values swap order."
        ) as vo:
            self.play(FadeIn(cp), FadeIn(sl))
            self.play(GrowArrow(a1), FadeIn(net), GrowArrow(a2), FadeIn(pb), FadeIn(pv), FadeIn(pt), Write(pol))
            vo.wait_until("a")
            self.play(Write(J), FadeIn(jl))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(pros[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\nabla_\theta J", r"=", r"\nabla_\theta \sum_\tau p_\theta(\tau)\, R(\tau)", font_size=36),
            cmath(r"\nabla_\theta J", r"=", r"\sum_\tau p_\theta(\tau)\, \nabla_\theta \log p_\theta(\tau)\, R(\tau)",
                  font_size=36),
            cmath(r"\nabla_\theta J", r"=", r"\mathbb E_\tau\big[\, R(\tau)\, \nabla_\theta \log p_\theta(\tau) \,\big]",
                  font_size=36),
            cmath(r"\log p_\theta(\tau)", r"=", r"\log p(s_0) + \sum_t \big[", r"\log \pi_\theta(a_t \mid s_t)",
                  r"+ \log P(s_{t+1} \mid s_t, a_t)", r"\big]", font_size=34),
            cmath(r"\nabla_\theta J", r"=", r"\mathbb E_\tau\Big[\, \sum_t", r"G_t", r"\,", r"\nabla_\theta \log "
                  r"\pi_\theta(a_t \mid s_t)", r"\Big]", font_size=36),
        ]
        rows[3][3].set_color(AGENT)
        rows[3][4].set_color(GREY_C)
        rows[4][3].set_color(REWARD)
        rows[4][5].set_color(SCORE)
        whys = [None, why(r"$\nabla p = p\, \nabla \log p$"), why(r"an average over episodes: \ sample it"),
                why(r"the environment's part doesn't depend on $\theta$"),
                why(r"rewards before $t$ can't be caused by $a_t$: \ keep the return-to-go $G_t$")]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-2.2, buff=0.42, edge=6.9)
        name = label(r"REINFORCE \ (Williams, 1992)", font_size=28, color=SCORE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The gradient of an expectation over episodes looks hopeless: the probabilities of episodes depend on "
            "theta, and on the environment's dynamics, which we don't know. <bookmark mark='a'/> The log-derivative "
            "trick from Part 5 rescues it: the gradient of p is p times the gradient of log p. <bookmark mark='b'/> "
            "So the gradient is itself an average over episodes, and an average can be estimated by sampling: play "
            "some episodes and average. <bookmark mark='c'/> Better still, the log-probability of an episode splits "
            "into the policy's choices and the environment's transitions, and the environment's part doesn't depend "
            "on theta. Its gradient is zero. We never need the model. <bookmark mark='d'/> One refinement: an action "
            "can't affect rewards that came before it, so each action is credited only with the return that "
            "followed it. This is REINFORCE, Ronald Williams's algorithm from 1992."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(FadeIn(name))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def intuition(self):
        probs = ValueTracker(0.0)
        p0 = np.array([0.25, 0.35, 0.2, 0.2])
        G = np.array([+1.0, -0.6, +0.3, -0.2])
        p1 = p0 * np.exp(0.9 * G)
        p1 = p1 / p1.sum()
        bars = LiveBars(p0, max_value=0.6, height=3.0, bar_width=0.9, gap=0.5, colors=[AGENT] * 4,
                        labels=[r"$a_1$", r"$a_2$", r"$a_3$", r"$a_4$"], label_font=28, show_values=True, digits=2)
        bars.place(-1.6, x=-2.4)
        rl = VGroup(*[MathTex(rf"G = {g:+.1f}", font_size=26, color=REWARD if g > 0 else C.PENALTY)
                      .next_to(bars.labels[i], DOWN, buff=0.2) for i, g in enumerate(G)])
        arrows = VGroup(*[Arrow(bars.bar(i).get_top() + UP * 0.1, bars.bar(i).get_top() + UP * (0.1 + 0.9 * g),
                                buff=0, color=REWARD if g > 0 else C.PENALTY, stroke_width=5,
                                max_tip_length_to_length_ratio=0.3) for i, g in enumerate(G)])
        txt = VGroup(label(r"sample actions, \ see what followed", font_size=26),
                     label(r"push up $\log \pi$ of each, \ in proportion to its return", font_size=26, color=SCORE),
                     label(r"good actions grow, \ bad ones shrink, \ the rest renormalizes", font_size=26,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.4, 0])
        tag = note(r"illustrative").to_corner(DR, buff=0.25)
        with self.voiceover(
            "In plain terms: the policy tries actions. <bookmark mark='a'/> Each one is followed by some return. "
            "<bookmark mark='b'/> Nudge the log-probability of every action taken, up in proportion to its return. "
            "<bookmark mark='c'/> Actions followed by good outcomes become more likely, and since the probabilities "
            "sum to one, everything else gives way. It is trial and error, Thorndike's law of effect, written as a "
            "gradient."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(tag), FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeOut(arrows), *bars.to(p1), FadeIn(txt[2]), run_time=2.0)
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def baseline(self):
        rows = [
            cmath(r"\nabla_\theta J", r"=", r"\mathbb E\Big[\, \sum_t", r"\big(G_t - b(s_t)\big)", r"\,",
                  r"\nabla_\theta \log \pi_\theta(a_t \mid s_t)", r"\Big]", font_size=36),
            cmath(r"\mathbb E_{a \sim \pi}\big[\, b(s)\, \nabla_\theta \log \pi_\theta(a \mid s) \,\big]", r"=",
                  r"b(s) \sum_a \nabla_\theta \pi_\theta(a \mid s)", font_size=36),
            cmath(r"\mathbb E_{a \sim \pi}\big[\, b(s)\, \nabla_\theta \log \pi_\theta(a \mid s) \,\big]", r"=",
                  r"b(s)\, \nabla_\theta \sum_a \pi_\theta(a \mid s)", r"=", r"b(s)\, \nabla_\theta 1", r"=", r"0",
                  font_size=36),
        ]
        rows[0][3].set_color(TDERR)
        whys = [why(r"subtract any baseline $b(s)$"), why(r"$\pi \nabla \log \pi = \nabla \pi$"),
                why(r"probabilities sum to $1$: \ no bias")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.8, buff=0.6, edge=6.9)
        # four actions' returns: all large and positive, so every action is pushed up; only the differences matter
        Gs = np.array([182.0, 197.0, 205.0, 190.0])
        xs, y0, k_raw = (-3.6, -1.2, 1.2, 3.6), -3.0, 2.9 / 205
        raw = VGroup(*[Arrow([x, y0, 0], [x, y0 + g_ * k_raw, 0], buff=0, color=SCORE, stroke_width=6,
                             max_tip_length_to_length_ratio=0.08) for x, g_ in zip(xs, Gs)])
        rlab = VGroup(*[MathTex(rf"G = {g_:.0f}", font_size=26, color=REWARD).next_to([x, y0, 0], DOWN, buff=0.12)
                        for x, g_ in zip(xs, Gs)])
        top_ = label(r"every return is positive: \ every action is pushed up", font_size=24, color=GREY_A)
        top_.move_to([0, 0.9, 0])
        b_ = Gs.mean()
        yb = y0 + b_ * k_raw - 1.2
        bl = DashedLine([-4.6, yb, 0], [4.6, yb, 0], color=TDERR, stroke_width=2.5)
        bt = MathTex(rf"b = {b_:.1f}", font_size=26, color=TDERR).next_to(bl, RIGHT, buff=0.12)
        diff = VGroup(*[Arrow([x, yb, 0], [x, yb + (g_ - b_) * 0.09, 0], buff=0, color=SCORE, stroke_width=6,
                              max_tip_length_to_length_ratio=0.3) for x, g_ in zip(xs, Gs)])
        dlab = VGroup(*[MathTex(rf"G - b = {g_ - b_:+.1f}", font_size=24, color=REWARD if g_ > b_ else C.PENALTY)
                        .move_to([x, y0 - 0.25, 0]) for x, g_ in zip(xs, Gs)])
        with self.voiceover(
            "The catch is variance. In the cart-pole, every return is positive, so every action gets pushed up, and "
            "the signal is the small difference between big numbers. <bookmark mark='a'/> The cure is to subtract a "
            "baseline, any function of the state, from the return. <bookmark mark='b'/> It costs nothing: averaged "
            "over the action, the baseline term is b times the gradient of the sum of the probabilities, "
            "<bookmark mark='c'/> and the sum of the probabilities is always one. Its gradient is zero. The estimate "
            "stays unbiased, and can get much less noisy."
        ) as vo:
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in raw], lag_ratio=0.15), FadeIn(rlab), FadeIn(top_))
            vo.wait_until("a")
            step(0)
            self.play(FadeOut(top_), Create(bl), FadeIn(bt), ReplacementTransform(raw, diff),
                      ReplacementTransform(rlab, dlab), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(bl, bt, diff, dlab)))
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloud(self):
        d = load("pg_cloud")
        A, B = np.asarray(d["cloud_raw"]), np.asarray(d["cloud_base"])
        s = float(np.percentile(np.abs(np.concatenate([A, B])), 97))
        mk = lambda ctr: Axes(x_range=[-s, s, s], y_range=[-s, s, s], x_length=4.6, y_length=4.6, tips=False,
                              axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(ctr)
        a1, a2 = mk([-3.3, -0.4, 0]), mk([3.3, -0.4, 0])
        clip = lambda P: P[(np.abs(P) < s).all(1)]
        d1 = VGroup(*[Dot(a1.c2p(x, y), radius=0.035, color=GREY_B).set_opacity(0.7) for x, y in clip(A)])
        d2 = VGroup(*[Dot(a2.c2p(x, y), radius=0.035, color=BASE).set_opacity(0.8) for x, y in clip(B)])
        true1 = Arrow(a1.c2p(0, 0), a1.c2p(d["mean_norm"], 0), buff=0, color=SCORE, stroke_width=5)
        true2 = Arrow(a2.c2p(0, 0), a2.c2p(d["mean_norm"], 0), buff=0, color=SCORE, stroke_width=5)
        t1 = label(r"without a baseline", font_size=26, color=GREY_B).next_to(a1, UP, buff=0.15)
        t2 = label(r"with a baseline", font_size=26, color=BASE).next_to(a2, UP, buff=0.15)
        ratio = d["var_raw"] / d["var_base"]
        cap = label(rf"each dot: \ the gradient estimated from one episode \ ($300$ each). \ Variance: \ "
                    rf"${ratio:.1f}\times$ smaller", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        tl = label(r"arrow: \ the true gradient", font_size=20, color=SCORE).next_to(a1, DOWN, buff=0.08)
        with self.voiceover(
            "Here is what that buys, measured. Take a half-trained cart-pole policy, play three hundred episodes, "
            "and compute the gradient each episode alone would give. Each dot is one estimate, projected onto the "
            "true gradient's direction and one other. <bookmark mark='a'/> Without a baseline the estimates scatter "
            "widely around the true gradient, the orange arrow. <bookmark mark='b'/> With a baseline, the average "
            f"return at each time step, they cluster: the variance is {ratio:.1f} times smaller. Same expected "
            "gradient, about half as many episodes needed to see it as clearly."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(t1), FadeIn(t2))
            self.play(LaggedStart(*[FadeIn(p) for p in d1], lag_ratio=0.004), run_time=3)
            vo.wait_until("a")
            self.play(GrowArrow(true1), FadeIn(tl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in d2], lag_ratio=0.004), GrowArrow(true2), FadeIn(cap), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def actor_critic(self):
        rows = [
            cmath(r"A(s_t, a_t)", r"=", r"Q(s_t, a_t) - V(s_t)", font_size=36),
            cmath(r"\delta_t", r"=", r"r_{t+1} + \gamma V_w(s_{t+1}) - V_w(s_t)", font_size=36),
            cmath(r"\hat A_t", r"=", r"\sum_{l \ge 0} (\gamma \lambda)^l\, \delta_{t+l}", font_size=36),
        ]
        for r_ in rows:
            r_[0].set_color(TDERR)
        whys = [why(r"the advantage: \ better or worse than usual?"), why(r"the critic's TD error estimates it"),
                why(r"GAE: \ blend $n$-step estimates, \ like TD($\lambda$)")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        actor = VGroup(RoundedRectangle(width=2.6, height=0.8, corner_radius=0.12, stroke_color=AGENT, stroke_width=2.5),
                       label(r"actor $\pi_\theta$", font_size=26, color=AGENT))
        critic = VGroup(RoundedRectangle(width=2.6, height=0.8, corner_radius=0.12, stroke_color=VALUE, stroke_width=2.5),
                        label(r"critic $V_w$", font_size=26, color=VALUE))
        for b_ in (actor, critic):
            b_[1].move_to(b_[0])
        pair = VGroup(actor, critic).arrange(RIGHT, buff=2.2).move_to(DOWN * 1.9)
        arr = Arrow(critic.get_left(), actor.get_right(), buff=0.1, color=TDERR, stroke_width=3)
        al = label(r"$\hat A_t$: \ was that better than expected?", font_size=22, color=TDERR).next_to(pair, UP, buff=0.2)
        cite_ = cite(r"Barto, Sutton \& Anderson (1983); \ Schulman et al., \textit{GAE} (2016)")
        with self.voiceover(
            "The best baseline is the state's value, V. Then what multiplies the gradient is the advantage: how much "
            "better this action turned out than what you'd expect in this state anyway. <bookmark mark='a'/> We "
            "don't know V, so learn it with a second network, the critic, trained by TD. Its TD error is itself an "
            "estimate of the advantage. <bookmark mark='b'/> And just as TD lambda blends n-step returns, generalized "
            "advantage estimation blends n-step advantages, with lambda trading bias for variance. "
            "<bookmark mark='c'/> An actor that acts, and a critic that judges: actor-critic, an architecture that "
            "goes back to Barto, Sutton and Anderson's pole-balancer of 1983, the very task on screen in this chapter."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(pair), GrowArrow(arr), FadeIn(al), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("pg")
        grid = np.asarray(d["grid"])
        g = axes([0, 100_000], [0, 500], x_length=7.2, y_length=4.0, xlabel=r"steps of experience",
                 ylabel=r"episode length \ (mean of $3$ runs)", xticks=[0, 50_000, 100_000], yticks=[0, 250, 500],
                 xfmt=lambda v: f"{int(v / 1000)}" + (r"\text{k}" if v else ""), center=[-1.2, -0.3, 0])
        items = (("reinforce", REINF, r"REINFORCE"), ("baseline", BASE, r"with a baseline"),
                 ("ac", AC, r"actor-critic (GAE)"))
        lines, bands = VGroup(), VGroup()
        for key, col, _ in items:
            Y = np.asarray(d[key])
            bands.add(band(g.ax, grid, np.nanmin(Y, 0), np.nanmax(Y, 0), col, 0.12))
            lines.add(curve(g.ax, grid, np.nanmean(Y, 0), col, 3))
        lg = legend([(c, t) for _, c, t in items], font_size=20).next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        tag = note(r"computed: \ cart-pole, \ the same networks and step budget").to_corner(DR, buff=0.2)
        with self.voiceover(
            "On the cart-pole, with the same networks and the same budget of experience: plain REINFORCE, "
            "<bookmark mark='a'/> REINFORCE with a baseline, <bookmark mark='b'/> and actor-critic with "
            "generalized advantages. Each reduction in variance makes learning faster and steadier."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(bands[0]), Create(lines[0]), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(FadeIn(bands[1]), Create(lines[1]), FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(FadeIn(bands[2]), Create(lines[2]), FadeIn(lg[2]))
        self.wait(0.3)
        self.clear_scene()
