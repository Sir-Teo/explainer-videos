from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES

SHELF = [(r"the machine", r"Harris and Harris; \ Patterson and Hennessy; \ Bryant and O'Hallaron", DATA),
         (r"languages", r"Abelson and Sussman; \ Appel; \ Pierce, \ \textit{Types and Programming Languages}", HEAD),
         (r"algorithms", r"Cormen, \ Leiserson, \ Rivest and Stein; \ Kleinberg and Tardos", YES),
         (r"theory", r"Sipser; \ Arora and Barak; \ Motwani and Raghavan", NO),
         (r"systems", r"Arpaci-Dusseau, \ \textit{OSTEP}; \ Kurose and Ross; \ Kleppmann", KERN),
         (r"software", r"Brooks, \ \textit{The Mythical Man-Month}; \ Ousterhout", LAM),
         (r"research", r"Hamming, \ ``You and Your Research''; \ P\'olya, \ \textit{How to Solve It}", WHITE)]


class Outro(VoiceoverScene):
    def construct(self):
        self.act11()
        self.map_()
        self.shelf()
        self.goodbye()

    def act11(self):
        head = label(r"Act XI, \ the research frontier", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for n, t, d, c in ((56, r"Spectral Graphs and Expanders", r"eigenvalues that know a graph", HEAD),
                           (57, r"Learning Theory", r"when learning is possible", YES),
                           (58, r"Semantics", r"what a program means", DATA),
                           (59, r"Distributed Computing Theory", r"what many processes can compute", LAM),
                           (60, r"Domain-Specific Hardware", r"machines built for one job", KERN),
                           (61, r"Doing Research", r"how results are made", NO)):
            rows.add(VGroup(label(rf"{n}", font_size=28, color=c), label(t, font_size=26, color=WHITE),
                            label(d, font_size=21, color=GREY_A)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.2)
        with self.voiceover(
            "The last act went past the degree, to the first year of research. <bookmark mark='a'/> Eigenvalues that "
            "know a graph's shape; theorems about when learning is possible; three meanings for every program; the "
            "limits of what distributed processes can compute; hardware built for a single job; and, in this part, "
            "the methods by which every result in the series was made."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.35), run_time=4)
        self.wait(0.5)
        self.clear_scene()

    def map_(self):
        title = label(r"Computer Science, \ Built: \ sixty-one parts", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART).scale(1.0).next_to(title, DOWN, buff=0.4)
        foot = wrapped_label(r"from two piles of pebbles to the open problems: \ every layer built on the one "
                             r"below, \ and every one of them built here", 12.4, font_size=21, color=WHITE).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "And that is the whole map: sixty-one parts. <bookmark mark='a'/> It began with two piles of pebbles and "
            "a rule, and it ends on questions nobody can yet answer. Every layer was built on the one below it, and "
            "every one of them was built here, from gates to a cluster, from a proof to a protocol."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(smap), FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def shelf(self):
        head = label(r"The final reading list", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for t, books, c in SHELF:
            rows.add(VGroup(label(t, font_size=21, color=c), wrapped_label(books, 9.6, font_size=18,
                                                                         color=GREY_A)).arrange(RIGHT, buff=0.5))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.5)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.5)
        for r in rows:
            r[1].shift(RIGHT * (2.3 - r[0].width))
        foot = note(r"every part's own sources are in its notes", font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "If you want to keep going, here is a shelf. <bookmark mark='a'/> For the machine, Harris and Harris, "
            "Patterson and Hennessy, and Bryant and O'Hallaron. For languages, Abelson and Sussman, Appel, and "
            "Pierce. For algorithms, the book by Cormen, Leiserson, Rivest and Stein, and Kleinberg and Tardos. For "
            "theory, Sipser, Arora and Barak, and Motwani and Raghavan. For systems, the Arpaci-Dusseaus, Kurose and "
            "Ross, and Kleppmann. For software, Brooks and Ousterhout. And for research itself, Hamming's lecture "
            "and Pólya's How to Solve It."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.4), run_time=6)
        self.wait(1.0)
        self.clear_scene()

    def goodbye(self):
        title = label(r"Thank you", font_size=48, color=HEAD).move_to(UP * 0.8)
        sub = wrapped_label(r"the pebbles are still there: \ take one, \ and start", 10.0, font_size=26,
                            color=WHITE).next_to(title, DOWN, buff=0.5)
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "This is the end of Computer Science, Built. Thank you for watching all of it. The open problems are "
            "real, and some of them will be solved by people who started exactly where this series did, with a few "
            "pebbles and a rule. Take one, and start."
        ):
            self.play(FadeIn(title), FadeIn(sub), FadeIn(credit))
        self.wait(4.0)


_ = (BG, DATA, KERN, LAM, NO, YES)
