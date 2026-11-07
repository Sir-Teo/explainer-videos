from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403


class Exploration(VoiceoverScene):
    def construct(self):
        self.card()
        self.pressure()
        self.sodium()
        self.by_age()
        self.energy()
        self.deciles()
        self.lessons()

    def card(self):
        card = chapter_card(4, r"Exploration", r"Look before you model", part=PART)
        with self.voiceover("Chapter four. Exploration."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pressure(self):
        d = load("explore")
        e, h = np.asarray(d["edges_sbp"], float), np.asarray(d["hist_sbp"])
        A = axes([80, 200], [0, 0.16], x_length=8.6, y_length=4.2, xlabel=r"systolic pressure, \ mm Hg (weighted)",
                 ylabel=r"share of adults", xticks=[80, 100, 120, 140, 160, 180, 200], yticks=[0, 0.05, 0.1, 0.15],
                 center=[-1.4, 0.3, 0], yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        bars = hist_bars(ax, e, h, color=BP)
        q = d["q_sbp"]
        line = DashedLine(ax.c2p(130, 0), ax.c2p(130, 0.16), color=OBS, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"3,071 adults not on BP medicine", font_size=22),
            label(rf"median {q[1]:.0f}; \ 10\% below {q[0]:.0f}, \ 10\% above {q[2]:.0f}", font_size=22, color=BP),
            label(r"skewed right: \ a long tail of high pressure", font_size=22),
            label(rf"dashed: \ 130, \ the line for ``high'' since 2017: \ {100 * d['share_130']:.0f}\% above", font_size=22, color=OBS),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "Exploration means looking at the data before any model, to learn their shapes and find surprises. "
            "<bookmark mark='a'/> First the outcome, weighted to the population. <bookmark mark='b'/> The median systolic "
            "pressure is a hundred and eighteen; one adult in ten is below a hundred and three, one in ten above a hundred and "
            "forty-one. <bookmark mark='c'/> The distribution is skewed to the right, with a long tail of high pressures, even "
            "among people not being treated. <bookmark mark='d'/> Since 2017 American guidelines call a systolic pressure of "
            "a hundred and thirty or more high; twenty-four percent of these untreated adults are above it."
        ) as vo:
            self.add(nh_tag(corner=DR))
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(line), FadeIn(rows[3]))
        self.clear_scene()

    def sodium(self):
        d = load("explore")
        e, h = np.asarray(d["edges_na"], float), np.asarray(d["hist_na"])
        A = axes([0, 10], [0, 0.07], x_length=8.6, y_length=4.2, xlabel=r"sodium on the recall day, \ g (weighted)",
                 ylabel=r"share of adults", xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.02, 0.04, 0.06], center=[-1.4, 0.3, 0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        bars = hist_bars(ax, e, h, color=SALT)
        guide = DashedLine(ax.c2p(2.3, 0), ax.c2p(2.3, 0.07), color=HIT, stroke_width=2.5)
        q = d["q_na"]
        rows = fit_rows(VGroup(
            label(rf"median {q[1]:.2f} g; \ mean {d['mean_na']:.2f} g", font_size=22, color=SALT),
            label(rf"10\% below {q[0]:.1f} g, \ 10\% above {q[2]:.1f} g", font_size=22),
            label(rf"green: \ the 2.3 g guideline; \ {100 * d['share_over_2300']:.0f}\% above", font_size=22, color=HIT),
            label(r"skewed too; \ and one day is not a usual day", font_size=22, color=RES),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Then the exposure. On the recall day the median adult ate three point two six grams of "
            "sodium, and the mean is three point five five. <bookmark mark='b'/> The spread is wide: a tenth ate under one point "
            "six, a tenth over five point eight. <bookmark mark='c'/> Seventy-six percent were above the guideline that day. "
            "<bookmark mark='d'/> But remember chapter one's warning: much of this spread is day-to-day variation, not a "
            "difference between people. A histogram of usual intake would be narrower."
        ) as vo:
            self.play(FadeIn(A), Create(guide))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def by_age(self):
        d = load("explore")
        mids = [25, 35, 45, 55, 65, 75]
        A = axes([20, 80], [105, 140], x_length=5.4, y_length=3.8, xlabel=r"age", ylabel=r"mean systolic, \ mm Hg",
                 xticks=[20, 40, 60, 80], yticks=[110, 120, 130, 140], center=[-3.6, 0.3, 0], font_size=18)
        B = axes([20, 80], [2.5, 4.5], x_length=5.4, y_length=3.8, xlabel=r"age", ylabel=r"mean sodium, \ g",
                 xticks=[20, 40, 60, 80], yticks=[2.5, 3, 3.5, 4, 4.5], center=[3.4, 0.3, 0], font_size=18)
        lines = VGroup()
        for ax, key in ((A.ax, "by_age"), (B.ax, "na_by_age")):
            for sx, col in (("men", BLUE), ("women", RED)):
                ys = d[key][sx]
                lines.add(VGroup(polyline(ax, mids, ys, col, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=col) for a, b in zip(mids, ys)]))
        key = VGroup(label(r"men", font_size=22, color=BLUE), label(r"women", font_size=22, color=RED)).arrange(RIGHT, buff=0.6)
        key.to_edge(UP, buff=0.4)
        foot = fit_rows(VGroup(
            label(r"pressure rises with age; \ sodium falls with age", font_size=24, color=OBS),
            label(r"so age pulls the crude slope down: \ a confounder in the opposite direction", font_size=22, color=RES),
        ), 12.4, 0.2, [0, -2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now relationships. On the left, mean systolic pressure by decade of age, men in "
            "blue, women in red. It rises steadily with age; men are higher until their fifties, and women overtake "
            "them after seventy. <bookmark mark='b'/> On the right, mean sodium by age. Men report more sodium than "
            "women in this sample, and both eat less as they age. <bookmark mark='c'/> Put those together: older "
            "people have higher pressure and eat less salt. So in the raw data, age alone produces a negative "
            "relationship between salt and pressure. That's the crude slope of minus point one four from the hook: a "
            "confounder pushing in the opposite direction from the effect we're looking for."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines[2]), Create(lines[3]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def energy(self):
        d = load("explore")
        A = axes([0, 5], [0, 10], x_length=6.4, y_length=4.4, xlabel=r"energy on the recall day, \ 1,000 kcal",
                 ylabel=r"sodium, \ g", xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 2, 4, 6, 8, 10], center=[-2.6, 0.3, 0])
        ax = A.ax
        kc, na = np.asarray(d["kcal_sub"]), np.asarray(d["na_sub"])
        m = (kc < 5) & (na < 10)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=SALT, fill_opacity=0.7) for a, b in zip(kc[m], na[m])])
        b = np.polyfit(kc, na, 1)
        line = Line(ax.c2p(0.3, b[1] + 0.3 * b[0]), ax.c2p(4.8, b[1] + 4.8 * b[0]), color=DES, stroke_width=4)
        rows = fit_rows(VGroup(
            label(rf"correlation {d['r_na_kcal']:.2f}", font_size=26, color=DES),
            label(rf"more food, \ more salt: \ about {b[0]:.1f} g per 1,000 kcal", font_size=22),
            label(r"energy also tracks body size, \ activity, \ and sex", font_size=22, color=GREY_A),
            label(r"adjusting for energy: \ salt per calorie, \ the epidemiologist's habit (Willett)", font_size=22, color=OBS),
            label(r"but it leaves little sodium variation to learn from", font_size=22, color=RES),
        ), 4.9, 0.4, [3.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Next, sodium against total energy on the same day. The correlation is point seven five. "
            "<bookmark mark='b'/> People who eat more food eat more salt, about one and a half grams per thousand kilocalories. "
            "<bookmark mark='c'/> And energy intake goes with body size, physical activity and sex, which have their own links "
            "to pressure. <bookmark mark='d'/> That's why nutritional epidemiologists, following Walter Willett, adjust for "
            "energy, so that the question becomes the saltiness of the diet rather than its size. <bookmark mark='e'/> The "
            "cost: once energy is held fixed, much less of the variation in sodium is left to learn from, and a lot of what's "
            "left is day-to-day noise."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.002), Create(line), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def deciles(self):
        d = load("explore")
        dec = d["deciles"]
        xs = np.arange(1, 11)
        A = axes([0.5, 10.5], [100, 140], x_length=8.4, y_length=4.2, xlabel=r"sodium decile on the recall day",
                 ylabel=r"mean systolic, \ mm Hg", xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], yticks=[100, 110, 120, 130, 140],
                 center=[-1.4, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(x, r["sbp"]), radius=0.08, color=BP) for x, r in zip(xs, dec)])
        bars = VGroup(*[Line(ax.c2p(x, r["sbp"] - 2 * r["se"]), ax.c2p(x, r["sbp"] + 2 * r["se"]), color=BP, stroke_width=2)
                        for x, r in zip(xs, dec)])
        rows = fit_rows(VGroup(
            label(rf"lowest decile: \ {dec[0]['na']:.1f} g, \ {dec[0]['sbp']:.0f} mm Hg", font_size=22),
            label(rf"highest decile: \ {dec[-1]['na']:.1f} g, \ {dec[-1]['sbp']:.0f} mm Hg", font_size=22),
            label(r"a six-fold range of sodium; \ no visible trend", font_size=22, color=OBS),
            label(r"bars: \ $\pm 2$ design SE; \ estimated decile cuts treated as fixed", font_size=20, color=GREY_B),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And the relationship itself, without assuming a straight line: mean pressure in "
            "each tenth of the sodium distribution. The lowest tenth averaged one point two grams and a hundred and "
            "twenty millimetres. <bookmark mark='b'/> The highest averaged seven point three grams and a hundred and "
            "twenty-two. <bookmark mark='c'/> Across a six-fold range of sodium there is no visible trend, only "
            "noise. <bookmark mark='d'/> The bars now use design-based standard errors, with the other PSUs retained "
            "as zero domain contributions. They describe an unadjusted association; they do not bound a causal "
            "effect."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.1), FadeIn(bars), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"pressure: \ skewed, \ rising with age, \ different for men and women", font_size=24, color=BP),
            label(r"sodium: \ skewed, \ noisy, \ falling with age, \ tied to energy", font_size=24, color=SALT),
            label(r"confounders push in both directions", font_size=24, color=OBS),
            label(r"the raw picture is flat: \ the model must hold the others fixed", font_size=24),
            label(r"we looked, \ but we change nothing in the plan because of what we saw", font_size=22, color=RES),
        ), 12.4, 0.5, [0, 0, 0])
        intro = label('Exploration reveals patterns without identifying their causes', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> What did we learn? Pressure is skewed, rises with age, and differs between men and women. "
            "<bookmark mark='b'/> Sodium is skewed, noisy, falls with age, and tracks energy. <bookmark mark='c'/> The "
            "confounders push in different directions, <bookmark mark='d'/> so the raw picture can't answer the question; a model "
            "must compare like with like. <bookmark mark='e'/> And one discipline: we looked at everything, but we don't change "
            "the plan because of what we saw. If we did, the plan would no longer protect us."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
