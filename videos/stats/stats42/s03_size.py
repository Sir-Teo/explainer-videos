from __future__ import annotations

import math

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403


class TrialSize(VoiceoverScene):
    def construct(self):
        self.card()
        self.individual()
        self.deff()
        self.towns()
        self.tradeoff()
        self.sensitivity()
        self.power()

    def card(self):
        card = chapter_card(2, r"Case 1: \ how many towns", r"What does the correlation cost?", part=PART)
        with self.voiceover("Chapter two. How many towns?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def individual(self):
        s = load("size")
        rows = [
            cmath(r"\hat\tau", r"\sim", r"N\big(\tau, \ 2\sigma^2 / n\big) \ \ \text{(n adults per arm, independent)}", font_size=32),
            cmath(r"\text{power}", r"\approx", r"\Phi\big(|\tau| / \text{SE} - z_{0.975}\big) = 0.8 \quad (\delta=|\tau|)", font_size=30),
            cmath(r"n", r"=", r"\frac{2 (z_{0.975} + z_{0.80})^2 \sigma^2}{\delta^2} = \frac{2 (1.96 + 0.84)^2 \times 16.5^2}{4^2}", font_size=32),
            cmath(r"\phantom{n}", r"=", rf"{s['n_ind']:.0f} \text{{ adults per arm}}", font_size=34),
        ]
        rows[3][-1].set_color(CASE1)
        whys = [why(r"two arms, \ Part 13"), why(r"80\% power at 5\%"), why(r"solve for $n$"), why(r"if adults were independent")]
        with self.voiceover(
            f"<bookmark mark='a'/> Start as if adults were independent, as in Part thirteen. With n adults per arm, the difference in means is normal around the true effect, with variance two sigma squared over n. <bookmark mark='b'/> We want an eighty percent chance of a significant result at the five percent level when the effect is the ministry's four millimetres. The usual planning approximation keeps the rejection tail in the direction of the effect; the opposite tail is negligible here. For a reduction in pressure the relevant tail is negative, with delta denoting its magnitude. <bookmark mark='c'/> Setting it to eighty percent and solving gives the familiar formula: two times one point nine six plus point eight four, squared, times sigma squared, over delta squared. <bookmark mark='d'/> With sigma sixteen and a half, that is {s['n_ind']:.0f} adults per arm. If only adults were what we randomized."
        ) as vo:
            heading = label('Normal-approximation planning uses the magnitude of the effect', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def deff(self):
        s = load("size")
        rows = [
            cmath(r"\bar y_j", r"=", r"\mu + \tau z_j + b_j + \bar e_j, \ \ \text{Var}(b_j) = \rho\sigma^2, \ \text{Var}(e_{ij}) = (1 - \rho)\sigma^2", font_size=28),
            cmath(r"\text{Var}(\bar y_j)", r"=", r"\rho\sigma^2 + (1 - \rho)\sigma^2 / m = \frac{\sigma^2}{m}\big[1 + (m - 1)\rho\big]", font_size=32),
            cmath(r"\text{DE}", r"=", rf"1 + (m - 1)\rho = 1 + 49 \times {s['icc']:.3f} = {s['de50']:.2f}", font_size=34),
            cmath(r"\text{so}", r":", r"m \text{ correlated adults are worth } m / \text{DE} \text{ independent ones}", font_size=30),
        ]
        rows[2][-1].set_color(CASE1)
        whys = [why(r"a town's mean"), why(r"its variance"), why(r"Kish's design effect, \ Part 18"), why(r"50 adults $\approx$ 13.5")]
        with self.voiceover(
            f"<bookmark mark='a'/> Now the towns. A town's mean pressure is the overall mean, plus the effect if the town is "
            f"treated, plus the town's own deviation b j, with variance rho sigma squared, plus the average of its adults' "
            f"deviations. <bookmark mark='b'/> Its variance is rho sigma squared plus one minus rho, sigma squared over m: "
            f"sigma squared over m, times one plus m minus one times rho. <bookmark mark='c'/> The factor in brackets is Kish's "
            f"design effect from Part eighteen. With fifty adults per town and rho of {say(s['icc'], 3)}, it is "
            f"{say(s['de50'], 2)}. <bookmark mark='d'/> Fifty correlated adults carry the information of about thirteen and a "
            f"half independent ones. A small correlation, multiplied by a large town, is a large cost."
        ) as vo:
            heading = label('The design effect assumes equal-sized, independent clusters', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def towns(self):
        s = load("size")
        r50 = [r for r in s["rows"] if r["m"] == 50][0]
        rows = [
            cmath(r"n \times \text{DE}", r"=", rf"{s['n_ind']:.0f} \times {s['de50']:.2f} = {s['n_ind'] * s['de50']:.0f} \text{{ adults per arm}}", font_size=32),
            cmath(r"k", r"=", rf"{s['n_ind'] * s['de50']:.0f} / 50 = {r50['k']:.1f} \ \to \ {math.ceil(r50['k'])} \text{{ towns per arm}}", font_size=32),
            cmath(r"+1", r":", r"\text{a } t \text{ with } 2k - 2 \text{ df, not a } z \ \ \text{(Hayes \& Moulton)}", font_size=30),
            cmath(r"\text{the plan}", r":", rf"{r50['k_t']} + {r50['k_t']} = {2 * r50['k_t']} \text{{ towns}}, \ {2 * r50['people']:,} \text{{ adults}}", font_size=34),
        ]
        rows[3][-1].set_color(CASE1)
        whys = [why(r"inflate"), why(r"divide by town size"), why(r"few clusters"), why(r"of the island's 200")]
        with self.voiceover(
            f"<bookmark mark='a'/> So inflate the independent answer by the design effect: {s['n_ind']:.0f} times "
            f"{say(s['de50'], 2)} is about {s['n_ind'] * s['de50']:.0f} adults per arm. <bookmark mark='b'/> At fifty adults "
            f"a town, that is {say(r50['k'], 1)} towns, so {math.ceil(r50['k'])}. <bookmark mark='c'/> With so few units, the "
            f"analysis will use a t distribution with two k minus two degrees of freedom rather than a normal, and Richard "
            f"Hayes and Lawrence Moulton's rule of thumb adds one town per arm to pay for it. <bookmark mark='d'/> The plan: "
            f"{r50['k_t']} towns in each arm, {2 * r50['k_t']} of the island's two hundred, and "
            f"{2 * r50['people']:,} adults measured at the end."
        ) as vo:
            heading = label('Round up clusters and allow for a finite-cluster t analysis', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tradeoff(self):
        s = load("size")
        ms, kc = np.asarray(s["ms"]), np.asarray(s["k_curve"])
        A = axes([np.log10(5), 3], [0, 60], x_length=7.4, y_length=4.4, xlabel=r"adults measured per town, \ $m$",
                 ylabel=r"towns needed per arm", xticks=[1, 2, 3], yticks=[0, 20, 40, 60], log_x=True,
                 xfmt=lambda v: f"{10 ** v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        line = curve(ax, np.log10(ms), kc, CASE1, 4)
        floor = DashedLine(ax.c2p(np.log10(5), s["k_inf"]), ax.c2p(3, s["k_inf"]), color=S.ACCENT, stroke_width=2.5)
        fl = label(rf"$2(z+z)^2 \rho\sigma^2 / \delta^2 = {s['k_inf']:.1f}$", font_size=20, color=S.ACCENT).next_to(ax.c2p(2.2, s["k_inf"]), DOWN, buff=0.12)
        dots = VGroup(*[Dot(ax.c2p(np.log10(r["m"]), r["k"]), radius=0.07, color=WHITE) for r in s["rows"]])
        tab = table_rows([[r"$m$", r"towns", r"adults"]] + [[f"{r['m']}", f"{2 * r['k_t']}", f"{2 * r['people']:,}"] for r in s["rows"]],
                         font_size=22, col_buff=0.45, row_buff=0.14)
        tab.move_to([4.45, 0.6, 0])
        msg = label(r"adults are cheap; \ towns are the sample size", font_size=24, color=S.ACCENT).move_to([4.45, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Could we buy fewer towns by measuring more adults in each? Here is the number of towns needed per arm against the number of adults per town, on a log scale. <bookmark mark='b'/> More adults help at first, then hardly at all. <bookmark mark='c'/> The curve can never fall below this floor: even with infinitely many adults, each town's mean still carries its own deviation, and {say(s['k_inf'], 1)} towns per arm is the limiting normal-approximation count for this unadjusted equal-size design. Baseline adjustment or a different target can change it. <bookmark mark='d'/> In the table, ten adults per town needs eighty-two towns; fifty needs forty-two; five hundred still needs thirty-four, and seventeen thousand measurements. <bookmark mark='e'/> In a cluster trial, adults are cheap, and towns are the sample size."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(dots))
            vo.wait_until("c")
            self.play(Create(floor), FadeIn(fl))
            vo.wait_until("d")
            self.play(FadeIn(tab))
            vo.wait_until("e")
            self.play(FadeIn(msg))
        self.clear_scene()

    def sensitivity(self):
        s = load("size")
        p = load("pilot")
        rhos = np.linspace(0.0, 0.1, 101)
        k = s["n_ind"] * (1 + 49 * rhos) / 50
        A = axes([0, 0.1], [0, 40], x_length=7.4, y_length=4.4, xlabel=r"intraclass correlation $\rho$ (before the extra $t$ town)",
                 ylabel=r"towns per arm \ ($m = 50$)", xticks=[0, 0.025, 0.05, 0.075, 0.1], yticks=[0, 10, 20, 30, 40],
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        line = curve(ax, rhos, np.ceil(k), CASE1, 4)
        band_ = Rectangle(width=ax.c2p(p["icc_ci"][1], 0)[0] - ax.c2p(p["icc_ci"][0], 0)[0], height=ax.c2p(0, 40)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=TOWNC, fill_opacity=0.18).move_to(ax.c2p(np.mean(p["icc_ci"]), 20))
        marks = VGroup()
        for r, c in [(p["icc"], TOWNC), (s["icc"], S.ACCENT)]:
            kk = math.ceil(s["n_ind"] * (1 + 49 * r) / 50)
            marks.add(VGroup(DashedLine(ax.c2p(r, 0), ax.c2p(r, kk), color=c, stroke_width=2.5), Dot(ax.c2p(r, kk), color=c, radius=0.08)))
        k_p = math.ceil(s["n_ind"] * (1 + 49 * p["icc"]) / 50)
        side = fit_rows(VGroup(
            label(r"the plan is only as good as $\rho$", font_size=24),
            label(rf"pilot's $\hat\rho = {p['icc']:.3f}$: \ {k_p} towns per arm", font_size=24, color=TOWNC),
            label(rf"planning $\rho = {s['icc']:.3f}$: \ {math.ceil(s['n_ind'] * s['de50'] / 50)} towns per arm", font_size=24, color=S.ACCENT),
            label(r"each 0.01 of $\rho$ costs about 2.6 towns per arm", font_size=24, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The answer is only as good as rho. Here is the number of towns per arm against the intraclass correlation, with the pilot's interval shaded. <bookmark mark='b'/> Plan with the pilot's estimate and you would recruit {k_p} towns per arm. <bookmark mark='c'/> Plan with our more cautious value and you recruit twenty, before the extra one for the t. <bookmark mark='d'/> Every hundredth of correlation costs about two and a half towns per arm before rounding: the unrounded design effect is linear in rho. An exam answer that reports one sample size, without this line, is half an answer."
        ) as vo:
            self.play(FadeIn(A), FadeIn(band_))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def power(self):
        s = load("size")
        ks, pw, pn = np.asarray(s["ks"]), np.asarray(s["power"]), np.asarray(s["power_naive"])
        A = axes([4, 40], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"towns per arm \ (50 adults each)",
                 ylabel=r"power at $\delta = 4$ mm Hg", xticks=[5, 10, 20, 30, 40], yticks=[0, 0.5, 0.8, 1],
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        honest = curve(ax, ks, pw, CASE1, 4)
        naive = curve(ax, ks, pn, NAIVEC, 4)
        line80 = DashedLine(ax.c2p(4, 0.8), ax.c2p(40, 0.8), color=GREY_B, stroke_width=2)
        i21 = int(np.where(ks == 21)[0][0])
        dot = Dot(ax.c2p(21, pw[i21]), color=CASE1, radius=0.09)
        i8 = int(np.where(ks == 8)[0][0])
        side = fit_rows(VGroup(
            label(r"power, \ honestly: \ cluster means, \ $t_{2k-2}$", font_size=24, color=CASE1),
            label(rf"21 towns per arm: \ {pw[i21]:.2f}", font_size=24, color=CASE1),
            label(r"the power one would claim, \ treating adults as independent", font_size=24, color=NAIVEC),
            label(rf"8 towns per arm: \ claimed {pn[i8]:.2f}, \ true {pw[i8]:.2f}", font_size=24, color=NAIVEC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Finally, the power curve itself, computed honestly: cluster means, and a noncentral t with two k minus two degrees of freedom. <bookmark mark='b'/> At twenty-one towns per arm, the power is {say(pw[i21], 2)}, as planned. <bookmark mark='c'/> In red, the power one would claim by treating every adult as independent. <bookmark mark='d'/> At eight towns per arm, that calculation promises {pn[i8] * 100:.0f} percent power; the power under this Gaussian cluster model is {pw[i8] * 100:.0f} percent. This is the self-deception Cornfield warned of, and it happens at the planning stage, before a single adult is measured."
        ) as vo:
            self.play(FadeIn(A), FadeIn(line80))
            vo.wait_until("a")
            self.play(Create(honest), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dot), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(naive), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
