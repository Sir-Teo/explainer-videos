from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403

TH = [("epistemicism", r"epistemicism"), ("supervaluationism", r"supervaluationism"), ("degrees", r"degrees"),
      ("gluts (LP)", r"gluts (LP)"), ("nihilism", r"nihilism")]
CL = [("tolerance", r"tolerance"), ("extremes", r"extremes"), ("bivalence", r"bivalence"),
      ("logic", r"classical logic")]


class Epistemic(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"A sharp line no one can see", r"Could `bald' have an exact boundary we cannot know?",
                            lit=(1994,), part=PART)
        with self.voiceover("Chapter twelve. A sharp line no one can see."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.margin()
        self.context()
        self.price_list()
        self.table()

    def margin(self):
        d = load("margin")
        n = d["n"] + 1
        st = ["T" if d["known_bald"][i] else "F" if d["known_not"][i] else "I" for i in range(n)]
        heads = men_row([None] * n, width=12.4, r=0.13, y=0.4)
        hc = history_card(1994, r"Timothy Williamson", r"\textit{Vagueness}: \ bivalence and classical logic, intact",
                          width=6.4, color=HIST).to_corner(UL, buff=0.3)
        hc2 = history_card(1988, r"Roy Sorensen", r"\textit{Blindspots}", width=3.6, color=HIST).next_to(hc, RIGHT,
                                                                                                      buff=0.3)
        step = 12.4 / (n - 1)
        x0 = -6.2
        cut = Line([x0 + step * (d["cutoff"] - 0.5), 1.0, 0], [x0 + step * (d["cutoff"] - 0.5), -0.2, 0],
                   color=WHITE, stroke_width=4)
        cl = label(r"the cutoff: \ sharp, \ and real", font_size=22).next_to(cut, UP, buff=0.1)
        strip = status_strip(st, width=12.4, height=0.3, y=-0.6)
        keys = VGroup(label(r"known bald", font_size=22, color=OK), label(r"unknowable", font_size=22, color=HALF),
                      label(r"known not bald", font_size=22, color=BAD)).arrange(RIGHT, buff=1.2).next_to(strip, DOWN,
                                                                                                    buff=0.3)
        mfe = VGroup(label(r"margin for error:", font_size=26, color=GOAL),
                     label(rf"to know man $i$ is bald, \ the men within {d['margin']} of $i$ must be bald too",
                           font_size=24)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.85)
        res = label(rf"so the {d['unknown']} men nearest the line can never be known either way", font_size=24,
                    color=HALF).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The third theory is the boldest, because it changes nothing in the logic. <bookmark mark='a'/>Roy "
            "Sorensen and Timothy Williamson argue that 'bald' has a sharp cutoff: one hair does make the "
            "difference, somewhere. Classical logic and bivalence are kept whole. <bookmark mark='b'/>Then why can "
            "no one say where the line is? Williamson's answer is a margin for error. To know that a man is bald, "
            "your belief must be safe: it must not be the kind of belief you would hold even if you were wrong. Our "
            "judgments of baldness cannot tell neighbours apart, so you know that man i is bald only if the men "
            "near him are bald too. <bookmark mark='c'/>The Reasoner applies the principle with a margin of "
            f"{d['margin']}. Far from the cutoff, we know. <bookmark mark='d'/>But the {d['unknown']} men nearest the "
            "line can never be known to be on either side. Vagueness, on this view, is ignorance, and an "
            "ignorance that no investigation could cure."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(hc2), LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.03))
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(mfe))
            vo.wait_until("c")
            self.play(FadeIn(strip), FadeIn(keys))
            vo.wait_until("d")
            self.play(FadeIn(res), Indicate(VGroup(*[strip[i] for i in range(n) if st[i] == "I"]), color=HALF))
        self.clear_scene()

    def context(self):
        head = label(r"Contextualism: \ the line moves when you look", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        n = 21
        heads = men_row([None] * n, width=12.0, r=0.2, y=0.9)
        step = 12.0 / (n - 1)
        x0 = -6.0
        ln = Line([x0 + step * 9.5, 1.5, 0], [x0 + step * 9.5, 0.3, 0], color=WHITE, stroke_width=4)
        pair = SurroundingRectangle(VGroup(heads[9], heads[10]), color=GOAL, buff=0.08)
        txt = VGroup(label(r"compare man 9 and man 10 side by side: \ you judge them alike", font_size=24),
                     label(r"so the boundary is never where you are looking", font_size=24, color=GOAL),
                     label(r"Kamp 1981; \ Raffman 1994; \ Graff Fara 2000; \ Shapiro 2006", font_size=20,
                           color=GREY_B)).arrange(DOWN, buff=0.22).move_to([0, -1.4, 0])
        with self.voiceover(
            "A fourth family of views says the line exists, but moves. <bookmark mark='a'/>Picture a cutoff "
            "between man nine and man ten. <bookmark mark='b'/>Now put those two side by side and ask about both. "
            "You will judge them alike, both bald or both not, and in that context the boundary is somewhere else. "
            "<bookmark mark='c'/>So every tolerance conditional you actually consider comes out true, because "
            "considering it moves the line away from it. Hans Kamp, Diana Raffman, Delia Graff Fara and Stewart "
            "Shapiro have developed versions of this idea. Tolerance holds wherever you look, and fails only where "
            "you are not looking."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.04))
            vo.wait_until("a")
            self.play(Create(ln))
            vo.wait_until("b")
            self.play(Create(pair), FadeIn(txt[0]))
            self.play(ln.animate.shift(RIGHT * step * 4), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(txt[1]), FadeIn(txt[2]))
            self.play(pair.animate.move_to(VGroup(heads[13], heads[14])), ln.animate.shift(LEFT * step * 7),
                      run_time=1.5)
        self.clear_scene()

    def price_list(self):
        d = load("quartet")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(x) for x in d["mus"]], radius=2.95, width=3.5, font_size=20,
                       center=[0, -0.5, 0], title=r"The Price List: \ the sorites quartet")
        positions = [(("T",), r"a sharp line", r"epistemicism: \ Sorensen, Williamson; \ in part, Fine"),
                     (("B",), r"a gap, or degrees", r"Fine 1975; \ Machina 1976; \ Smith 2008"),
                     (("L",), r"a tolerant logic", r"Hyde 1997 (LP); \ Cobreros et al.\ 2012 (ST)"),
                     (("E",), r"no bald men", r"nihilism: \ Unger 1979; \ Wheeler")]
        assert sorted(tuple(x) for x in d["mcs"]) == sorted(p[0] for p in positions)
        with self.voiceover(
            "As a Price List: four claims, inconsistent together, as the Reasoner showed in Chapter 10. Tolerance; "
            "the extremes; bivalence; and classical logic. <bookmark mark='a'/>Give up tolerance, and you have a "
            "sharp line, known or unknowable: Williamson and Sorensen. <bookmark mark='b'/>Give up bivalence, and "
            "you have gaps, as in supervaluations, or degrees. <bookmark mark='c'/>Give up classical logic, and keep "
            "tolerance with a logic in which the chain breaks: Dominic Hyde's glut theory, in LP, where modus ponens "
            "fails; or the logic ST of Cobreros, Égré, Ripley and van Rooij, where every step is valid but chaining "
            "them is not. <bookmark mark='d'/>Or give up the extremes: Peter Unger argued in 1979 that there are no "
            "bald men, and no heaps, and indeed no ordinary things at all."
        ) as vo:
            self.play(FadeIn(pl.title), LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25),
                      Create(pl.conflict))
            for i, (mk, (mcs, name, who)) in enumerate(zip("abcd", positions)):
                vo.wait_until(mk)
                if i:
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=2.7)
                self.play(*anims)
        self.clear_scene()

    def table(self):
        d = load("quartet")["theories"]
        head = label(r"Each theory computed in its own semantics: \ what it keeps", font_size=30,
                     color=CONN).to_edge(UP, buff=0.45)
        hd = [label(r"theory", font_size=22, color=P.CLAIM)] + [label(t, font_size=22, color=P.CLAIM) for _, t in CL]
        rows = [[label(t, font_size=24)] + [d[k][c] for c, _ in CL] for k, t in TH]
        grid = ValueGrid(hd, rows, col_w=[3.4, 2.0, 1.9, 2.0, 2.6], cell_h=0.66, font_size=28).next_to(head, DOWN,
                                                                                                     buff=0.5)
        note_ = label(r"supervaluations and degrees give up tolerance too: \ every price list hides a second price",
                      font_size=24, color=GOAL).to_edge(DOWN, buff=0.4)
        assert all(sum(not v for v in d[k].values()) >= 1 for k, _ in TH)
        with self.voiceover(
            "The Reasoner can be more precise than the Price List, by computing each theory in its own semantics, "
            "on ten men. <bookmark mark='a'/>The epistemicist keeps everything but tolerance: one conditional is "
            "false. <bookmark mark='b'/>The supervaluationist loses bivalence, and also tolerance, since the "
            "conditionals in the penumbra are not super-true. <bookmark mark='c'/>The degree theorist, likewise: "
            "the conditionals are nearly true, but not true. <bookmark mark='d'/>The glut theorist keeps tolerance "
            "and the extremes, by giving up bivalence and modus ponens. <bookmark mark='e'/>The nihilist keeps "
            "everything except that some men are bald. <bookmark mark='f'/>So most theories pay twice. The "
            "sorites is cheap to state and expensive to answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            for mk, r in zip("abcde", range(len(rows))):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(grid.cell[r][c], scale=0.6) for c in range(1, 5)], lag_ratio=0.15))
            vo.wait_until("f")
            self.play(FadeIn(note_))
        self.clear_scene()
