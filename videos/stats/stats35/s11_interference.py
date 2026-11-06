from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Interference(VoiceoverScene):
    def construct(self):
        self.card()
        self.herd()
        self.epidemic()
        self.design()
        self.effects()
        self.numbers()
        self.naive()
        self.exposure()

    def card(self):
        card = chapter_card(10, r"Interference", r"When your treatment affects me", lit=(2008,), part=PART)
        with self.voiceover("Chapter ten. Interference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def herd(self):
        rows = fit_rows(VGroup(
            label(r"a vaccine protects the vaccinated, \ and the people they would have infected", font_size=26),
            label(r"so my outcome depends on your vaccination: \ SUTVA fails", font_size=26, color=MISSC),
            label(r"also: \ classroom peers, \ job-training markets, \ social networks, \ online platforms", font_size=26, color=GREY_A),
            label(r"assume interference only within groups: \ partial interference \ (Sobel 2006)", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A vaccine protects the person vaccinated, and also the people that person would otherwise "
            "have infected. <bookmark mark='b'/> So my chance of infection depends on whether you were vaccinated, and "
            "SUTVA fails. <bookmark mark='c'/> The same happens with classroom peers, with job-training programmes whose "
            "graduates compete for the same jobs, in social networks, and on online platforms where sellers and buyers "
            "interact. <bookmark mark='d'/> A workable compromise, which Michael Sobel called partial interference in 2006, "
            "assumes that units affect each other only within groups, such as towns, and not across them."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def epidemic(self):
        d = load("interfere")
        rows = [
            cmath(r"P(\text{infected})", r"=", r"r_j \,(1 - 0.6\, v_i)\,(1 - 0.6\, s_j)", font_size=32),
            cmath(r"r_j", r":", r"\text{town } j\text{'s attack rate, \ about } 15\%", font_size=30),
            cmath(r"v_i, \ s_j", r":", r"\text{my vaccination; \ my town's vaccinated share}", font_size=30),
            cmath(r"\text{nobody vs everybody}", r":", rf"{100 * d['none']:.1f}\% \ \to \ {100 * d['all']:.1f}\%", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"the World's epidemic: \ 200 towns, \ 100 each"), why(r"larger in bigger towns"),
                why(r"a direct and a spillover effect"), why(r"the policy question")]
        with self.voiceover(
            "<bookmark mark='a'/> The World has an epidemic in its two hundred towns, with a hundred residents each in the "
            "study. A resident's chance of infection is the town's attack rate, times a factor for their own vaccination, "
            "times a factor for the share of their town that is vaccinated. <bookmark mark='b'/> Attack rates average about "
            "fifteen percent, higher in bigger towns. <bookmark mark='c'/> So the vaccine has a direct effect, through my "
            "own vaccination, and a spillover effect, through my neighbours'. <bookmark mark='d'/> With nobody vaccinated, "
            + say(100 * d["none"], 1) + " percent of residents are infected; with everybody, " + say(100 * d["all"], 1) + "."
        ) as vo:
            self.add(epi_tag())
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def design(self):
        xy = World().towns["xy"]
        g = np.random.default_rng(5)
        psi = np.zeros(len(xy), int)
        psi[g.choice(len(xy), len(xy) // 2, replace=False)] = 1
        dots = VGroup(*[Dot([0.62 * x - 2.0, 0.62 * y + 0.2, 0], radius=0.07, color=(Y1C if p else Y0C), fill_opacity=0.9)
                        for (x, y), p in zip(xy, psi)])
        side = fit_rows(VGroup(
            label(r"stage 1: \ each town gets a strategy", font_size=22),
            label(r"blue: \ vaccinate 30\%", font_size=22, color=Y0C),
            label(r"red: \ vaccinate 70\%", font_size=22, color=Y1C),
            label(r"stage 2: \ within each town, \ a lottery picks who", font_size=22, color=TAUC),
            label(r"Hudgens \& Halloran (2008)", font_size=20, color=GREY_A),
        ), 4.2, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> To learn both effects, randomize twice. Michael Hudgens and Elizabeth Halloran set out the "
            "two-stage design in 2008. First, each town is randomly given a strategy: <bookmark mark='b'/> vaccinate thirty "
            "percent of its residents, <bookmark mark='c'/> or seventy. <bookmark mark='d'/> Then, within each town, a "
            "lottery decides which residents receive the vaccine."
        ) as vo:
            self.add(epi_tag())
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def effects(self):
        rows = [
            cmath(r"\text{direct}(\psi)", r"=", r"\bar Y(0; \psi) - \bar Y(1; \psi)", font_size=32),
            cmath(r"\text{indirect}", r"=", r"\bar Y(0; 30\%) - \bar Y(0; 70\%)", font_size=32),
            cmath(r"\text{total}", r"=", r"\bar Y(0; 30\%) - \bar Y(1; 70\%)", font_size=32),
            cmath(r"\text{overall}", r"=", r"\bar Y(30\%) - \bar Y(70\%)", font_size=32),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"vaccinated vs not, \ same strategy"), why(r"the unvaccinated, \ across strategies: \ herd protection"),
                why(r"both together"), why(r"the policy comparison")]
        with self.voiceover(
            "<bookmark mark='a'/> Four effects can now be estimated, each a comparison of average infection rates. The "
            "direct effect compares vaccinated and unvaccinated residents within towns of the same strategy. <bookmark "
            "mark='b'/> The indirect, or spillover, effect compares unvaccinated residents of thirty-percent towns with "
            "unvaccinated residents of seventy-percent towns: protection from the neighbours alone. <bookmark mark='c'/> The "
            "total effect combines the two. <bookmark mark='d'/> And the overall effect compares whole towns under the two "
            "strategies, which is what a health ministry choosing a policy wants to know."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def numbers(self):
        d = load("interfere")
        e, t = d["est"], d["true_effects"]
        rows = [[r"effect \ (points of infection risk)", r"estimate", r"truth"],
                [r"direct, \ 30\% towns", rf"{100 * e['direct0']:.1f}", rf"{100 * t['direct0']:.1f}"],
                [r"direct, \ 70\% towns", rf"{100 * e['direct1']:.1f}", rf"{100 * t['direct1']:.1f}"],
                [r"indirect (spillover)", rf"{100 * e['indirect']:.1f}", rf"{100 * t['indirect']:.1f}"],
                [r"total", rf"{100 * e['total']:.1f}", rf"{100 * t['total']:.1f}"],
                [r"overall: \ 70\% vs 30\% towns", rf"{100 * e['overall']:.1f}", rf"{100 * t['overall']:.1f}"]]
        tab = table_rows(rows, font_size=26, col_buff=0.9, row_buff=0.28,
                         colors=[GREY_A, Y0C, Y0C, TAUC, BANDC, Y1C]).move_to([0, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One run of the two-stage trial, with the truth computed from the World's potential "
            "outcomes. <bookmark mark='b'/> The direct effect is about eight points in the thirty-percent towns, and smaller, "
            "about six, in the seventy-percent towns, where the unvaccinated are already protected by their neighbours. "
            "<bookmark mark='c'/> The spillover effect is about three to four points: an unvaccinated person is noticeably "
            "safer in a well-vaccinated town. <bookmark mark='d'/> The overall effect of the higher coverage policy is about "
            "five points of infection risk for the average resident."
        ) as vo:
            self.add(epi_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]))
        self.clear_scene()

    def naive(self):
        d = load("interfere")
        rows = fit_rows(VGroup(
            label(r"an ordinary trial: \ vaccinate a random half of everyone", font_size=26),
            label(rf"it estimates the direct effect at 50\% coverage: \ {100 * d['rct50']:.1f} points", font_size=26, color=Y0C),
            label(r"and is silent about the herd effect, \ the reason for mass vaccination", font_size=26, color=MISSC),
            label(r"worse: \ the direct effect itself depends on the coverage", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An ordinary individually randomized trial would vaccinate a random half of everyone. "
            "<bookmark mark='b'/> It estimates a direct effect, about " + say(100 * d["rct50"], 0) + " points here, at fifty "
            "percent coverage. <bookmark mark='c'/> It says nothing about the spillover, which is the main argument for "
            "vaccinating whole populations. <bookmark mark='d'/> Worse, its direct effect is specific to its own coverage: "
            "in a population with different coverage, the vaccine's direct effect is different."
        ) as vo:
            self.add(epi_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def exposure(self):
        rows = fit_rows(VGroup(
            label(r"general networks: \ exposure mappings, \ e.g. `treated, \ with $k$ treated friends'", font_size=26),
            label(r"Aronow \& Samii (2017): \ Horvitz--Thompson estimators with known exposure probabilities", font_size=26, color=GREY_A),
            label(r"markets and platforms: \ switchback and cluster designs (Part 58)", font_size=26, color=GREY_A),
            label(r"the lesson: \ define the estimand for the interference you believe in", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When the interference runs through a social network rather than fixed groups, the "
            "approach generalizes through exposure mappings, such as treated with k treated friends. <bookmark mark='b'/> "
            "Peter Aronow and Cyrus Samii showed in 2017 how to estimate effects of such exposures with Part 18's "
            "Horvitz–Thompson estimators, using each unit's known probability of each exposure under the design. <bookmark "
            "mark='c'/> Online marketplaces use switchback designs, randomizing over time, and cluster designs over "
            "geography. <bookmark mark='d'/> The lesson is to define the estimand for the interference you believe in, and "
            "randomize at the level it implies."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
