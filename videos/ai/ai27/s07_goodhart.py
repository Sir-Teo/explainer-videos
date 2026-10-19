from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import GOLD, KLC, PART, POLICY, PROXY, REWARD, load, said


class Goodhart(VoiceoverScene):
    def construct(self):
        self.card()
        self.law()
        self.bon_kl()
        self.curves()
        self.scaling()

    def card(self):
        card = chapter_card(6, r"When the measure becomes the target", r"How hard can you optimize a learned reward?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter six. When the measure becomes the target."):
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
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
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
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("bon")
        kl = np.asarray(d["kl"])
        x = np.sqrt(kl)
        ys = {k: np.asarray(d[k]) for k in ("small_proxy", "small_gold", "large_proxy", "large_gold")}
        lo = min(float(v.min()) for v in ys.values())
        hi = max(float(v.max()) for v in ys.values())
        g = axes([0, float(np.ceil(x.max() * 2) / 2)], [np.floor(lo * 4) / 4, np.ceil(hi * 4) / 4], x_length=7.4,
                 y_length=4.0, xlabel=r"$\sqrt{\mathrm{KL}}$ from the fine-tuned model \ (best-of-$n$, $n = 1 \dots 256$)",
                 ylabel=r"average score of the chosen line", xticks=[0, 1, 2], center=[-1.0, -0.2, 0])
        mk = lambda key, col, w, dash=False: (DashedVMobject if dash else (lambda m: m))(
            VMobject().set_points_as_corners([g.ax.c2p(a, b) for a, b in zip(x, ys[key])]).set_stroke(col, w))
        sp, sg = mk("small_proxy", PROXY, 3), mk("small_gold", GOLD, 4)
        lp, lg_ = mk("large_proxy", PROXY, 3), mk("large_gold", GOLD, 4)
        sp.set_stroke(opacity=0.55)
        sg.set_stroke(opacity=0.55)
        ns = list(d["ns"])
        rm = load("rm")
        key = legend([(PROXY, r"what the reward model thinks"), (GOLD, r"what gold thinks")], font_size=20)
        key.next_to(g, RIGHT, buff=0.3).shift(UP * 1.0)
        size = VGroup(label(rf"faint: \ reward model from ${int(rm['sizes'][0])}$ comparisons", font_size=18,
                            color=GREY_B),
                      label(rf"bold: \ from ${int(rm['sizes'][-1]):,}$".replace(",", "{,}"), font_size=18,
                            color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(key, DOWN, buff=0.3)
        size.align_to(key, LEFT)
        tag = note(r"computed: \ $256$ lines per prompt from our fine-tuned model, \ expectations over every "
                   r"subset of size $n$").to_corner(DR, buff=0.2)
        sgold, lgold = ys["small_gold"], ys["large_gold"]
        peak_s = int(np.argmax(sgold))
        if peak_s < len(ns) - 1 and sgold[-1] < sgold[peak_s] - 0.02:
            small_said = (f"With the small reward model, gold rises at first, peaks around n = {ns[peak_s]}, then "
                          f"falls back to {sgold[-1]:.2f} while the reward model's own score keeps climbing to "
                          f"{ys['small_proxy'][-1]:.2f}: over-optimization.")
        else:
            small_said = (f"With the small reward model, gold climbs only to {sgold[-1]:.2f} while the reward "
                          f"model's own score reaches {ys['small_proxy'][-1]:.2f}: the gap between them widens.")
        large_said = (f"The reward model trained on more comparisons tracks gold further: gold reaches "
                      f"{lgold.max():.2f}.")
        ex = d["examples"][0]
        with self.voiceover(
            "Here is the experiment, after Gao, Schulman and Hilton of OpenAI. For each prompt, our fine-tuned model "
            "writes two hundred and fifty-six lines; best-of-n picks with a reward model, and we score the pick "
            "with both the reward model and gold, against the square root of the KL. <bookmark mark='a'/> The "
            "reward model always believes things are getting better: by construction, its score of its own favourite "
            f"rises with n. <bookmark mark='b'/> Gold tells the truth. {small_said} <bookmark mark='c'/> "
            f"{large_said} A better reward model can be pushed harder before it breaks, but every learned reward "
            "breaks somewhere."
        ) as vo:
            self.play(FadeIn(g), FadeIn(key), FadeIn(tag), FadeIn(size))
            vo.wait_until("a")
            self.play(Create(sp), Create(lp), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(sg), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lg_), run_time=2.0)
        self.wait(0.3)
        pick = said(ex[1], chars=50, font_size=18, max_lines=2).to_edge(DOWN, buff=0.3)
        pl = label(rf"the small reward model's favourite line about the {ex[0]}: \ it scores ${ex[2]:+.2f}$, \ "
                   rf"gold says ${ex[3]:+.2f}$", font_size=20, color=GREY_A).next_to(pick, UP, buff=0.12)
        with self.voiceover(
            f"This is the line about the {ex[0]} that the small reward model liked best out of all two hundred and "
            "fifty-six."
        ):
            self.play(VGroup(g, sp, sg, lp, lg_, key, size).animate.shift(UP * 0.7), FadeOut(tag))
            self.play(FadeIn(pick), FadeIn(pl))
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
                          r"proxy reward model's size, \ so the overoptimization can be predicted", width=8.6,
                          color=GOLD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Gao and colleagues ran this at scale, with a large reward model playing the part of the people, and "
            "found that gold reward follows simple curves in the square root of the KL. For best-of-n, d times alpha "
            "minus beta d: up, then down. <bookmark mark='a'/> For reinforcement learning, the same with a "
            "logarithm, falling more slowly. <bookmark mark='b'/> The coefficients change smoothly with the size of "
            "the reward model, so how far it is safe to optimize can be predicted. In practice that is what the KL "
            "leash, and early stopping, are for."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
