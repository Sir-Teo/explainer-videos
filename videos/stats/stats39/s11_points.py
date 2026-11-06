from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class Points(VoiceoverScene):
    def construct(self):
        self.card()
        self.snow_map()
        self.nearest()
        self.ripley()
        self.lplot()
        self.caveat()
        self.cox()

    def card(self):
        card = chapter_card(10, r"Point patterns", r"Where the events are", lit=(1855, 1976), part=PART)
        with self.voiceover("Chapter ten. Point patterns."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def _map(self, d, s=0.36, c=(-2.0, 0.0)):
        pts = np.vstack([np.asarray(d["deaths"], float), np.asarray(d["pumps"], float)])
        w = (pts[:, 0].min() - 0.4, pts[:, 0].max() + 0.4, pts[:, 1].min() - 0.4, pts[:, 1].max() + 0.4)
        cx, cy = (w[0] + w[1]) / 2, (w[2] + w[3]) / 2
        P = lambda a, b: np.array([(a - cx) * s + c[0], (b - cy) * s + c[1], 0])
        frame = Rectangle(width=(w[1] - w[0]) * s, height=(w[3] - w[2]) * s, stroke_color=GREY_D, stroke_width=1.5).move_to(P(cx, cy))
        return P, frame

    def snow_map(self):
        d = load("snow")
        P, frame = self._map(d)
        deaths = np.asarray(d["deaths"], float)
        pumps = np.asarray(d["pumps"], float)
        dd = VGroup(*[Dot(P(a, b), radius=0.035, color=PTC, fill_opacity=0.85) for a, b in deaths])
        pp = VGroup(*[Triangle(fill_color=Y0C, fill_opacity=1, stroke_width=0).scale(0.1).move_to(P(a, b)) for a, b in pumps])
        br = Triangle(fill_color=TAUC, fill_opacity=1, stroke_width=0).scale(0.16).move_to(P(*pumps[d["broad"]]))
        bl = label(r"Broad Street", font_size=20, color=TAUC).next_to(br, UP, buff=0.08)
        side = fit_rows(VGroup(
            label(r"London, \ August--September 1854", font_size=22),
            label(rf"red: \ {d['n']} cholera deaths, \ by house", font_size=22, color=PTC),
            label(r"blue: \ the 13 public water pumps", font_size=22, color=Y0C),
            label(r"gold: \ the Broad Street pump", font_size=22, color=TAUC),
            label(r"digitized by Waldo Tobler, \ from Snow's 1855 map", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In late August 1854 cholera killed hundreds of people in a few streets of Soho, in "
            "London. <bookmark mark='b'/> John Snow, whose natural experiment we met in Part thirty-seven, mapped every "
            "death, by house. <bookmark mark='c'/> He also marked the public water pumps, <bookmark mark='d'/> and the "
            "deaths crowded around one: the pump on Broad Street. <bookmark mark='e'/> These are his points, as digitized "
            "by Waldo Tobler, of the first law of geography."
        ) as vo:
            self.add(snowmap_tag())
            vo.wait_until("a")
            self.play(FadeIn(frame), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(br), FadeIn(bl), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def nearest(self):
        d = load("snow")
        P, frame = self._map(d)
        deaths = np.asarray(d["deaths"], float)
        pumps = np.asarray(d["pumps"], float)
        D = np.sqrt(((deaths[:, None, :] - pumps[None, :, :]) ** 2).sum(2))
        near = np.argmin(D, 1)
        dd = VGroup(*[Dot(P(a, b), radius=0.035, color=TAUC if k == d["broad"] else GREY_C, fill_opacity=0.9)
                      for (a, b), k in zip(deaths, near)])
        pp = VGroup(*[Triangle(fill_color=Y0C, fill_opacity=1, stroke_width=0).scale(0.1).move_to(P(a, b)) for a, b in pumps])
        cnt = np.asarray(d["counts"], int)
        order = np.argsort(-cnt)[:4]
        rows = [[r"nearest pump", r"deaths"]] + [[d["labels"][i].replace("#", r"\#"), f"{cnt[i]}"] for i in order]
        tab = table_rows(rows, font_size=22, col_buff=0.5, row_buff=0.22,
                         colors=[GREY_A] + [TAUC if i == d["broad"] else GREY_B for i in order]).move_to([4.9, 1.0, 0])
        foot = fit_rows(VGroup(
            label(rf"{100 * d['share_broad']:.0f}\% of the deaths are nearest Broad Street", font_size=22, color=TAUC),
            label(r"Snow had the pump's handle removed on 8 September", font_size=22, color=GREY_A),
        ), 3.8, 0.35, [4.9, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Assign each death to its nearest pump, as Snow did with a diagram of walking distances. "
            "<bookmark mark='b'/> " + str(cnt[d["broad"]]) + " of the " + str(d["n"]) + " deaths, " + str(round(100 * d["share_broad"]))
            + " percent, are nearest the Broad Street pump; the next pump has " + str(cnt[order[1]]) + ". <bookmark "
            "mark='c'/> Snow persuaded the parish to remove the pump's handle on the eighth of September. The epidemic was "
            "already declining, so the removal proved little by itself; the map, and the brewery and workhouse whose "
            "workers drank other water and were spared, made the case."
        ) as vo:
            self.add(snowmap_tag())
            vo.wait_until("a")
            self.play(FadeIn(frame), FadeIn(dd), FadeIn(pp))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def ripley(self):
        rows = [
            cmath(r"\text{CSR}", r":", r"\text{a homogeneous Poisson process: \ no clustering, \ no repulsion}", font_size=30),
            cmath(r"K(r)", r"=", r"\lambda^{-1} E[\#\text{ other points within } r \text{ of a typical point}]", font_size=30),
            cmath(r"\text{CSR}", r":", r"K(r) = \pi r^2, \ \ L(r) = \sqrt{K(r)/\pi} = r", font_size=30),
            cmath(r"L(r) - r", r":", r"> 0 \text{ clustered}, \ < 0 \text{ regular}", font_size=30),
        ]
        rows[1][-1].set_color(PTC)
        whys = [why(r"complete spatial randomness"), why(r"Ripley (1976)"), why(r"Besag's $L$: \ a straight line"),
                why(r"at every scale $r$")]
        with self.voiceover(
            "<bookmark mark='a'/> For points, the null model is complete spatial randomness: a Poisson process with "
            "constant intensity, where points neither attract nor repel. <bookmark mark='b'/> Brian Ripley's K function of "
            "1976 counts the expected number of other points within a distance r of a typical point, divided by the "
            "intensity. <bookmark mark='c'/> Under complete randomness it is the area of a disc, so its square-root version, "
            "Besag's L, is a straight line. <bookmark mark='d'/> L minus r above zero means clustering at that scale, below "
            "zero means regularity, like trees competing for light."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lplot(self):
        d = load("snow")
        r = np.asarray(d["r"], float)
        L, lo, hi = (np.asarray(d[k], float) for k in ("L", "lo", "hi"))
        A = axes([0, 3], [-0.2, 2.0], x_length=7.4, y_length=4.2, xlabel=r"distance $r$ \ (map units)", ylabel=r"$L(r) - r$",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1, 1.5, 2], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        env = band(ax, r, lo, hi, NULLC, 0.45)
        c = polyline(ax, r, L, PTC, 3)
        side = fit_rows(VGroup(
            label(r"grey: \ 95\% band from 199 CSR patterns", font_size=22, color=NULLC),
            label(r"red: \ Snow's deaths", font_size=22, color=PTC),
            label(r"far above at every scale: \ strongly clustered", font_size=22, color=PTC),
        ), 4.6, 0.45, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Simulate a hundred and ninety-nine random patterns of the same size in the same window, "
            "and the middle ninety-five percent of their L minus r curves form a thin band around zero. <bookmark "
            "mark='b'/> Snow's deaths lie far above it, <bookmark mark='c'/> at every scale: the deaths are strongly "
            "clustered."
        ) as vo:
            self.add(snowmap_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(env), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def caveat(self):
        rows = fit_rows(VGroup(
            label(r"but people do not live at random either", font_size=28, color=MISSC),
            label(r"deaths would cluster wherever the houses are, \ with or without a bad pump", font_size=26),
            label(r"the right null: \ an inhomogeneous process \ with intensity $\propto$ the population", font_size=26, color=TAUC),
            label(r"then: \ the inhomogeneous $K$ \ (Baddeley, \ M{\o}ller \& Waagepetersen 2000), \ or case--control designs", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But this test answers the wrong question. <bookmark mark='b'/> People do not live at "
            "random, so deaths would cluster wherever the houses are, with or without a contaminated pump. <bookmark "
            "mark='c'/> The right comparison is a process whose intensity follows the population at risk. <bookmark "
            "mark='d'/> Adrian Baddeley, Jesper Møller and Rasmus Waagepetersen's inhomogeneous K function does that, and "
            "epidemiologists compare the cases with controls drawn from the same population, as Snow in effect did by "
            "counting who drank from which pump."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def cox(self):
        rows = [
            cmath(r"\text{Poisson process}", r":", r"N(B) \sim \text{Poisson}\big(\textstyle\int_B \lambda(s)\, ds\big)", font_size=30),
            cmath(r"\text{Cox process}", r":", r"\lambda(s) \text{ itself random}", font_size=30),
            cmath(r"\text{log-Gaussian Cox}", r":", r"\log \lambda(s) = x(s)^\top\beta + W(s), \ \ W \text{ a GP}", font_size=30),
            cmath(r"\text{fit}", r":", r"\text{counts on a fine grid: \ a Poisson GLMM with a GMRF \ (INLA)}", font_size=28),
        ]
        rows[2][-1].set_color(FIELDC)
        whys = [why(r"independent counts in disjoint sets"), why(r"Cox (1955): \ doubly stochastic"),
                why(r"M{\o}ller et al.\ (1998)"), why(r"chapter 8 again")]
        with self.voiceover(
            "<bookmark mark='a'/> Models for points start from the Poisson process, whose counts in disjoint regions are "
            "independent Poisson variables with mean the integral of the intensity. <bookmark mark='b'/> David Cox in 1955 "
            "made the intensity itself random. <bookmark mark='c'/> In the log-Gaussian Cox process, the log intensity is "
            "a regression plus a Gaussian process: clustering comes from the hills of the hidden field. <bookmark "
            "mark='d'/> Counting the points on a fine grid turns it into a Poisson model with a Markov random field, so "
            "chapter eight's tools fit it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
