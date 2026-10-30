from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, HIST, MODEL, OBS, PART, REWARD, WORLD, framed, gray, load, node_box, spread_band

PRIOR, POST = C.MODEL_Q, C.TRUE_P
BAL, PLAIN = C.INTERVAL, GREY_B


class Dreamer(VoiceoverScene):
    def construct(self):
        self.card()
        self.rssm()
        self.loss()
        self.balance()
        self.symlog()
        self.imagine()
        self.replay()
        self.curves()

    def card(self):
        card = chapter_card(12, r"Dreamer: learning inside a dream", r"Can an agent learn to act in its own imagination?",
                            part=PART)
        with self.voiceover("Chapter twelve. Dreamer: learning inside a dream."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rssm(self):
        xs = [-5.6, -2.8, 0.0]
        hs = VGroup(*[node_box(rf"$h_{{{t}}}$", MODEL, 28, height=0.7) for t in ("t-1", "t", "t+1")])
        zs = VGroup(*[node_box(rf"$z_{{{t}}}$", POST, 28, height=0.7) for t in ("t-1", "t", "t+1")])
        for k, x in enumerate(xs):
            hs[k].move_to([x, 0.9, 0])
            zs[k].move_to([x + 1.1, -0.5, 0])
        imgs = VGroup(*[RoundedRectangle(width=0.8, height=0.8, corner_radius=0.08, stroke_color=OBS, stroke_width=2)
                        for _ in xs])
        for k, x in enumerate(xs):
            imgs[k].move_to([x + 1.1, -2.4, 0])
        il = VGroup(*[MathTex(rf"x_{{{t}}}", font_size=26, color=OBS).move_to(i_) for t, i_ in zip(("t-1", "t", "t+1"), imgs)])
        rec = VGroup(*[Arrow(hs[k].get_right(), hs[k + 1].get_left(), buff=0.08, color=MODEL) for k in range(2)])
        al = VGroup(*[MathTex(rf"a_{{{t}}}", font_size=24, color=AGENT).next_to(r_, UP, buff=0.08) for t, r_ in zip(("t-1", "t"), rec)])
        zh = VGroup(*[Arrow(zs[k].get_top(), hs[k + 1].get_left() + DOWN * 0.15, buff=0.08, color=GREY_B, stroke_width=2)
                      for k in range(2)])
        post = VGroup(*[Arrow(imgs[k].get_top(), zs[k].get_bottom(), buff=0.08, color=POST, stroke_width=2.5) for k in range(3)])
        hz = VGroup(*[Arrow(hs[k].get_bottom(), zs[k].get_left(), buff=0.08, color=PRIOR, stroke_width=2.5) for k in range(3)])
        parts = VGroup(
            label(r"$h$: \ a GRU's memory, \ deterministic", font_size=20, color=MODEL),
            label(r"$z$: \ $8$ categorical variables, \ sampled", font_size=20, color=POST),
            label(r"prior $p(z_t \mid h_t)$: \ a guess without looking", font_size=20, color=PRIOR),
            label(r"posterior $q(z_t \mid h_t, x_t)$: \ after looking", font_size=20, color=POST),
            label(r"from $(h_t, z_t)$: \ the picture $\hat x_t$, \ the reward $\hat r_t$", font_size=20, color=REWARD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for p_ in parts:
            p_.scale(1.25)
        parts.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if parts.width > 6.0:
            parts.width = 6.0
        parts.to_corner(UR, buff=0.3)
        hist = history_card(r"2019--25", r"PlaNet, \ Dreamer, \ DreamerV2, \ V3 \ (Hafner et al.)", r"V2 learned Atari "
                            r"inside its model; \ V3, \ one set of settings for over $150$ tasks, \ collected diamonds in "
                            r"Minecraft from scratch \ (\textit{Nature}, 2025)", width=4.6, color=HIST,
                            font_size=21).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Our bouncing-ball model only predicted. Danijar Hafner's Dreamer agents, from 2019 on, learn a world "
            "model and then learn to act entirely inside it. Its core is a recurrent state-space model. "
            "<bookmark mark='a'/> A recurrent network carries a deterministic memory h from step to step, updated "
            "with each action. <bookmark mark='b'/> Beside it sits a stochastic state z, here eight categorical "
            "variables. <bookmark mark='c'/> From the memory alone, the prior guesses z without looking at the "
            "picture. <bookmark mark='d'/> When there is a picture, the posterior looks at it and corrects the guess. "
            "<bookmark mark='e'/> From h and z the model redraws the picture and predicts the reward. "
            "<bookmark mark='f'/> DreamerV3, in 2023, ran with one fixed set of settings across more than a hundred "
            "and fifty tasks, and was the first to collect diamonds in Minecraft without human data."
        ) as vo:
            self.play(FadeIn(hs), *[GrowArrow(r_) for r_ in rec], FadeIn(al))
            self.play(FadeIn(parts[0]))
            vo.wait_until("b")
            self.play(FadeIn(zs), *[GrowArrow(a_) for a_ in zh], FadeIn(parts[1]))
            vo.wait_until("c")
            self.play(*[GrowArrow(a_) for a_ in hz], FadeIn(parts[2]))
            vo.wait_until("d")
            self.play(FadeIn(imgs), FadeIn(il), *[GrowArrow(a_) for a_ in post], FadeIn(parts[3]))
            vo.wait_until("e")
            self.play(FadeIn(parts[4]))
            vo.wait_until("f")
            self.play(FadeIn(hist, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loss(self):
        rows = [
            cmath(r"\mathcal L", r"=", r"-\log p(x_t \mid h_t, z_t)", font_size=32),
            cmath(r"\mathcal L", r"=", r"-\log p(x_t \mid h_t, z_t) - \log p(r_t \mid h_t, z_t)", font_size=32),
            cmath(r"\mathcal L", r"=", r"\ldots + \beta_{\mathrm{dyn}} \max\!\big(1, \mathrm{KL}[\mathrm{sg}(q) \,\|\, p]\big)",
                  font_size=32),
            cmath(r"\mathcal L", r"=", r"\ldots + \beta_{\mathrm{rep}} \max\!\big(1, \mathrm{KL}[q \,\|\, \mathrm{sg}(p)]\big)",
                  font_size=32),
            cmath(r"\beta_{\mathrm{dyn}}", r"=", r"0.5, \quad \beta_{\mathrm{rep}} = 0.1", font_size=32),
        ]
        whys = [why(r"redraw the picture"), why(r"predict the reward"),
                why(r"pull the prior towards what was seen: \ the dynamics"),
                why(r"keep the posterior predictable: \ the representation"),
                why(r"balanced: \ the prior moves more; \ below $1$ nat, \ free")]
        step = ladder(self, rows, whys, keep=5, top=3.0, x=-2.4, buff=0.45, edge=6.9)
        sg = label(r"$\mathrm{sg}$: \ stop the gradient, \ treat as a constant", font_size=22, color=GREY_A)
        sg.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "It learns from three terms. <bookmark mark='a'/> Redraw each picture from the state. "
            "<bookmark mark='b'/> Predict each reward. <bookmark mark='c'/> And make the prior agree with the "
            "posterior, so that the model can predict without looking: that is what lets it dream. The agreement is "
            "a KL divergence, and DreamerV2 split it in two. One part, with the posterior frozen, trains the prior "
            "towards what was seen. <bookmark mark='d'/> The other, with the prior frozen, nudges the posterior "
            "towards states the prior can predict. <bookmark mark='e'/> Weighting the first more, the prior moves "
            "more: KL balancing. And below one nat the KL is free, so the posterior is never squeezed to say "
            "nothing."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.2)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(sg))
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def balance(self):
        k = load("klbal")
        cfg = k["params"]["configs"]
        Eb, Ep = np.asarray(k["balanced_err"]), np.asarray(k["plain_err"])
        n = Eb.shape[1]
        xs = np.arange(1, n + 1)
        ymax = float(max(Eb.max(), Ep.max())) * 1.1
        g = axes([0, n, 5], [0, ymax, 1], x_length=7.0, y_length=4.2, xlabel=r"steps dreamed ahead, \ from $6$ real frames",
                 ylabel=r"pixels wrong per frame", xticks=[0, 10, 20, 30], yticks=list(range(0, int(ymax) + 1, 2)),
                 center=[-2.3, -0.4, 0])
        bb, bp = spread_band(g.ax, xs, Eb, BAL), spread_band(g.ax, xs, Ep, PLAIN)
        leg = legend([(BAL, rf"balanced: \ $\beta_{{\mathrm{{dyn}}}} = {cfg['balanced'][0]}$, \ "
                            rf"$\beta_{{\mathrm{{rep}}}} = {cfg['balanced'][1]}$"),
                      (PLAIN, rf"plain: \ both ${cfg['plain'][0]}$")], font_size=20).to_corner(UR, buff=0.4)
        mb, mp_ = float(Eb.mean()), float(Ep.mean())
        tag = note(rf"computed: \ the world model alone, \ random play, \ {len(k['params']['seeds'])} seeds each, \ "
                   r"band min--max, \ same total KL weight", font_size=17).to_edge(DOWN, buff=0.15)
        sep = Eb.max(0) < Ep.min(0)
        if mb < 0.85 * mp_:
            v = (f"With balancing, its dreams average {mb:.1f} wrong pixels a frame over thirty steps; without, "
                 f"{mp_:.1f}. The bands do not even overlap." if sep.mean() > 0.5 else
                 f"With balancing, its dreams average {mb:.1f} wrong pixels a frame over thirty steps; without, "
                 f"{mp_:.1f}.")
        elif mp_ < 0.85 * mb:
            v = (f"Here, surprisingly, the plain KL dreams better: {mp_:.1f} wrong pixels a frame against {mb:.1f}. "
                 "On a world this small, balancing does not pay off.")
        else:
            v = (f"On a world this small the difference is slight: {mb:.1f} wrong pixels a frame with balancing, "
                 f"{mp_:.1f} without. Balancing matters more on harder worlds, like Atari's.")
        with self.voiceover(
            "Does balancing matter? We trained just the world model of our small game both ways, three seeds each, "
            "with the same total weight on the KL, <bookmark mark='a'/> and let each dream thirty steps ahead from "
            f"six real frames, counting the pixels it gets wrong. <bookmark mark='b'/> {v}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bp[0]), Create(bp[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(bb[0]), Create(bb[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def symlog(self):
        s = load("symlog")
        scales = [float(v) for v in s["scales"]]
        raw, sym = np.asarray(s["raw_err"]), np.asarray(s["symlog_err"])
        g = axes([-6, 6, 2], [-3, 3, 1], x_length=4.6, y_length=3.2, xticks=[-6, 0, 6], yticks=[-2, 0, 2],
                 center=[-4.3, 0.9, 0])
        xx = np.linspace(-6, 6, 120)
        c = curve(g.ax, xx, np.sign(xx) * np.log1p(np.abs(xx)), BAL, 3.5)
        f = cmath(r"\operatorname{symlog}(x) = \operatorname{sign}(x)\,\ln(1 + |x|)", font_size=28).next_to(g, DOWN, buff=0.25)
        fl = label(r"predict $\operatorname{symlog}(r)$, \ read back with its inverse", font_size=20, color=GREY_A)
        fl.next_to(f, DOWN, buff=0.15)
        W = 3.6
        bars = VGroup()
        for j, sc in enumerate(scales):
            row = VGroup()
            for M_, col in ((raw, PLAIN), (sym, BAL)):
                v = float(np.clip(M_[:, j].mean(), 0, 1))
                row.add(Rectangle(width=max(W * v, 0.02), height=0.22, stroke_width=0, fill_color=col, fill_opacity=0.9))
            row.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            name = label(rf"rewards about ${sc:g}$", font_size=19, color=GREY_A)
            vals = VGroup(*[MathTex(rf"{100 * float(M_[:, j].mean()):.0f}\%", font_size=20, color=col)
                            .next_to(r_, RIGHT, buff=0.1) for M_, col, r_ in ((raw, PLAIN, row[0]), (sym, BAL, row[1]))])
            bars.add(VGroup(name, row, vals))
        for k, b_ in enumerate(bars):
            b_[1].move_to([1.6 + W / 2, 1.6 - 0.95 * k, 0], aligned_edge=LEFT).align_to([1.6, 0, 0], LEFT)
            b_[0].next_to(b_[1], UP, buff=0.05).align_to(b_[1], LEFT)
            for v_, r_ in zip(b_[2], b_[1]):
                v_.next_to(r_, RIGHT, buff=0.1)
        bl = label(r"error, \ relative to the reward's size", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.25)
        bl.align_to(bars, LEFT)
        leg = legend([(PLAIN, r"squared error on raw rewards"), (BAL, r"after symlog")], font_size=18)
        leg.next_to(bars, DOWN, buff=0.3).align_to(bars, LEFT)
        tag = note(rf"computed: \ one network, \ four games' rewards, \ {raw.shape[0]} seeds, \ {int(s['steps'])} steps",
                   font_size=17).to_edge(DOWN, buff=0.12)
        r1, s1 = float(raw[:, 0].mean()), float(sym[:, 0].mean())
        rL, sL = float(raw[:, -1].mean()), float(sym[:, -1].mean())
        if r1 > 2 * s1:
            v = (f"Trained on raw rewards, the network spends itself on the largest game and gets the smallest one "
                 f"{100 * r1:.0f} percent wrong. With symlog, every game is learned: {100 * s1:.0f} percent on the "
                 f"smallest, {100 * sL:.0f} on the largest.")
        else:
            v = (f"Here the raw rewards get the smallest game {100 * r1:.0f} percent wrong and symlog "
                 f"{100 * s1:.0f}: a smaller gap than expected.")
        with self.voiceover(
            "A second trick from DreamerV3 lets one set of settings work everywhere. Rewards in one game are "
            "around one, in another around a thousand, and a squared error is dominated by the largest. "
            "<bookmark mark='a'/> So V3 predicts the symmetric logarithm of the reward and undoes it afterwards: "
            "close to the identity near zero, logarithmic far away. <bookmark mark='b'/> We trained one small "
            "network to predict the rewards of four games whose scales differ a thousandfold. "
            f"<bookmark mark='c'/> {v} Our Dreamer predicts its rewards this way, as a distribution over bins in "
            "symlog space."
        ) as vo:
            self.play(FadeIn(g), Create(c), Write(f), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(bl), FadeIn(leg), *[FadeIn(b_[0]) for b_ in bars])
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[1][0], LEFT), FadeIn(b_[2][0])) for b_ in bars],
                                  lag_ratio=0.2), run_time=1.5)
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[1][1], LEFT), FadeIn(b_[2][1])) for b_ in bars],
                                  lag_ratio=0.2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def imagine(self):
        d = load("dreamer")
        P = d["params"]
        rows = [
            cmath(r"R^\lambda_t", r"=", r"\hat r_{t+1} + \gamma\big[(1 - \lambda)\, v(s_{t+1}) + \lambda\, R^\lambda_{t+1}\big]",
                  font_size=30),
            cmath(r"\nabla_\theta J", r"=", r"\mathbb E\Big[\sum_t \tfrac{R^\lambda_t - v(s_t)}{\max(1, S)}\, \nabla_\theta "
                  r"\log \pi_\theta(a_t \mid s_t)\Big] + \eta\, \nabla_\theta \mathcal H", font_size=30),
            cmath(r"v", r"\leftarrow", r"\text{regress } R^\lambda_t", font_size=30),
        ]
        whys = [why(r"the rewards dreamed, \ then the critic's guess"), why(r"Part 26's REINFORCE with a baseline; \ $S$: "
                                                                         r"the returns' range"),
                why(r"the critic learns the dreamed returns")]
        step = ladder(self, rows, whys, keep=3, top=0.4, x=-2.0, buff=0.5, edge=6.9)
        snap = d["snaps"][str(max(int(k) for k in d["snaps"]))]
        own = np.asarray(snap["own"])
        strip = Group(*[framed(gray(f_, 0.62, MODEL)) for f_ in own[:12]]).arrange(RIGHT, buff=0.06).move_to([0, 2.6, 0])
        sl = label(rf"what our trained agent dreams: \ ${len(own)}$ steps of its own play, \ never seen", font_size=20,
                   color=MODEL).next_to(strip, DOWN, buff=0.15)
        with self.voiceover(
            "Then the agent learns to act without touching the real game. <bookmark mark='a'/> From states the model "
            f"has seen, it dreams {int(P['horizon'])} steps ahead, choosing actions with the current policy, "
            "rewards predicted by the model. <bookmark mark='b'/> The return of each dream mixes the rewards it "
            "dreamed with a critic's estimate of what comes after, a lambda-return. The policy follows Part 26's "
            "REINFORCE, with the critic as baseline, scaled by the spread of the returns, plus a little entropy. "
            "<bookmark mark='c'/> The critic learns the dreamed returns. The real game is only used to collect more "
            "experience for the model."
        ) as vo:
            self.play(FadeIn(strip), FadeIn(sl))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("dreamer")
        snaps = d["snaps"]
        its = sorted(int(k) for k in snaps)
        S_ = 0.62
        rows = Group()
        real = np.asarray(snaps[str(its[0])]["real"])
        n = min(12, real.shape[0])
        rr = Group(*[framed(gray(f_, S_, WORLD)) for f_ in real[:n]]).arrange(RIGHT, buff=0.05)
        for it in its:
            dr = np.asarray(snaps[str(it)]["dream"])
            rows.add(Group(*[framed(gray(f_, S_, MODEL)) for f_ in dr[:n]]).arrange(RIGHT, buff=0.05))
        Group(rr, *rows).arrange(DOWN, buff=0.12).move_to([0.9, -0.2, 0])
        steps_per = int(d["params"]["steps_per_iter"])
        ll = VGroup(label(r"reality", font_size=20, color=WORLD).next_to(rr, LEFT, buff=0.25),
                    *[label(rf"after ${it * steps_per:,}$ updates".replace(",", "{,}"), font_size=18, color=MODEL)
                      .next_to(r_, LEFT, buff=0.25) for it, r_ in zip(its, rows)])
        head = label(r"the same $6$ real frames, \ then dreamed under the same actions", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.35)
        wrong = [float(((np.asarray(snaps[str(it)]["dream"])[:n] > 0.5) != (real[:n] > 0.5)).sum((1, 2)).mean())
                 for it in its]
        lit = float((real[:n] > 0.5).sum((1, 2)).mean())
        better = wrong[-1] < 0.5 * wrong[0]
        trend = (f"from {wrong[0]:.1f} wrong pixels a frame untrained to {wrong[-1]:.1f} after "
                 f"{its[-1] * steps_per:,} updates, in pictures with about {lit:.0f} lit pixels." if better else
                 f"but its dreams improve little: {wrong[0]:.1f} wrong pixels a frame at first, {wrong[-1]:.1f} at the end.")
        with self.voiceover(
            "Here is our Dreamer-lite learning the game of catch. At each checkpoint it watches the same six real "
            "frames, then dreams on, given the same actions as reality. <bookmark mark='a'/> Untrained, its dreams "
            "have nothing to do with the game. <bookmark mark='b'/> As it trains, the dreams come to match reality, "
            f"{trend} <bookmark mark='c'/> Errors still creep in the longer it dreams, as in chapter eleven, and "
            "a new ball, which appears at a random place, can never be dreamed exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rr), FadeIn(ll[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(ll[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_, shift=DOWN * 0.1), FadeIn(l_))
                                    for r_, l_ in zip(rows[1:], ll[2:])], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("c")
            box = SurroundingRectangle(rows[-1], color=MODEL, buff=0.06)
            self.play(Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("dreamer")
        C_ = np.asarray(d["curves"])  # (seeds, points, 3)
        steps = C_[0, :, 1]
        rates = C_[:, :, 2]
        rnd = float(d["random_catch"])
        g = axes([0, float(steps[-1]), 1000], [0, 1, 0.25], x_length=7.0, y_length=4.2,
                 xlabel=r"steps of real play \ (its experience)", ylabel=r"balls caught", xticks=[0, 2000, 4000, 6000][:1 + int(steps[-1] // 2000)],
                 xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), yticks=[0, 0.5, 1], yfmt=lambda v: f"{int(100 * v)}\\%",
                 center=[-2.3, -0.4, 0])
        ax = g.ax
        b = spread_band(ax, steps, rates, AGENT)
        rl = DashedLine(ax.c2p(0, rnd), ax.c2p(float(steps[-1]), rnd), color=GREY_B)
        rll = label(rf"random paddle: \ ${100 * rnd:.0f}\%$", font_size=20, color=GREY_B).next_to(ax.c2p(float(steps[-1]), rnd), UP, buff=0.1)
        rll.align_to(rl, RIGHT)
        fin = np.asarray(d["final"])
        balls = int(d["params"]["eval_eps"]) * 6
        tag = note(rf"computed: \ {len(fin)} seeds, \ band min--max; \ each point: \ its greedy play over "
                   rf"${balls}$ balls", font_size=17).to_edge(DOWN, buff=0.15)
        # its real play at the end: ball and paddle columns over one episode
        snap = d["snaps"][str(max(int(k) for k in d["snaps"]))]
        traj = np.asarray(snap["traj"])
        mini = axes([0, len(traj), 10], [0, 11, 5], x_length=4.2, y_length=2.4, xlabel=r"step", ylabel=r"column",
                    xticks=[0, 30, 60], yticks=[0, 11], font_size=16, center=[4.4, 1.3, 0])
        bx = curve(mini.ax, np.arange(len(traj)), traj[:, 0], WORLD, 2)
        px = curve(mini.ax, np.arange(len(traj)), traj[:, 2], AGENT, 3)
        ml = legend([(WORLD, r"the ball"), (AGENT, r"its paddle")], font_size=16).next_to(mini, DOWN, buff=0.2)
        lo, hi, mean = float(fin.min()), float(fin.max()), float(fin.mean())
        landed = [k for k in range(len(traj)) if traj[k, 1] == 11]
        caught = sum(1 for k in landed if traj[k, 2] - 2 <= min(traj[k, 0], 10) <= traj[k, 2] + 1)
        game = (f"the paddle heads for where each ball will land, and catches {caught} of {len(landed)}." if
                caught >= len(landed) - 1 else f"it catches {caught} of the {len(landed)} balls.")
        if mean > rnd + 0.3:
            v = (f"After about {int(steps[-1]):,} steps of real play, the {len(fin)} seeds catch {100 * lo:.0f} to "
                 f"{100 * hi:.0f} percent of the balls, against {100 * rnd:.0f} percent for a random paddle: the policy "
                 "was learned entirely in dreams.")
        elif mean > rnd + 0.1:
            v = (f"After about {int(steps[-1]):,} steps of real play, the seeds catch {100 * lo:.0f} to "
                 f"{100 * hi:.0f} percent of the balls, against {100 * rnd:.0f} percent for a random paddle: real "
                 "learning, though far from perfect.")
        else:
            v = (f"After about {int(steps[-1]):,} steps of real play, the seeds catch {100 * lo:.0f} to "
                 f"{100 * hi:.0f} percent, hardly better than the random paddle's {100 * rnd:.0f}: at this budget the "
                 "dream is not yet good enough to learn from.")
        with self.voiceover(
            "And the policy, trained only in those dreams, is tested in the real game. "
            f"<bookmark mark='a'/> {v} <bookmark mark='b'/> On the right, one of its real games at the end: "
            f"{game}"
        ) as vo:
            self.play(FadeIn(g), Create(rl), FadeIn(rll), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(b[0]), Create(b[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(mini), Create(bx), Create(px), FadeIn(ml), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
