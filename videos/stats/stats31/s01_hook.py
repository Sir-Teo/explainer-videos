from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.roads()
        self.torgerson()
        self.rebuild()
        self.europe()
        self.error()
        self.stress()
        self.lesson()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1952,)).to_edge(UP, buff=0.35)
        hc = history_card(1952, r"Warren Torgerson, \ \emph{Psychometrika}",
                          r"`Multidimensional scaling: \ I. Theory and method.' \ Given only the distances between "
                          r"things, \ recover where the things are: \ points in a space whose distances match",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"no coordinates, \ no map: \ only a table of distances", font_size=24),
            label(r"can the map be rebuilt from the table alone?", font_size=24, color=PATH),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Suppose you are given no map at all, only a table: the distance by road between every pair "
            "of towns. <bookmark mark='b'/> Can you rebuild the map? <bookmark mark='c'/> In 1952 the psychologist Warren "
            "Torgerson showed how, for a very different purpose: people judge how similar things feel, and he wanted to "
            "place those judgements as points in a space whose distances match them. This part is about the structure "
            "hidden in many variables, and this is its first and most visual example."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def roads(self):
        d = load("towns")
        xy = np.asarray(d["xy"])
        dm = DistanceMap(xy, xy, width=7.6, height=5.2, center=[-2.0, 0.2, 0], edges=[tuple(e) for e in d["edges"]],
                         sizes=np.asarray(d["weight"]))
        rows = fit_rows(VGroup(
            label(rf"the World's {d['n']} towns", font_size=22),
            label(r"roads to each town's four nearest neighbours", font_size=22, color=GREY_B),
            label(r"each road 10--30\% longer than straight", font_size=22, color=GREY_B),
            label(rf"road distance: \ the shortest route; \ {d['pairs']:,} of them", font_size=22),
            label(rf"a typical route is {d['detour']:.1f} times the straight line", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World has two hundred towns on its island. <bookmark mark='b'/> Roads join each town to "
            "its four nearest neighbours, and every road winds, ten to thirty percent longer than the straight line. "
            "<bookmark mark='c'/> The road distance between two towns is the length of the shortest route through the "
            "network: nineteen thousand nine hundred distances in all. <bookmark mark='d'/> A typical route is almost twice "
            "the straight-line distance, because it zigzags from town to town. Now throw the map away and keep only the "
            "table."
        ) as vo:
            self.add(world_tag())
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in dm.truth], lag_ratio=0.005), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(dm.roads), FadeIn(rows[1]), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def torgerson(self):
        rows = [
            cmath(r"d_{ij}^2", r"=", r"\|x_i\|^2 + \|x_j\|^2 - 2 x_i^\top x_j", font_size=32),
            cmath(r"B", r"=", r"-\tfrac12 J D^{(2)} J, \ \ J = I - \tfrac1n \mathbf 1 \mathbf 1^\top", font_size=30),
            cmath(r"B", r"=", r"X X^\top \ \ \text{if the distances are Euclidean}", font_size=30),
            cmath(r"\hat X", r"=", r"V_2 \Lambda_2^{1/2}: \ \text{the top two eigenvectors}", font_size=30),
        ]
        rows[1][2].set_color(MAPC)
        whys = [why(r"distances hide inner products"), why(r"double-centring removes the norms"),
                why(r"a Gram matrix, \ Part 4"), why(r"the best rank-2 Gram matrix")]
        with self.voiceover(
            "<bookmark mark='a'/> The trick is the cosine rule. A squared distance is two squared lengths minus twice an inner "
            "product. <bookmark mark='b'/> Subtract the row means and the column means of the squared distances and add back "
            "the grand mean, double-centring, and halve: the lengths cancel, leaving a matrix of inner products about the "
            "centroid. <bookmark mark='c'/> If the distances come from real points, that matrix is X times X transpose, Part "
            "4's Gram matrix. <bookmark mark='d'/> So its top eigenvectors, scaled by root eigenvalue, are the coordinates: "
            "the best two-dimensional configuration, up to rotation and reflection."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rebuild(self):
        d = load("towns")
        xy, fit = np.asarray(d["xy"]), np.asarray(d["fitted"])
        dm = DistanceMap(xy, fit, width=7.6, height=5.2, center=[-2.0, 0.2, 0], sizes=np.asarray(d["weight"]))
        rows = fit_rows(VGroup(
            label(r"blue: \ the map rebuilt from road distances", font_size=22, color=PCC),
            label(r"rotated and scaled onto the truth \ (Procrustes)", font_size=22, color=GREY_B),
            label(r"gold rings: \ where the towns really are", font_size=22, color=TRUE),
            label(rf"typical error {d['rmse']:.2f} on an island 10 wide", font_size=22, color=RES),
            label(rf"two dimensions hold {100 * d['explained']:.0f}\%", font_size=22),
            label(rf"{100 * d['negative_share']:.0f}\% negative: \ roads aren't straight", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the map classical scaling builds from the table alone. <bookmark mark='b'/> It comes "
            "out in an arbitrary orientation, so rotate, reflect and scale it onto the truth, Procrustes's fit. "
            "<bookmark mark='c'/> The gold rings mark where the towns really are. <bookmark mark='d'/> The shape of the "
            "island comes back, with a typical error of about two thirds of a unit on an island ten across, largest at the "
            "coast, where routes are most roundabout. <bookmark mark='e'/> Two dimensions capture eighty-one percent of the "
            "structure, and some eigenvalues are negative: road distances are not the distances of any flat map, and the "
            "negative part measures how far from it they are."
        ) as vo:
            self.add(world_tag())
            self.play(FadeIn(dm.truth))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in dm.rebuilt], lag_ratio=0.005), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(dm.truth, color=TRUE), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(dm.residuals), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def europe(self):
        d = load("euro")
        X = np.asarray(d["X"])
        names = d["names"]
        idx = list(range(len(names)))
        dm = DistanceMap(X, X, width=7.0, height=5.6, center=[-2.2, 0.1, 0], names=names, label_idx=idx, font_size=16,
                         dot_radius=0.07)
        rows = fit_rows(VGroup(
            label(r"21 European cities: \ 210 road distances", font_size=22),
            label(r"classical scaling, \ turned so that north is up", font_size=22, color=PCC),
            label(rf"two dimensions hold {100 * d['explained']:.0f}\%", font_size=22),
            label(r"Lisbon west, \ Athens south-east, \ Stockholm north", font_size=22, color=MAPC),
        ), 4.0, 0.42, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real data: John Hartigan's table of road distances between twenty-one European cities, two "
            "hundred and ten numbers. <bookmark mark='b'/> Classical scaling, with the result turned so north is up. "
            "<bookmark mark='c'/> Two dimensions hold eighty-seven percent of the structure. <bookmark mark='d'/> And the map "
            "of Europe appears: Lisbon and Gibraltar in the south-west, Stockholm in the north, Athens far to the south-east, "
            "Paris, Brussels and Cologne clustered in the middle, without a single coordinate given."
        ) as vo:
            self.add(euro_tag())
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in dm.rebuilt], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(dm.labels), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def error(self):
        d = load("euro")
        w = d["worst"]
        hdr = [r"\textbf{pair}", r"\textbf{road distance in the table}", r"\textbf{on the rebuilt map}"]
        body = [[rf"{a} -- {b}", f"{r:,.0f} km", f"{m:,.0f} km"] for a, b, r, m in w]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A, RES, GREY_B, GREY_B])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"Cologne--Geneva is about 750 km by road: \ the table's 1,662 is an error in the data", font_size=22, color=RES),
            label(r"Athens--Rome: \ Athens's other distances run overland, \ so no flat map can honour this short one", font_size=22),
            label(r"the residuals are a check on the data, \ not just on the method", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The pairs the map fits worst are instructive. Cologne to Geneva: the table says one thousand "
            "six hundred and sixty-two kilometres, the map seven hundred. The real road distance is about seven hundred and "
            "fifty: the number in this classic data set is wrong, and the map found it. <bookmark mark='b'/> Athens to Rome: "
            "eight hundred kilometres in the table, seventeen hundred on the map. Athens's distances to every other city run "
            "overland, around the Balkans, so the map must put Athens far away, and one short entry, perhaps by sea, cannot "
            "be honoured in a flat map. <bookmark mark='c'/> A multivariate summary is also a check on "
            "the data that went into it."
        ) as vo:
            self.add(euro_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[2]), FadeIn(tb[3]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"many numbers, \ few dimensions: \ the structure is low-rank", font_size=26),
            label(r"eigenvectors find it: \ scaling, \ principal components, \ factors", font_size=26, color=PCC),
            label(r"covariance and its inverse carry the geometry", font_size=26, color=MAPC),
            label(r"and when variables outnumber observations, \ it all breaks: \ chapter ten", font_size=26, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson of the map: a table of many numbers can have few real dimensions. "
            "<bookmark mark='b'/> Eigenvectors find them, here and again and again in this part: in scaling, principal "
            "components, factor analysis and canonical correlation. <bookmark mark='c'/> The covariance matrix and its inverse "
            "carry the geometry of the data. <bookmark mark='d'/> And when there are almost as many variables as "
            "observations, the classical toolkit breaks, which chapter ten makes precise."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 31", font_size=34, color=GREY_B), label(r"Multivariate Analysis", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the data matrix; \ Mahalanobis distance; \ the Wishart distribution",
            r"Hotelling's $T^2$; \ MANOVA's four statistics",
            r"principal components; \ factor analysis; \ canonical correlation",
            r"discriminant analysis; \ clustering by $k$-means and mixtures",
            r"graphical models; \ what happens as $p$ approaches $n$",
        ], color=PCC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 4, \ 5 and 22").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.multi}; \ the map from distances").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-one: multivariate analysis. <bookmark mark='b'/> We'll meet the data matrix and "
            "Mahalanobis distance; derive the Wishart distribution of the sample covariance; test mean vectors with "
            "Hotelling's T squared and MANOVA; find low-dimensional structure by principal components, factor analysis and "
            "canonical correlation; separate groups by discriminant analysis and find them by clustering; read conditional "
            "independence from the inverse covariance; and see what goes wrong as the number of variables approaches the "
            "number of observations."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

    def stress(self):
        rows = [
            cmath(r"\text{stress}", r"=", r"\Big(\textstyle\sum_{i<j} (d_{ij} - \hat d_{ij})^2 / \sum_{i<j} d_{ij}^2\Big)^{1/2}", font_size=28),
            cmath(r"\text{Europe}", r":", r"0.090", font_size=32),
            cmath(r"\text{nonmetric}", r":", r"\text{only the order of the } d_{ij} \text{ matters}", font_size=30),
            cmath(r"\text{use}", r":", r"\text{similarity judgements, \ where numbers are rough}", font_size=28),
        ]
        rows[1][-1].set_color(MAPC)
        whys = [why(r"Kruskal's badness of fit"), why(r"`fair to good', \ by Kruskal's scale"), why(r"Shepard (1962), \ Kruskal (1964)"), why(r"Torgerson's original purpose")]
        with self.voiceover(
            "<bookmark mark='a'/> How good is a map overall? Joseph Kruskal's stress compares the distances on the map "
            "with the distances in the table, relative to their size. <bookmark mark='b'/> For Europe it is point oh "
            "nine, somewhere between fair and good on Kruskal's own rough scale. <bookmark mark='c'/> Roger Shepard "
            "and Kruskal went further, with nonmetric scaling: find a map whose distances are in the same order as the "
            "dissimilarities, ignoring their actual values. <bookmark mark='d'/> That is what psychologists needed, "
            "because people can say which two colours seem more alike, but not by how much."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
