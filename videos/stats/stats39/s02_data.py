from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class SpatialData(VoiceoverScene):
    def construct(self):
        self.card()
        self.tobler()
        self.kinds()
        self.meuse_map()
        self.world_map()
        self.model()
        self.neff()

    def card(self):
        card = chapter_card(1, r"Spatial data", r"Near things are more related", lit=(1970,), part=PART)
        with self.voiceover("Chapter one. Spatial data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def tobler(self):
        q = label(r"\emph{``Everything is related to everything else, \ but near things are more related than distant things.''}",
                  font_size=28, color=GREY_A).move_to([0, 1.2, 0])
        if q.width > 12.4:
            q.width = 12.4
        rows = fit_rows(VGroup(
            label(r"Waldo Tobler (1970): \ the first law of geography", font_size=26, color=TAUC),
            label(r"it breaks independence, \ and it makes prediction possible", font_size=26, color=FIELDC),
        ), 12.4, 0.5, [0, -1.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Waldo Tobler, a geographer, wrote in 1970: everything is related to everything else, but "
            "near things are more related than distant things. <bookmark mark='b'/> He called it the first law of geography. "
            "<bookmark mark='c'/> It is the reason spatial data break the independence that most of statistics assumes, and "
            "the reason prediction at unmeasured places is possible at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def kinds(self):
        rows = [[r"kind", r"what is random", r"examples", r"chapters"],
                [r"geostatistical", r"a field, \ seen at chosen sites", r"zinc, \ pollution, \ rainfall", r"2--8"],
                [r"areal (lattice)", r"values for fixed regions", r"disease rates by district", r"9"],
                [r"point patterns", r"where the events are", r"cases, \ trees, \ crimes", r"10"]]
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.36, colors=[GREY_A, FIELDC, AREAC, PTC]).move_to([0, 0.5, 0])
        foot = label(r"Cressie (1993): \ the three kinds of spatial data", font_size=22, color=GREY_A).move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Noel Cressie's textbook sorts spatial data into three kinds. <bookmark mark='b'/> "
            "Geostatistical data: a field that exists everywhere, measured at chosen sites, such as zinc in soil or pollution "
            "in air. <bookmark mark='c'/> Areal or lattice data: one value for each of a fixed set of regions, such as disease "
            "rates by district. <bookmark mark='d'/> And point patterns, where the locations themselves are the random part: "
            "where the cases occurred, where the trees grow."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def meuse_map(self):
        d = load("meuse")
        x, y, z = (np.asarray(d[k], float) for k in ("x", "y", "z"))
        riv = np.asarray(d["river"], float) / 1000
        cx, cy = 180.0, 331.65
        s = 1.75
        P = lambda a, b: np.array([(a - cx) * s - 1.6, (b - cy) * s + 0.1, 0])
        lo, hi = float(z.min()), float(z.max())
        F = FieldSurface([lo, hi], [0, 0], [lo, hi], 0.1, width=1.0)
        dots = VGroup(*[Dot(P(a, b), radius=0.04 + 0.05 * (v - lo) / (hi - lo), color=F.colour(v)) for a, b, v in zip(x, y, z)])
        rv = VMobject(stroke_color=Y0C, stroke_width=2, stroke_opacity=0.7)
        k = (riv[:, 0] > 178.4) & (riv[:, 0] < 181.6) & (riv[:, 1] > 329.6) & (riv[:, 1] < 333.8)
        rv.set_points_as_corners([P(a, b) for a, b in riv[k]])
        side = fit_rows(VGroup(
            label(r"155 topsoil samples, \ Stein, \ NL", font_size=24),
            label(r"zinc: \ 113 to 1,839 ppm \ (log scale)", font_size=24, color=FIELDC),
            label(r"blue: \ the river Meuse", font_size=24, color=Y0C),
            label(r"high by the river, \ low inland", font_size=24, color=GREY_A),
        ), 4.2, 0.45, [4.6, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A real field. In 1993 Mathieu Rikken and Ruud van Rijn sampled the topsoil at a hundred "
            "and fifty-five places in a flood plain of the river Meuse, near the Dutch village of Stein, and measured heavy "
            "metals. <bookmark mark='b'/> Here is zinc, with bigger, brighter dots for higher concentrations, on a log "
            "scale. <bookmark mark='c'/> The river, in blue, deposits contaminated sediment when it floods. <bookmark "
            "mark='d'/> So zinc is high near the river and low inland: a trend, plus deviations that are themselves "
            "correlated between neighbouring samples."
        ) as vo:
            self.add(meuse_tag())
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(rv), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def world_map(self):
        d = load("world")
        px, py, truth = (np.asarray(d[k], float) for k in ("px", "py", "truth"))
        F = FieldSurface(px, py, truth, 0.2, width=8.0, center=[-1.8, 0.3, 0])
        st = F.dots(np.asarray(d["sx"], float), np.asarray(d["sy"], float), WHITE, 0.04)
        key = F.key(r"pollution ($\mu$g/m$^3$)").move_to([4.6, -2.0, 0])
        side = fit_rows(VGroup(
            label(r"20 + 3 $\times$ traffic", font_size=24, color=FIELDC),
            label(r"\ \ + a Mat\'ern field", font_size=24, color=FIELDC),
            label(r"traffic: \ high by the big towns", font_size=24),
            label(r"300 stations, \ error SD 0.8", font_size=24, color=GREY_A),
        ), 3.6, 0.42, [4.7, 1.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And the World's field, which we will keep using because, unlike Meuse, its truth is known "
            "everywhere. Fine-particle pollution is twenty units, plus three times a traffic index that is high around the "
            "big towns, plus a smooth random field. <bookmark mark='b'/> It is highest in the cities, and varies smoothly "
            "between them. <bookmark mark='c'/> Three hundred stations measure it, each with a small measurement error."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(F), FadeIn(key), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(st), FadeIn(side[3]))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"Z(s)", r"=", r"\mu(s) + W(s) + \varepsilon(s)", font_size=34),
            cmath(r"\mu(s)", r"=", r"x(s)^\top \beta \quad \text{(trend: \ river distance, \ traffic)}", font_size=30),
            cmath(r"W(s)", r":", r"\text{a zero-mean random field, \ } \text{Cov}(W(s), W(s')) = C(s - s')", font_size=30),
            cmath(r"\varepsilon(s)", r":", r"\text{independent noise: \ the nugget}", font_size=30),
        ]
        rows[2][-1].set_color(FIELDC)
        whys = [why(r"the geostatistical model"), why(r"large-scale variation"), why(r"small-scale, \ correlated"),
                why(r"measurement error, \ micro-scale")]
        with self.voiceover(
            "<bookmark mark='a'/> The standard model writes the value at location s as three parts. <bookmark mark='b'/> A "
            "trend, a regression on covariates such as distance to the river or traffic. <bookmark mark='c'/> A random "
            "field with mean zero, whose covariance between two places depends on how far apart they are. <bookmark "
            "mark='d'/> And independent noise, which geostatisticians call the nugget, after the nuggets of gold that make "
            "two samples a few centimetres apart differ."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def neff(self):
        d = load("extra")
        rows = [
            cmath(r"\text{Var}(\bar Z)", r"=", r"\tfrac{1}{n^2} \textstyle\sum_{i,j} C(s_i - s_j)", font_size=32),
            cmath(r"n_{\text{eff}}", r"=", r"\text{Var}(Z)\,/\,\text{Var}(\bar Z)", font_size=32),
            cmath(r"\text{the World}", r":", rf"300 \text{{ stations}}, \ n_{{\text{{eff}}}} = {d['n_eff']:.1f}", font_size=32),
            cmath(r"\text{SE of the mean}", r":", rf"{d['se_true']:.2f}, \ \text{{not}} \ \sigma/\sqrt{{n}} = {d['se_naive']:.2f}", font_size=32),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"every pair's covariance counts"), why(r"the effective sample size"), why(r"the true covariance"),
                why(r"seven times wider")]
        with self.voiceover(
            "<bookmark mark='a'/> Why does dependence matter? The variance of an average is a sum over every pair of "
            "observations of their covariance, not just the n variances. <bookmark mark='b'/> Divide the variance of one "
            "value by it, and we get the effective sample size: the number of independent values the average is worth. "
            "<bookmark mark='c'/> For the World's three hundred stations, with the true covariance, it is " + say(d["n_eff"], 1)
            + ". On an island only a few ranges wide, the stations mostly repeat one another about the island-wide level. "
            "<bookmark mark='d'/> The honest standard error of their mean is " + say(d["se_true"], 2) + ", seven times the "
            "textbook formula's " + say(d["se_naive"], 2) + ". Prediction at a place is a different matter: there, nearby "
            "stations are exactly what we want."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
