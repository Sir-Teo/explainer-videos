from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ concentration, \ non-competes, \ high minimums", r"What is still unsettled?",
             "Chapter fifteen. Frontier: concentration, non-competes, high minimums.",
             lit={2003: r"Manning", 2024: r"California's \$20"}, scale=("firm", "nation"), horizon=("a decade",))
        self.real_minimum()
        self.questions()

    def real_minimum(self):
        F = load("film")
        t, v = np.array(F["t"]), np.array(F["v"])
        ax = plane([1938, 2026], [0, 22], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[1940, 1960, 1980, 2000, 2020], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"dollars an hour, \ 2025 prices", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}",
                   font_size=14)
        ln = path(ax, t, v, WAGE, 3.2, smooth=False)
        ca = dot(ax, 2024.5, 20, LOSS, 0.1)
        cal = label(r"California's fast food, \ 2024: \ \$20", font_size=16, color=LOSS).next_to(
            ax.ax.c2p(2024.5, 20), LEFT, buff=0.15)
        fed = label(rf"the federal minimum: \ \${F['last_nominal']:.2f} since 2009", font_size=17, color=WAGE).next_to(
            ax.ax.c2p(2010, v[-1]), DOWN, buff=0.35)
        side = VGroup(
            label(rf"its real peak: \ \${F['peak']:.2f}, \ {F['peak_y']}", font_size=18, color=WAGE),
            label(r"many states and cities \\ now set their own, \\ far above it", font_size=18, color=WHITE),
            label(r"Seattle's lesson: \\ the effects grow \\ with the level", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Department of Labor and BLS, \ via FRED; \ California AB 1228", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier begins with the level. <bookmark mark='a'/> America's federal minimum has been "
            f"{F['last_nominal']:.2f} dollars an hour since 2009; in today's prices it peaked at "
            f"{F['peak']:.2f} in {F['peak_y']}. <bookmark mark='b'/> States and cities now set their own, and some are "
            "far above anything studied in the 1990s: in 2024 California set twenty dollars for large fast-food "
            "chains. <bookmark mark='c'/> The evidence of this part was gathered mostly at moderate levels, and "
            "Seattle suggests the effects grow with the level. Where the line lies is the question for the next "
            "decade."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(fed), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(ca, scale=1.5), FadeIn(cal), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"employer concentration: \ do few employers in a town mean lower pay?", font_size=21, color=MCL),
            label(r"non-competes: \ contracts that stop workers taking a rival's job", font_size=21, color=LOSS),
            label(r"high minimums: \ where do the job losses begin?", font_size=21, color=NJ),
            label(r"the return to college: \ for whom, \ and is it falling?", font_size=21, color=SCHOOL),
            label(r"platform work: \ flexible hours, \ and who sets the pay", font_size=21, color=SUPPLY),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(r"Manning (2003); \ Sokolova and Sorensen (2021)", corner=DR, font_size=12)
        with self.voiceover(
            "The open questions. <bookmark mark='a'/> Employer concentration: where a few firms do most of a town's "
            "hiring, are wages lower, and should antitrust care about labour markets as well as product markets? "
            "<bookmark mark='b'/> Non-compete agreements, which stop workers from joining a rival: in 2024 America's "
            "Federal Trade Commission adopted a rule banning most of them, but a federal court set it aside, and it "
            "never took effect. <bookmark mark='c'/> High minimums: where do the losses begin? "
            "<bookmark mark='d'/> The "
            "return to college: is it falling for the marginal student? <bookmark mark='e'/> And platform work, where "
            "hours are free and the platform sets the pay."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
