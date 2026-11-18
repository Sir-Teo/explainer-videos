from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.learned()

    def card(self):
        self.chapter(15, r"Frontier: \ design as a science", r"Can a design be predicted, \ not just argued?", lit=(2018, 2021), extra=((2018, r"learned index structures"),
                                                     (2021, r"metastable failures")), part=PART, said="Chapter fifteen, the frontier. Can a design be predicted, and not just argued for?")

    def learned(self):
        self.ask(r"A learned index replaces a B-tree with...", [r"a bigger tree",
                 r"a model of where keys fall"], 1,
                 say="A learned index replaces the B-tree's pages with what?",
                 reveal="A model of the key distribution, predicting each key's position.")
        L = load("learned")
        head = label(r"An index that learns the data", font_size=36).to_edge(UP, buff=0.3)
        # schematic: a staircase of keys and a few line segments fitted to it
        x0, y0 = -6.0, -1.9
        import random
        rng = random.Random(2)
        pts, t = [], 0.0
        for k in range(60):
            t += rng.expovariate(1.0) * (4 if 20 <= k < 30 else 1)
            pts.append((t, k))
        tmax = pts[-1][0]
        dots = VGroup(*[Dot([x0 + p[0] / tmax * 5.6, y0 + p[1] / 60 * 3.6, 0], radius=0.04, color=DATA) for p in pts])
        segs = VGroup(Line([x0, y0, 0], [x0 + pts[20][0] / tmax * 5.6, y0 + 20 / 60 * 3.6, 0], color=HEAD,
                           stroke_width=3),
                      Line([x0 + pts[20][0] / tmax * 5.6, y0 + 20 / 60 * 3.6, 0],
                           [x0 + pts[30][0] / tmax * 5.6, y0 + 30 / 60 * 3.6, 0], color=HEAD, stroke_width=3),
                      Line([x0 + pts[30][0] / tmax * 5.6, y0 + 30 / 60 * 3.6, 0],
                           [x0 + pts[59][0] / tmax * 5.6, y0 + 59 / 60 * 3.6, 0], color=HEAD, stroke_width=3))
        axl = VGroup(label(r"key", font_size=16, color=GREY_B).move_to([x0 + 2.8, y0 - 0.3, 0]),
                     label(r"position", font_size=16, color=GREY_B).rotate(PI / 2).move_to([x0 - 0.3, y0 + 1.8, 0]))
        sch = note(r"schematic", font_size=15).next_to(dots, UP, buff=0.1)
        rows = [[f"{r['eps']}", f"{r['segments']:,}", f"{r['bytes'] / 1000:.1f} kB", f"{r['search_steps']}"]
                for r in L["rows"]]
        rows.append([r"B+ tree", f"{L['btree_inner_nodes']}", f"{L['btree_inner_bytes'] / 1000:.0f} kB",
                     f"{L['btree_steps']}"])
        tab = grid_table([r"max error", r"segments", r"model size", r"comparisons"], rows,
                         widths=[1.8, 1.8, 1.9, 1.9], row_h=0.45, font_size=18, mono_cols=())
        tab.to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        for cell in tab.cells[-1]:
            cell.set_color(GREY_A)
        foot = wrapped_label(rf"{L['keys']:,} bursty timestamps; \ Kraska et al., \ ``The case for learned index "
                             r"structures'' \ (2018); \ the PGM-index \ (Ferragina and Vinciguerra, \ 2020) \ with "
                             r"guarantees", 12.4, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "An index maps a key to a position. A B-tree does it with a hierarchy of sorted pages, knowing nothing "
            "about the keys. <bookmark mark='a'/> But the map from key to position is a function, and a function "
            "can be learned. Fit a few straight lines to it, each guaranteed to predict a position within a fixed "
            "error, and finish with a short binary search. <bookmark mark='b'/> On a million bursty timestamps, "
            f"an error bound of 32 needs {L['rows'][1]['segments']} segments, about "
            f"{L['rows'][1]['bytes'] / 1000:.0f} kilobytes, and seven comparisons; the B-tree's inner nodes take "
            f"about {L['btree_inner_bytes'] / 1000:.0f} kilobytes and some {L['btree_steps']} comparisons. "
            "<bookmark mark='c'/> Tim Kraska and colleagues made the case for learned indexes in 2018; the "
            "PGM-index of Paolo Ferragina and Giorgio Vinciguerra added worst-case guarantees. Learned structures "
            "for updates, multiple dimensions and shifting data remain open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(axl), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(segs), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()





_ = (DATA, KERN, LAM, NO, YES)
