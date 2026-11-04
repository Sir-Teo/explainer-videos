from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403

MEN, WOMEN = "#6FA8DC", "#E59AB8"


class Latent(VoiceoverScene):
    def construct(self):
        self.card()
        self.heights()
        self.marginalize()
        self.posterior()
        self.simpson()

    def card(self):
        card = chapter_card(10, r"Latent variables", r"A variable you never see, \ shaping the ones you do", lit=(1894,), part=PART)
        with self.voiceover("Chapter ten. Latent variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def heights(self):
        d = load("latent")
        xs, ed, hist = np.asarray(d["xs"]), np.asarray(d["edges"]), np.asarray(d["hist"])
        A = axes([140, 205], [0, 0.05], x_length=8.4, y_length=4.2, xlabel=r"adult height (cm)", xticks=[150, 160, 170, 180, 190, 200],
                 center=[-1.6, -0.6, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        h = hist_bars(ax, ed, hist, color=GREY_C, opacity=0.6)
        fm = curve(ax, xs, np.asarray(d["fm"]), MEN, 3)
        ff = curve(ax, xs, np.asarray(d["ff"]), WOMEN, 3)
        mix = curve(ax, xs, np.asarray(d["mix"]), EXACT, 3.5)
        rows = VGroup(
            MathTex(rf"\text{{men: }} {d['mu_m']:.1f} \pm {d['sd_m']:.1f}", font_size=28, color=MEN),
            MathTex(rf"\text{{women: }} {d['mu_f']:.1f} \pm {d['sd_f']:.1f}", font_size=28, color=WOMEN),
            MathTex(rf"\text{{everyone: SD }} {d['sd_all']:.1f}", font_size=28, color=EXACT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.4)
        tag = simulated_tag()
        with self.voiceover(
            "Some variables shape the data without appearing in it. <bookmark mark='a'/> Here are the heights of all "
            "the World's adults. <bookmark mark='b'/> The histogram is a blend of two normal curves, one for men and "
            "one for women, each weighted by about a half. <bookmark mark='c'/> Their mixture, gold, matches the "
            "histogram. The overall standard deviation, over nine centimetres, is larger than either group's, because "
            "it includes the gap between the groups: Eve's law again. If the data didn't record sex, it would be a "
            "latent variable: present in the process, absent from the table."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h))
            vo.wait_until("b")
            self.play(Create(fm), Create(ff), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(Create(mix), FadeIn(rows[2]))
        self.clear_scene()

    def marginalize(self):
        rows = [
            cmath(r"f(x)", r"=", r"\sum_k P(Z = k)\, f(x \mid Z = k)", font_size=36),
            cmath(r"f(x)", r"=", r"\pi\, \phi\Big(\frac{x - \mu_1}{\sigma_1}\Big)\frac{1}{\sigma_1} + (1 - \pi)\, \phi\Big(\frac{x - \mu_2}"
                  r"{\sigma_2}\Big)\frac{1}{\sigma_2}", font_size=30),
        ]
        rows[0][2].set_color(EXACT)
        whys = [why(r"marginalize the latent class $Z$"), why(r"a two-component normal mixture")]
        hist = history_card(1894, r"Karl Pearson, \ Naples crabs", r"Weldon's forehead measurements of 1,000 crabs: \ fitted as a "
                            r"mixture of two normals by the method of moments, \ suspecting two subspecies", color=S.MUSEUM,
                            width=7.0, font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In symbols, a latent class Z with probabilities pi k, and given the class a density for x. "
            "<bookmark mark='a'/> Marginalize the class away: sum over it, weighting by its probabilities. "
            "<bookmark mark='b'/> With two normal components it's the two-component mixture. <bookmark mark='c'/> "
            "Karl Pearson fitted one in 1894 to Raphael Weldon's measurements of crabs from the Bay of Naples, "
            "suspecting two subspecies, solving a ninth-degree polynomial by hand to match the moments. Today mixtures "
            "are fitted by the EM algorithm of Part 22, and the latent variables of factor analysis and topic models "
            "grow from this one formula."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.clear_scene()

    def posterior(self):
        d = load("latent")
        xs, fm, ff = np.asarray(d["xs"]), np.asarray(d["fm"]), np.asarray(d["ff"])
        post = fm / (fm + ff)
        A = axes([140, 205], [0, 1.05], x_length=8.0, y_length=3.8, xlabel=r"height (cm)", ylabel=r"$P(\text{man} \mid \text{height})$",
                 xticks=[150, 160, 170, 180, 190, 200], yticks=[0, 0.5, 1], center=[-1.8, -0.6, 0])
        ax = A.ax
        cv = curve(ax, xs, post, MEN, 3.5)
        half = DashedLine(ax.c2p(140, 0.5), ax.c2p(205, 0.5), color=GREY_C, stroke_width=1.5)
        x_half = float(np.interp(0.5, post, xs))
        mark = Dot(ax.c2p(x_half, 0.5), radius=0.08, color=EXACT)
        ml = MathTex(rf"{x_half:.1f}\ \text{{cm}}", font_size=26, color=EXACT).next_to(mark, UR, buff=0.1)
        f = MathTex(r"P(Z = k \mid x)", r"=", r"\frac{\pi_k f(x \mid k)}{\sum_j \pi_j f(x \mid j)}", font_size=32).to_corner(UR, buff=0.4)
        f[0].set_color(COND)
        note_ = label(r"Bayes' theorem for the latent class: \ the ``E'' step of EM", font_size=22, color=GREY_B).next_to(f, DOWN, buff=0.2)
        note_.align_to(f, RIGHT)
        with self.voiceover(
            "Going the other way, the data tell us about the latent class. <bookmark mark='a'/> Given only a "
            "height, the chance that the person is a man is Bayes' theorem: the man's component at that height, over "
            "the total. <bookmark mark='b'/> It rises smoothly from near zero for short adults to near one for tall "
            f"ones, crossing a half at about {x_half:.0f} centimetres. These posterior class probabilities are the "
            "expectation step of the EM algorithm."
        ) as vo:
            self.play(FadeIn(A), Create(half))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(note_))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(mark), FadeIn(ml))
        self.clear_scene()

    def simpson(self):
        e = load("extras")["clinic"]
        card = upgrade_card(1, r"in the World's clinic, the treated recovered less often overall but more often within "
                            r"each severity", r"that the reversal was a curiosity of tables", r"severity is a latent variable "
                            r"that the treatment depends on: marginalizing it mixes two very different groups", width=10.6,
                            font_size=23).to_edge(UP, buff=0.35)
        rows = VGroup(
            MathTex(rf"P(\text{{recover}} \mid \text{{treated}}) = {e['t_all']:.3f}", r"\quad<\quad",
                    rf"P(\text{{recover}} \mid \text{{not}}) = {e['c_all']:.3f}", font_size=28),
            MathTex(r"=", rf"\underbrace{{{e['p_sev_t']:.2f}}}_{{P(\text{{severe}} \mid \text{{treated}})}} \times {e['t_sev']:.3f}",
                    rf"+ {1 - e['p_sev_t']:.2f} \times {e['t_mild']:.3f}", font_size=28),
            MathTex(r"\text{vs.}", rf"\ {e['p_sev_c']:.2f} \times {e['c_sev']:.3f} + {1 - e['p_sev_c']:.2f} \times {e['c_mild']:.3f}",
                    font_size=28),
            label(r"the mixing weights differ, \ because doctors treat the sicker patients", font_size=24, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.0, 0])
        rows[0][0].set_color(S.TREAT)
        rows[0][2].set_color(S.CTRL)
        tag = simulated_tag(r"simulated: the World's clinic (Part 1)")
        with self.voiceover(
            "Latent variables explain a paradox from Part 1. <bookmark mark='a'/> In the World's clinic, the treated "
            "recovered less often overall, yet more often within each level of severity. <bookmark mark='b'/> "
            "Marginalizing over severity mixes the severe and the mild. <bookmark mark='c'/> For the treated, the "
            "overall rate is a mixture weighted mostly toward the severe, sixty-three percent of them, because doctors "
            "treat the sicker patients; <bookmark mark='d'/> for the untreated, a mixture weighted toward the mild. "
            "Different weights on very different groups reverse the comparison. Simpson's paradox is a latent "
            "variable that the treatment depends on, and Part 36 shows when we can adjust for it."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=DOWN * 0.2), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()
