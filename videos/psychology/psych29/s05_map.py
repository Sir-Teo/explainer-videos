from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403

SHORT = {
    "Grief at death of mother": r"grief", "Savoring a Coke": r"savouring a Coke",
    "Very pleasant surprise": r"pleasant surprise", "Maternal love-baby in arms": r"maternal love",
    "Physical exhaustion": r"exhaustion", "Something wrong with plane": r"something wrong with the plane",
    "Anger at seeing dog beaten": r"anger", "Pulling hard on seat of chair": r"straining",
    "Unexpectedly meets old boyfriend": r"meets an old flame", "Revulsion": r"revulsion",
    "Extreme pain": r"extreme pain", "Knows plane will crash": r"the plane will crash", "Light sleep": r"light sleep",
}


class Map(VoiceoverScene):
    def construct(self):
        self.card()
        self.data()
        self.mds()
        self.circumplex()
        self.on_you()

    def card(self):
        card = chapter_card(4, r"On you: \ the map of feelings", r"How many dimensions does feeling have?",
                            lit={1958: r"Engen et al.", 1962: r"Abelson \& Sermat", 1980: r"Russell"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter four. On you: the map of feelings."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def data(self):
        d = load("faces")
        head = heading(r"Thirteen faces, \ 1962")
        n = len(d["labels"])
        names = VGroup(*[label(SHORT[lab], font_size=17, color=FACE) for lab in d["labels"]])
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-4.4, -0.3, 0])
        grid = VGroup()
        D = None
        from explainer.psychology import opendata
        D = opendata.faces_1962()["D"]
        cell = 0.28
        for i in range(n):
            for j in range(n):
                v = D[i, j] / D.max()
                grid.add(Square(side_length=cell, stroke_width=0.5, stroke_color=GREY_D, fill_color=interpolate_color(
                    ManimColor(BLACK), ManimColor(FACE), 1 - v), fill_opacity=1).move_to([j * cell, -i * cell, 0]))
        grid.move_to([-0.9, -0.3, 0])
        gl = label(r"dissimilarity: \ bright = alike", font_size=16, color=GREY_B).next_to(grid, UP, buff=0.15)
        rows = rows_of([
            (r"Engen, \ Levy and Schlosberg: \ photographs of one actress posing 13 situations", WHITE),
            (r"Robert Abelson and Vello Sermat, \ 1962: \ people judged how different each pair of faces looked",
             FACE),
            (r"78 pairs, \ one table of dissimilarities, \ and no theory put in", COG),
            (r"each face was also rated on three scales: \ pleasant--unpleasant, \ attention--rejection, \ "
             r"tension--sleep", MODEL),
        ], 4.2, 20, 0.3).move_to([4.6, -0.1, 0])
        tag = historical_tag(archive.FACES_1962.cite)
        with self.voiceover(
            "Here is a way to ask how many dimensions feeling has without deciding in advance. "
            "<bookmark mark='a'/> In the 1950s Trygg Engen, Nissim Levy and Harold Schlosberg photographed one "
            "actress posing thirteen situations: grief at a mother's death, savouring a Coke, a very pleasant "
            "surprise, anger at seeing a dog beaten, and so on. <bookmark mark='b'/> In 1962 Robert Abelson and Vello "
            "Sermat asked people to judge how different each pair of faces looked. <bookmark mark='c'/> That gives "
            "seventy-eight pairs and one table of dissimilarities, with no theory put in. <bookmark mark='d'/> "
            "Separately, each face had been rated on three scales: pleasant against unpleasant, attention against "
            "rejection, and tension against sleep. The table is still distributed with a statistics package, and "
            "Psyche reads it directly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(grid), FadeIn(gl))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mds(self):
        d = load("faces")
        head = heading(r"Derivation: \ multidimensional scaling")
        eqs = VGroup(
            MathTex(r"B = -\tfrac12\, J D^{(2)} J, \qquad J = I - \tfrac1n \mathbf{1}\mathbf{1}^\top", font_size=32),
            MathTex(r"B = V \Lambda V^\top \ \Rightarrow \ X = V_{2} \Lambda_{2}^{1/2}", font_size=32),
        ).arrange(DOWN, buff=0.3)
        e = d["eig"]
        pos = e[e > 0]
        A = axes([0.5, 6.5], [0, 0.6], x_length=5.0, y_length=3.0, xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 0.25, 0.5],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"dimension",
                 ylabel=r"share of variance", center=[-3.5, -0.6, 0], font_size=16)
        share = pos[:6] / pos.sum()
        bb = bars(A.ax, np.arange(1, 7), share, FACE, width=0.6)
        rows = rows_of([
            (r"if distances were drawn on a plane, \ double-centring their squares gives the plane's coordinates "
             r"back, \ up to rotation", WHITE),
            (rf"the first two dimensions carry {pct(d['share'])} of the variance; \ the rest is small", FACE),
            (r"the data ask for two dimensions, \ not six", COG),
        ], 5.8, 21, 0.3)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{emotion.classical\_mds}")
        with self.voiceover(
            "Torgerson's classical scaling turns such a table into a map. <bookmark mark='a'/> If the "
            "dissimilarities were distances between points on a plane, then squaring them and double-centring, "
            "subtracting row and column means, gives back the matrix of the points' inner products, whose top "
            "eigenvectors are the coordinates, up to a rotation. Apply it to any table, and the eigenvalues say how "
            f"many dimensions it needs. <bookmark mark='b'/> Here the first two dimensions carry "
            f"{100 * d['share']:.0f} percent of the variance, and the rest is small. <bookmark mark='c'/> The "
            "faces ask for two dimensions, not six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Write(eqs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb], lag_ratio=0.15), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def circumplex(self):
        d = load("faces")
        head = heading(r"The two dimensions are named by the ratings")
        X = np.asarray(d["X"], float)
        sc = 0.42
        origin = np.array([-3.0, -0.3, 0])
        pts = VGroup()
        dots = [Dot(origin + sc * np.array([x, y, 0]), radius=0.07, color=FACE) for x, y in X]
        placed = [(dt.get_left()[0], dt.get_right()[0], dt.get_bottom()[1], dt.get_top()[1]) for dt in dots]

        def free(m, own):
            l, r, b_, t_ = m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1]
            return all(r < L - 0.03 or l > R + 0.03 or t_ < B - 0.03 or b_ > T + 0.03
                       for k, (L, R, B, T) in enumerate(placed) if k != own)

        # crowded points first; each label takes the first side that overlaps no dot and no placed label
        dens = [sum(np.linalg.norm(X[i] - X[j]) < 1.5 for j in range(len(X))) for i in range(len(X))]
        texts = [None] * len(X)
        for i in sorted(range(len(X)), key=lambda i: -dens[i]):
            t = label(SHORT[d["labels"][i]], font_size=15, color=WHITE)
            for side in (UP, DOWN, RIGHT, LEFT, UR, UL, DR, DL):
                t.next_to(dots[i], side, buff=0.06)
                if free(t, i):
                    break
            placed.append((t.get_left()[0], t.get_right()[0], t.get_bottom()[1], t.get_top()[1]))
            texts[i] = t
        for dt, t in zip(dots, texts):
            pts.add(VGroup(dt, t))
        def arrow_for(key, col, name):
            v = np.asarray(d[f"{key}_dir"], float)
            a = Arrow(origin - 2.6 * np.array([v[0], v[1], 0]), origin + 2.6 * np.array([v[0], v[1], 0]), buff=0,
                      color=col, stroke_width=3, max_tip_length_to_length_ratio=0.05,
                      stroke_opacity=0.75)
            lab = label(name, font_size=17, color=col).next_to(a.get_end(), UR, buff=0.05)
            return VGroup(a, lab)
        pu = arrow_for("PU", PLEAS, r"pleasant")
        ts = arrow_for("TS", BODY, r"tension")
        rows = rows_of([
            (r"regress each rating on the map: \ its best direction, \ and how well the map predicts it", WHITE),
            (rf"pleasant--unpleasant: \ $R = {d['PU_R']:.2f}$", PLEAS),
            (rf"tension--sleep: \ $R = {d['TS_R']:.2f}$, \ nearly at right angles to it", BODY),
            (r"Russell, \ 1980: \ emotion words too arrange themselves in a circle around these two axes, \ "
             r"valence and arousal: \ the circumplex", COG),
        ], 5.2, 21, 0.3).move_to([3.7, -0.1, 0])
        tag = psyche_tag(r"\texttt{emotion.fit\_scale}; \ data: Abelson \& Sermat (1962)")
        with self.voiceover(
            "Here is the map, with the thirteen faces in place. <bookmark mark='a'/> Now bring in the ratings. For "
            "each scale, regress the faces' ratings on their positions: the direction in which the rating rises "
            f"fastest, and how well the map predicts it. <bookmark mark='b'/> Pleasantness: R of {d['PU_R']:.2f}. "
            f"<bookmark mark='c'/> Tension against sleep: R of {d['TS_R']:.2f}, at nearly a right angle to "
            "pleasantness. The two dimensions in nobody's theory are pleasantness and arousal. "
            "<bookmark mark='d'/> In 1980 James Russell found the same with emotion words: they arrange themselves "
            "around a circle on these two axes, valence and arousal. He called it the circumplex."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(pu[0]), FadeIn(pu[1]), FadeIn(rows[1]))
            self.bring_to_front(pts)
            vo.wait_until("c")
            self.play(GrowArrow(ts[0]), FadeIn(ts[1]), FadeIn(rows[2]))
            self.bring_to_front(pts)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def on_you(self):
        d = load("pairs")
        head = heading(r"On you: \ same feeling, \ or different?")
        stage = demo_stage(5.6, 2.4, center=[-3.5, 1.4, 0])
        pair = VGroup(face(0.9, 0.3, radius=0.5), face(0.7, 0.75, radius=0.5)).arrange(RIGHT, buff=1.0).move_to(
            stage).shift(DOWN * 0.1)
        q = label(r"same feeling, \ or different?", font_size=20, color=YOU).next_to(pair, DOWN, buff=0.15)
        # Psyche's maps after one and ten judgments of each pair
        def mini(X, center, title, col):
            g = VGroup()
            for (x, y), (tx, ty) in zip(np.asarray(X), np.asarray(d["true"])):
                p = np.array(center) + 1.1 * np.array([x, y, 0])
                tp = np.array(center) + 1.1 * np.array([tx, ty, 0])
                g.add(Line(tp, p, color=GREY_D, stroke_width=1.5), Dot(tp, radius=0.04, color=GREY_B),
                      Dot(p, radius=0.06, color=col))
            t = label(title, font_size=16, color=col).move_to(np.array(center) + [0, -1.45, 0])
            return VGroup(g, t)
        m1 = mini(d["X1"], [-5.0, -1.4, 0], rf"each pair once: \ $r = {d['r1']:.2f}$", MODEL)
        m10 = mini(d["X10"], [-2.0, -1.4, 0], rf"ten times: \ $r = {d['r10']:.2f}$", PLEAS)
        rows = rows_of([
            (r"this part's interactive shows you pairs of ten schematic faces: \ 45 pairs, \ same feeling or "
             r"different", YOU),
            (r"the share of `different' answers is a dissimilarity; \ scaling turns it into your map", WHITE),
            (r"Psyche, \ judging each pair from its distance on the plane plus noise: \ grey dots are the faces' "
             r"true places, \ coloured dots the recovered ones", MODEL),
            (r"even one coarse yes-or-no per pair recovers most of the plane", PLEAS),
        ], 5.4, 21, 0.3).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{emotion.pairs\_map}")
        with self.voiceover(
            "Now you can make the map yourself. <bookmark mark='a'/> This part's interactive shows you pairs of ten "
            "schematic faces, all forty-five pairs, and asks: same feeling, or different? "
            "<bookmark mark='b'/> The share of 'different' answers for each pair is a dissimilarity, and scaling "
            "turns the table into your map. <bookmark mark='c'/> Here is Psyche doing it, judging each pair from "
            "its distance on the plane plus noise. Grey dots are the faces' true places; coloured dots are the "
            f"recovered ones. <bookmark mark='d'/> Judging each pair once, the map already correlates "
            f"{d['r1']:.2f} with the truth; ten times, {d['r10']:.2f}. Even one coarse yes or no per pair recovers "
            "most of the plane. Your own map will tell you whether you see two dimensions, or something else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(stage), FadeIn(pair), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(m1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(m10), FadeIn(rows[3]))
        self.clear_scene()
