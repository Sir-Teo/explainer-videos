from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


def model_table(rows, color=WHITE, font_size=40, col: float = 0.55, row: float = 0.5) -> VGroup:
    """A mental model: one row per individual, one column per term (a, b, c), blanks where a term is absent."""
    out = VGroup()
    for i, r in enumerate(rows):
        for j, t in enumerate(r):
            if t != ".":
                out.add(label(t, font_size=font_size, color=color).move_to([j * col, -i * row, 0]))
    frame = Rectangle(width=3 * col + 0.2, height=len(rows) * row + 0.1, stroke_opacity=0).move_to(
        [col, -(len(rows) - 1) * row / 2, 0])
    return VGroup(frame, out)


class Accounts(VoiceoverScene):
    def construct(self):
        self.card()
        self.models()
        self.shortcuts()
        self.scores()

    def card(self):
        card = chapter_card(2, r"Rules, \ models and shortcuts", r"How do people get to an answer, \ right or wrong?",
                            lit={1935: r"Woodworth \& Sells", 1983: r"Johnson-Laird", 1999: r"Chater \& Oaksford"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter two. Rules, models and shortcuts."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def models(self):
        head = heading(r"Mental models: \ imagine, \ then look for a counterexample")
        prem = VGroup(label(r"Some $A$ are $B$.", font_size=32), label(r"No $B$ are $C$.", font_size=32)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.6, 1.9, 0])
        m1 = model_table([["a", "b", "."], ["a", ".", "."], [".", ".", "c"]], color=SEARCH)
        m2 = model_table([["a", "b", "."], ["a", ".", "c"], [".", ".", "c"]], color=SEARCH)
        t1 = label(r"first model", font_size=24, color=GREY_A)
        t2 = label(r"a second model", font_size=24, color=GREY_A)
        g1 = VGroup(t1, m1).arrange(DOWN, buff=0.3).move_to([-5.0, -0.2, 0])
        g2 = VGroup(t2, m2).arrange(DOWN, buff=0.3).move_to([-1.9, -0.2, 0])
        c1 = wrapped_label(r"suggests: \ \emph{no $A$ are $C$}", 2.6, 24, CONTENT).next_to(g1, DOWN, buff=0.35)
        c2 = wrapped_label(r"refutes it; \ \emph{some $A$ are not $C$} \ survives", 2.8, 24, MODEL).next_to(
            g2, DOWN, buff=0.35)
        second = VGroup(*[t_ for t_ in m2[1] if abs(t_.get_center()[1] - m2[1][0].get_center()[1] + 0.5) < 0.1])
        hl = SurroundingRectangle(second, color=LOST, buff=0.1)
        rows = rows_of([
            (r"Johnson-Laird, \ 1983: \ people build a model of the premises, \ read a conclusion off it, \ and "
             r"may search for a model that refutes it", WHITE),
            (r"the more models a syllogism needs, \ the harder it is", LOGIC),
            (r"errors come from stopping at the first model", LOST),
        ], 5.6, 24, 0.36).move_to([3.7, 0.2, 0])
        tag = published_tag(r"Johnson-Laird (1983); \ Johnson-Laird \& Bara (1984)")
        with self.voiceover(
            "How do people reason, when they do? One answer is that the mind applies rules of inference, like a "
            "logician's proof. Phil Johnson-Laird proposed instead that people imagine. <bookmark mark='a'/> Some A "
            "are B. No B are C. <bookmark mark='b'/> Imagine a few individuals that make the premises true: an A that "
            "is a B, another A, and a C, kept apart from the Bs. This first model suggests that no A are C. "
            "<bookmark mark='c'/> But a careful reasoner looks for a counterexample: a second model where the other "
            "A is also a C. The premises are still true, and no A are C is refuted. What survives in every model is "
            "that some A are not C. <bookmark mark='d'/> On this theory, the more models a syllogism needs, the "
            "harder it is, and errors come from stopping at the first one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(prem))
            vo.wait_until("b")
            self.play(FadeIn(g1), FadeIn(c1))
            vo.wait_until("c")
            self.play(FadeIn(g2), Create(hl))
            self.play(FadeIn(c2))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.clear_scene()

    def shortcuts(self):
        head = heading(r"Or shortcuts that skip the logic")
        items = [
            (r"atmosphere", CONTENT, r"Woodworth \& Sells, \ 1935", r"a negative premise makes a negative conclusion "
             r"feel right; \ a \emph{some} makes a \emph{some}"),
            (r"matching", SEARCH, r"Wetherick \& Gilhooly, \ 1995", r"answer in the mood of the more cautious premise"),
            (r"probability heuristics", INSIGHT, r"Chater \& Oaksford, \ 1999", r"treat \emph{all}, \ \emph{some}, "
             r"\ \emph{no} as probabilities; \ answer in the mood of the least informative premise"),
        ]
        from videos.psychology.psych24.compute import R
        mood = {"A": r"all $A$ are $C$", "I": r"some $A$ are $C$", "E": r"no $A$ are $C$",
                "O": r"some $A$ are not $C$"}
        valid = R.predict("IE1", "logic")
        cols = VGroup()
        for k, (acct, (t, c, who, what)) in enumerate(zip(("atmosphere", "matching", "phm"), items)):
            body = VGroup(label(t, font_size=30, color=c), label(who, font_size=20, color=GREY_B),
                          wrapped_label(what, 3.5, 23, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = RoundedRectangle(corner_radius=0.15, width=4.1, height=4.0, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-4.35 + 4.35 * k, 0.45, 0])
            body.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.25)
            pred = R.predict("IE1", acct)
            assert len(pred) == 1 and pred[0].endswith("ac")
            ok = pred[0] in valid
            ex = VGroup(label(r"some $A$ are $B$, \ no $B$ are $C$:", font_size=19, color=GREY_B),
                        label(r"$\rightarrow$ \ " + mood[pred[0][0]] + (r" \ \ (valid)" if ok else r" \ \ (does not follow)"),
                              font_size=21, color=GOOD if ok else LOST)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            ex.move_to(box.get_bottom() + UP * 0.3, aligned_edge=DOWN).align_to(box, LEFT).shift(RIGHT * 0.25)
            cols.add(VGroup(box, body, ex))
        assert [R.predict("IE1", a)[0] in valid for a in ("atmosphere", "matching", "phm")] == [True, False, False]
        note = rows_of([(r"all three predict an answer for every syllogism, \ and none ever predicts \emph{no valid "
                         r"conclusion}", LOST)], 12.6, 26, 0.3).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Others argued that most people don't reason through syllogisms at all. <bookmark mark='a'/> The oldest "
            "idea, from 1935, is atmosphere: a negative premise makes a negative conclusion feel right, and a some "
            "makes a some. <bookmark mark='b'/> Matching says people answer in the mood of the more cautious "
            "premise. <bookmark mark='c'/> And Nick Chater and Mike Oaksford's probability heuristics treat all, "
            "some and no as statements of probability, and pick the mood of the least informative premise. "
            "Take the premises from before, some A are B and no B are C. Atmosphere happens to land on the valid "
            "answer; matching and probability heuristics both say no A are C, which doesn't follow. "
            "<bookmark mark='d'/> Notice what all three have in common: they always predict a conclusion, and never "
            "that nothing follows."
        ) as vo:
            self.play(FadeIn(head))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()

    def scores(self):
        d = load("syllogisms")
        head = heading(r"Scored against 139 people")
        accts = [("logic", r"logic", LOGIC), ("atmosphere", r"atmosphere", CONTENT), ("matching", r"matching", SEARCH),
                 ("phm", r"probability\\heuristics", INSIGHT)]
        nv, nn = int(d["n_valid"]), 64 - int(d["n_valid"])
        A = axes([0, 4], [0, 1], x_length=6.4, y_length=3.4, xticks=[], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"commonest answer predicted", center=[-2.9, 0.2, 0],
                 font_size=16)
        bv = VGroup(*[bars(A.ax, [k + 0.32], [d[f"{a}_hits_valid"] / nv], c, 0.3) for k, (a, _, c) in enumerate(accts)])
        bn = VGroup(*[bars(A.ax, [k + 0.68], [d[f"{a}_hits_nvc"] / nn], c, 0.3, opacity=0.4)
                      for k, (a, _, c) in enumerate(accts)])
        names = VGroup(*[label(t, font_size=18, color=c).next_to(A.ax.c2p(k + 0.5, 0), DOWN, buff=0.12)
                         for k, (_, t, c) in enumerate(accts)])
        key = VGroup(label(rf"solid: \ the {nv} syllogisms with a valid conclusion", font_size=19, color=GREY_A),
                     label(rf"faint: \ the {nn} with none", font_size=19, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(names, DOWN, buff=0.25).align_to(A, LEFT)
        lv = {a: d[f"{a}_hits_valid"] for a, _, _ in accts}
        ln = {a: d[f"{a}_hits_nvc"] for a, _, _ in accts}
        assert lv["atmosphere"] == max(lv.values()) and ln["logic"] == max(ln.values())
        assert ln["atmosphere"] == ln["matching"] == ln["phm"]  # "for every shortcut"
        rows = rows_of([
            (rf"where something follows, \ atmosphere predicts the commonest answer for {lv['atmosphere']} of {nv}, "
             rf"\ logic for {lv['logic']}", CONTENT),
            (rf"where nothing follows, \ only logic can say so: \ {ln['logic']} of {nn}; \ the shortcuts "
             rf"{ln['atmosphere']}", LOGIC),
            (r"Khemlani \& Johnson-Laird, \ 2012: \ twelve theories surveyed, \ seven tested on six studies; \ none "
             r"fits well", LOST),
        ], 5.2, 23, 0.36).move_to([3.9, 0.0, 0])
        tag = psyche_tag(r"\texttt{reason.predict}, \ \texttt{score}; \ open data: \ Ragni (2016)")
        with self.voiceover(
            "Psyche scores each account against the hundred and thirty-nine people, asking how often it predicts "
            "the commonest answer to each syllogism. <bookmark mark='a'/> Where a valid conclusion exists, the "
            f"shortcuts do well. Atmosphere predicts the commonest answer for {lv['atmosphere']} of the {nv}, "
            f"logic for {lv['logic']}. <bookmark mark='b'/> Where nothing follows, the picture reverses. Many "
            f"people do say that no valid conclusion follows, and only logic predicts that: {ln['logic']} of the "
            f"{nn}, against {ln['atmosphere']} for every shortcut. <bookmark mark='c'/> People are neither logicians "
            "nor pure pattern-matchers, and no single account fits. In 2012 Sangeet Khemlani and Phil Johnson-Laird "
            "surveyed twelve theories of the syllogism, tested seven against the data of six studies, and found "
            "that none fitted well."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bv], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bn], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
