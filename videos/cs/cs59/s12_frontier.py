from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.classes()
        self.decomposition()
        self.open()

    def card(self):
        card = chapter_card(11, r"Frontier: \ the complexity of locality",
                            r"Which local problems need how many rounds?", lit=(1995, 2020),
                            extra=((1995, r"Naor and Stockmeyer: \ what can be computed locally?"),
                                   (2020, r"Rozho\v{n} and Ghaffari: \ network decomposition")), part=PART)
        with self.voiceover("Chapter eleven, the frontier. Which local problems need how many rounds?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def classes(self):
        head = label(r"Only three speeds on a ring", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"$O(1)$", r"trivial labellings; \ anything checkable with no symmetry to break", YES],
                [r"$\Theta(\log^* n)$", r"three-colouring, \ maximal independent set, \ maximal matching", HEAD],
                [r"$\Theta(n)$", r"two-colouring an even ring; \ anything needing global parity", NO]]
        tab = grid_table([r"rounds", r"examples"], [r[:2] for r in rows], widths=[2.6, 9.0], row_h=0.75,
                         font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6)
        for i, r in enumerate(rows, start=1):
            for cell in tab.cells[i]:
                cell.set_color(r[2])
        note_ = wrapped_label(r"locally checkable labellings \ (LCLs, \ Naor and Stockmeyer 1995): \ on paths and "
                              r"cycles, \ every LCL takes one of these three times, \ and which one is decidable; \ on "
                              r"trees and general graphs \ (Chang and Pettie 2017; \ Balliu et al.) \ the landscape is "
                              r"richer, \ with gaps proved by round elimination", 12.4, font_size=19,
                              color=GREY_A).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Linial's bound has grown into a theory. <bookmark mark='a'/> A locally checkable labelling is a problem "
            "whose solution each node can verify by looking at its neighbourhood, like a colouring. Moni Naor and "
            "Larry Stockmeyer introduced them in 1995. <bookmark mark='b'/> On rings and paths, every such problem "
            "takes either constant time, or log star time, or time linear in n, and nothing in between. Three "
            "colours is log star; two colours on an even ring is linear, because a node must know the parity of its "
            "position. <bookmark mark='c'/> On trees and general graphs the landscape is richer, and charting it, "
            "with tools such as round elimination, is active research."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def decomposition(self):
        head = label(r"Breakthroughs of the last few years", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"deterministic decomposition", r"Rozho\v{n} and Ghaffari \ (2020): \ networks split into clusters "
                 r"of small diameter in polylog rounds, \ deterministically; \ many problems followed", YES),
            tile(r"CONGEST", r"the same questions when each message carries only $O(\log n)$ bits: \ shortest "
                 r"paths, \ cuts and matchings, \ with lower bounds from communication complexity", DATA),
            tile(r"randomness and locality", r"how much faster randomized algorithms can be: \ the gaps for colouring "
                 r"and independent sets are still being closed", HEAD),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"local algorithms now also run inside centralized ones: \ the same ideas give fast "
                             r"parallel and sublinear-time algorithms", 12.4, font_size=21, color=WHITE).to_edge(
            DOWN, buff=0.6)
        with self.voiceover(
            "Three threads have moved fast. <bookmark mark='a'/> In 2020 Václav Rozhoň and Mohsen Ghaffari showed "
            "how to split any network into clusters of small diameter deterministically in polylogarithmic rounds, "
            "a question open for decades, and many deterministic algorithms followed from it. <bookmark mark='b'/> "
            "In the CONGEST model each message is only logarithmically many bits, and shortest paths, cuts and "
            "matchings get lower bounds from communication complexity. <bookmark mark='c'/> And how much randomness "
            "helps locality is still being settled, problem by problem. <bookmark mark='d'/> The same ideas now run "
            "inside ordinary algorithms, giving fast parallel and sublinear-time methods."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Maximal independent set}: \ the exact round complexity on general graphs, \ "
                          r"deterministic and randomized.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{$(\Delta + 1)$-colouring}: \ is there a deterministic algorithm as fast as "
                          r"the best randomized one?", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Byzantine agreement}: \ the communication cost with an adaptive adversary.",
                          12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Population protocols}: \ the fastest exact majority with few states.", 12.4,
                          font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ the deterministic LOCAL complexity of "
                             r"maximal independent set on general graphs, \ with matching upper and lower bounds", 12.4,
                             font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> The exact number of rounds needed for a maximal independent set on "
            "general graphs. <bookmark mark='b'/> Whether deterministic colouring with one more colour than the "
            "maximum degree can be as fast as randomized. <bookmark mark='c'/> The communication cost of Byzantine "
            "agreement against an adversary who chooses whom to corrupt as the protocol runs. <bookmark mark='d'/> "
            "And the fastest population protocols for majority with few states. <bookmark mark='e'/> This part's "
            "research problem is the first: matching upper and lower bounds for computing a maximal independent set "
            "deterministically in the LOCAL model."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
