from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403

ITEM_TEXT = {"A1": r"Am indifferent to the feelings of others", "C2": r"Continue until everything is perfect",
             "E4": r"Make friends easily", "N1": r"Get angry easily", "O1": r"Am full of ideas"}


def loading_grid(L, items, cell=0.22):
    out = VGroup()
    for i in range(len(items)):
        for k in range(5):
            v = float(L[i, k])
            c = TRAIT_COL[TRAITS[k]]
            col = interpolate_color(ManimColor("#14181F"), ManimColor(c if v >= 0 else GREY_B), min(1.0, abs(v) / 0.7))
            out.add(Rectangle(width=cell * 2.2, height=cell, stroke_width=0.5, stroke_color=BLACK, fill_color=col,
                              fill_opacity=1).move_to([k * cell * 2.2, -i * cell, 0]))
    return out


TRAITS = ("A", "C", "E", "N", "O")


class Factors(VoiceoverScene):
    def construct(self):
        self.card()
        self.items()
        self.how_many()
        self.loadings()
        self.scales()

    def card(self):
        card = chapter_card(2, r"Five factors in 2{,}800 people", r"Do the five appear in a real sample?",
                            lit={2010: r"SAPA"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter two. Five factors in two thousand eight hundred people."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def items(self):
        d = load("factors")
        head = heading(r"Twenty-five items, \ 2{,}800 people")
        hm = heatmap(d["R"], names=None, cell=0.2, values=False, lo=0.0, hi=0.7).move_to([-3.6, -0.3, 0])
        ticks = VGroup()
        for k, t in enumerate(TRAITS):
            ticks.add(label(t, font_size=18, color=TRAIT_COL[t]).next_to(hm.cells[5 * k + 2][0], LEFT, buff=0.12))
        ex = VGroup(*[VGroup(label(k, font_size=18, color=TRAIT_COL[k[0]]), label(v, font_size=18, color=GREY_A))
                      .arrange(RIGHT, buff=0.2) for k, v in ITEM_TEXT.items()]).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.18)
        rows = rows_of([
            (r"the SAPA project, \ 2010: \ 2{,}800 people rated how accurately 25 statements from the public-domain "
             r"International Personality Item Pool described them, \ from 1, \ very inaccurate, \ to 6, \ very "
             r"accurate", WHITE),
            (r"five items were written for each trait; \ seven are reverse-keyed, \ like ``Am indifferent to the "
             r"feelings of others''", GREY_A),
            (rf"the correlations, \ for the {num(d['n'])} people who answered every item, \ show five blocks along "
             r"the diagonal", YOU),
        ], 6.2, 20, 0.3).move_to([3.3, 1.0, 0])
        ex.next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        tag = published_tag(r"data: \ Revelle et al.\ (SAPA, \ 2010), \ recomputed")
        with self.voiceover(
            "Now the same question in real answers. <bookmark mark='a'/> In 2010 the SAPA project, run from William "
            "Revelle's laboratory, asked two thousand eight hundred people how accurately each of twenty-five "
            "statements described them, from one, very inaccurate, to six, very accurate. The statements come from "
            "the International Personality Item Pool, which is in the public domain. <bookmark mark='b'/> Five were "
            "written for each trait, and seven are reverse-keyed: agreeable people should disagree with Am "
            "indifferent to the feelings of others. <bookmark mark='c'/> Here are the correlations for the "
            f"{d['n']:,} people who answered every item. Five blocks stand out along the diagonal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hm), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(ex))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def how_many(self):
        d = load("factors")
        head = heading(r"How many factors? \ Ask random data")
        ks = np.arange(1, 11)
        A = axes([0.5, 10.5], [0, 5.5], x_length=6.2, y_length=4.0, xticks=list(range(1, 11)), yticks=[0, 1, 2, 3, 4, 5],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"factor", ylabel=r"eigenvalue",
                 center=[-2.9, -0.3, 0], font_size=15)
        real = VGroup(curve(A.ax, ks, d["eigen"][:10], YOU, stroke_width=4), scatter(A.ax, ks, d["eigen"][:10], YOU,
                                                                                       radius=0.07))
        rand = curve(A.ax, ks, d["random"][:10], GREY_B, stroke_width=3)
        key = legend([(YOU, r"the real answers"), (GREY_B, r"random answers, \ same size \ (95th percentile)")],
                     font_size=16).move_to(A.ax.c2p(6.8, 4.6))
        rows = rows_of([
            (r"each eigenvalue is how much of the items' shared variance one more factor would carry", WHITE),
            (r"John Horn's parallel analysis, \ 1965: \ keep a factor only if it carries more than the same factor "
             r"would in random data of the same size", MODEL),
            (rf"the real eigenvalues beat the random ones for the first {d['keep']} factors, \ and not after", YOU),
        ], 5.6, 21, 0.36).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{personality.parallel}")
        with self.voiceover(
            "How many factors are in these answers? <bookmark mark='a'/> Each eigenvalue says how much of the items' "
            "shared variance one more factor would carry. They fall away from the first. <bookmark mark='b'/> John "
            "Horn's parallel analysis, from 1965, says keep a factor only if it carries more than the same factor "
            "would in random answers of the same size. Psyche generates fifty sets of random answers. "
            f"<bookmark mark='c'/> The real eigenvalues beat the random ones for the first {d['keep']} factors, and "
            "not after. The data choose five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(real[0]), FadeIn(real[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(rand), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def loadings(self):
        d = load("factors")
        head = heading(r"Five factors, \ rotated")
        grid = loading_grid(d["L"], d["items"], cell=0.21).move_to([-3.2, -0.45, 0])
        names = VGroup(*[label(it, font_size=13, color=TRAIT_COL[it[0]]).next_to(grid[5 * i], LEFT, buff=0.1)
                         for i, it in enumerate(d["items"])])
        cols = VGroup(*[label(t, font_size=18, color=TRAIT_COL[t]).next_to(grid[k], UP, buff=0.1)
                        for k, t in enumerate(TRAITS)])
        own = np.abs(d["own"])
        rows = rows_of([
            (r"maximum likelihood finds five factors; \ varimax rotates them so each item loads mainly on one", WHITE),
            (rf"every item loads most on its own trait's factor: \ {own.min():.2f} to {own.max():.2f}", YOU),
            (r"the reverse-keyed items load negatively, \ as they should", GREY_A),
            (r"the weakest are an agreeableness item and an openness item: \ items differ in quality, \ which Part 45's "
             r"item response theory will measure", MODEL),
        ], 6.4, 21, 0.36).move_to([3.0, -0.3, 0])
        tag = psyche_tag(r"\texttt{statkit.multi.factor\_ml, \ varimax}")
        with self.voiceover(
            "Now fit five. <bookmark mark='a'/> Maximum likelihood finds the five factors, and varimax rotates them, "
            "Thurstone's idea from Part 32, so that each item loads mainly on one. <bookmark mark='b'/> Every one of "
            "the twenty-five items loads most on the factor of its own trait, with loadings from "
            f"{own.min():.2f} to {own.max():.2f} in size. <bookmark mark='c'/> The reverse-keyed items load "
            "negatively, as they should. <bookmark mark='d'/> The weakest are an agreeableness item and an openness "
            "item. Items differ in quality, which Part 45's item response theory will measure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(names), FadeIn(cols))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01), FadeIn(rows[0]), run_time=3.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def scales(self):
        d = load("factors")
        head = heading(r"Five scales")
        hm = heatmap(d["Rs"], names=[TRAIT_NAME[t] for t in TRAITS], cell=0.8, font_size=18, lo=0.0, hi=0.7)
        hm.move_to([-2.4, -0.2, 0])
        al = VGroup(*[label(rf"$\alpha = {a:.2f}$", font_size=18, color=TRAIT_COL[t]).next_to(hm.cells[i][4], RIGHT,
                                                                                             buff=0.25)
                      for i, (t, a) in enumerate(zip(TRAITS, d["alpha"]))])
        Rs = d["Rs"]
        rows = rows_of([
            (r"average each person's five items, \ reverse-keyed ones flipped, \ to get a score on each trait", WHITE),
            (rf"Cronbach's alpha, \ Part 3: \ from {min(d['alpha']):.2f} for openness to {max(d['alpha']):.2f} for "
             r"neuroticism, \ with only five items each", MODEL),
            (rf"the five are not independent: \ agreeableness and extraversion correlate {Rs[0, 2]:.2f}, \ and "
             r"neuroticism correlates negatively with all four", YOU),
        ], 5.0, 21, 0.36).move_to([4.0, -0.2, 0])
        tag = psyche_tag(r"\texttt{personality.score}; \ \texttt{measure.cronbach\_alpha}")
        with self.voiceover(
            "From factors to scores. <bookmark mark='a'/> Average each person's five items for a trait, with the "
            "reverse-keyed ones flipped, and you have a score on each trait. <bookmark mark='b'/> Their reliability, "
            f"Cronbach's alpha from Part 3, runs from {min(d['alpha']):.2f} for openness to "
            f"{max(d['alpha']):.2f} for neuroticism, with only five items each. <bookmark mark='c'/> And the five "
            f"aren't independent. Agreeableness and extraversion correlate {Rs[0, 2]:.2f}, and neuroticism "
            "correlates negatively with all four others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(al), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
