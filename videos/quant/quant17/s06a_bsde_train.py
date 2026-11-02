from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import deep as D
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, house_lab, illustration, load


class BSDETrain(VoiceoverScene):
    def construct(self):
        b = load("bsde")
        s = load("bsde_seeds")
        self.card()
        self.replay(b, s)
        self.result(b, s)
        self.linear(b, s)
        self.lab(b)
        self.why_it_scales(b)

    def card(self):
        c = chapter_card(9, r"Watching the deep BSDE converge", r"How sure is the answer, and why does it scale?",
                         part=PART)
        with self.voiceover("Chapter nine. Watching the deep BSDE converge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def replay(self, b, s):
        c0 = [c for c in b["curve"] if c["iter"] <= 2000]
        c1 = s["seed1"]["curve"]
        it = np.array([c["iter"] for c in c1], float)
        L = np.array([[c["u0"] for c in c1], [np.interp(i, [c["iter"] for c in c0], [c["u0"] for c in c0]) for i in it]])
        sn = s["seed1"]["snaps"]
        its = ["0", "100", "300", "1000", "2000"]
        allv = np.concatenate([np.r_[np.asarray(sn[i]["Y"]), np.asarray(sn[i]["g"])] for i in its])
        lo, hi = float(np.percentile(allv, 1)), float(np.percentile(allv, 99))

        def frame(i):
            g = axes([lo, hi], [lo, hi], x_length=3.9, y_length=3.9, xlabel=r"payoff $\min_i X^i_T$",
                     ylabel=r"$Y_N$", xticks=[round(lo), round(hi)], yticks=[round(lo), round(hi)], font_size=13)
            Y, gg = np.asarray(sn[its[i]]["Y"]), np.asarray(sn[its[i]]["g"])
            dots = VGroup(*[Dot(g.ax.c2p(np.clip(a, lo, hi), np.clip(y, lo, hi)), radius=0.025, color=NET)
                            for a, y in zip(gg, Y)])
            diag = DashedLine(g.ax.c2p(lo, lo), g.ax.c2p(hi, hi), stroke_color=WHITE, stroke_width=1.5)
            return VGroup(g, diag, dots, label(rf"step {its[i]}: where 256 paths land", font_size=17,
                                               color=GREY_A).next_to(g, DOWN, buff=0.12))
        rp = TrainingReplay(it, L, frame, checkpoints=[0, 100, 300, 1000, 2000], ylabel=r"today's price $u_0$")
        ref = DashedLine(rp.ax.c2p(0, b["reference"]), rp.ax.c2p(2000, b["reference"]), stroke_color=REF,
                         stroke_width=2) if rp.lo < b["reference"] < rp.hi else VGroup()
        leg = legend([(NET, r"$u_0$: seed 1 (line), seeds 0 and 1 (band)"), (REF, rf"reference {b['reference']:.3f}"),
                      (WHITE, r"left: perfect landing, $Y_N = $ payoff")], font_size=16).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now the training itself, replayed. On the right, today's price, the guess, step by step: the line is a "
            "second run, the band spans it and the first. On the left, where two hundred and fifty-six test paths land "
            "at expiry, against their payoffs: a perfect solver would put every dot on the diagonal. "
            "<bookmark mark='a'/> At the start the dots are a shapeless cloud, and the guess is wherever it was "
            "dropped. Within a few hundred steps the cloud tilts toward the diagonal, and the guess slides toward the "
            "reference. By two thousand steps the cloud is a tight band around the diagonal."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(ref), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 4))
        self.wait(0.4)
        self.clear_scene()

    def result(self, b, s):
        cv = b["curve"]
        it = np.array([c["iter"] for c in cv])
        u = np.array([c["u0"] for c in cv])
        ref, nd = b["reference"], b["no_default_mc"]
        t0, t1 = s["tail0"], s["tail1"]
        lo, hi = min(u.min(), ref) - 1.0, max(u.max(), ref) + 1.0
        g = axes([0, it.max()], [lo, hi], x_length=7.2, y_length=4.4, xlabel=r"training step",
                 ylabel=r"today's price $u_0$", xticks=[0, 1000, 2000, 3000, 4000],
                 xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), yticks=[round(v) for v in np.linspace(lo + 0.5, hi - 0.5, 3)],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, it, u, NET, stroke_width=3)
        r1 = DashedLine(ax.c2p(0, ref), ax.c2p(it.max(), ref), stroke_color=REF, stroke_width=2)
        tail = Rectangle(width=ax.c2p(4000, 0)[0] - ax.c2p(3000, 0)[0],
                         height=abs(ax.c2p(0, t0["mean"] + t0["sd"])[1] - ax.c2p(0, t0["mean"] - t0["sd"])[1]),
                         stroke_width=0, fill_color=GOOD, fill_opacity=0.35).move_to(
            ax.c2p(3500, t0["mean"]))
        rel = 100 * (t0["mean"] - ref) / ref
        rel_single = 100 * b["rel_error"]
        direction = "above" if rel > 0 else "below"
        side = VGroup(
            MathTex(rf"u_0 = {t0['mean']:.2f} \pm {t0['sd']:.2f}", font_size=38, color=GOOD),
            label(rf"mean and spread of the last {t0['n']} logged values (steps 3{{,}}000--4{{,}}000)", font_size=18,
                  color=GREY_A),
            label(rf"{rel:+.2f}\% against the reference {ref:.3f}", font_size=20, color=GREY_A),
            label(rf"seed 1, steps 1{{,}}000--2{{,}}000: {t1['mean']:.2f} $\pm$ {t1['sd']:.2f}", font_size=20, color=NET),
            wrapped_label(rf"a single final value would have said {rel_single:.2f}\%; Han, Jentzen and E reported 0.46\% "
                          rf"in 27 minutes; here {b['seconds'] / 60:.0f} minutes on a shared CPU", 4.2, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        leg = legend([(NET, r"seed 0, 4{,}000 steps"), (REF, rf"reference {ref:.3f} (multilevel Picard)"),
                      (GOOD, r"the tail: mean $\pm$ one standard deviation")], font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        with self.voiceover(
            "The full four thousand steps of the first run. How should the answer be read off? Not from the last "
            "step: the guess still jitters with every random batch. <bookmark mark='a'/> Average the last thousand "
            f"steps instead: {t0['mean']:.2f}, give or take {t0['sd']:.2f}, which is {abs(rel):.2f} percent "
            f"{direction} the reference of {ref:.1f}, computed by a different method altogether, "
            f"multilevel Picard iteration. The second run, at half the steps, gives {t1['mean']:.2f}. Han, Jentzen and "
            "E reported an error of 0.46 percent in their paper."
        ) as vo:
            self.play(FadeIn(g), Create(r1), FadeIn(leg[1]))
            self.play(Create(line), FadeIn(leg[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(tail), FadeIn(leg[2]), LaggedStart(*[FadeIn(m) for m in side], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def linear(self, b, s):
        cv = s["linear"]["curve"]
        it = np.array([c["iter"] for c in cv])
        u = np.array([c["u0"] for c in cv])
        nd, se = b["no_default_mc"], b["no_default_se"]
        tl = s["tail_lin"]
        lo, hi = min(u.min(), nd) - 1, max(u.max(), nd) + 1
        g = axes([0, it.max()], [lo, hi], x_length=7.2, y_length=4.0, xlabel=r"training step", ylabel=r"$u_0$, no default",
                 xticks=[0, 500, 1000, 1500], yticks=[round(v) for v in np.linspace(lo + 0.5, hi - 0.5, 3)],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        line = curve(g.ax, it, u, NET, stroke_width=3)
        r1 = DashedLine(g.ax.c2p(0, nd), g.ax.c2p(it.max(), nd), stroke_color=BAD, stroke_width=2)
        gap = tl["mean"] - nd
        side = VGroup(MathTex(rf"\text{{deep BSDE}}\ {tl['mean']:.2f} \pm {tl['sd']:.2f}", font_size=32, color=NET),
                      MathTex(rf"\text{{Monte Carlo}}\ {nd:.2f} \pm {se:.2f}", font_size=32, color=BAD),
                      wrapped_label(rf"the same solver, the same networks, default switched off: it lands "
                                    rf"{abs(gap):.2f} {'above' if gap > 0 else 'below'} plain discounted Monte Carlo on "
                                    r"400{,}000 paths. And ignoring default would overprice the real claim by "
                                    rf"{nd - b['reference']:.1f}", 4.4, 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "And the check with a known answer. Switch default off: the equation becomes linear, and the price is just "
            "the discounted average payoff, which plain Monte Carlo gives on four hundred thousand paths. "
            f"<bookmark mark='a'/> The same solver, trained from scratch, settles at {tl['mean']:.2f}, against "
            f"{nd:.2f} by Monte Carlo. It passes. And the difference between the two problems, {nd - b['reference']:.1f}, "
            "is what the default risk is worth."
        ) as vo:
            self.play(FadeIn(g), Create(r1), FadeIn(side[1]))
            self.play(Create(line), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, b):
        card = house_lab(r"the forward sweep", D.deep_bsde, "def run(n):", 11)
        card.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)
        cv = {c["iter"]: c["u0"] for c in b["curve"]}
        outs = [f"u0 at step 0: {cv[0]:.2f}   step 1000: {cv[1000]:.2f}   step 4000: {cv[4000]:.2f}",
                f"reference (multilevel Picard): {b['reference']:.3f}"]
        with self.voiceover(
            "The House's forward sweep: draw the noise for a hundred assets and forty steps, start every path at the "
            "guess, and at each date step the price with the default term and that date's network's hedge. "
            "<bookmark mark='a'/> Training only adds the squared miss and an optimizer."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        self.wait(0.5)
        self.clear_scene()

    def why_it_scales(self, b):
        p = b["params"]
        rows = [cmath(r"\text{work per step}", r"=", r"O\big(N\,d\,(d + 10)\,B\big)", font_size=40,
                      colors={r"\text{work per step}": GOOD}),
                cmath(r"\text{grid}", r"=", r"10^{d}\ \text{nodes}", font_size=40, colors={r"\text{grid}": BAD})]
        whys = [why(rf"$N - 1 = {p['N'] - 1}$ small networks of width $d + 10$, a batch of $B = 64$ paths: polynomial in "
                    r"the dimension. Hutzenthaler, Jentzen, Kruse and Nguyen (2020) proved that ReLU networks approximate "
                    r"semilinear heat equations with a number of parameters polynomial in $d$ and $1/\varepsilon$; "
                    r"Jentzen, Kuckuck and von Wurstemberger's book (2023) collects the theory"),
                why(r"against ten points per axis: the curse of dimensionality")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.4, buff=1.0, edge=6.9)
        cards = VGroup(
            firm_card(r"Deep Galerkin (DGM)", r"Sirignano and Spiliopoulos (2018): minimize the PDE's residual at random "
                      r"points; needs second derivatives of the network, which the BSDE form avoids", width=4.0,
                      font_size=16),
            firm_card(r"Multilevel Picard", r"E, Hutzenthaler, Jentzen and Kruse: a non-learned Monte Carlo method for "
                      r"the same equations; the source of the 57.300 reference", width=4.0, font_size=16),
            firm_card(r"Part 16's grids", r"finite differences: exact and fast in one to three dimensions, impossible "
                      r"beyond", width=4.0, font_size=16),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.3)
        for c_ in cards:
            c_[0].set_stroke(GREY_C)
        with self.voiceover(
            "Why does it scale? The work per step grows at most with the square of the dimension, while a grid "
            "multiplies by ten with every asset; and Hutzenthaler, Jentzen, Kruse and Nguyen proved that networks of "
            "polynomial size suffice for such equations. <bookmark mark='a'/> Its relatives: the deep Galerkin method "
            "fits the equation's residual instead, needing second derivatives; multilevel Picard iteration solves it "
            "without learning, and supplied our reference. <bookmark mark='b'/> And a question: the loss stalls near "
            "thirty, not zero. Is the network failing? No: the time grid and batch noise put a floor under it. Judge "
            "the solver by its price."
            " Next: deciding when to stop, by network."
        ) as vo:
            step(0)
            step(1)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeOut(cards), FadeIn(ask(r"the loss stalls near 30, not 0. Is the network failing?")))
        self.wait(0.5)
        self.clear_scene()
