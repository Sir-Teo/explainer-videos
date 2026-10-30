from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, lag, load, takeaway_card

SLOW, FAST, CLIP, GCL = OPT_COLORS["muon"], C.SURPRISE, C.BITS, "#7FD3FF"
WD_COLS = ["#7FD3FF", C.BITS, C.SURPRISE]


class Stability(VoiceoverScene):
    def construct(self):
        self.card()
        self.logits()
        self.qkclip()
        self.adam_clip()
        self.equilibrium()
        self.measured()
        self.takeaway()

    def card(self):
        c = chapter_card(15, r"Keeping training stable", r"What blows up, \ and what holds it?", part=PART)
        with self.voiceover("Chapter fifteen. Keeping training stable."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def logits(self):
        s = load("spikes")
        logs = {k: np.asarray(s[f"log_{k}"]) for k in s["names"]}  # seed x row x (step, loss, max score)
        T = float(logs["muon_slow"][0, -1, 0])
        ax = CornerAxes(x_range=[0, T, 500], y_range=[0, 5, 1], x_length=6.6, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.8, -0.5, 0])
        xt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=18, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in np.arange(0, T + 1, 500)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08) for k in range(6)])
        xn = label(r"training steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"the largest attention score, \ $\max_{i,j} q_i \cdot k_j / \sqrt{d}$", font_size=20, color=GREY_A)
        yn.next_to(ax, UP, buff=0.12).align_to(ax, LEFT)

        def line(k, col, sd=0, sw=3):
            L = logs[k][sd]
            return curve(ax, L[:, 0], np.log10(np.clip(L[:, 2], 1, 1e5)), col, sw)

        slow = line("muon_slow", SLOW)
        fast = line("muon_fast", FAST)
        cfg = s["cfgs"]
        lr_s, lr_f = cfg["muon_slow"]["lr"], cfg["muon_fast"]["lr"]
        lg = VGroup(label(rf"Muon, \ $\eta = {lr_s:g}$", font_size=22, color=SLOW), label(rf"Muon, \ $\eta = {lr_f:g}$",
                                                                                         font_size=22, color=FAST))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.2, 1.9, 0])
        model = label(r"a one-layer transformer on Part 1's books: \\ $32$ characters of context, \ $2$ heads, \ no "
                      r"normalization of $q$ or $k$", font_size=20, color=GREY_A).move_to([4.2, 0.6, 0])
        keep_in_frame(model)
        mx_s, mx_f = (float(np.mean(s[f"maxlogit_{k}"])) for k in ("muon_slow", "muon_fast"))
        hs, hf = (float(np.mean(s[f"held_{k}"])) for k in ("muon_slow", "muon_fast"))
        res = label(rf"held-out bits: \ ${hs:.2f}$ \ against \ ${hf:.2f}$", font_size=22, color=WHITE).next_to(model, DOWN, buff=0.4)
        cite_ = cite(r"Part 18: \ loss spikes and logit growth at scale", corner=DR)
        said1 = (f"<bookmark mark='c'/> The faster run ends worse, {hf:.2f} bits against {hs:.2f}."
            if hf > hs else
            f"<bookmark mark='c'/> Here the faster run still ends at {hf:.2f} bits, against {hs:.2f}.")
        with self.voiceover(
            "Large runs sometimes blow up: the loss jumps, and training must be rolled back. Part eighteen "
            "tells that story at scale. Here is one mechanism, provoked on purpose, in a one-layer transformer on "
            "our books, the kind part thirteen builds. <bookmark mark='a'/> Watch the largest attention score, a "
            "query times a key. With Muon at a moderate rate it grows "
            f"to about {mx_s:,.0f}. <bookmark mark='b'/> At four times the rate it runs away, to about {mx_f:,.0f}: "
            "the softmax becomes a hard choice, its gradients vanish, and the heads stop learning. "
            + said1
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(model), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(slow), FadeIn(lg[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(fast), FadeIn(lg[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def qkclip(self):
        s = load("spikes")
        s["cfgs"]
        head = label(r"QK-clip, \ per head $h$, \ after every step", font_size=30).to_edge(UP, buff=0.3)
        cl = {r"\gamma": CLIP, r"\tau": CLIP}
        rows = [
            cmath(r"S^h", "=", r"\max_{i,j}\; \frac{(W_q^h x_i) \cdot (W_k^h x_j)}{\sqrt{d}}", font_size=34),
            cmath(r"W_q^h \to \sqrt{\gamma}\, W_q^h,\ W_k^h \to \sqrt{\gamma}\, W_k^h", r"\;\Rightarrow\;", r"S^h \to \gamma\, S^h",
                  font_size=34, colors=cl),
            cmath(r"\gamma", "=", r"\tau / S^h \quad \text{whenever } S^h > \tau", font_size=34, colors=cl),
        ]
        whys = [why(r"bilinear in the two weight matrices"), why(r"scale both by $\sqrt\gamma$"),
                why(r"so the score lands exactly on $\tau$")]
        step = ladder(self, rows, whys, keep=3, top=2.1, x=-1.4, buff=0.55, edge=6.9)
        hist = history_card(2025, r"Kimi Team \ (Moonshot AI)", rf"MuonClip: \ Muon plus QK-clip, \ $\tau = 100$. \ Kimi K2, "
                            r"\ a trillion parameters, \ trained on $15.5$ trillion tokens \ ``with zero loss spike''",
                            width=7.0).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2025 Moonshot AI met exactly this while training Kimi K2 with Muon, and fixed it surgically. "
            "<bookmark mark='a'/> After each step, measure each head's largest score. <bookmark mark='b'/> The score "
            "is bilinear in the head's query and key weights, so scaling both by the square root of gamma scales the "
            "score by gamma. <bookmark mark='c'/> Whenever it exceeds a threshold tau, choose gamma to put it exactly "
            "on tau. Nothing else changes. With tau at a hundred, Kimi K2, a model with a trillion parameters, "
            "trained on fifteen and a half trillion tokens, its report says with zero loss spikes."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k)
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def adam_clip(self):
        s = load("spikes")
        logs = {k: np.asarray(s[f"log_{k}"]) for k in s["names"]}
        cfg = s["cfgs"]
        T = float(logs["muon_slow"][0, -1, 0])
        ax = CornerAxes(x_range=[0, T, 500], y_range=[0, 5, 1], x_length=6.0, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.2, 0.3, 0])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08) for k in range(0, 6, 1)])
        yn = label(r"the largest attention score", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xn = label(r"steps", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.1)

        def line(k, col, sd=0, sw=3):
            L = logs[k][sd]
            return curve(ax, L[:, 0], np.log10(np.clip(L[:, 2], 1, 1e5)), col, sw)

        lines = VGroup(line("muon_fast", FAST), line("muon_fast_qkclip", CLIP), line("adam_fast", "#FF9F45"),
                       line("adam_fast_gclip", GCL), line("adam_fast_qkclip", "#C792EA"))
        names = [("muon_slow", rf"Muon, \ $\eta = {cfg['muon_slow']['lr']:g}$", SLOW),
                 ("muon_fast", rf"Muon, \ $\eta = {cfg['muon_fast']['lr']:g}$", FAST),
                 ("muon_fast_qkclip", r"\dots \ with QK-clip", CLIP),
                 ("adam_fast", rf"AdamW, \ $\eta = {cfg['adam_fast']['lr']:g}$", "#FF9F45"),
                 ("adam_fast_gclip", r"\dots \ with gradient clipping", GCL),
                 ("adam_fast_qkclip", r"\dots \ with QK-clip", "#C792EA")]
        tab = VGroup(label(r"held-out bits, \ seed $0$ \ / \ seed $1$", font_size=20, color=GREY_A))
        for k, nm, col in names:
            h = s[f"held_{k}"]
            tab.add(label(rf"{nm}: \ ${h[0]:.2f}$ \ / \ ${h[1]:.2f}$", font_size=20, color=col))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.7, 0.5, 0])
        keep_in_frame(tab)
        clip_eq = cmath(r"g \;\leftarrow\; g \cdot \min\!\Big(1, \frac{c}{\|g\|}\Big)", font_size=32).move_to([-3.2, -2.6, 0])
        cl_ = label(r"gradient clipping \ (Pascanu, Mikolov \& Bengio, 2013)", font_size=20, color=GCL).next_to(clip_eq, DOWN, buff=0.12)
        hq = s["held_muon_fast_qkclip"]
        hf = s["held_muon_fast"]
        q_ok = all(a < b for a, b in zip(hq, hf))
        ha, hg, haq = s["held_adam_fast"], s["held_adam_fast_gclip"], s["held_adam_fast_qkclip"]
        g_both = all(a < b for a, b in zip(hg, ha))
        g_one = sum(a < b - 0.05 for a, b in zip(hg, ha)) == 1
        mxq = max(s["maxlogit_muon_fast_qkclip"])
        said2 = (f"and it ends at {hq[0]:.2f} and {hq[1]:.2f} bits for the two seeds, against {hf[0]:.2f} and "
            f"{hf[1]:.2f} without it. "
            if q_ok else
            f"but its loss is not better on both seeds: {hq[0]:.2f} and {hq[1]:.2f} against {hf[0]:.2f} and {hf[1]:.2f}. ")
        said3 = (f"<bookmark mark='b'/> It rescues both seeds here, {hg[0]:.2f} and {hg[1]:.2f} bits against "
            f"{ha[0]:.2f} and {ha[1]:.2f}. "
            if g_both else
            (f"<bookmark mark='b'/> It rescues one seed, at {min(hg):.2f} bits, but not the other, at {max(hg):.2f}: "
            "clipping limits each step, not the slow drift that sends the scores up. "
            if g_one else
            f"<bookmark mark='b'/> Here it doesn't save the run: {hg[0]:.2f} and {hg[1]:.2f} bits. "))
        with self.voiceover(
            f"On our small transformer, QK-clip at tau a hundred holds the fast Muon run's scores near the threshold, "
            f"never above about {mxq:.0f}, "
            + said2
            + "<bookmark mark='a'/> AdamW, run far too fast, blows its scores up even further. The oldest remedy is "
            "gradient clipping, from 2013: whenever the gradient is longer than some c, shrink it to length c. "
            + said3
            + f"QK-clip, which targets the cause, gives {haq[0]:.2f} and {haq[1]:.2f}."
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(yn), FadeIn(xn), FadeIn(tab[0]), FadeIn(tab[1:4]))
            self.play(Create(lines[0]), Create(lines[1]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(lines[2]), FadeIn(tab[4]), Write(clip_eq), FadeIn(cl_))
            vo.wait_until("b")
            self.play(Create(lines[3]), Create(lines[4]), FadeIn(tab[5:]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def equilibrium(self):
        head = label(r"a matrix followed by a normalization: \ $W$ and $2W$ give the same network", font_size=28).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"\nabla_W L \cdot W", "=", r"0", font_size=34),
            cmath(r"W_{t+1}", "=", r"(1 - \eta\lambda)\, W_t - \eta\, u_t", font_size=34),
            cmath(r"\mathbb{E}\|W_{t+1}\|^2", r"\approx", r"(1 - 2\eta\lambda)\,\|W_t\|^2 + \eta^2\, \textstyle\sum_k \langle u_t, u_{t+k}\rangle",
                  font_size=32),
            cmath(r"\|W\|^2", r"\approx", r"\frac{\eta}{2\lambda}\,\|u\|^2\, \frac{1 + \beta_1}{1 - \beta_1}", font_size=36,
                  colors={r"\frac{\eta}{2\lambda}\,\|u\|^2\, \frac{1 + \beta_1}{1 - \beta_1}": C.BITS}),
        ]
        whys = [why(r"scale-invariant: \ the gradient is orthogonal to $W$"), why(r"decoupled decay, \ then Adam's step $u$"),
                why(r"$u$ nearly orthogonal to $W$; \ momentum correlates the $u$s"),
                why(r"balance: \ the decay removes what the steps add")]
        step = ladder(self, rows, whys, keep=4, top=2.3, x=-1.6, buff=0.45, edge=6.9)
        tl = label(r"reached in about $1/(2\eta\lambda)$ steps; \ then $\|W\| \propto \sqrt{\eta/\lambda}$", font_size=24,
                   color=C.BITS).to_edge(DOWN, buff=0.4)
        cite_ = cite(r"T.~van Laarhoven (2017); \ A.~Kosson, B.~Messmer \& M.~Jaggi, \textit{Rotational Equilibrium} (2024)",
                     corner=DL)
        with self.voiceover(
            "Weight decay has a second life in modern networks. Most weight matrices are followed by a "
            "normalization, which makes them scale-invariant: W and twice W give the same network. "
            "<bookmark mark='a'/> Then the gradient is orthogonal to W, so a step can never shrink it. "
            "<bookmark mark='b'/> Decay shrinks W by a factor; Adam's step u adds to it. <bookmark mark='c'/> Square "
            "the norm: the decay removes two eta lambda of it per step, and the steps add eta squared times u's size, "
            "times how strongly successive steps are correlated, which momentum sets. <bookmark mark='d'/> They "
            "balance at an equilibrium norm, proportional to the square root of eta over lambda. "
            "<bookmark mark='e'/> So weight decay doesn't regularize these weights at all: it sets the size at which "
            "each step is a fixed fraction of the matrix, an effective learning rate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("e")
            self.play(FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        e = load("equilibrium")
        wds = list(e["wd"])
        steps = int(e["steps"])
        top = max(max(np.asarray(e[f"track_{w}"])[:, 1].max(), e[f"pred_{w}"]) for w in wds) * 1.12
        ax = CornerAxes(x_range=[0, steps, 1000], y_range=[0, top, 10], x_length=6.8, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.6, -0.4, 0])
        xt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=18, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in range(0, steps + 1, 1000)])
        yt = VGroup(*[MathTex(f"{v:.0f}", font_size=18, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in np.arange(0, top, 10)])
        xn = label(r"AdamW steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"$\|W\|$, \ the normalized hidden matrix of our character model", font_size=20, color=GREY_A)
        yn.next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        groups, rows = VGroup(), VGroup()
        for w, col in zip(wds, WD_COLS):
            T = np.asarray(e[f"track_{w}"])
            p = float(e[f"pred_{w}"])
            groups.add(VGroup(curve(ax, T[:, 0], T[:, 1], col, 3),
                              DashedLine(ax.c2p(0, p), ax.c2p(steps, p), color=col, stroke_width=2)))
            rows.add(label(rf"$\lambda = {w:g}$: \ ${e[f'norm_{w}']:.1f}$ \ (predicted ${p:.1f}$)", font_size=22, color=col))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.4, 1.3, 0])
        sl = float(e["slope"])
        sll = label(rf"$\|W\| \propto \lambda^{{{sl:.2f}}}$ \ (derived: \ $\lambda^{{-0.5}}$)", font_size=24, color=C.BITS)
        sll.next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        dl = label(r"dashed: \ the equilibrium predicted from \\ the measured size of Adam's steps", font_size=20, color=GREY_A)
        dl.next_to(sll, DOWN, buff=0.3).align_to(rows, LEFT)
        tag = note(rf"$\eta = {float(e['lr']):g}$, \ constant; \ $\beta_1 = 0.9$; \ computed").to_corner(DL, buff=0.2)
        errs = [abs(e[f"norm_{w}"] / e[f"pred_{w}"] - 1) for w in wds]
        worst = max(errs)
        nomom = float(e[f"pred_nomom_{wds[0]}"])
        said4 = (f"<bookmark mark='b'/> The dashed lines are the predicted equilibria, and every measured norm is "
            f"within {worst:.0%} of its prediction. "
            if worst < 0.25 else
            f"<bookmark mark='b'/> The dashed lines are the predicted equilibria; the worst is off by {worst:.0%}. ")
        with self.voiceover(
            "Measure it on our character model, with a normalization added after its second hidden matrix, and "
            "three decay strengths, each four times the last. <bookmark mark='a'/> Each norm rises or falls to a "
            "level, and stays there, faster for stronger decay. "
            + said4
            + f"Without the momentum factor the prediction would be {nomom:.1f} for the first, far too small. "
            f"<bookmark mark='c'/> And four times the decay halves the norm: the fitted power is {sl:.2f}, against "
            "minus a half derived."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[Create(g_[0]) for g_ in groups], run_time=2.5)
            vo.wait_until("b")
            self.play(*[Create(g_[1]) for g_ in groups], lag([FadeIn(r_) for r_ in rows], lag_ratio=0.3), FadeIn(dl))
            vo.wait_until("c")
            self.play(FadeIn(sll))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Find the cause, \ then clip it",
                          r"Runaway attention scores are bilinear in $W_q, W_k$: \ QK-clip rescales just those. \ "
                          r"Gradient clipping caps each step. \ Weight decay sets the norm, \ $\|W\| \propto \sqrt{\eta/\lambda}$.",
                          r"Next: \ the optimizer race of 2024--2026")
        with self.voiceover(
            "So instability has causes, and the best fixes target them: QK-clip rescales just the two matrices that "
            "make a score, clipping caps every step, and weight decay quietly sets the size of every normalized "
            "matrix. Finally: what the field has learned about all this since 2024."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
