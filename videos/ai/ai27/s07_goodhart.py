from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, GOLD, KLC, PART, POLICY, PROXY, REWARD, load, node_box, said, ticks


class Goodhart(VoiceoverScene):
    def construct(self):
        self.card()
        self.law()
        self.bon_kl()
        self.curves()
        self.scaling()

    def card(self):
        card = chapter_card(7, r"When the measure becomes the target", r"How hard can you optimize a learned reward?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter seven. When the measure becomes the target."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def law(self):
        quote = label(r"``When a measure becomes a target, \\ it ceases to be a good measure.''", font_size=40)
        quote.move_to(UP * 1.6)
        who = label(r"Goodhart's law, \ in Marilyn Strathern's words (1997)", font_size=24, color=GREY_A)
        who.next_to(quote, DOWN, buff=0.3)
        cases = VGroup(
            label(r"a reward model that likes longer answers: \ the policy learns to pad", font_size=26),
            label(r"a reward model that likes agreement: \ the policy learns to flatter", font_size=26),
            label(r"a boat-racing agent rewarded for targets hit: \ circles forever, never finishing", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.4)
        cite_ = cite(r"Goodhart (1975); \ Amodei \& Clark, \textit{Faulty reward functions in the wild} (OpenAI, 2016)")
        hist = VGroup(
            history_card(1975, r"Charles Goodhart, \ economist", r"statistics used to steer policy stop meaning what "
                         r"they used to", width=5.6, color=GOLD),
            history_card(1997, r"Marilyn Strathern, \ anthropologist", r"the general form: \ any measure that becomes "
                         r"a target", width=5.6, color=GOLD),
        ).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.5)
        with self.voiceover(
            "In 1975 the economist Charles Goodhart observed that statistics used to steer policy stop meaning what "
            "they used to. The anthropologist Marilyn Strathern later put it in the form everyone quotes: when a "
            "measure becomes a target, it ceases to be a good measure. <bookmark mark='a'/> A reward model is a "
            "measure. If it slightly prefers longer answers, optimizing it produces padding. <bookmark mark='b'/> If "
            "it slightly prefers answers that agree with the user, optimizing it produces flattery. "
            "<bookmark mark='c'/> Reinforcement learning has always done this: in 2016 OpenAI showed a boat-racing "
            "agent, rewarded for hitting targets along the course, that learned to circle a lagoon forever, hitting "
            "the same three targets and never finishing the race."
        ) as vo:
            self.play(FadeIn(quote), FadeIn(who))
            self.play(FadeIn(hist[0], shift=UP * 0.15))
            self.wait(2.0)
            self.play(FadeIn(hist[1], shift=UP * 0.15))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(FadeOut(hist), run_time=0.6)
                self.play(FadeIn(cases[k], shift=UP * 0.15), *([FadeIn(cite_)] if k == 2 else []))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bon_kl(self):
        rows = [
            cmath(r"\pi_{\mathrm{BoN}}", r":\ ", r"\text{draw } n \text{ answers from } \pi_{\mathrm{ref}},\ \text{keep "
                  r"the one } r \text{ likes best}", font_size=32),
            cmath(r"\mathrm{KL}\big(\pi_{\mathrm{BoN}} \,\|\, \pi_{\mathrm{ref}}\big)", r"=",
                  r"\log n - \frac{n-1}{n}", font_size=36),
            cmath(r"n = 4", r":\ ", r"0.64 \text{ nats}, \quad n = 64:\ 3.17, \quad n = 1024:\ 5.93", font_size=32),
        ]
        rows[1][2].set_color(KLC)
        whys = [why(r"the simplest optimizer of a reward model"),
                why(r"the answer at quantile $u$ is chosen with density $n u^{n-1}$: \ integrate its log"),
                why(r"it grows only like $\log n$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.6, buff=0.7, edge=6.9)
        # n draws on a reward axis, the best one ringed: bigger n reaches further into the tail (schematic)
        g_ = np.random.default_rng(3)
        axis = NumberLine(x_range=[-3, 3, 1], length=9.0, color=GREY_C, include_ticks=False).move_to([0, -2.4, 0])
        al = label(r"the reward model's score of each draw", font_size=20, color=PROXY).next_to(axis, DOWN, buff=0.2)

        def draws(n):
            v = np.clip(g_.normal(size=n), -2.9, 2.9)
            dots = VGroup(*[Dot(axis.n2p(x) + UP * 0.25, radius=0.06, color=GREY_B) for x in v])
            best = Circle(radius=0.14, color=PROXY, stroke_width=3).move_to(dots[int(np.argmax(v))])
            name = label(rf"best of $n = {n}$", font_size=22, color=PROXY).next_to(axis, UP, buff=0.75)
            return VGroup(dots, best, name)

        pics = [draws(n) for n in (4, 64, 1024)]
        stag = note(r"schematic").to_corner(DR, buff=0.25)
        with self.voiceover(
            "To measure the effect, we need a way to optimize a reward model by a controlled amount. The simplest "
            "is best-of-n: draw n answers from the reference model and keep the one the reward model likes best. "
            "Bigger n, harder optimization. <bookmark mark='a'/> Its divergence from the reference has a closed "
            "form: log n minus n minus one over n. The chosen answer is the best of n, so if u is its quantile under "
            "the reward model, its density is n times u to the n minus one, and the KL is the expected log of that. "
            "<bookmark mark='b'/> It grows only like log n: best of a thousand is under six nats. Best-of-n is cheap "
            "to reason about, and in practice it is a strong baseline that labs still use."
        ) as vo:
            step(0)
            self.play(Create(axis), FadeIn(al), FadeIn(stag), FadeIn(pics[0][0]), FadeIn(pics[0][2]))
            self.play(Create(pics[0][1]))
            self.play(FadeOut(pics[0]), FadeIn(pics[1][0]), FadeIn(pics[1][2]))
            self.play(Create(pics[1][1]))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeOut(pics[1]), FadeIn(pics[2][0]), FadeIn(pics[2][2]))
            self.play(Create(pics[2][1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("bon")
        kl = np.asarray(d["kl"])
        x = np.sqrt(kl)
        ys = {k: np.asarray(d[k]) for k in ("small_proxy", "small_gold", "large_proxy", "large_gold")}
        xmax = float(np.ceil(x.max() * 2) / 2)
        xl = r"$\sqrt{\mathrm{KL}}$ \ (best-of-$n$, $n = 1 \dots 256$)"
        # two panels, each on its own scale: the reward models' scores run to several units, gold moves by tenths
        phi = max(float(ys["small_proxy"].max()), float(ys["large_proxy"].max()))
        glo = min(float(ys["small_gold"].min()), float(ys["large_gold"].min()))
        ghi = max(float(ys["small_gold"].max()), float(ys["large_gold"].max()))
        gp = 0.15 * (ghi - glo + 1e-6)
        g = axes([0, xmax], [0, float(np.ceil(phi))], x_length=5.0, y_length=3.6, xlabel=xl,
                 ylabel=r"what the reward model thinks", xticks=[0, 1, 2], yticks=ticks(0, float(np.ceil(phi)), 3),
                 center=[-3.5, -0.2, 0])
        g2 = axes([0, xmax], [glo - gp, ghi + gp], x_length=5.0, y_length=3.6, xlabel=xl,
                  ylabel=r"what gold thinks", xticks=[0, 1, 2], yticks=[round(glo, 2), round(ghi, 2)],
                  yfmt=lambda v: rf"{v:+.2f}", center=[3.1, -0.2, 0])
        mk = lambda ax_, key, col, w: VMobject().set_points_as_corners(
            [ax_.ax.c2p(a, b) for a, b in zip(x, ys[key])]).set_stroke(col, w)
        sp, sg = mk(g, "small_proxy", PROXY, 3), mk(g2, "small_gold", GOLD, 4)
        lp, lg_ = mk(g, "large_proxy", PROXY, 4), mk(g2, "large_gold", GOLD, 5)
        sp.set_stroke(opacity=0.5)
        sg.set_stroke(opacity=0.5)
        ns = list(d["ns"])
        rm = load("rm")
        size = VGroup(label(rf"faint: \ reward model from ${int(rm['sizes'][0])}$ comparisons", font_size=18,
                            color=GREY_B),
                      label(rf"bold: \ from ${int(rm['sizes'][-1]):,}$".replace(",", "{,}"), font_size=18,
                            color=GREY_B)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        tag = note(r"computed: \ $256$ lines per prompt from our fine-tuned model, \ expectations over every "
                   r"subset of size $n$").to_corner(DR, buff=0.2)
        sgold, lgold = ys["small_gold"], ys["large_gold"]
        s_end, l_end = round(float(sgold[-1]), 2) + 0.0, round(float(lgold[-1]), 2) + 0.0  # no "-0.00"
        peak_s = int(np.argmax(sgold))
        if peak_s < len(ns) - 1 and sgold[-1] < sgold[peak_s] - 0.02:
            small_said = (f"With the small reward model, gold rises at first, peaks around n = {ns[peak_s]}, then "
                          f"falls back to {s_end:.2f} while the reward model's own score keeps climbing to "
                          f"{ys['small_proxy'][-1]:.2f}: over-optimization.")
        else:
            small_said = (f"With the small reward model, gold climbs only to {s_end:.2f} while the reward "
                          f"model's own score reaches {ys['small_proxy'][-1]:.2f}: the gap between them widens.")
        peak_l = int(np.argmax(lgold))
        if peak_l < len(ns) - 1 and lgold[-1] < lgold[peak_l] - 0.02:
            large_said = (f"The reward model trained on more comparisons tracks gold further: gold reaches "
                          f"{lgold.max():.2f} at n = {ns[peak_l]}, and then it too falls back, to {l_end:.2f}.")
        else:
            large_said = (f"The reward model trained on more comparisons tracks gold further: gold reaches "
                          f"{lgold.max():.2f}.")
        ex = d["examples"][0]
        # where each n sits on the KL axis: a ruler above each panel, at the panel's own x scale
        marks = VGroup()
        for ax_ in (g, g2):
            y_r = ax_.ax.get_top()[1] + 0.85
            x0_, x1_ = ax_.ax.c2p(0, 0)[0], ax_.ax.c2p(xmax, 0)[0]
            ruler = VGroup(Line([x0_, y_r, 0], [x1_, y_r, 0], color=GREY_C, stroke_width=1.5))
            for n_, x_ in zip(ns, x):
                if n_ in (1, 4, 16, 64, 256):
                    xx = ax_.ax.c2p(x_, 0)[0]
                    ruler.add(Line([xx, y_r - 0.07, 0], [xx, y_r + 0.07, 0], color=GREY_B, stroke_width=2))
                    ruler.add(MathTex(rf"{n_}", font_size=18, color=GREY_B).move_to([xx, y_r + 0.24, 0]))
            ruler.add(MathTex(r"n", font_size=20, color=GREY_B).next_to([x0_, y_r, 0], LEFT, buff=0.15))
            marks.add(ruler)
        # the procedure, while it is described, before the axes it fills
        steps = VGroup(node_box(rf"${ns[-1]}$ lines per prompt", ASSIST, font_size=24),
                       node_box(r"best-of-$n$: \ a reward model picks", PROXY, font_size=24),
                       node_box(r"score the pick: \ reward model \ and \ gold", GOLD, font_size=24)
                       ).arrange(RIGHT, buff=0.9).move_to(UP * 0.4)
        if steps.width > 13.0:
            steps.scale_to_fit_width(13.0)
        s_arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.1, color=GREY_B,
                                  stroke_width=2.5, max_tip_length_to_length_ratio=0.25) for k in range(2)])
        s_cite = cite(r"after Gao, Schulman \& Hilton, \textit{Scaling laws for reward model overoptimization} "
                      r"(2023)")
        with self.voiceover(
            "Here is the experiment, after Gao, Schulman and Hilton of OpenAI. For each prompt, our fine-tuned model "
            "writes two hundred and fifty-six lines; <bookmark mark='p1'/> best-of-n picks with a reward model, "
            "<bookmark mark='p2'/> and we score the pick with both the reward model and gold, "
            "<bookmark mark='p3'/> against the square root of the KL. <bookmark mark='a'/> The "
            "reward model always believes things are getting better: by construction, its score of its own favourite "
            f"rises with n. <bookmark mark='b'/> Gold tells the truth. {small_said} <bookmark mark='c'/> "
            f"{large_said} A better reward model can be pushed harder before it breaks, but every learned reward "
            "breaks somewhere."
        ) as vo:
            self.play(FadeIn(steps[0]), FadeIn(s_cite))
            vo.wait_until("p1")
            self.play(GrowArrow(s_arrows[0]), FadeIn(steps[1]))
            vo.wait_until("p2")
            self.play(GrowArrow(s_arrows[1]), FadeIn(steps[2]))
            vo.wait_until("p3")
            self.play(FadeOut(steps), FadeOut(s_arrows), FadeOut(s_cite), run_time=0.6)
            self.play(FadeIn(g), FadeIn(g2), FadeIn(size), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(sp), Create(lp), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(sg), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lg_), run_time=2.0)
        self.wait(0.3)
        pick = said(ex[1], chars=50, font_size=18, max_lines=2)
        pq = said(f"Write a line about the {ex[0]}.", "user", chars=32, font_size=18)
        row = VGroup(pq, pick).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        if row.width > 13.4:
            row.width = 13.4
        pl = label(rf"the small reward model's favourite of all ${ns[-1]}$: \ it scores ${ex[2]:+.2f}$, \ "
                   rf"gold says ${ex[3]:+.2f}$", font_size=20, color=GREY_A).next_to(row, UP, buff=0.12)
        with self.voiceover(
            f"This is the line about the {ex[0]} that the small reward model liked best out of all two hundred and "
            "fifty-six."
        ):
            self.play(VGroup(g, g2, sp, sg, lp, lg_).animate.shift(UP * 0.5), FadeOut(tag), FadeOut(size),
                      FadeOut(marks))
            self.play(FadeIn(row), FadeIn(pl))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scaling(self):
        rows = [
            cmath(r"R_{\mathrm{BoN}}(d)", r"=", r"d\,(\alpha - \beta d)", font_size=38),
            cmath(r"R_{\mathrm{RL}}(d)", r"=", r"d\,(\alpha - \beta \log d)", font_size=38),
        ]
        for r_ in rows:
            r_[0].set_color(GOLD)
        whys = [why(r"$d = \sqrt{\mathrm{KL}}$: \ gold reward of best-of-$n$, \ a rise and a fall"),
                why(r"the same shape for RL, \ falling more slowly")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.6, buff=0.7, edge=6.9)
        hc = history_card(2023, r"Gao, Schulman \& Hilton, \textit{Scaling laws for reward model overoptimization}",
                          r"a large ``gold'' reward model plays the people; \ the coefficients improve smoothly with the "
                          r"proxy reward model's size, \ so the overoptimization can be predicted", width=6.0,
                          color=GOLD).move_to([3.6, -1.1, 0])
        # the two shapes, with made-up coefficients (schematic): best-of-n's parabola, RL's slower fall
        dd = np.linspace(0.001, 6.0, 200)
        g = axes([0, 6], [0, 1.6], x_length=5.4, y_length=2.6, xlabel=r"$d = \sqrt{\mathrm{KL}}$",
                 ylabel=r"gold reward", center=[-3.4, -1.1, 0])
        cb = curve(g.ax, dd[dd <= 4.0], dd[dd <= 4.0] * (1 - 0.25 * dd[dd <= 4.0]), GOLD, 4)
        cr = curve(g.ax, dd, np.clip(dd * (1 - 0.5 * np.log(dd)), 0, None), KLC, 4)
        lb = label(r"best-of-$n$", font_size=20, color=GOLD).next_to(g.ax.c2p(2, 1.0), UP, buff=0.12)
        lr = label(r"RL", font_size=20, color=KLC).next_to(g.ax.c2p(4.6, 4.6 * (1 - 0.5 * np.log(4.6))), UR, buff=0.08)
        stag = note(r"schematic: \ illustrative coefficients").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Gao and colleagues ran this at scale, with a large reward model playing the part of the people, and "
            "found that gold reward follows simple curves in the square root of the KL. For best-of-n, d times alpha "
            "minus beta d: up, then down. <bookmark mark='a'/> For reinforcement learning, the same with a "
            "logarithm, falling more slowly. <bookmark mark='b'/> The coefficients change smoothly with the size of "
            "the reward model, so how far it is safe to optimize can be predicted. In practice that is what the KL "
            "leash, and early stopping, are for."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(g), FadeIn(stag))
            step(0)
            self.play(Create(cb), FadeIn(lb))
            vo.wait_until("a")
            step(1)
            self.play(Create(cr), FadeIn(lr))
            vo.wait_until("b")
            self.play(Indicate(hc))
        self.wait(0.3)
        self.clear_scene()
