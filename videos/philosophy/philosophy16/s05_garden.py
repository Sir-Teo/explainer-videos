from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403

LEVELS = [("outcome", ["DV1", "DV2", "mean"]), ("sample", ["20", "30"]),
          ("gender", ["all", "men", "women", "ctrl"]), ("outliers", ["keep", "drop"])]


class Garden(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"The garden of forking paths", r"How does noise become a discovery?",
                            lit=(2011, 2015), part=PART)
        with self.voiceover("Chapter four. The garden of forking paths."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tree()
        self.simulator()
        self.curse()
        self.crisis()
        self.remedies()

    def tree(self):
        d = load("garden")["one"]
        head = label(r"One data set of pure noise, \ 48 reasonable analyses", font_size=28, color=CONN).to_edge(
            UP, buff=0.3)
        xs = [-6.4, -4.4, -2.4, -0.4, 1.4]
        # leaves in order of the paths list
        leaves = []
        y_top, y_bot = 2.3, -3.2
        n_leaf = len(d["paths"])
        ys = [y_top - (y_top - y_bot) * i / (n_leaf - 1) for i in range(n_leaf)]
        g_edges = VGroup()
        nodes = VGroup()
        # level sizes: 3, 2, 4, 2 -> internal node positions are means of their leaves
        sizes = [len(v) for _, v in LEVELS]

        def build(level, lo, hi, x_parent, y_parent):
            span = (hi - lo) // sizes[level]
            for k in range(sizes[level]):
                a, b = lo + k * span, lo + (k + 1) * span
                y = sum(ys[a:b]) / (b - a)
                x = xs[level + 1]
                g_edges.add(Line([x_parent, y_parent, 0], [x, y, 0], color=GREY_D, stroke_width=1.2))
                if level + 1 < len(LEVELS):
                    nodes.add(Dot([x, y, 0], radius=0.03, color=GREY_C))
                    build(level + 1, a, b, x, y)
                else:
                    leaves.append((x, y))
        root = Dot([xs[0], (y_top + y_bot) / 2, 0], radius=0.06, color=WHITE)
        build(0, 0, n_leaf, xs[0], (y_top + y_bot) / 2)
        dots = VGroup()
        for (x, y), q in zip(leaves, d["paths"]):
            dots.add(Dot([x, y, 0], radius=0.055, color=BAD if q["p"] < 0.05 else GREY_B))
        lab = VGroup(*[label(name, font_size=17, color=GREY_A).move_to([(xs[i] + xs[i + 1]) / 2, 2.75, 0])
                       for i, (name, _) in enumerate(LEVELS)])
        hits = [i for i, q in enumerate(d["paths"]) if q["p"] < 0.05]
        best = min(hits, key=lambda i: d["paths"][i]["p"])
        bq = d["paths"][best]
        note = stack([(r"the planned analysis: \ $p = " + f"{d['default_p']:.2f}" + r"$", GREY_B),
                      (str(len(hits)) + r" of 48 paths: \ $p < 0.05$", BAD),
                      (r"best: \ " + bq["outcome"] + r", \ " + str(bq["n"]) + r" per group, \ " + bq["gender"] +
                       r": \ $p = " + f"{bq['p']:.3f}" + r"$", BAD),
                      (r"each path, \ alone, \ errs 5\% of the time", GREY_A)], font_size=19,
                     aligned_edge=LEFT, width=4.6).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "Andrew Gelman and Eric Loken gave the problem its name: the garden of forking paths. "
            "<bookmark mark='a'/>Here is one experiment in which nothing is going on: two conditions, twenty "
            "subjects each, pure noise. <bookmark mark='b'/>A researcher makes reasonable choices. Which outcome to "
            "analyse: the first measure, the second, or their average. Whether to stop at twenty per group or "
            "collect ten more. Whether to analyse everyone, men only, women only, or control for gender. Whether to "
            "drop an outlier. Forty-eight paths. <bookmark mark='c'/>The planned analysis gives p of point eight "
            "seven. But four of the forty-eight paths give p below point zero five, the best of them point zero one. "
            "<bookmark mark='d'/>No one needs to cheat. Each path, taken alone, has a five percent error rate. The "
            "trouble is that the path is chosen after seeing the data."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(root))
            vo.wait_until("b")
            self.play(FadeIn(lab), Create(g_edges), FadeIn(nodes), run_time=3)
            self.play(FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(note[0]))
            self.play(*[Indicate(dots[i], color=BAD, scale_factor=2.2) for i in hits], FadeIn(note[1]),
                      FadeIn(note[2]))
            vo.wait_until("d")
            self.play(FadeIn(note[3]))
        self.clear_scene()

    def simulator(self):
        d = load("garden")
        head = label(r"The $p$-hacking simulator", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sub = label(f"{d['studies']:,}".replace(",", "{,}") + r" studies of pure noise; \ share reaching $p < 0.05$",
                    font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        base_x = -2.2
        bars = VGroup()
        for i, r in enumerate(d["rows"]):
            y = 1.5 - i * 0.72
            nm = label(r["freedom"], font_size=20, color=WHITE if i < 5 else BAD)
            nm.move_to([base_x - 0.25 - nm.width / 2, y, 0])
            w = r["rate"] * 16
            b = Rectangle(width=max(w, 0.02), height=0.42, stroke_width=0, fill_color=BAD if i == 5 else FISH,
                          fill_opacity=0.85).move_to([base_x + w / 2, y, 0])
            v = label(rf"{100 * r['rate']:.1f}\%", font_size=20, color=BAD if i == 5 else FISH).next_to(b, RIGHT,
                                                                                                    buff=0.15)
            bars.add(VGroup(nm, b, v))
        five = DashedLine([base_x + 0.05 * 16, 1.9, 0], [base_x + 0.05 * 16, -2.3, 0], color=GREY_B,
                          stroke_width=1.5)
        fl = label(r"5\%", font_size=18, color=GREY_B).next_to(five, DOWN, buff=0.08)
        foot = label(r"Simmons, \ Nelson and Simonsohn \ (2011): \ `False-Positive Psychology'", font_size=20,
                     color=HIST).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner turns this into a machine. <bookmark mark='a'/>Four thousand studies of pure noise. "
            "<bookmark mark='b'/>With no freedom at all, about five percent reach significance, as they should. "
            "<bookmark mark='c'/>Allow a choice between two correlated outcomes and their average: nearly ten "
            "percent. <bookmark mark='d'/>Add ten more subjects when the first look fails: eight percent. Use gender, "
            "by subgroup or as a control: eleven percent. Drop an outlier: seven. <bookmark mark='e'/>Allow all four, "
            "and more than a third of studies of nothing find something. <bookmark mark='f'/>Joseph Simmons, Leif "
            "Nelson and Uri Simonsohn ran this experiment in 2011, and to make the point they also showed, with "
            "real data and honest-looking statistics, that listening to a Beatles song makes people younger."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub), Create(five), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("d")
            for b in bars[2:5]:
                self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]), run_time=0.7)
            vo.wait_until("e")
            self.play(FadeIn(bars[5][0]), GrowFromEdge(bars[5][1], LEFT), FadeIn(bars[5][2]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def curse(self):
        d = load("garden")["curse"]
        head = label(r"The winner's curse: \ significant results exaggerate", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        sub = label(r"a real but small effect, \ " + f"{d['effect']:g}" + r" standard deviations; \ keep only the "
                    r"studies with $p < 0.05$", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        hd = [r"n \text{ per group}", r"\text{power}", r"\text{exaggeration}", r"\text{wrong sign}"]
        rows = [[MathTex(str(r["n"]), font_size=26), MathTex(f"{r['power']:.2f}", font_size=26),
                 MathTex(f"{r['exaggeration']:.1f}" + r"\times", font_size=26,
                         color=BAD if r["exaggeration"] > 1.5 else OK),
                 MathTex(f"{100 * r['wrong_sign']:.1f}" + r"\%", font_size=26,
                         color=BAD if r["wrong_sign"] > 0.005 else OK)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[2.6, 2.0, 2.8, 2.6], cell_h=0.58, font_size=24).next_to(sub, DOWN, buff=0.4)
        foot = stack([(r"Gelman and Carlin \ (2014): \ type M \ (magnitude) \ and type S \ (sign) \ errors", HIST),
                      (r"low power plus a significance filter: \ replications \textit{must} find smaller effects",
                       GOAL)], font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There is a second reason replications find smaller effects, even without any p-hacking. "
            "<bookmark mark='a'/>Take a real but small effect, a fifth of a standard deviation, and keep only the "
            "studies that reach significance. <bookmark mark='b'/>With twenty subjects per group, the power is ten "
            "percent, and the studies that do reach significance overestimate the effect nearly four times over. "
            "Four percent of them even get its sign wrong. <bookmark mark='c'/>With fifty per group, the "
            "exaggeration is two and a half. <bookmark mark='d'/>Only with four hundred per group, and power of "
            "eighty percent, do significant results report roughly the truth. <bookmark mark='e'/>Andrew Gelman and "
            "John Carlin call these type M and type S errors. Low power plus a significance filter means that "
            "honest replications must find smaller effects."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[1])), FadeIn(VGroup(*grid.cell[2])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[3])))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def crisis(self):
        head = label(r"The replication record", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"psychology", r"Open Science Collaboration \ (2015): \ 36 of 97 significant results replicated; \ "
                            r"effects halved", BAD),
            (r"social science \ in \textit{Nature} and \textit{Science}", r"Camerer et al.\ \ (2018): \ 13 of 21; \ "
                                                                       r"effects about half", FISH),
            (r"economics \ (lab)", r"Camerer et al.\ \ (2016): \ 11 of 18", FISH),
            (r"cancer biology", r"Reproducibility Project \ (2021): \ effects 85\% smaller on average", BAD),
            (r"prediction markets", r"researchers' bets predicted which studies would replicate", OK),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.6, x_text=-2.4)
        with self.voiceover(
            "The garden is not hypothetical. <bookmark mark='a'/>In psychology, thirty-six of ninety-seven "
            "significant results replicated, with effects about half as large. <bookmark mark='b'/>Of twenty-one "
            "social science experiments published in Nature and Science, thirteen replicated. "
            "<bookmark mark='c'/>In laboratory economics, eleven of eighteen. <bookmark mark='d'/>In cancer biology, "
            "replicated effects were on average eighty-five percent smaller than the originals. "
            "<bookmark mark='e'/>And a striking twist: when researchers bet in prediction markets on which studies "
            "would replicate, the markets were largely right. Scientists could tell, collectively, which results "
            "were fragile."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def remedies(self):
        head = label(r"Remedies, \ and what they assume", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"preregistration", r"fix the path before seeing the data; \ Registered Reports \ (Chambers, \ 2013)",
             OK),
            (r"correction", r"Bonferroni; \ the false discovery rate \ (Benjamini and Hochberg, \ 1995)", NEYP),
            (r"power", r"larger samples: \ fewer false negatives \textit{and} a higher PPV", ALTC),
            (r"openness", r"data and code shared; \ multiverse analyses report every path", FISH),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=9.0, x_text=-2.8)
        foot = stack([(r"every remedy says: \ the evidence in the data depends on what \textit{would} have been done "
                       r"with other data", GOAL),
                      (r"a Bayesian or a likelihoodist denies exactly that \ (Chapter 6)", BAD)], font_size=22).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "The remedies are now standard. <bookmark mark='a'/>Preregistration: fix the analysis before seeing the "
            "data, or better, have the journal accept the study before the results exist. <bookmark mark='b'/>"
            "Correction for multiple tests, by Bonferroni's method or by controlling the false discovery rate. "
            "<bookmark mark='c'/>Power: larger samples mean fewer missed effects and a higher share of true "
            "positives. <bookmark mark='d'/>Openness: share data and code, and report the whole multiverse of "
            "reasonable analyses. <bookmark mark='e'/>Notice what every remedy assumes: that the evidence in the "
            "data depends on what would have been done had the data been different. <bookmark mark='f'/>A Bayesian "
            "or a likelihoodist denies exactly that. Chapter six explains why, and what it costs."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
