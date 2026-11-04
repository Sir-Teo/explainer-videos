from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


def island_outline(scale, center):
    t = np.linspace(0, 2 * np.pi, 240)
    wob = 0.86 + 0.1 * np.sin(3 * t + 0.7) + 0.05 * np.cos(5 * t)
    e = 2 / 2.6
    x = 5 * wob * np.sign(np.cos(t)) * np.abs(np.cos(t)) ** e * 1.04
    y = 3.4 * wob * np.sign(np.sin(t)) * np.abs(np.sin(t)) ** e * 1.04
    pts = [np.array([scale * a, scale * b, 0]) + center for a, b in zip(x, y)]
    return Polygon(*pts, stroke_color=S.WORLD, stroke_width=2, fill_color="#14261C", fill_opacity=0.9)


class TheWorld(VoiceoverScene):
    def construct(self):
        self.card()
        self.island()
        self.people()
        self.truth()
        self.seeds()

    def card(self):
        card = chapter_card(2, r"Building the World", r"A population whose truth we know", lit=(), part=PART)
        with self.voiceover("Chapter two. Building the World."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def island(self):
        d = load("world")
        sc, cen = 0.78, np.array([-2.3, -0.3, 0])
        land = island_outline(sc, cen)
        xy, pop, reg = np.asarray(d["xy"]), np.asarray(d["pop"]), np.asarray(d["region"])
        towns = VGroup(*[Circle(radius=0.025 + 0.42 * np.sqrt(p / pop.max()), stroke_width=1,
                                stroke_color=REGION_COLORS[r], fill_color=REGION_COLORS[r], fill_opacity=0.55)
                         .move_to(np.array([sc * x, sc * y, 0]) + cen) for (x, y), p, r in zip(xy, pop, reg)])
        order = np.argsort(-pop)
        stats_ = VGroup(
            label(rf"{fmt_int(d['n'])} residents", font_size=34),
            label(rf"{d['n_towns']} towns, \ {d['n_regions']} regions", font_size=30, color=GREY_A),
            label(rf"largest town: \ {fmt_int(d['largest_town'])}", font_size=26, color=GREY_A),
            label(rf"smallest: \ {fmt_int(d['smallest_town'])}", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.9, 1.2, 0])
        why_card = definition_card(r"Why build a world?", r"In real data the truth is hidden. \ Here every "
                                   r"parameter is a number we can compute, \ so every method can be graded.",
                                   color=S.WORLD, width=4.6, font_size=22).move_to([4.9, -1.8, 0])
        tag = simulated_tag()
        with self.voiceover(
            "Statistics has a teaching problem. Its methods promise things about the truth, and in real data "
            "the truth is never available to check them against. <bookmark mark='a'/> So we're going to build a "
            "population whose truth we do know. We'll call it the World. <bookmark mark='b'/> It's an island of "
            f"two hundred towns in ten regions, with {money(d['n'])} residents. A few towns are cities; the largest "
            f"has {money(d['largest_town'])} people, the smallest {money(d['smallest_town'])}, the way real "
            "settlements follow a power law. <bookmark mark='c'/> Every resident is a row of numbers: age, sex, "
            "height, income, and, as the series goes on, a school, a clinic, a vote, a lifetime, a genome. "
            "<bookmark mark='d'/> Because we generated every one of those numbers, every parameter is something we "
            "can compute exactly, and every method in the series can be graded against it, not just applied."
        ) as vo:
            self.play(DrawBorderThenFill(land), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(towns[i]) for i in order], lag_ratio=0.012), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, shift=LEFT * 0.2) for s_ in stats_], lag_ratio=0.3))
            self.play(Indicate(towns[int(order[0])], color=WHITE, scale_factor=1.3))
            vo.wait_until("d")
            self.play(FadeIn(why_card, shift=UP * 0.2))
        self.play(FadeOut(VGroup(land, towns, stats_, why_card)))
        self.tag = tag

    def people(self):
        d = load("world")
        edges = np.asarray(d["age_edges"])
        men, women = np.asarray(d["age_men"]), np.asarray(d["age_women"])
        top = max(men.max(), women.max())
        pyr = VGroup()
        bh = 0.17
        for i in range(len(men)):
            y = -2.6 + i * (bh + 0.02)
            wm, ww = 1.9 * men[i] / top, 1.9 * women[i] / top
            pyr.add(Rectangle(width=wm, height=bh, stroke_width=0, fill_color=MEN, fill_opacity=0.85)
                    .move_to([-4.6 - wm / 2, y, 0]))
            pyr.add(Rectangle(width=ww, height=bh, stroke_width=0, fill_color=WOMEN, fill_opacity=0.85)
                    .move_to([-4.6 + ww / 2, y, 0]))
        ages = VGroup(*[label(str(a), font_size=18, color=GREY_B).move_to([-6.85, -2.6 + (a // 5) * (bh + 0.02), 0])
                        for a in (0, 20, 40, 60, 80)])
        for a in ages:
            a.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.03)
        pt = label(r"ages", font_size=26, color=GREY_A).move_to([-4.6, 1.6, 0])
        mw = VGroup(label(r"men", font_size=22, color=MEN).move_to([-5.8, 1.2, 0]),
                    label(r"women", font_size=22, color=WOMEN).move_to([-3.4, 1.2, 0]))
        # heights
        he, hh = np.asarray(d["height_hist_edges"]), np.asarray(d["height_hist"])
        H = axes([140, 205], [0, hh.max() * 1.15], x_length=4.2, y_length=2.4, xlabel=r"adult height (cm)",
                 xticks=[150, 170, 190], center=[0.0, 0.6, 0])
        hb = hist_bars(H.ax, he, hh, color=S.TRUTH, opacity=0.7, stroke_width=0)
        hcap = label(rf"men {d['mean_height_men']:.1f}, \ women {d['mean_height_women']:.1f}", font_size=22,
                     color=GREY_A).next_to(H, DOWN, buff=0.1)
        # incomes
        sh = load("shape")
        lh = np.asarray(sh["lin_hist"])
        I2 = axes([0, 300], [0, lh.max() * 1.15], x_length=4.2, y_length=2.4, xlabel=r"adult income (thousands)",
                  xticks=[0, 100, 200, 300], center=[4.55, 0.6, 0])
        ib = hist_bars(I2.ax, np.linspace(0, 300, 61), lh, color=S.TRUTH, opacity=0.7, stroke_width=0)
        mean_l = vline(I2.ax, d["mean_income"] / 1000, MEAN, stroke_width=3)
        med_l = vline(I2.ax, d["median_income"] / 1000, MEDIAN, stroke_width=3)
        icap = VGroup(label(rf"median {money(d['median_income'])}", font_size=22, color=MEDIAN),
                      label(rf"mean {money(d['mean_income'])}", font_size=22, color=MEAN)).arrange(RIGHT, buff=0.4)
        icap.next_to(I2, DOWN, buff=0.1)
        with self.voiceover(
            "Who lives there? <bookmark mark='a'/> Here's the World's age pyramid: men to the left, women to the "
            "right, five-year bands, a slowly ageing population like most rich countries today. "
            "<bookmark mark='b'/> Their heights: men average "
            f"{d['mean_height_men']:.1f} centimetres and women {d['mean_height_women']:.1f}, drawn from bell "
            "curves, though as we'll see the mixture of the two isn't quite one. <bookmark mark='c'/> Their incomes "
            "look nothing like a bell. Most people earn modest amounts, and a long tail stretches far to the right: "
            f"the richest adult makes {money(d['max_income'])} a year. <bookmark mark='d'/> That tail drags the "
            f"mean, {money(d['mean_income'])}, well above the median, {money(d['median_income'])}, which is the "
            "income of the person exactly in the middle. Which of the two is the typical income is a question "
            "we'll answer properly in chapter four."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, RIGHT if j % 2 == 0 else LEFT) for j, r in enumerate(pyr)],
                                  lag_ratio=0.02), FadeIn(ages), FadeIn(pt), FadeIn(mw), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(H), LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb], lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(hcap))
            vo.wait_until("c")
            self.play(FadeIn(I2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in ib], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(med_l), Create(mean_l), FadeIn(icap))
        self.play(FadeOut(VGroup(pyr, ages, pt, mw, H, hb, hcap, I2, ib, mean_l, med_l, icap)))

    def truth(self):
        d = load("world")
        rows = [
            (r"mean adult height", rf"{d['mean_height']:.2f}\ \text{{cm}}"),
            (r"SD of adult height", rf"{d['sd_height']:.2f}\ \text{{cm}}"),
            (r"median adult income", rf"{fmt_int(d['median_income'])}"),
            (r"mean adult income", rf"{fmt_int(round(d['mean_income']))}"),
            (r"share earned by the top 1\%", rf"{100 * d['share_top1']:.1f}\%"),
        ]
        tab = VGroup()
        for name, val in rows:
            tab.add(VGroup(label(name, font_size=30, color=GREY_A), MathTex(val, font_size=36, color=S.TRUTH)))
        for r in tab:
            r[1].next_to(r[0], RIGHT, buff=0.6)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        vals = VGroup(*[r[1] for r in tab])
        x_right = max(v.get_right()[0] for v in vals)
        for v in vals:
            v.shift(RIGHT * (x_right - v.get_right()[0]))
        title = label(r"The truth, \ exactly", font_size=44, color=S.TRUTH)
        box = VGroup(title, tab).arrange(DOWN, buff=0.5).move_to([-2.2, 0.3, 0])
        later = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (
            r"families and heights \ (Part 5)", r"schools \ (Parts 25, 26)", r"a clinic \ (chapter 12; Part 35)",
            r"surveys and nonresponse \ (Parts 18, 41)", r"lifetimes \ (Part 40)", r"a pollution field \ (Part 39)",
            r"a genome \ (Parts 32, 33)")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lt = label(r"coming blocks", font_size=28, color=S.WORLD)
        lg = VGroup(lt, later).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.2, 0])
        with self.voiceover(
            "So here is something you can never write in real life: the truth. <bookmark mark='a'/> The mean adult "
            f"height in the World is {d['mean_height']:.2f} centimetres, and its standard deviation "
            f"{d['sd_height']:.2f}. The median income is {money(d['median_income'])}, the mean "
            f"{money(round(d['mean_income']))}, and the top one percent of earners take {pct(d['share_top1'])} "
            "percent of all income. <bookmark mark='b'/> These aren't estimates. Each is computed from all million "
            "residents: the population is finite, and these are its exact values. When a sample's average comes "
            "out at one hundred and sixty-eight point six, we'll know precisely how wrong it is. "
            "<bookmark mark='c'/> The World grows as the series does. Families arrive in Part 5, schools in Part "
            "25, surveys whose respondents aren't random, a clinic whose doctors treat the sickest patients "
            "(you'll visit it in chapter twelve), lifetimes, a pollution field, a genome. Each block is added without changing anything "
            "already there."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in tab], lag_ratio=0.4), run_time=4.0)
            vo.wait_until("b")
            self.play(Indicate(vals, color=S.TRUTH, scale_factor=1.08))
            vo.wait_until("c")
            self.play(FadeIn(lt), LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in later], lag_ratio=0.3),
                      run_time=4.0)
        self.play(FadeOut(VGroup(box, lg)))

    def seeds(self):
        code = code_block([
            "world = World(seed=1662)",
            "stream = SeedSequence([1662, crc32('height')])",
            "z = Generator(PCG64(stream)).standard_normal(N)",
            "height = where(male, 176 + 7.1 z, 163 + 6.4 z)",
        ], font_size=24).move_to([0, 1.4, 0])
        blocks = VGroup()
        for i, name in enumerate(["geography", "age", "sex", "height", "income", "families", "clinic"]):
            b = RoundedRectangle(width=1.7, height=0.7, corner_radius=0.1, stroke_color=S.WORLD, stroke_width=1.5,
                                 fill_color=S.WORLD, fill_opacity=0.12)
            t = Text(name, font="DejaVu Sans Mono", font_size=20, color=WHITE).move_to(b)
            blocks.add(VGroup(b, t))
        blocks.arrange(RIGHT, buff=0.18).move_to([0, -1.0, 0])
        caveat = label(r"the World teaches about methods, \ not about people; \ real data live in the Museum",
                       font_size=26, color=S.MUSEUM).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Two promises about the World itself. <bookmark mark='a'/> It's reproducible. Everything comes from one "
            "seed, sixteen sixty-two, after Graunt's book, so the same World is rebuilt on any computer. "
            "<bookmark mark='b'/> And it's stable. Each block, geography, ages, heights, incomes, draws from its own "
            "random stream, derived from the seed and the block's name. So when a later part adds a new block, "
            "nothing already in the World changes: a number shown in Part 1 is still true in Part 40. "
            "<bookmark mark='c'/> And one honest caveat. The World is simulated. It's a laboratory for learning how "
            "methods behave, not evidence about real people. For that, the series keeps a museum of real historical "
            "data, like Graunt's Bills, each with its source on screen."
        ) as vo:
            self.play(FadeIn(code, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(code[0] if len(code) else code, color=S.WORLD, scale_factor=1.04))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in blocks], lag_ratio=0.2))
            nb = VGroup(RoundedRectangle(width=1.7, height=0.7, corner_radius=0.1, stroke_color=S.ACCENT,
                                         stroke_width=2, fill_color=S.ACCENT, fill_opacity=0.15),
                        Text("schools", font="DejaVu Sans Mono", font_size=20, color=S.ACCENT))
            nb[1].move_to(nb[0])
            row = VGroup(*blocks, nb).arrange(RIGHT, buff=0.14).move_to([0, -1.0, 0])
            if row.width > 13.4:
                row.width = 13.4
            self.play(FadeIn(nb, shift=DOWN * 0.3))
            self.play(*[Indicate(b, color=S.WORLD, scale_factor=1.05) for b in blocks])
            vo.wait_until("c")
            self.play(FadeIn(caveat))
        self.clear_scene()
