from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403
from videos.psychology.psych21.s07_testing import hist_bars


class Drm(VoiceoverScene):
    def construct(self):
        self.card()
        self.reveal()
        self.data()
        self.model()
        self.accounts()

    def card(self):
        card = chapter_card(8, r"Words that were never there", r"How can you remember what you never saw?",
                            lit={1959: r"Deese", 1995: r"Roediger \& McDermott", 1998: r"Arndt \& Hirshman",
                                 2001: r"Roediger et al."},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter eight. Words that were never there."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def reveal(self):
        head = heading(r"Your test, \ scored")
        lst = VGroup(*[label(w, font_size=24, color=TRACE) for w in SLEEP_LIST])
        lst.arrange_in_grid(rows=3, cols=5, buff=(0.45, 0.25)).move_to([0, 1.7, 0])
        chips = VGroup()
        for w, kind in TEST_WORDS:
            col = {"studied": TRACE, "lure": FALSE, "unrelated": GREY_B}[kind]
            note = {"studied": r"in the list", "lure": r"never shown", "unrelated": r"not in the list"}[kind]
            chips.add(VGroup(word_chip(w, color=col, font_size=30, width=2.4),
                             label(note, font_size=20, color=col)).arrange(DOWN, buff=0.12))
        chips.arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.35)).move_to([0, -0.5, 0])
        rows = rows_of([
            (r"every word in the list is an associate of SLEEP: \ the list was built around a word it leaves out",
             WHITE),
            (r"if you said yes to SLEEP, \ and perhaps \emph{remembered} seeing it, \ you are in the majority",
             FALSE),
        ], 12.4, 25, 0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Take out your answers from the start of this part. Here's the list you saw. <bookmark mark='a'/> And "
            "here are the six test words. Tired, nap and bed were in the list. Butter and doctor were not. "
            "<bookmark mark='b'/> And sleep was never shown. Look at the list again: every word in it is an "
            "associate of sleep. The list was built around the one word it leaves out. "
            "<bookmark mark='c'/> If you said yes to sleep, and especially if you said you remembered seeing it, "
            "you're in the majority."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lst))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for i, c in enumerate(chips) if i != 1],
                                  lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(chips[1], scale=1.2), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), Indicate(chips[1], color=FALSE))
        self.clear_scene()

    def data(self):
        r = archive.ROEDIGER_MCDERMOTT_1995.data
        head = heading(r"Roediger and McDermott, \ 1995")
        A = axes([0, 2], [0, 1], x_length=4.2, y_length=3.0, xticks=[], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"free recall", center=[-4.4, 0.2, 0], font_size=18)
        B = axes([0, 2], [0, 1], x_length=4.2, y_length=3.0, xticks=[], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"recognised as old", center=[0.2, 0.2, 0], font_size=18)
        ra = bars(A.ax, [0.5, 1.5], [r["exp1_studied_recall"], r["exp1_lure_recall"]], TRACE, width=0.6)
        ra[1].set_fill(FALSE)
        rb = bars(B.ax, [0.5, 1.5], [r["exp1_hits"], r["exp1_lure_fa"]], TRACE, width=0.6)
        rb[1].set_fill(FALSE)
        names = VGroup()
        for ax_ in (A, B):
            names.add(label(r"studied words", font_size=19, color=TRACE).next_to(ax_.ax.c2p(0.5, 0), DOWN, buff=0.12),
                      label(r"the lure", font_size=19, color=FALSE).next_to(ax_.ax.c2p(1.5, 0), DOWN, buff=0.12))
        vals = VGroup(*[label(pct(v), font_size=20, color=GREY_A).next_to(b_, UP, buff=0.06) for b_, v in
                        zip(list(ra) + list(rb), [r["exp1_studied_recall"], r["exp1_lure_recall"], r["exp1_hits"],
                                                  r["exp1_lure_fa"]])])
        rows = rows_of([
            (rf"Experiment 1: \ {r['exp1_n']} students, \ {r['exp1_lists']} lists of {r['exp1_length']} associates "
             r"of a word not shown, \ from Deese's lists of 1959", GREY_A),
            (r"the lure was recalled about as often as a word from the middle of the list", FALSE),
            (r"and recognised almost as often as the words actually studied", FALSE),
            (rf"Experiment 2: \ {r['exp2_n']} students, \ {r['exp2_lists']} lists: \ lures recalled "
             rf"{pct(r['exp2_lure_recall'])} of the time, \ and {pct(r['exp2_lure_remember'])} of lures called old "
             r"were judged \emph{remembered}", CUE),
        ], 4.0, 20, 0.3).move_to([4.85, 0.0, 0])
        tag = historical_tag(archive.ROEDIGER_MCDERMOTT_1995.cite)
        with self.voiceover(
            "The lists go back to James Deese in 1959. Henry Roediger and Kathleen McDermott revived them in 1995, "
            "and found an illusion of unusual strength. <bookmark mark='a'/> Thirty-six students heard six lists of "
            "twelve words, each list made of associates of one word that was never presented, and recalled each "
            "list straight after. <bookmark mark='b'/> They recalled the missing word on "
            f"{spct(r['exp1_lure_recall'])} of the lists, about as often as a word from the middle of the list "
            "they had actually heard. <bookmark mark='c'/> And on a recognition test afterwards, they called it old "
            f"{spct(r['exp1_lure_fa'])} of the time, against {spct(r['exp1_hits'])} for the words really studied. "
            "<bookmark mark='d'/> In a second experiment with more lists, the false recall rose to "
            f"{spct(r['exp2_lure_recall'])}. And asked whether they remembered the word being presented, or just "
            f"knew it had been, people said they remembered it for {spct(r['exp2_lure_remember'])} of the lures "
            "they called old. A vivid memory of an event that never happened, in a few minutes, in the lab."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), FadeIn(names), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(ra[0], DOWN), GrowFromEdge(ra[1], DOWN), FadeIn(vals[0]), FadeIn(vals[1]),
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(rb[0], DOWN), GrowFromEdge(rb[1], DOWN), FadeIn(vals[2]), FadeIn(vals[3]),
                      FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def model(self):
        d = load("drm")
        head = heading(r"Derivation: \ the lure matches the sum")
        eqs = VGroup(
            MathTex(r"\mathbf{w}_i = a_i\,\mathbf{g} + \sqrt{1 - a_i^2}\;\mathbf{u}_i", font_size=34),
            MathTex(r"\mathbf{M} = \sum_{i=1}^{n} \mathbf{w}_i", font_size=34, color=TRACE),
            MathTex(r"F(\mathbf{x}) = \mathbf{x} \cdot \mathbf{M}", font_size=34, color=CUE),
            MathTex(r"F(\mathbf{g}) = \sum_i a_i \;\approx\; F(\mathbf{w}_j) = 1 + \sum_{i \ne j} a_i a_j",
                    font_size=30, color=FALSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-3.6, 1.0, 0])
        lo = float(min(d["unrelated"].min(), d["studied"].min(), d["lure"].min()))
        hi = float(max(d["studied"].max(), d["lure"].max()))
        edges = np.linspace(lo, hi, 40)
        A = axes([lo, hi], [0, 1.0], x_length=6.0, y_length=2.4, xticks=[], yticks=[],
                 xlabel=r"familiarity $F$", center=[3.6, 1.0, 0], font_size=18)
        sc = 1.0 / max(np.histogram(d["studied"], edges, density=True)[0].max(),
                       np.histogram(d["lure"], edges, density=True)[0].max(),
                       np.histogram(d["unrelated"], edges, density=True)[0].max())
        hs = VGroup(hist_bars(A.ax, d["unrelated"], edges, GREY_B, sc, 0.5),
                    hist_bars(A.ax, d["studied"], edges, TRACE, sc, 0.55),
                    hist_bars(A.ax, d["lure"], edges, FALSE, sc, 0.6))
        crit = DashedLine(A.ax.c2p(d["criterion"], 0), A.ax.c2p(d["criterion"], 1.0), color=WHITE)
        key = legend([(GREY_B, rf"unrelated: \ yes {pct(d['yes_unrelated'])}"),
                      (TRACE, rf"studied: \ yes {pct(d['yes_studied'])}"),
                      (FALSE, rf"the lure: \ yes {pct(d['yes_lure'])}")], font_size=19)
        key.arrange(RIGHT, buff=0.3)
        if key.width > 6.4:
            key.scale_to_fit_width(6.4)
        key.next_to(A, DOWN, buff=0.15)
        keep_in_frame(key)
        rows = rows_of([
            (r"each studied word is part theme $\mathbf{g}$, \ the lure's meaning, \ and part its own features", GREY_A),
            (r"memory is their sum; \ a test word's familiarity is its match to the sum", TRACE),
            (r"a studied word matches itself strongly and the rest weakly; \ the lure matches \emph{every} word a "
             r"little: \ the two come out close", FALSE),
            (r"one criterion, \ set to accept 86\% of studied words, \ accepts the lure about as often", CUE),
        ], 12.4, 22, 0.2).to_edge(DOWN, buff=0.65)
        ptag = psyche_tag(r"\texttt{memory.drm\_global\_matching}: \ 200 lists of 12")
        with self.voiceover(
            "Why would the lure feel so familiar? A global-matching model, like those of Part 12's recognition "
            "memory, gives a one-line answer. Jason Arndt and Elliot Hirshman made this argument in 1998 "
            "with Douglas Hintzman's MINERVA model. <bookmark mark='a'/> Write each studied word as a vector: a share a i of the "
            "theme, g, which is the lure's meaning, and the rest its own features. <bookmark mark='b'/> Memory "
            "is their sum, M. A test word's familiarity is how well it matches the whole sum. "
            "<bookmark mark='c'/> A studied word matches itself perfectly, and every other word a little. The lure "
            "matches nothing perfectly, but it matches every word a little, through the theme. Add up those little "
            "matches over the list, and the lure's familiarity comes out close to a studied word's. "
            f"<bookmark mark='d'/> Set one criterion so that {spct(d['yes_studied'])} of studied words are "
            f"accepted, as in the experiment, and the lure is accepted {spct(d['yes_lure'])} of the time; "
            f"unrelated words, {spct(d['yes_unrelated'])}. Nothing went wrong in this memory. It did exactly what "
            "summing similar experiences does: it extracted the gist."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), Write(eqs[2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eqs[3]), FadeIn(rows[2]))
            self.play(FadeIn(A), FadeIn(hs[0]), FadeIn(hs[1]), FadeIn(hs[2]))
            vo.wait_until("d")
            self.play(Create(crit), FadeIn(key), FadeIn(rows[3]))
        self.clear_scene()

    def accounts(self):
        head = heading(r"Three accounts, \ one lesson")
        rows = rows_of([
            (r"global matching: \ the lure resembles the whole list, \ so it feels familiar", CUE),
            (r"activation and monitoring: \ while you study, \ each word activates SLEEP; \ later you fail to tell "
             r"thought from seen \ (Roediger and colleagues, \ 2001)", FALSE),
            (r"fuzzy-trace theory: \ you keep a verbatim trace and a gist; \ the gist, \ \emph{sleep}, \ outlasts the "
             r"verbatim \ (Brainerd and Reyna)", CTX),
            (r"what they share: \ a memory system built to keep meaning will produce memories of meanings that "
             r"were never presented", WHITE),
            (r"one of the most replicated results in memory research: \ in the old, \ in experts, \ in people with "
             r"superior memory; \ weaker in young children, \ whose gist is weaker", MODEL),
        ], 12.4, 25, 0.36).move_to([0, -0.2, 0])
        with self.voiceover(
            "There are three main accounts of the illusion, and they're not exclusive. <bookmark mark='a'/> Global "
            "matching: the lure resembles the list as a whole, so it feels familiar. <bookmark mark='b'/> "
            "Activation and monitoring: as you hear each word, it brings sleep to mind; later you can't tell the "
            "word you thought of from the words you heard, a failure of source monitoring we'll meet in the next "
            "chapter. <bookmark mark='c'/> And fuzzy-trace theory, from Charles Brainerd and Valerie Reyna: you "
            "keep both a verbatim trace and the gist, and the gist, sleep, lasts longer than the verbatim. "
            "<bookmark mark='d'/> They share one lesson. A memory built to keep the meaning of experience will "
            "sometimes remember meanings that were never presented. <bookmark mark='e'/> And it's robust: the "
            "illusion appears in older adults, in experts, and, as we'll see, in people with extraordinary "
            "memories. It's weaker in young children, whose grasp of the gist is weaker, which is just what "
            "fuzzy-trace theory predicts."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
