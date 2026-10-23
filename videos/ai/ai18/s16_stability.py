from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (F, PART, STAB_C, STAB_NAME, load, spoken_int, take_away)


class Stability(VoiceoverScene):
    def construct(self):
        self.card()
        self.spikes()
        self.logits()
        self.sweep()
        self.zloss()
        self.muon()

    def card(self):
        card = chapter_card(15, r"Keeping the run stable", r"Why do big runs blow up, and what stops them?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter fifteen. Keeping the run stable."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def spikes(self):
        Pa = F.PALM
        g = axes([0, 100], [1.5, 4.5], x_length=9.0, y_length=3.2, xlabel=r"training step", ylabel=r"loss",
                 center=[0, 0.8, 0], font_size=18)
        xs = np.linspace(0, 100, 800)
        ys = 2.0 + 1.8 * np.exp(-xs / 18)
        for c in (38, 71):
            ys = ys + 1.3 * np.exp(-((xs - c) / 1.2) ** 2) * (xs > c - 3)
        cv = curve(g.ax, xs, ys, C.LOSS, 3)
        sch = note(r"schematic", font_size=18).next_to(g, UR, buff=0.0).shift(DOWN * 0.3 + LEFT * 0.4)
        facts = VGroup(
            label(rf"PaLM, $540$B: \ about ${Pa['spikes']}$ loss spikes, \ with gradient clipping on", font_size=22,
                  color=GREY_A),
            label(rf"the fix: \ restart about ${Pa['back']}$ steps earlier, \ skip ${Pa['skip'][0]}$--${Pa['skip'][1]}$ "
                  r"batches", font_size=22, color=GREY_A),
            label(r"not bad data: \ the same batches were fine from another point in training", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 2.2)
        src = cite(r"Chowdhery et al., PaLM (2022), Sec.\ 5.1", corner=DR, font_size=17)
        with self.voiceover(
            "Large runs have a failure that small ones rarely show: the loss suddenly jumps, and sometimes never comes "
            "back. <bookmark mark='a'/> Google's PaLM, at 540 billion parameters, spiked about twenty times, although "
            "its "
            "gradients were clipped. <bookmark mark='b'/> The fix was blunt: restart about a hundred steps before the "
            "spike, "
            "and skip the next two to five hundred batches. <bookmark mark='c'/> It wasn't bad data: the same batches "
            "were "
            "fine from another point in training. The trouble was the model's state, and today's models are built to "
            "keep it "
            "tame."
        ) as vo:
            self.play(FadeIn(g), Create(cv), FadeIn(sch), FadeIn(src), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logits(self):
        S = load("stability")
        runs = S["runs"]
        lr = S["lrs"][2]
        g = axes([0, S["steps"]], [0, 4], x_length=6.2, y_length=3.6, xlabel=r"step",
                 ylabel=r"largest attention logit $q \cdot k / \sqrt{d}$", xticks=[0, S["steps"]], yticks=[0, 1, 2, 3, 4],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-3.0, -0.4, 0], font_size=18)
        lines = VGroup()
        for cfg in ("plain", "qk"):
            for s in S["seeds"]:
                pr = np.asarray(runs[f"{cfg}_{lr:g}_{s}"]["probes"])
                lines.add(curve(g.ax, pr[:, 0], np.log10(np.maximum(pr[:, 1], 1)), STAB_C[cfg], 2.5))
        lg = legend([(STAB_C["plain"], r"plain attention"), (STAB_C["qk"], r"QK-norm")], font_size=18)
        lg.next_to(g.ax.c2p(0, 4), RIGHT, buff=0.3).shift(DOWN * 0.3)
        colors = {r"q": C.QUERY, r"k": C.KEY}
        rows = [
            cmath(r"\text{logit}", r"=", r"\frac{q \cdot k}{\sqrt{d}}", colors=colors, font_size=30),
            cmath(r"\text{QK-norm}", r":", r"q, k \leftarrow \mathrm{RMSNorm}(q), \mathrm{RMSNorm}(k)", colors=colors,
                  font_size=26),
            cmath(r"|\text{logit}|", r"\le", r"\gamma_q\,\gamma_k\,\sqrt{d}", colors=colors, font_size=30),
        ]
        whys = [why(r"grows with the weights", font_size=19), why(r"Dehghani et al.\ (2023)", font_size=19),
                why(r"Cauchy--Schwarz; \ only the gains can grow", font_size=19)]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=3.0, buff=0.5, edge=6.9)
        mx = S["maxlogit"]
        i = S["lrs"].index(lr)
        pl, qk = max(mx["plain"][i]), max(mx["qk"][i])
        tag = note(rf"computed: \ learning rate ${lr:g}$, \ two seeds each", font_size=18).to_corner(DR, buff=0.2)
        # what huge logits do to a softmax: the same eight logits, as they are and twenty times larger
        z = np.array([1.0, 0.5, 0.2, -0.3, 0.8, 0.1, -0.5, 0.3])

        def soft_bars(t, x0, col, name):
            p_ = np.exp(t - t.max())
            p_ = p_ / p_.sum()
            bs = VGroup(*[Rectangle(width=0.22, height=max(1.5 * v, 0.02), stroke_width=0, fill_color=col,
                                    fill_opacity=0.85).move_to([x0 + 0.28 * i, -2.3 + 0.75 * v, 0])
                          for i, v in enumerate(p_)])
            base_ = Line([x0 - 0.2, -2.3, 0], [x0 + 0.28 * 7 + 0.2, -2.3, 0], color=GREY_D, stroke_width=1.5)
            return VGroup(base_, bs, label(name, font_size=19, color=col).next_to(base_, DOWN, buff=0.12))

        sm = VGroup(soft_bars(z, 1.0, STAB_C["qk"], r"logits $z$"), soft_bars(20 * z, 4.3, STAB_C["plain"],
                                                                           r"logits $20z$"))
        sm_t = label(r"softmax of the same logits \ (illustrative)", font_size=19, color=GREY_A)
        sm_t.next_to(sm, UP, buff=0.2)
        with self.voiceover(
            "One state that goes wrong is attention itself. A query and a key give a logit, their dot product over the "
            "square root of the dimension, and nothing stops the weights from growing until the logits are huge. "
            "<bookmark mark='a'/> Then the softmax puts all its weight on one position, its gradients vanish, and "
            "training "
            "can lock up. Wortsman and colleagues reproduced this in small models by raising the learning rate; so "
            "did we. "
            f"<bookmark mark='b'/> At a learning rate of {lr:g}, our plain model's largest attention logit reaches "
            f"{pl:,.0f}. "
            "<bookmark mark='c'/> The fix, used in ViT-22B, Olmo 2, Qwen3 and GLM-4.5, is QK-norm: normalize every "
            "query and "
            "key before the dot product, <bookmark mark='d'/> and the logit is bounded by the norms' learned gains "
            "times the "
            f"square root of the dimension. With it, our largest logit stays at {qk:.0f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            step(0)
            self.play(FadeIn(lg[0]), *[Create(l_) for l_ in lines[:len(S["seeds"])]], run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(sm_t), FadeIn(sm[0]))
            self.play(FadeIn(sm[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(Indicate(lines[0], color=YELLOW))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(sm, sm_t)))  # the ladder needs the room
            step(1)
            vo.wait_until("d")
            step(2)
            self.play(FadeIn(lg[1]), *[Create(l_) for l_ in lines[len(S["seeds"]):]], run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        S = load("stability")
        lrs = S["lrs"]
        fin = S["final"]
        allv = [v for c in fin for row in fin[c] for v in row]
        lo, hi = math.floor(min(allv) * 4) / 4, math.ceil(max(allv) * 4) / 4
        g = axes([math.log10(lrs[0]) - 0.15, math.log10(lrs[-1]) + 0.15], [lo, hi], x_length=7.0, y_length=4.0,
                 xlabel=r"learning rate", ylabel=rf"final held-out loss, \ ${S['steps']}$ steps",
                 xticks=[math.log10(x) for x in lrs], yticks=[lo, hi],
                 xfmt=lambda v: f"{10 ** v:.3g}", yfmt=lambda v: f"{v:.2f}", center=[-1.6, -0.3, 0], font_size=18)
        marks = VGroup()
        for cfg in S["configs"]:
            pts = VGroup()
            means = []
            for i, lr in enumerate(lrs):
                vals = fin[cfg][i]
                x = math.log10(lr) + {"plain": -0.04, "qk": 0.0, "qkz": 0.04}[cfg]
                for v in vals:
                    pts.add(Dot(g.ax.c2p(x, v), radius=0.05, color=STAB_C[cfg]))
                means.append((x, float(np.mean(vals))))
            ln = VMobject(color=STAB_C[cfg], stroke_width=2.5).set_points_as_corners([g.ax.c2p(a, b) for a, b in means])
            marks.add(VGroup(ln, pts))
        lg = legend([(STAB_C[c], STAB_NAME[c]) for c in S["configs"]], font_size=20).move_to([4.6, 1.2, 0])
        # every run's training, small: held-out loss against step, all learning rates, designs and seeds
        evs = {k: np.asarray(r["evals"]) for k, r in S["runs"].items()}
        etop = min(8.6, max(e[:, 2].max() for e in evs.values()))
        ebot = math.floor(min(e[:, 2].min() for e in evs.values()) * 2) / 2
        gr = axes([0, S["steps"]], [ebot, etop], x_length=3.0, y_length=1.9, xlabel=r"step", ylabel=r"held-out loss",
                  xticks=[0, S["steps"]], yticks=[ebot, round(etop, 1)], yfmt=lambda v: f"{v:.1f}",
                  center=[4.9, -1.7, 0], font_size=15)
        runs_ = VGroup(*[curve(gr.ax, e[:, 0], np.minimum(e[:, 2], etop), STAB_C[k.split("_")[0]], 1.3)
                         .set_stroke(opacity=0.6) for k, e in evs.items()])
        rn = note(rf"all ${len(evs)}$ runs, \ training", font_size=15).next_to(gr, DOWN, buff=0.05)
        hi_lr = len(lrs) - 1
        pl, qk = np.mean(fin["plain"][hi_lr]), np.mean(fin["qk"][hi_lr])
        lo_lr = 0
        pl0, qk0 = np.mean(fin["plain"][lo_lr]), np.mean(fin["qk"][lo_lr])
        best_plain = min(range(len(lrs)), key=lambda i: np.mean(fin["plain"][i]))
        best_qk = min(range(len(lrs)), key=lambda i: np.mean(fin["qk"][i]))
        sp = max(abs(fin[c][hi_lr][0] - fin[c][hi_lr][1]) for c in ("plain", "qk"))
        ratio = float(np.mean(S["maxlogit"]["plain"][hi_lr]) / np.mean(S["maxlogit"]["qk"][hi_lr]))
        if pl - qk > max(sp, 0.02):
            verdict = (f"At the highest learning rate, {lrs[hi_lr]:g}, the plain model ends at {pl:.2f} nats and the "
                       f"one with QK-norm at {qk:.2f}, a gap larger than the {sp:.2f} between seeds: normalizing "
                       "queries and keys widens the range of learning rates that train well.")
        elif qk - pl > max(sp, 0.02):
            verdict = (f"At the highest learning rate, {lrs[hi_lr]:g}, the plain model ends at {pl:.2f} nats and the "
                       f"one with QK-norm at {qk:.2f}, a gap larger than the {sp:.2f} between seeds: in runs this "
                       "short, QK-norm cost a little.")
        else:
            verdict = (f"At the highest learning rate, {lrs[hi_lr]:g}, the plain model ends at {pl:.2f} nats and the "
                       f"one with QK-norm at {qk:.2f}, but two seeds of one design differ by up to {sp:.2f}: in runs "
                       "this short the loss can't tell them apart, although the plain model's largest attention logit "
                       f"is {ratio:.0f} times larger.")
        best = (f"The best learning rate is {lrs[best_plain]:g} without QK-norm and {lrs[best_qk]:g} with it."
                if best_plain != best_qk else f"Both do best at a learning rate of {lrs[best_qk]:g}.")
        tag = note(rf"computed: \ ${len(lrs)}$ learning rates $\times$ $3$ designs $\times$ $2$ seeds", font_size=18)
        tag.to_corner(DR, buff=0.2)
        src = cite(r"after Wortsman et al., \textit{Small-scale proxies for large-scale instabilities} (ICLR 2024)",
                   corner=DL, font_size=17)
        with self.voiceover(
            "Wortsman's test of a fix is a sweep: train at many learning rates and see how far up the loss stays "
            f"good. Here is ours: {len(lrs)} learning rates, plain, with QK-norm, and with QK-norm and the z-loss we "
            "will see next, two seeds each. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> " + best
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(src))
            self.play(FadeIn(gr), FadeIn(rn), LaggedStart(*[Create(c_) for c_ in runs_], lag_ratio=0.04), run_time=2.5)
            self.play(LaggedStart(*[Create(m_[0]) for m_ in marks], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(m_[1]) for m_ in marks], lag_ratio=0.3), FadeIn(lg), run_time=3.0)
            vo.wait_until("a")
            self.play(*[Indicate(m_[1], color=YELLOW, scale_factor=1.1) for m_ in marks[:2]])
            vo.wait_until("b")
            self.play(Indicate(lg, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zloss(self):
        S = load("stability")
        runs = S["runs"]
        lr = S["lrs"][0]
        colors = {r"z": C.PROB, r"Z": C.LOSS}
        rows = [
            cmath(r"\mathrm{softmax}(z + c)", r"=", r"\mathrm{softmax}(z)", colors=colors, font_size=30),
            cmath(r"\log Z", r"=", r"\log \sum_j e^{z_j}", colors=colors, font_size=30),
            cmath(r"L", r"=", r"L_{\text{CE}} + 10^{-4}\,(\log Z)^2", colors=colors, font_size=30),
            cmath(r"\frac{\partial}{\partial z_i}", r"=", r"\ldots + 2 \cdot 10^{-4} \log Z \cdot \mathrm{softmax}_i(z)",
                  colors=colors, font_size=28),
        ]
        whys = [why(r"a shift of every logit changes nothing", font_size=19), why(r"so this can drift anywhere",
                                                                                 font_size=19),
                why(r"PaLM's z-loss: \ pull it to $0$", font_size=19), why(r"a gentle push on all logits at once",
                                                                          font_size=19)]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-3.4, buff=0.38, edge=6.9)
        g = axes([0, S["steps"]], [-2, 12], x_length=5.0, y_length=2.4, xlabel=r"step", ylabel=r"mean $\log Z$",
                 xticks=[0, S["steps"]], yticks=[0, 5, 10], center=[3.3, -2.0, 0], font_size=17)
        lines = VGroup()
        ends = {}
        for cfg in ("qk", "qkz"):
            for s in S["seeds"]:
                pr = np.asarray(runs[f"{cfg}_{lr:g}_{s}"]["probes"])
                lines.add(curve(g.ax, pr[:, 0], np.clip(pr[:, 3], -2, 12), STAB_C[cfg], 2.5))
                ends.setdefault(cfg, []).append(float(pr[-1, 3]))
        lg = legend([(STAB_C["qk"], r"without z-loss"), (STAB_C["qkz"], r"with z-loss")], font_size=17)
        lg.move_to(g.ax.c2p(S["steps"] * 0.5, 11.0), aligned_edge=UP)
        a, b = np.mean(ends["qk"]), np.mean(ends["qkz"])
        spread_z = max(abs(v[0] - v[1]) for v in ends.values())
        if a - b > max(spread_z, 0.3):
            zl = f"In our runs, log Z ends at {a:.1f} without it and {b:.2f} with it."
        elif abs(a - b) <= spread_z:
            zl = (f"In our short runs it changes nothing we can measure: log Z ends near {a:.1f} either way. It is "
                  "meant for long runs, where the logits have time to drift.")
        else:
            zl = (f"In our short runs it barely moves log Z: {a:.2f} without it, {b:.2f} with it. The penalty is tiny "
                  "next to the loss; it is there for long runs, where the logits have time to drift.")
        tag = note(rf"computed: \ learning rate ${lr:g}$", font_size=18).to_corner(DR, buff=0.15)
        with self.voiceover(
            "The second fix is for the output layer. A softmax doesn't change if every logit shifts by the same "
            "amount. <bookmark mark='a'/> So their log-sum-exp, log Z, is free to drift, and in sixteen-bit "
            "arithmetic large logits lose their precision. <bookmark mark='b'/> PaLM added a tiny penalty, ten to "
            "the minus four times log Z squared: the z-loss. <bookmark mark='c'/> Its gradient nudges all the "
            "logits together toward a normalizer of one, without changing what the model predicts. "
            "<bookmark mark='d'/> " + zl
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(FadeIn(g), FadeIn(lg[0]), FadeIn(tag),
                      LaggedStart(*[Create(l_) for l_ in lines[:len(S["seeds"])]], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(lg[1]), LaggedStart(*[Create(l_) for l_ in lines[len(S["seeds"]):]], lag_ratio=0.2),
                      run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def muon(self):
        K, V4, M = F.KIMIK2, F.DSV4, F.MOONLIGHT
        rows = VGroup(
            label(r"Muon at scale", font_size=30, color=C.MUON),
            label(rf"Moonlight (2025): \ about ${M['efficiency']:.0f}\times$ the compute efficiency of AdamW, \ in "
                  r"scaling-law fits", font_size=22, color=GREY_A),
            label(r"but with Muon, attention logits grew faster, \ and MLA has no keys to normalize", font_size=22,
                  color=GREY_A),
            label(rf"Kimi K2's QK-Clip: \ if a head's largest logit passes $\tau = {K['tau']}$, \ shrink its $W_q$, $W_k$",
                  font_size=22, color=C.MUON),
            label(rf"${K['heads_clipped']}\%$ of heads clipped early on; \ none after ${K['clip_steps']:,}$ steps; \ "
                  rf"${K['tokens'] / 1e12:.1f}$T tokens, \ no loss spike".replace(",", "{,}"), font_size=22,
                  color=GREY_A),
            label(r"DeepSeek-V4 (2026): \ Muon, \ RMSNorm on queries and keys instead; \ spikes traced to "
                  r"outliers in the experts", font_size=22, color=GREY_A),
            label(r"\ \ fixed by routing with slightly older weights while a spike lasts, \ and clamping SwiGLU",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        if rows.width > 13.2:
            rows.width = 13.2
        rows.to_edge(UP, buff=0.35)
        tau = K["tau"]
        gq = axes([0, 1], [0, 2.2 * tau], x_length=6.4, y_length=1.9, xlabel=r"training", ylabel=r"a head's largest logit",
                  xticks=[], yticks=[0, tau], yfmt=lambda v: rf"\tau = {tau}" if v else "0", center=[-1.6, -2.45, 0],
                  font_size=17)
        xs_ = np.linspace(0, 1, 120)
        free = np.minimum(2.15 * tau, 0.35 * tau + 2.4 * tau * xs_ ** 0.7)  # schematic: keeps growing
        rise = 0.35 * tau + 2.4 * tau * xs_ ** 0.7
        capped = np.where(xs_ < 0.45, np.minimum(rise, tau), tau - 0.25 * tau * np.tanh((xs_ - 0.45) * 4))
        fc = DashedVMobject(curve(gq.ax, xs_, free, GREY_B, 2.5), num_dashes=40)
        cc = curve(gq.ax, xs_, capped, C.MUON, 3)
        tl_ = DashedLine(gq.ax.c2p(0, tau), gq.ax.c2p(1, tau), color=C.MUON, dash_length=0.05, stroke_width=1.5)
        qlg = legend([(GREY_B, r"without the clip"), (C.MUON, r"with QK-Clip")], font_size=18)
        qlg.next_to(gq, RIGHT, buff=0.4).align_to(gq, UP)
        qsch = note(r"schematic, \ after Kimi Team (2025)", font_size=17).next_to(qlg, DOWN, buff=0.2).align_to(qlg, LEFT)
        src = cite(r"Liu et al.\ (2025); \ Kimi Team (2025), Sec.\ 2.1; \ DeepSeek-AI (2026), Secs.\ 2.4, 4.2.3",
                   corner=DR, font_size=16)
        with self.voiceover(
            "The newest source of trouble is the optimizer. Part 11's Muon went to scale in 2025: Moonshot's "
            "Moonlight study "
            "found it about twice as compute-efficient as AdamW. <bookmark mark='a'/> But with Muon the attention "
            "logits grew "
            "faster, and Kimi K2's latent attention never forms its keys in full, so QK-norm can't be applied. "
            "<bookmark mark='b'/> Moonshot's fix, QK-Clip: after each update, if a head's largest logit has passed a "
            "hundred, "
            "shrink that head's query and key weights. It clipped 12.7 percent of the heads early on and none after "
            "seventy "
            "thousand steps, and K2 trained on 15.5 trillion tokens without a loss spike. <bookmark mark='c'/> "
            "DeepSeek-V4 also "
            "uses Muon, normalizes its queries and keys, and tames the rare spikes from its experts by clamping "
            "SwiGLU and "
            "routing with slightly older weights."
        ) as vo:
            self.play(FadeIn(rows[:2]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(gq), FadeIn(qlg[0]), FadeIn(qsch), Create(fc), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), Create(tl_))
            self.play(FadeIn(qlg[1]), Create(cc), run_time=2.0)
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5]), FadeIn(rows[6]))
        self.wait(0.3)
        self.clear_scene()
