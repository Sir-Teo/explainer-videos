from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.board()
        self.budget()
        self.codes()

    def card(self):
        card = chapter_card(13, r"Frontier: \ what is the limit for?", r"Is a small working memory a flaw, \ or a design?",
                            lit={2012: r"Sims et al.", 2018: r"van den Berg \& Ma"}, part=PART, scale=("mind", "brain"),
                            marr=("what", "how"))
        with self.voiceover("Chapter thirteen. Frontier: what is the limit for?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def board(self):
        head = heading(r"Settled, \ and open")
        left = VGroup(label(r"settled", font_size=30, color=GOOD), *[
            wrapped_label(t, 5.6, 24, GREY_A) for t in (
                r"a brief, \ large visual store, \ then a small workspace",
                r"forgetting in seconds is mostly interference",
                r"about three to four items without rehearsal",
                r"precision falls continuously with load",
                r"practice does not transfer far",
            )]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        right = VGroup(label(r"open", font_size=30, color=LOST), *[
            wrapped_label(t, 5.6, 24, GREY_A) for t in (
                r"slots, \ resources, \ or variable precision with a few slots",
                r"firing, \ silent synapses, \ or both",
                r"is the executive one thing?",
                r"why the limit is so small: \ a cost, \ or an optimum?",
            )]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, -0.1, 0])
        with self.voiceover(
            "Where the field stands. <bookmark mark='a'/> Settled: a brief, large visual store feeds a small "
            "workspace. Most short-term forgetting is interference, not decay. Without rehearsal people hold about "
            "three or four items. Precision falls continuously as more is held. And practice on memory tasks does "
            "not transfer far. <bookmark mark='b'/> Open: whether the limit has slots at all, or variable precision "
            "with a few slots. Whether items are held in firing, in silent synapses, or both. Whether the executive "
            "is one thing. And the deepest question: why is the workspace so small?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in left], lag_ratio=0.6), run_time=6.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in right], lag_ratio=0.6), run_time=5.0)
        self.clear_scene()

    def budget(self):
        d = load("budget")
        head = heading(r"A fixed budget of information, \ shared out")
        A = axes([0, 8], [0, 90], x_length=6.4, y_length=3.6, xticks=[1, 2, 4, 6, 8], yticks=[0, 30, 60, 90],
                 xlabel=r"squares held", ylabel=r"error s.d., \ degrees", center=[-2.7, 0.45, 0], font_size=18)
        ax = A.ax
        pts = scatter(ax, d["N"], d["sd"], DATA, 0.09, 1)
        c = curve_in(ax, d["n"], d["fit"], MODEL, 4)
        eq = MathTex(r"\sigma_N = \sigma_1\,2^{\,R - R/N}", font_size=40, color=MODEL).move_to([3.6, 2.2, 0])
        rows = rows_of([
            (r"rate-distortion theory: \ each extra bit halves a Gaussian memory's error", WHITE),
            (rf"share $R$ bits among $N$ items: \ fitted, \ $R$ = {d['bits']:.1f} bits, \ "
             rf"$\sigma_1$ = {d['sd1']:.0f}$^\circ$", MODEL),
            (r"the open data's spreads, \ one per set size, \ fall near the curve", DATA),
            (r"the limit as an optimum: \ spend precision where it pays, \ given a cost of information", EXEC),
            (r"Sims, \ Jacobs and Knill, \ 2012; \ van den Berg and Ma, \ 2018: \ Part 58", GREY_A),
        ], 5.4, 22, 0.3).move_to([3.85, -0.4, 0])
        ptag = psyche_tag(r"\texttt{wm.budget\_sd}: \ least squares on log s.d.")
        tag = published_tag(archive.BAYS_2009.cite)
        with self.voiceover(
            "One answer treats the limit not as a flaw but as a budget. <bookmark mark='a'/> Information theory's "
            "rate-distortion result says that for a Gaussian quantity, each extra bit spent on encoding halves the "
            "error's standard deviation. <bookmark mark='b'/> Suppose working memory has a fixed number of bits, "
            f"shared equally among the items. Fitted to the Bays data, the budget is about {d['bits']:.1f} bits, and "
            f"one item alone is held to about {d['sd1']:.0f} degrees. <bookmark mark='c'/> The four observed "
            "spreads fall near the curve, with only two parameters for four set sizes. <bookmark mark='d'/> Go one "
            "step further and make the budget itself a choice: information costs metabolic energy, so a rational "
            "system spends precision where it pays, and fewer bits when the reward for accuracy is small. "
            "<bookmark mark='e'/> Chris Sims, Robert Jacobs and David Knill proposed working memory as such an "
            "efficient channel in 2012, and van den Berg and Ma's resource-rational model of 2018 derived the set-size "
            "effect itself as an optimum. That idea, the brain as an efficient code, is Part 58."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq), Create(c), FadeIn(rows[1]), FadeIn(ptag), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(pts, color=DATA))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def codes(self):
        head = heading(r"Attention, \ memory and machines")
        rows = rows_of([
            (r"the focus: \ perhaps one item is held in an active state, \ the rest in a wider, \ quieter store", WHITE),
            (r"Oberauer's benchmarks, \ 2018: \ a list of findings every model of working memory must explain", EXEC),
            (r"working memory and long-term memory may be one system in different states: \ Part 20", LOOP),
            (r"language models hold a context of thousands of words, \ with attention over all of it: \ no small "
             r"workspace", MODEL),
            (r"whether a small workspace is a limit to engineer around, \ or a feature that forces abstraction, \ is "
             r"a live question: \ Part 60", GREY_A),
        ], 12.4, 26, 0.36).move_to([0, -0.2, 0])
        with self.voiceover(
            "Three threads to follow from here. <bookmark mark='a'/> Many researchers now distinguish a focus of "
            "attention, perhaps a single item held in an especially active state, from a wider set of items held "
            "more quietly, which may be the silent synapses of chapter eight. <bookmark mark='b'/> In 2018 Klaus "
            "Oberauer and a large group of colleagues published a list of benchmark findings that any model of "
            "working memory should explain, an attempt to turn a field of rival boxes into a field of tested "
            "theories. <bookmark mark='c'/> Some argue that working memory is not a separate store at all, but the "
            "currently activated part of long-term memory, which is where Part 20 picks up. <bookmark mark='d'/> And "
            "the machines of Part 60 are a strange contrast. A language model attends over a context of thousands "
            "of words with no small workspace at all. <bookmark mark='e'/> Whether our four items are a limitation "
            "to engineer around, or a constraint that forces compression and abstraction, is one of the questions "
            "that part takes up."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
