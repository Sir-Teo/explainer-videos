from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403

MOODS = {"A": r"All", "I": r"Some", "E": r"No", "O": r"Some \ldots\ not"}


def venn(center=(0, 0, 0), r: float = 1.15):
    c = np.array(center, float)
    A = Circle(radius=r, color=CONTENT, stroke_width=3).move_to(c + np.array([-0.62, 0.42, 0]))
    B = Circle(radius=r, color=LOGIC, stroke_width=3).move_to(c + np.array([0.62, 0.42, 0]))
    C = Circle(radius=r, color=SEARCH, stroke_width=3).move_to(c + np.array([0.0, -0.62, 0]))
    labs = VGroup(label(r"$A$", font_size=34, color=CONTENT).next_to(A, UL, buff=-0.25),
                  label(r"$B$", font_size=34, color=LOGIC).next_to(B, UR, buff=-0.25),
                  label(r"$C$", font_size=34, color=SEARCH).next_to(C, DOWN, buff=0.08))
    return A, B, C, labs


def shade(mob, color=LOST):
    return mob.set_fill(color, opacity=0.55).set_stroke(width=0)


class Deduction(VoiceoverScene):
    def construct(self):
        self.card()
        self.forms()
        self.derive()
        self.data()
        self.belief()

    def card(self):
        card = chapter_card(1, r"Deduction", r"What follows from what, \ and do people see it?",
                            lit={1983: r"Evans et al.", 2012: r"Khemlani \& Johnson-Laird", 2016: r"Ragni"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. Deduction."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def forms(self):
        head = heading(r"Sixty-four syllogisms")
        ex = VGroup(label(r"All \emph{artists} are \emph{beekeepers}.", font_size=34, color=WHITE),
                    label(r"All \emph{beekeepers} are \emph{chemists}.", font_size=34, color=WHITE),
                    label(r"So: \ all \emph{artists} are \emph{chemists}.", font_size=34, color=MODEL)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.2, 1.3, 0])
        moods = VGroup(*[label(rf"{k}: \ {v}", font_size=28, color=LOGIC) for k, v in
                         (("A", r"All $X$ are $Y$"), ("I", r"Some $X$ are $Y$"), ("E", r"No $X$ are $Y$"),
                          ("O", r"Some $X$ are not $Y$"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        moods.move_to([3.6, 1.3, 0])
        rows = rows_of([
            (r"two premises, \ each in one of four moods, \ and the middle term in one of four arrangements: \ "
             r"$4 \times 4 \times 4 = 64$ syllogisms", WHITE),
            (r"nine possible answers: \ four moods, \ in either direction, \ or \emph{no valid conclusion}", LOGIC),
            (r"Aristotle catalogued the valid ones; \ for two thousand years they were the core of logic", GREY_A),
        ], 12.6, 26, 0.36).move_to([0, -1.9, 0])
        with self.voiceover(
            "The oldest piece of formal reasoning is the syllogism. <bookmark mark='a'/> All artists are beekeepers. "
            "All beekeepers are chemists. So all artists are chemists. <bookmark mark='b'/> Each premise has one of "
            "four forms: all, some, no, and some are not. <bookmark mark='c'/> Two premises, four forms each, and "
            "four ways to arrange the terms make sixty-four syllogisms. <bookmark mark='d'/> For each there are nine "
            "possible answers: a conclusion in one of the four forms, running in either direction, or no valid "
            "conclusion at all. <bookmark mark='e'/> Aristotle catalogued the valid ones, and for two thousand years "
            "they were most of logic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ex], lag_ratio=0.8), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(moods))
            for m, r in zip("cde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def derive(self):
        d = load("syllogisms")
        head = heading(r"Derivation: \ validity by brute force")
        A, B, C, labs = venn(center=(-3.4, 0.0, 0))
        a_not_b = shade(Difference(A, B))
        b_not_c = shade(Difference(B, C))
        prem = VGroup(label(r"All $A$ are $B$: \ $A$ outside $B$ is empty", font_size=24, color=LOST),
                      label(r"All $B$ are $C$: \ $B$ outside $C$ is empty", font_size=24, color=LOST)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(VGroup(A, B, C), DOWN, buff=0.35)
        rows = rows_of([
            (r"three terms make eight kinds of thing; \ a \emph{model} says which kinds exist: \ $2^8$ models", WHITE),
            (r"each premise rules some models out; \ a conclusion is \emph{valid} if it is true in every model "
             r"left", LOGIC),
            (r"here every $A$ that exists is inside $C$: \ \emph{all $A$ are $C$} \ follows", MODEL),
            (rf"Psyche checks all 64 syllogisms this way: \ {d['n_valid']} have a valid conclusion \ (assuming each "
             rf"term names something), \ {64 - d['n_valid']} have none", MODEL),
        ], 6.2, 24, 0.36).move_to([3.4, 0.0, 0])
        tag = psyche_tag(r"\texttt{reason.valid\_conclusions}")
        assert d["n_valid"] == 27  # the narration says twenty-seven
        with self.voiceover(
            "How do you know which conclusions are valid? Psyche does it by brute force. <bookmark mark='a'/> Three "
            "terms divide the world into eight kinds of thing: things that are A and B but not C, and so on. A model "
            "of the world says which of the eight kinds exist, so there are two hundred and fifty-six models. "
            "<bookmark mark='b'/> Each premise rules some of them out. All A are B empties the part of A outside B. "
            "All B are C empties the part of B outside C. A conclusion is valid if it's true in every model that's "
            "left. <bookmark mark='c'/> Here, every A that exists is inside C, so all A are C follows. "
            "<bookmark mark='d'/> Done for all sixty-four, twenty-seven syllogisms have a valid conclusion, if we "
            "assume each term names something that exists, and thirty-seven have none."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(A), Create(B), Create(C), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(a_not_b), FadeIn(prem[0]), FadeIn(rows[1]))
            self.play(FadeIn(b_not_c), FadeIn(prem[1]))
            vo.wait_until("c")
            self.play(Indicate(A, color=MODEL), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def data(self):
        d = load("syllogisms")
        head = heading(r"139 people, \ every syllogism")
        acc = d["accuracy"]
        tasks = [str(t) for t in d["tasks"]]
        grid = VGroup()
        cell = 0.33
        x0, y0 = -6.2, 2.15
        for k, t in enumerate(tasks):
            i, j = k // 4, k % 4  # rows: mood pairs; columns: figures
            col = interpolate_color(ManimColor(LOST), ManimColor(GOOD), float(acc[k]))
            sq = Rectangle(width=cell * 1.8, height=cell, stroke_width=0.5, stroke_color=BLACK, fill_color=col,
                           fill_opacity=0.9)
            sq.move_to([x0 + (j + 0.5) * cell * 2.0, y0 - (i + 0.5) * cell, 0])
            grid.add(sq)
        rlab = VGroup(*[label(tasks[4 * i][:2], font_size=15, color=GREY_A).next_to(grid[4 * i], LEFT, buff=0.08)
                        for i in range(16)])
        clab = VGroup(*[label(str(j + 1), font_size=15, color=GREY_A).next_to(grid[j], UP, buff=0.08)
                        for j in range(4)])
        ctitle = label(r"figure", font_size=16, color=GREY_B).next_to(clab, UP, buff=0.06)
        gkey = VGroup(label(r"share right:", font_size=16, color=GREY_B),
                      Square(0.2, stroke_width=0, fill_color=LOST, fill_opacity=0.9), label(r"0", font_size=16, color=GREY_B),
                      Square(0.2, stroke_width=0, fill_color=GOOD, fill_opacity=0.9), label(r"1", font_size=16, color=GREY_B)
                      ).arrange(RIGHT, buff=0.1).next_to(grid, DOWN, buff=0.15)
        grid0 = grid.copy().set_fill(GREY_D, 0.6)
        intro = rows_of([(r"Ragni et al., \ 2016: \ 139 people online, \ all 64 syllogisms, \ nine possible answers "
                          r"to each", GREY_A)], 7.4, 21, 0.2).move_to([2.6, -3.0, 0])
        ex1 = load("syllogisms")["ex_AA1"]
        ex2 = load("syllogisms")["ex_EA1"]
        resp = [str(r) for r in d["responses"]]
        A1 = axes([0, 9], [0, 0.8], x_length=6.6, y_length=1.55, xticks=[], yticks=[0, 0.4, 0.8],
                  yfmt=lambda v: f"{v:.1f}", ylabel=r"share", center=[2.3, 1.35, 0], font_size=15)
        A2 = axes([0, 9], [0, 0.8], x_length=6.6, y_length=1.55, xticks=[], yticks=[0, 0.4, 0.8],
                  yfmt=lambda v: f"{v:.1f}", ylabel=r"share", center=[2.3, -1.3, 0], font_size=15)
        val1, val2 = str(d["valid_str"][tasks.index("AA1")]).split("/"), str(d["valid_str"][tasks.index("EA1")]).split("/")
        b1 = VGroup(*[bars(A1.ax, [k + 0.5], [v], GOOD if resp[k] in val1 else GREY_B, 0.7) for k, v in enumerate(ex1)])
        b2 = VGroup(*[bars(A2.ax, [k + 0.5], [v], GOOD if resp[k] in val2 else GREY_B, 0.7) for k, v in enumerate(ex2)])
        xl = lambda ax: VGroup(*[label(r_.replace("ac", r"$_{ac}$").replace("ca", r"$_{ca}$"), font_size=17,  # noqa: E731
                                       color=GREY_A).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.08)
                                 for k, r_ in enumerate(resp)])
        t1 = label(rf"All $A$ are $B$, \ all $B$ are $C$: \ {pct(ex1[resp.index('Aac')])} say \emph{{all $A$ are $C$}}",
                   font_size=19, color=WHITE).next_to(A1, UP, buff=0.12)
        t2 = label(rf"No $A$ are $B$, \ all $B$ are $C$: \ {pct(ex2[resp.index('Oca')])} find the valid answer",
                   font_size=19, color=WHITE).next_to(A2, UP, buff=0.12)
        rows = rows_of([
            (rf"right answers: \ {pct(d['mean_acc'])} overall, \ {pct(d['acc_valid'])} where a conclusion follows, \ "
             rf"{pct(d['acc_nvc'])} where none does", WHITE),
            (r"green: \ the valid answer \ (no valid conclusion is the last bar)", GOOD),
        ], 7.4, 21, 0.2).move_to([2.6, -3.0, 0])
        tag = psyche_tag(r"open data: \ Ragni (2016), \ via CCOBRA")
        hard = int(round(100 * ex2[resp.index("Oca")]))
        assert resp[int(np.argmax(ex2))] == "Eac" and ex2.max() < 0.5  # "the commonest answer", not "most people"
        with self.voiceover(
            "What do people do? Marco Ragni's lab gave all sixty-four syllogisms to a hundred and thirty-nine people, "
            "and the answers are open. <bookmark mark='a'/> Each square is one syllogism, green where most people "
            "were right, red where most were wrong. The pattern is anything but random: some are nearly always "
            f"solved, some almost never. <bookmark mark='b'/> All A are B, all B are C: {spct(ex1[resp.index('Aac')])} "
            "say all A are C. <bookmark mark='c'/> No A are B, all B are C. The commonest answer is no A are C, which "
            f"doesn't follow. The valid answer, some C are not A, is chosen by {hard} percent. "
            f"<bookmark mark='d'/> Overall, {spct(d['mean_acc'])} of answers are right: {spct(d['acc_valid'])} "
            f"where a conclusion follows, and {spct(d['acc_nvc'])} where none does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid0), FadeIn(rlab), FadeIn(clab), FadeIn(ctitle),
                      FadeIn(intro))
            vo.wait_until("a")
            self.play(LaggedStart(*[Transform(g0, g) for g0, g in zip(grid0, grid)], lag_ratio=0.02), FadeIn(gkey),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(A1), FadeIn(xl(A1.ax)), FadeIn(b1), FadeIn(t1),
                      Indicate(grid0[tasks.index("AA1")], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(A2), FadeIn(xl(A2.ax)), FadeIn(b2), FadeIn(t2),
                      Indicate(grid0[tasks.index("EA1")], color=WHITE))
            vo.wait_until("d")
            self.play(FadeOut(intro), FadeIn(rows))
        self.clear_scene()

    def belief(self):
        head = heading(r"Belief bias")
        vals = [("valid,\\\\believable", 0.89, GOOD), ("valid,\\\\unbelievable", 0.56, GOOD),
                ("invalid,\\\\believable", 0.71, LOST), ("invalid,\\\\unbelievable", 0.10, LOST)]
        A = axes([0, 4], [0, 1], x_length=5.6, y_length=3.2, xticks=[], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"conclusion accepted", center=[-3.2, 0.1, 0],
                 font_size=16)
        bs = VGroup(*[bars(A.ax, [k + 0.5], [v], c, 0.6) for k, (_, v, c) in enumerate(vals)])
        nums = VGroup(*[label(pct(v), font_size=20, color=WHITE).next_to(b, UP, buff=0.06) for b, (_, v, _) in
                        zip(bs, vals)])
        names = VGroup(*[label(t, font_size=17, color=GREY_A).next_to(A.ax.c2p(k + 0.5, 0), DOWN, buff=0.12)
                         for k, (t, _, _) in enumerate(vals)])
        ex = VGroup(label(r"No addictive things are inexpensive.", font_size=22),
                    label(r"Some cigarettes are inexpensive.", font_size=22),
                    label(r"So: \ some addictive things are not cigarettes.", font_size=22, color=LOST)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows = rows_of([
            (r"Evans, \ Barston \& Pollard, \ 1983: \ the same logical forms with believable or unbelievable "
             r"conclusions", WHITE),
            (r"believable conclusions are accepted more, \ and most of all when they do not follow", LOST),
        ], 6.0, 23, 0.32)
        side = VGroup(ex, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.4, 0.2, 0])
        tag = published_tag(r"Evans, \ Barston \& Pollard (1983), \ as tabulated by Evans et al. (2001)")
        with self.voiceover(
            "And people reason differently about different content, even when the logic is the same. "
            "<bookmark mark='a'/> No addictive things are inexpensive. Some cigarettes are inexpensive. So some "
            "addictive things are not cigarettes. It sounds true, and it doesn't follow. <bookmark mark='b'/> In "
            "1983 Jonathan Evans, Julie Barston and Paul Pollard gave people syllogisms whose conclusions were "
            "valid or invalid, and believable or not. <bookmark mark='c'/> Valid and believable conclusions were "
            "accepted eighty-nine percent of the time; invalid and unbelievable ones only ten. "
            "<bookmark mark='d'/> But an invalid conclusion that people believed was accepted seventy-one percent "
            "of the time, more than a valid one they didn't believe. Belief bias: what you know about the world "
            "leaks into what you think follows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(names), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(bs[0]), FadeIn(nums[0]), FadeIn(bs[3]), FadeIn(nums[3]))
            vo.wait_until("d")
            self.play(FadeIn(bs[1]), FadeIn(nums[1]), FadeIn(bs[2]), FadeIn(nums[2]), FadeIn(rows[1]))
        self.clear_scene()
