from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


def plane(center=(-2.6, 0.0), s=1.0):
    """A stylized bomber seen from above: fuselage, wings, tail and four engine nacelles, as named regions."""
    cx, cy = center
    P = lambda x, y: np.array([cx + s * x, cy + s * y, 0])  # noqa: E731
    fus = Polygon(P(-0.35, 2.6), P(0.35, 2.6), P(0.4, 1.8), P(0.4, -2.2), P(0.15, -2.8), P(-0.15, -2.8), P(-0.4, -2.2), P(-0.4, 1.8),
                  stroke_color=GREY_B, stroke_width=2, fill_color=GREY_E, fill_opacity=0.6)
    wings = Polygon(P(-3.6, 0.2), P(-0.4, 0.9), P(0.4, 0.9), P(3.6, 0.2), P(3.6, -0.3), P(0.4, -0.1), P(-0.4, -0.1), P(-3.6, -0.3),
                    stroke_color=GREY_B, stroke_width=2, fill_color=GREY_E, fill_opacity=0.6)
    tail = Polygon(P(-1.3, -2.2), P(1.3, -2.2), P(1.3, -2.55), P(-1.3, -2.55), stroke_color=GREY_B, stroke_width=2,
                   fill_color=GREY_E, fill_opacity=0.6)
    engines = VGroup(*[Circle(radius=0.28 * s, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_E, fill_opacity=0.9).move_to(P(x, 0.45))
                       for x in (-2.3, -1.2, 1.2, 2.3)])
    fuel = VGroup(*[Rectangle(width=0.5 * s, height=0.3 * s, stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_E, fill_opacity=0.9).move_to(P(x, 0.2))
                    for x in (-0.75, 0.75)])
    return VGroup(wings, fus, tail, fuel, engines), P


def hits_in(region: str, k: int, P, g):
    pts = []
    while len(pts) < k:
        if region == "engines":
            ex = g.choice([-2.3, -1.2, 1.2, 2.3])
            r, th = 0.25 * np.sqrt(g.random()), g.uniform(0, 2 * np.pi)
            pts.append(P(ex + r * np.cos(th), 0.45 + r * np.sin(th)))
        elif region == "fuel system":
            ex = g.choice([-0.75, 0.75])
            pts.append(P(ex + g.uniform(-0.22, 0.22), 0.2 + g.uniform(-0.12, 0.12)))
        elif region == "fuselage":
            pts.append(P(g.uniform(-0.33, 0.33), g.uniform(-2.6, 2.5)))
        else:
            if g.random() < 0.8:
                x = g.uniform(-3.5, 3.5)
                if abs(x) < 0.45 or any(abs(x - e) < 0.32 for e in (-2.3, -1.2, 1.2, 2.3)):
                    continue
                pts.append(P(x, g.uniform(-0.2, 0.15)))
            else:
                pts.append(P(g.uniform(-1.25, 1.25), g.uniform(-2.5, -2.25)))
    return pts


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.holes()
        self.wald()
        self.table()
        self.legend()
        self.lesson()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1943,)).to_edge(UP, buff=0.35)
        hc = history_card(1943, r"Abraham Wald, \ \emph{A Method of Estimating Plane Vulnerability Based on Damage of Survivors}",
                          r"At Columbia University's Statistical Research Group, \ Wald was asked how to armour bombers. \ Armour is "
                          r"heavy, \ so it can go only where it does the most good. \ The data were the bullet holes in the planes that "
                          r"came back. \ The planes that did not come back, \ which carried the answer, \ could not be inspected",
                          color=MNC, width=11.2, font_size=22).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(r"the sample: \ only the survivors", font_size=24, color=MNC),
            label(r"the missing planes are missing \ because of \ what was done to them", font_size=24, color=GREY_A),
        ), 12.0, 0.35, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1943 Abraham Wald, a mathematician at Columbia University's Statistical Research "
            "Group, was asked where to put armour on bombers. Armour is heavy, so it can go only where it does the most "
            "good, and the data were the bullet holes in the planes that came back. <bookmark mark='b'/> The planes that "
            "did not come back, the ones that held the answer, could not be inspected. <bookmark mark='c'/> They were "
            "missing precisely because of what had happened to them."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def holes(self):
        d = load("wald")
        pl, P = plane(center=(-2.4, 0.2), s=0.95)
        g = np.random.Generator(np.random.PCG64(4111))
        scale = 220 / sum(d["ret_hits"])
        dots = VGroup()
        for a, k in zip(d["areas"], d["ret_hits"]):
            for p in hits_in(a, max(1, int(round(k * scale))), P, g):
                dots.add(Dot(p, radius=0.035, color=MISSC))
        side = fit_rows(VGroup(
            label(rf"{d['returned']:,} of {d['n']:,} planes came back", font_size=22),
            label(r"red: \ hits on the planes that returned", font_size=22, color=MISSC),
            label(r"many on the fuselage and wings", font_size=22, color=GREY_A),
            label(r"few on the engines", font_size=22, color=MNC),
            label(r"a stylized World of planes, \ not Wald's own data", font_size=20, color=GREY_B),
        ), 3.8, 0.42, [4.8, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A stylized version. Of two thousand bombers sent out, each hit a few times at random "
            "over its surface, " + f"{d['returned']:,}" + " came back. <bookmark mark='b'/> Here are the hits on the ones "
            "that returned. <bookmark mark='c'/> The fuselage and the wings are peppered. <bookmark mark='d'/> The "
            "engines have few holes. The obvious conclusion was to armour where the holes are."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(pl), FadeIn(side[0]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots], lag_ratio=0.01), FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*[Indicate(e, color=MNC) for e in pl[4]], FadeIn(side[3]))
        self.clear_scene()

    def wald(self):
        rows = fit_rows(VGroup(
            label(r"Wald: \ hits land roughly evenly over the plane", font_size=26),
            label(r"so the engines' missing holes are on the planes that did not return", font_size=26, color=MNC),
            label(r"armour where the survivors were \emph{not} hit", font_size=26, color=TAUC),
            label(r"and estimate each area's lethality from the deficit \ (Mangel \& Samaniego 1984)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Wald's reasoning: bullets and flak land roughly in proportion to area. <bookmark "
            "mark='b'/> So if the returning planes have few engine hits, the missing engine hits must be on the planes "
            "that did not return: a hit there brought the plane down. <bookmark mark='c'/> Armour the places where the "
            "survivors were not hit. <bookmark mark='d'/> Wald went further, and his memoranda, reconstructed by Marc "
            "Mangel and Francisco Samaniego in 1984, estimated how lethal a hit in each area was from the size of each "
            "deficit."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("wald")
        rows = [[r"area", r"share of surface", r"share of returners' hits", r"missing hits"]]
        for a, s_, r_, df in zip(d["areas"], d["share"], d["ret_share"], d["deficit"]):
            rows.append([a, f"{100 * s_:.0f}\\%", f"{100 * r_:.1f}\\%", f"{100 * df:+.0f}\\%" if df > 0 else f"{100 * df:.0f}\\%"])
        cols = [GREY_A] + [MNC if df > 0.1 else None for df in d["deficit"]]
        tab = table_rows(rows, font_size=26, col_buff=0.9, row_buff=0.34, colors=cols).move_to([0, 0.6, 0])
        foot = label(r"the engines carry 15\% of the surface but 10.5\% of the survivors' hits: \ the rest went down with their planes",
                     font_size=22, color=MNC).move_to([0, -2.0, 0])
        if foot.width > 12.4:
            foot.width = 12.4
        with self.voiceover(
            "<bookmark mark='a'/> The numbers. <bookmark mark='b'/> The engines are fifteen percent of the surface but "
            "carry only " + say(100 * d["ret_share"][0], 1) + " percent of the survivors' hits: thirty percent of the hits "
            "they should have are missing. The fuel system is short too. <bookmark mark='c'/> The fuselage and wings carry "
            "more than their share, because hits there were survivable. The holes we can see tell us where it is safe to be "
            "hit."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(r) for r in tab[1:]])
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"survivorship bias: \ the data that reach us were filtered by the outcome", font_size=26, color=MNC),
            label(r"funds that closed, \ patients who dropped out, \ people who did not answer", font_size=26),
            label(r"the questions: \ why is it missing? \ \ does it matter? \ \ what can be done?", font_size=26, color=TAUC),
            label(r"and its cousin: \ values we see, \ but wrongly \ (measurement error)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Survivorship bias: the data that reach us have been filtered by the very outcome we care "
            "about. <bookmark mark='b'/> Investment funds that closed vanish from the averages; patients who felt worst "
            "leave the trial; people with something to hide do not answer the survey. <bookmark mark='c'/> This part asks "
            "three questions: why is it missing, does it matter, and what can be done about it. <bookmark mark='d'/> And it "
            "ends with a cousin of missing data: values we do see, but wrongly."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 41", font_size=34, color=GREY_B), label(r"What You Didn't See", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Rubin's mechanisms: \ MCAR, \ MAR, \ MNAR; \ when missingness can be ignored",
            r"the easy methods' sins; \ EM and likelihood under MAR",
            r"multiple imputation and Rubin's rules; \ weighting as causal inference",
            r"MNAR: \ Heckman, \ pattern mixtures, \ tipping points; \ MRP",
            r"measurement error: \ attenuation, \ regression calibration, \ SIMEX, \ misclassification",
        ], color=TAUC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 18, \ 22 and 36").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.mi}; \ the mask grid; \ data: \ air quality, \ NHANES, \ Mroz").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-one: what you didn't see. <bookmark mark='b'/> We'll classify why data go "
            "missing and prove when the reason can be ignored; expose the easy fixes; use likelihood and EM; build multiple "
            "imputation and its rules; see weighting as causal inference; face data missing for reasons that matter, with "
            "Heckman's model and tipping points; repair a self-selected poll; and correct for measurement error."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

    def legend(self):
        rows = fit_rows(VGroup(
            label(r"the famous picture of a plane covered in red dots: \ drawn decades later", font_size=26, color=GREY_A),
            label(r"Wald's memoranda were equations: \ kill probabilities from hit counts", font_size=26, color=TAUC),
            label(r"he treated the unseen planes as data with a known cause of absence", font_size=26, color=MNC),
            label(r"the first modern analysis of data missing not at random", font_size=26, color=MIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A note on the legend. The famous picture of a returning bomber covered in red dots was drawn "
            "decades later, and the details of the story have grown in the retelling. <bookmark mark='b'/> Wald's actual "
            "memoranda were mathematics: from the counts of hits on returning planes, he derived estimates of the chance that "
            "a hit in each area would bring a plane down. <bookmark mark='c'/> He treated the planes that never came back as "
            "data, missing for a reason he could model. <bookmark mark='d'/> It is one of the first modern analyses of data "
            "missing not at random."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

