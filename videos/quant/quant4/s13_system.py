from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, load

NAMES = {"flat": r"flat", "martingale": r"doubling", "dalembert": r"d'Alembert", "labouchere": r"Labouch\`ere",
         "fibonacci": r"Fibonacci", "oscar": r"Oscar's grind"}
SYS = ["flat", "martingale", "dalembert", "labouchere", "fibonacci", "oscar"]


class System(VoiceoverScene):
    def construct(self):
        s = load("systems")
        self.card()
        self.derive()
        self.curtain(s)
        self.six(s)
        self.table(s)
        self.lab(s)

    def card(self):
        c = chapter_card(4, r"You can't beat the system", r"Can a clever stake turn a fair game in your favour?",
                         part=PART)
        with self.voiceover("Chapter four. You can't beat the system."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        cols = {r"H_k": DRIFT, r"H_{n+1}": DRIFT}
        rows = [cmath(r"(H \cdot M)_n", r"=", r"\sum_{k \le n} H_k\,\Delta M_k, \quad H_k \in \mathcal{F}_{k-1}",
                      font_size=40),
                cmath(r"\mathbb{E}\big[\Delta (H \cdot M)_{n+1} \mid \mathcal{F}_n\big]", r"=",
                      r"H_{n+1}\,\mathbb{E}[\Delta M_{n+1} \mid \mathcal{F}_n] = 0", font_size=40, colors=cols),
                cmath(r"\mathbb{E}[\text{gain}]", r"=", r"-\tfrac{1}{37}\,\mathbb{E}\Big[\sum_k H_k\Big]", font_size=40,
                      colors={r"-\tfrac{1}{37}\,\mathbb{E}\Big[\sum_k H_k\Big]": LOSS}),
                cmath(r"H_k = \operatorname{sign}\Delta M_k \in \mathcal{F}_k", r"\Rightarrow",
                      r"(H \cdot M)_n = \sum_k |\Delta M_k| = n", font_size=40, colors={r"(H \cdot M)_n = \sum_k |\Delta M_k| = n": LOSS})]
        whys = [why(r"the martingale transform: the stake $H_k$ is decided before step $k$ (it is predictable) and "
                    r"bounded"),
                why(r"take out what is known (chapter 2): the stake is known, the step averages to zero"),
                why(r"on red at a European wheel each unit staked loses $1/37$ on average: the same tax, whatever the "
                    r"system"),
                why(r"a cheat who stakes after seeing the step wins every time: predictability is the whole hypothesis")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-1.0, buff=0.75, edge=6.9)
        head = label(r"Williams, \textit{Probability with Martingales}, ch.\ 10: ``you can't beat the system''",
                     font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "A betting system decides each stake from what has happened so far. Call the stake H. The gambler's "
            "wealth is the sum of stake times step: the martingale transform, with one rule, that the stake is fixed "
            "before the step is seen. <bookmark mark='a'/> Then, taking out what is known, the expected next gain is "
            "the stake times the expected next step, which is zero. The transform of a martingale is a martingale: "
            "no system turns a fair game favourable. <bookmark mark='b'/> On a roulette wheel each unit on red loses "
            "one thirty-seventh on average, so every system loses one thirty-seventh of what it stakes: the same tax "
            "per unit. <bookmark mark='c'/> A cheat who could stake after seeing the outcome would win every round. "
            "The whole theorem is the word before."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def curtain(self, s):
        wins = [bool(v) for v in s["demo_wins"]]
        stakes = [float(v) for v in s["demo_stakes"]]
        n = len(wins)
        cw = 0.82
        cards = VGroup(*[RoundedRectangle(width=cw, height=1.1, corner_radius=0.08, stroke_color=GREY_B,
                                          stroke_width=2, fill_color=GREY_E, fill_opacity=1) for _ in range(n)])
        cards.arrange(RIGHT, buff=0.14).to_edge(UP, buff=1.2)
        faces = VGroup(*[MathTex("H" if w else "T", font_size=36, color=QC.GAIN if w else LOSS).move_to(c)
                         for c, w in zip(cards, wins)])
        curtain = Rectangle(width=cards.width + 0.3, height=1.35, stroke_width=0, fill_color=GREY_D,
                            fill_opacity=1).move_to(cards)
        sb_base = cards.get_bottom()[1] - 0.25
        bars = VGroup(*[Rectangle(width=cw * 0.6, height=0.3 * h, stroke_width=0, fill_color=DRIFT,
                                  fill_opacity=0.9).move_to([c.get_x(), sb_base - 0.15 * h, 0])
                        for c, h in zip(cards, stakes)])
        blabel = label(r"stake, set before the card is turned (doubling)", font_size=20, color=DRIFT).next_to(
            bars, LEFT, buff=0.2).shift(DOWN * 0.05)
        if blabel.get_left()[0] < -7.0:
            blabel.next_to(bars, DOWN, buff=0.7).align_to(bars, LEFT)
        g = axes([0, n], [-4, 6], x_length=cards.width, y_length=2.5, ylabel=r"wealth", xticks=[], yticks=[-4, 0, 4],
                 font_size=16)
        g.next_to(bars, DOWN, buff=0.9).align_to(cards, LEFT)
        ax = g.ax
        wealth = np.concatenate([[0.0], np.cumsum([h if w else -h for h, w in zip(stakes, wins)])])
        steps_ = VGroup(*[Line(ax.c2p(k, wealth[k]), ax.c2p(k + 1, wealth[k + 1]), color=MART, stroke_width=3.5)
                          for k in range(n)])
        with self.voiceover(
            "Here is the rule as a machine. Twelve fair tosses lie behind a curtain, and before each the doubling "
            "system sets its stake. <bookmark mark='a'/> Only then is the card turned and the wealth steps. "
            "<bookmark mark='b'/> Each step is a stake known in advance times a fair coin, and fair coins average out."
        ) as vo:
            self.play(FadeIn(cards), FadeIn(curtain), FadeIn(g))
            vo.wait_until("a")
            for k in range(n):
                anims = [GrowFromEdge(bars[k], UP)]
                if k == 0:
                    anims.append(FadeIn(blabel))
                self.play(*anims, run_time=0.35)
                self.play(FadeIn(faces[k]), curtain.animate.stretch_to_fit_width(
                    max(cards.get_right()[0] - cards[k].get_right()[0] - 0.02, 0.01), about_edge=RIGHT),
                    Create(steps_[k]), run_time=0.45)
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()

    def six(self, s):
        R = s["games"]["roulette"]
        panels = VGroup()
        trackers = ValueTracker(0.0)
        lives, reads = VGroup(), VGroup()
        for i, k in enumerate(SYS):
            path = np.asarray(R[k]["path"])
            lo, hi = float(min(path.min(), -10)), float(max(path.max(), 10))
            g = axes([0, 200], [lo, hi], x_length=3.6, y_length=1.6, xticks=[], yticks=[], font_size=14)
            name = label(NAMES[k], font_size=22, color=WHITE).next_to(g, UP, buff=0.08).align_to(g, LEFT)
            panels.add(VGroup(g, name))
        panels.arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.9)).to_edge(UP, buff=0.7)
        for i, k in enumerate(SYS):
            g = panels[i][0]
            path = np.asarray(R[k]["path"])
            lives.add(tracing(g.ax, np.arange(len(path)), path, trackers, MART, stroke_width=2.2))
            rk, rv = np.asarray(R[k]["running_k"], float), np.asarray(R[k]["running"], float)
            ro = readout(r"\text{loss} \div \text{staked} =", lambda rk=rk, rv=rv: float(np.interp(
                10 ** (np.log10(rk[0]) + trackers.get_value() / 200 * (np.log10(rk[-1]) - np.log10(rk[0]))), rk, rv)),
                digits=4, font_size=22, color=LOSS).next_to(g, DOWN, buff=0.12)
            reads.add(ro)
        zero = VGroup(*[DashedLine(p[0].ax.c2p(0, 0), p[0].ax.c2p(200, 0), color=GREY_D, stroke_width=1) for p in panels])
        cap = label(r"one session of 200 spins each (line), and the running ratio over 20{,}000 sessions (number)",
                    font_size=20, color=GREY_B).to_edge(DOWN, buff=0.35)
        tax = MathTex(r"-1/37 = -0.0270", font_size=34, color=LOSS).next_to(cap, UP, buff=0.15)
        with self.voiceover(
            "Now six famous systems on European roulette, all betting red. Flat betting. Doubling. D'Alembert, one "
            "unit more after a loss and one less after a win. Labouchère, which crosses numbers off a written line. "
            "Fibonacci. And Oscar's grind, which tries to win one unit per series. <bookmark mark='a'/> Each panel "
            "plays one session of two hundred spins, while the number under it is the loss divided by the amount "
            "staked, accumulated over twenty thousand sessions. The paths could not look more different: steady "
            "drifts, long climbs, sudden cliffs. <bookmark mark='b'/> The numbers all settle on the same value: minus "
            "one thirty-seventh, two point seven percent of everything staked."
        ) as vo:
            self.play(FadeIn(panels), FadeIn(zero), FadeIn(cap))
            vo.wait_until("a")
            self.add(lives, reads)
            self.play(trackers.animate.set_value(200.0), run_time=9, rate_func=linear)
            for m_ in (*lives, *reads):
                m_.clear_updaters()
            vo.wait_until("b")
            self.play(FadeIn(tax), *[Indicate(r, color=LOSS, scale_factor=1.05) for r in reads])
        self.wait(0.4)
        self.clear_scene()

    def table(self, s):
        R, F = s["games"]["roulette"], s["games"]["fair"]
        head = [label(t, font_size=20, color=GREY_B) for t in (r"system", r"mean P\&L", r"mean staked",
                                                                 r"loss $\div$ staked", r"P(up)", r"skew")]
        rows = []
        within = True
        within_fair = True
        for k in SYS:
            v, f = R[k], F[k]
            ok = abs(v["ratio"] + 1 / 37) <= 2 * v["ratio_se"] + 1e-12
            within &= ok
            within_fair &= abs(f["pnl"]) <= 2 * f["pnl_se"]
            rows.append([label(NAMES[k], font_size=22),
                         MathTex(rf"{v['pnl']:.1f} \pm {v['pnl_se']:.1f}", font_size=24),
                         MathTex(rf"{v['staked']:,.0f}".replace(",", "{,}"), font_size=24),
                         MathTex(rf"{v['ratio']:.4f} \pm {v['ratio_se']:.4f}", font_size=24, color=LOSS if ok else QC.IDEA),
                         MathTex(rf"{100 * v['p_up']:.0f}\%", font_size=24, color=MART),
                         MathTex(rf"{v['skew']:+.1f}", font_size=24)])
        grid = VGroup(*head, *[c for r in rows for c in r]).arrange_in_grid(rows=7, cols=6, buff=(0.45, 0.2),
                                                                             col_alignments="lccccc")
        grid.to_edge(UP, buff=0.5)
        if grid.width > 13.0:
            grid.scale_to_fit_width(13.0)
        verdict = ("every ratio is within two standard errors of minus one thirty-seventh"
                   if within else "most ratios sit within two standard errors of minus one thirty-seventh; the "
                                  "heavy-tailed ones need more sessions")
        fair = ("and on a fair coin every mean is within two standard errors of zero." if within_fair else
                "and on a fair coin the means scatter around zero.")
        note_ = wrapped_label(r"20{,}000 sessions of 200 spins on European red, table limit 500 units; $\pm$ one "
                              r"standard error", 12.0, 20, GREY_B).next_to(grid, DOWN, buff=0.35)
        pred = desk_question(r"Labouch\`ere or flat betting: which loses more per unit staked on roulette?",
                             r"Neither: both lose $1/37$ of what they stake. Labouch\`ere stakes more, so it loses more "
                             r"in total, but wins more sessions.", width=9.6, font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The ledger. The systems differ in how much they stake and in the shape of their results. Doubling "
            "and Fibonacci win most sessions, and pay for it with rare large losses: their skew is strongly negative. "
            f"<bookmark mark='a'/> But divide the loss by the amount staked, and {verdict}, {fair} <bookmark mark='b'/> "
            "So, which loses more per unit staked, Labouchère or flat betting? Neither. Labouchère stakes far "
            "more and so loses more in total, while winning more of its sessions: a pleasant evening, most nights, "
            "paid for on the others."
        ) as vo:
            self.play(FadeIn(VGroup(*head)), LaggedStart(*[FadeIn(VGroup(r[0], r[1], r[2], r[4], r[5])) for r in rows],
                                                          lag_ratio=0.2), FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, s):
        card = lab_card(r"the martingale transform", [
            "def martingale_transform(H, dM):",
            "    \"\"\"(H . M)_n: stake H_k, fixed before step k, times dM_k.\"\"\"",
            "    return np.concatenate([[0.0], np.cumsum(np.asarray(H) * np.asarray(dM))])",
            "",
            "H = system_stakes(\"martingale\", wins)   # doubling: decided from the past",
            "dM = np.where(wins, 1.0, -1.0)",
            "martingale_transform(H, dM)[-1]",
        ], source="explainer/quant/house/martingale.py", width=9.0).to_edge(UP, buff=0.5)
        wins = [bool(v) for v in s["demo_wins"]]
        stakes = [float(v) for v in s["demo_stakes"]]
        total = sum(h if w else -h for h, w in zip(stakes, wins))
        with self.voiceover(
            "In the House the transform is one line, and each system is a function from past outcomes to the next "
            "stake. <bookmark mark='a'/> On the twelve tosses it reproduces the curtain. Chapter sixteen turns this "
            "line into a test."
            " Changing the stakes fails. What about choosing when to stop?"
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, ["stakes: " + " ".join(f"{h:g}" for h in stakes),
                                 "tosses: " + " ".join("H" if w else "T" for w in wins),
                                 f"final wealth: {total:+g}"])
        self.wait(0.4)
        self.clear_scene()
