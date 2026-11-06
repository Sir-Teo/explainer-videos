from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class RegressionToMean(VoiceoverScene):
    def construct(self):
        self.card()
        self.world()
        self.both_ways()
        self.stable()
        self.slump()
        self.flight()

    def card(self):
        card = chapter_card(7, r"Regression to the mean", r"Not a force: \ a fact about imperfect correlation", lit=(1886,), part=PART)
        with self.voiceover("Chapter seven. Regression to the mean."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def world(self):
        d = load("regression")
        rows = VGroup(
            label(r"the World's tallest tenth of mid-parents:", font_size=28),
            MathTex(rf"\text{{mid-parent: }} +{d['mid_dev']:.1f}\ \text{{cm above average}}", font_size=32, color=MARG),
            MathTex(rf"\text{{their sons: }} +{d['ch_dev']:.1f}\ \text{{cm}}", font_size=32, color=COND),
            MathTex(rf"\text{{ratio}}\ {d['ratio']:.2f} \ \approx\ \text{{the slope}}\ {d['slope']:.2f}", font_size=30, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.6, 0])
        q = label(r"is the population becoming more average? \ no: \ its spread does not shrink", font_size=26, color=S.ACCENT)
        q.to_edge(DOWN, buff=0.7)
        tag = simulated_tag()
        intro = label("The World's tallest mid-parents", font_size=36)
        with self.voiceover(
            "Regression to the mean appears in the World too. <bookmark mark='a'/> Take the tallest tenth of "
            f"mid-parents: on average {d['mid_dev']:.1f} centimetres above the mean. <bookmark mark='b'/> Their sons are "
            f"tall, but only {d['ch_dev']:.1f} centimetres above average. <bookmark mark='c'/> The ratio is close to the "
            "regression slope. <bookmark mark='d'/> Does that mean the population is converging to the average, "
            "generation by generation? No: the World's sons are just as spread out as their fathers. Galton was "
            "puzzled by exactly this. The resolution is that regression is not a force; it's a property of a "
            "conditional mean when the correlation is imperfect."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn((VGroup(rows[0], rows[1]), rows[2], rows[3])[k], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.clear_scene()

    def both_ways(self):
        d = load("galton")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        g = np.random.Generator(np.random.PCG64(2))
        jx, jy = x + g.uniform(-0.45, 0.45, len(x)), y + g.uniform(-0.45, 0.45, len(y))
        A = axes([63, 74], [61, 75], x_length=5.6, y_length=5.0, xlabel=r"mid-parent (in)", ylabel=r"child (in)",
                 xticks=[64, 68, 72], yticks=[62, 66, 70, 74], center=[-3.4, -0.4, 0])
        ax = A.ax
        pts = scatter(ax, jx, jy, color=DATA, radius=0.02, opacity=0.5)
        P = np.asarray(d["P"])
        C = np.asarray(d["C"])
        tall_c = y >= 72.2
        mean_par_tall = float(x[tall_c].mean())
        rows = VGroup(
            label(r"tallest children ($\ge 72.2$ in):", font_size=26),
            MathTex(rf"\text{{their mid-parents average }} {mean_par_tall:.2f}", font_size=28, color=COND),
            MathTex(rf"\text{{vs. children }} {y[tall_c].mean():.2f};\ \ \text{{mean mid-parent}}\ {d['mx']:.2f}", font_size=26, color=GREY_A),
            label(r"parents regress toward the mean of \emph{their} generation too", font_size=26, color=S.ACCENT),
            label(r"time has no direction here: \ it is the ellipse", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.2, 0.3, 0])
        band = Rectangle(width=ax.c2p(74, 0)[0] - ax.c2p(63, 0)[0], height=ax.c2p(0, 75)[1] - ax.c2p(0, 72)[1], stroke_width=0,
                         fill_color=COND, fill_opacity=0.15).move_to(ax.c2p(68.5, 73.5))
        src = historical_tag(r"Galton (1886), jittered within cells", corner=DR)
        with self.voiceover(
            "The clearest proof that it isn't a force: it runs backwards. <bookmark mark='a'/> In Galton's data, take "
            "the tallest children instead. <bookmark mark='b'/> Their parents were tall too, but less extreme: the "
            "parents regress toward their generation's mean. <bookmark mark='c'/> If regression were a biological "
            "force pulling families toward the average, it couldn't act backwards in time. It's simply what happens "
            "for a bivariate Gaussian: select on one being extreme in standard units, and the other will on average "
            "be less so. It's the shape of the ellipse."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pts, lag_ratio=0.001), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        _ = (P, C)
        self.clear_scene()

    def slump(self):
        d = load("regression")
        t1, t2 = np.asarray(d["t1"]), np.asarray(d["t2"])
        A = axes([-4, 4], [-4, 4], x_length=5.0, y_length=5.0, xlabel=r"test 1", ylabel=r"test 2", xticks=[-2, 0, 2],
                 yticks=[-2, 0, 2], center=[-3.6, -0.4, 0])
        ax = A.ax
        pts = scatter(ax, t1, t2, color=SIM, radius=0.02, opacity=0.5)
        rows = VGroup(
            MathTex(r"\text{score} = \text{skill} + \text{luck}", font_size=32),
            MathTex(rf"\operatorname{{corr}}(\text{{test 1}}, \text{{test 2}}) = {d['r12']:.2f}", font_size=28, color=GREY_A),
            MathTex(rf"\text{{top tenth on test 1: }} {d['best_t1']:.2f} \to {d['best_t2']:.2f}", font_size=28, color=S.RESID),
            MathTex(rf"\text{{bottom tenth: }} {d['worst_t1']:.2f} \to {d['worst_t2']:.2f}", font_size=28, color=S.LIK),
            label(r"the rookie of the year's second season; \ the cover jinx;", font_size=24, color=GREY_B),
            label(r"the treatment that ``works'' on the worst cases", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 0.2, 0])
        for r in rows:
            if r.width > 6.4:
                r.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 0.2, 0])  # re-align after clamping
        tag = note(r"simulated: 10,000 people, \ $(\text{skill}+\text{luck})/\sqrt2$; independent standard-normal components").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Regression to the mean fools people constantly. <bookmark mark='a'/> Suppose a test score is skill plus "
            "luck, in equal measure. Ten thousand people take two tests; their scores correlate at about a half. "
            f"<bookmark mark='b'/> The top tenth on the first test averaged {d['best_t1']:.2f} standard deviations above "
            f"the mean. On the second test they fall to about {d['best_t2']:.2f}. <bookmark mark='c'/> The bottom tenth "
            "improve by the same amount. Nobody changed; the luck that put them in the extreme group didn't repeat. "
            "<bookmark mark='d'/> That's the sophomore slump, the magazine-cover jinx, and the false success of any "
            "treatment given to the people who did worst, who would have improved anyway. Part 35's randomized "
            "controls exist partly to defeat it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pts, lag_ratio=0.001), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4:]))
        self.clear_scene()

    def flight(self):
        hc = history_card(r"1960s", r"Daniel Kahneman and the Israeli Air Force flight instructors",
                          r"``praise makes cadets worse, \ and punishment makes them better'': \ after an exceptionally good "
                          r"landing, the next is usually worse, \ whatever the instructor says", color=S.MUSEUM, width=8.4,
                          font_size=24).move_to([0, 1.0, 0])
        cite = note(r"D. Kahneman, \emph{Thinking, Fast and Slow} (2011), ch.~17; \ Tversky \& Kahneman (1974)").to_edge(DOWN, buff=0.5)
        moral = label(r"to learn whether something works, \ compare with what would have happened anyway", font_size=28,
                      color=S.ACCENT).move_to([0, -1.4, 0])
        intro = label("Kahneman's flight instructors", font_size=36)
        with self.voiceover(
            "Daniel Kahneman told a story about this. <bookmark mark='a'/> Lecturing to flight instructors in the "
            "Israeli Air Force, he said praise works better than punishment. An instructor objected: whenever he "
            "praised a cadet for an exceptionally smooth landing, the next one was worse; whenever he shouted at a "
            "cadet for a bad one, the next was better. <bookmark mark='b'/> He was seeing regression to the mean. "
            "Exceptional performances are partly luck, and are usually followed by more ordinary ones, whatever the "
            "instructor says. <bookmark mark='c'/> The moral reaches through the whole degree: to learn whether "
            "something works, you must compare with what would have happened anyway."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def stable(self):
        e = load("extras")["stable"]
        rows = [
            cmath(r"\mathrm{Var}(\text{child})", r"=", r"b^2\,\mathrm{Var}(\text{mid-parent})", r"+", r"\mathrm{Var}(\text{residual})", font_size=32),
            cmath(rf"{e['vy']:.2f}", r"=", rf"{e['b2vx']:.2f}", r"+", rf"{e['res']:.2f}", font_size=38),
        ]
        for r in rows:
            r[2].set_color(COND)
            r[4].set_color(S.RESID)
        whys = [why(r"OLS variance decomposition: residual $\perp$ fitted value"), why(r"Galton's table")]
        txt = VGroup(label(r"regression shrinks the predictable part toward the mean,", font_size=26),
                     label(r"and the unpredictable part spreads it out again:", font_size=26),
                     label(r"regression alone does not force a shrinking population spread", font_size=26, color=S.ACCENT))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.7)
        intro = label('Regression need not shrink the population', font_size=36)
        with self.voiceover(
            "Galton's own puzzle was this: if children regress toward the mean, why doesn't the population become "
            "more uniform every generation? Eve's law answers it. <bookmark mark='a'/> A child's height is the "
            "predictable part, the slope times the parents' deviation, plus a residual. Their variances add. "
            "<bookmark mark='b'/> In Galton's data, the predictable part has shrunk to a variance of about one point "
            "three, but the residual adds five, and together they give back the children's full variance. "
            "<bookmark mark='c'/> Regression pulls the predictable part toward the mean, and fresh, unpredictable "
            "variation spreads it out again: there is no necessary shrinking of the population spread. The table itself is not evidence about many generations."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=0.7, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(txt))
        self.clear_scene()
