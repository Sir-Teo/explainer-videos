from __future__ import annotations

import numpy as np

from explainer.music.monochord import chromatic as X
from videos.music.music19.common import *  # noqa: F403

PCN = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
LEVELS = [r"root", r"root and fifth", r"triad", r"scale of the key", r"all twelve"]


def space_grid(space, new=None, cell: float = 0.52):
    """Lerdahl's basic space as a 5 x 12 grid, top level first; cells in ``space`` filled, cells in ``new`` (by level) marked."""
    g = VGroup()
    for lv in range(5):
        for pc in range(12):
            on = pc in space[lv]
            hot = new is not None and pc in new[lv]
            sq = Square(side_length=cell - 0.05, stroke_width=1.2, stroke_color=DIM,
                        fill_color=EAR if hot else (TUNE if on else DIM), fill_opacity=0.9 if (on or hot) else 0.15)
            sq.move_to([(pc - 5.5) * cell, (2 - lv) * cell, 0])
            g.add(sq)
    heads = VGroup(*[label(tex(PCN[pc]), font_size=19, color=GREY_B).move_to([(pc - 5.5) * cell, 2.75 * cell + 0.05, 0]) for pc in range(12)])
    names = VGroup(*[label(LEVELS[lv], font_size=20, color=GREY_B).move_to([-6.2 * cell, (2 - lv) * cell, 0], aligned_edge=RIGHT) for lv in range(5)])
    for n in names:
        n.align_to([-6.15 * cell, 0, 0], RIGHT)
    return VGroup(g, heads, names)


class Tension(SoundScene):
    def construct(self):
        chapter(self, 10, r"Measuring tension", r"Can a number say how far a chord has gone?", extra=((2001, r"Lerdahl's \textit{Tonal Pitch Space}"),))
        self.space()
        self.distance()
        self.curves()
        self.tree()

    # ------------------------------------------------------------------
    def space(self):
        C = (0, "major")
        sp = X.basic_space(0, "major", C)
        grid = space_grid(sp).move_to(UP * 0.5)
        side = VGroup(label(r"C major in C:", font_size=26, color=TUNE),
                      label(r"each level a filter: \ what matters most at the top", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.2).next_to(grid, DOWN, buff=0.45)
        with self.voiceover(
            "In 2001 the composer and theorist Fred Lerdahl proposed a number for how far one chord is from another. "
            "<bookmark mark='a'/> It starts from what he called the basic space: five layers of notes, from the most "
            "important to the least. For the C major chord in the key of C: at the top, the root, C. Below it, root "
            "and fifth. Then the triad, C, E, G. Then the seven notes of the key. Then all twelve. "
            "<bookmark mark='b'/> The picture is Part 15's tonal hierarchy, the probe-tone profile, written as levels."
        ) as vo:
            self.play(FadeIn(grid[1]), FadeIn(grid[2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(sq) for sq in grid[0]], lag_ratio=0.005), run_time=2.0)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distance(self):
        d = load("tension")
        C = (0, "major")
        bx, by = X.basic_space(0, "major", C), X.basic_space(7, "major", C)
        new = [by[l] - bx[l] for l in range(5)]
        k = sum(len(n) for n in new[:4])
        grid = space_grid(by, new).move_to(LEFT * 2.9 + DOWN * 0.3)
        title = label(r"C major $\to$ G major, \ in C: \ pink, \ the notes new to G's space", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        f = VGroup(label(r"$\delta(x \to y) = i + j + k$", font_size=34, color=WHITE),
                   label(r"$i$: \ steps between the keys, \ on the circle of fifths", font_size=22, color=GREY_A),
                   label(r"$j$: \ steps between the roots, \ on the circle of fifths", font_size=22, color=GREY_A),
                   label(r"$k$: \ new notes in $y$'s space, \ level by level", font_size=22, color=GREY_A),
                   label(rf"C to G: \ $0 + 1 + {k} = {d['examples']['I-V']}$", font_size=28, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        f.scale_to_fit_width(min(f.width, 5.2)).next_to(grid, RIGHT, buff=0.45).shift(UP * 0.4)
        ex = VGroup(label(rf"C to A minor: \ {d['examples']['I-vi']}", font_size=22, color=WHITE),
                    label(rf"C to D minor: \ {d['examples']['I-ii']}", font_size=22, color=WHITE),
                    label(rf"C major to F$\sharp$ major, \ in its own key: \ {d['examples']['C to F# major']}", font_size=22, color=EAR)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(f, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            "Now move to the G major chord, still in C. Its space has G at the top, G and D below, then G, B, D, and "
            "the same scale. <bookmark mark='a'/> Lerdahl's distance adds three counts. <bookmark mark='b'/> i: how many "
            "steps apart the two keys are on the circle of fifths; here none. j: how many steps apart the roots are; "
            "C to G is one. <bookmark mark='c'/> And k: how many notes in the new chord's space are not in the old "
            f"one's, the pink cells; here {say(k)}. <bookmark mark='d'/> So C to G is {say(d['examples']['I-V'])}. "
            f"<bookmark mark='e'/> C to A minor is {say(d['examples']['I-vi'])}, C to D minor "
            f"{say(d['examples']['I-ii'])}. And C major to F sharp major, in F sharp's own key, is "
            f"{say(d['examples']['C to F# major'])}: the whole width of the map."
        ) as vo:
            self.play(FadeIn(title), FadeIn(grid))
            vo.wait_until("a")
            self.play(FadeIn(f[0]))
            vo.wait_until("b")
            self.play(FadeIn(f[1]), FadeIn(f[2]))
            vo.wait_until("c")
            self.play(FadeIn(f[3]))
            vo.wait_until("d")
            self.play(FadeIn(f[4]))
            vo.wait_until("e")
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("tension")
        specs = (("diatonic", r"within the key", ["C", "Am", "Dm", "G7", "C"]),
                 ("mixture", r"through mixture and the Neapolitan", ["C", "A♭", "D♭", "G7", "C"]),
                 ("trapdoor", r"through a trapdoor", ["C", "F", "A♭7", "D♭", "A♭7", "D♭"]))
        cells = VGroup()
        for name, title, names in specs:
            t = d[name]["tension"]
            ch = columns(t, [tex(n) for n in names], width=3.6, height=2.4, color=WEAK, hot=(int(np.argmax(t)),), hot_color=EAR, fmt="{:.0f}", font_size=20)
            cells.add(VGroup(label(title, font_size=22, color=TUNE), ch).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        cap = label(r"each bar: \ the distance from the chord before", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.55)
        mx = [max(d[n]["tension"]) for n, _, _ in specs]
        with self.voiceover(
            "Score each chord by its distance from the one before, and a progression becomes a curve. "
            f"<bookmark mark='a'/> Within the key, no step costs more than {say(mx[0])}. <bookmark mark='b'/> Through "
            f"mixture and the Neapolitan, the curve climbs to {say(mx[1])}, as the D flat chord is followed by the "
            f"dominant. <bookmark mark='c'/> Through the trapdoor, the single chord that changes the key costs "
            f"{say(mx[2])}, and then the new key settles at once. <bookmark mark='d'/> In 2007 Lerdahl and Carol "
            "Krumhansl asked listeners to rate tension, moment by moment, in passages of tonal music, and found that a version of this model, with chords arranged in a tree rather than a chain, "
            "followed their ratings well."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(cells[0]))
            for mark, c_ in zip("bc", cells[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(c_))
            vo.wait_until("d")
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self):
        C = (0, "major")
        prog = [(0, "major", C), (9, "minor", C), (2, "minor", C), (7, "7", C), (0, "major", C)]
        names = ["C", "Am", "Dm", "G7", "C"]
        seq = X.tension_curve(prog)
        parent = {1: 0, 2: 3, 3: 4}                              # Am elaborates the opening C; Dm elaborates G7; G7 the final C
        hier = [0] * 5
        for k in (3, 2, 1):
            hier[k] = X.chord_distance(prog[parent[k]], prog[k]) + hier[parent[k]]
        xs = [-5.6, -4.3, -3.0, -1.7, -0.4]
        leaves = VGroup(*[label(n, font_size=26, color=WHITE).move_to([x, -1.6, 0]) for n, x in zip(names, xs)])
        top = Dot([-3.0, 1.9, 0], radius=0.06, color=GREY_B)
        nodes = {0: [-4.95, 0.9, 0], 4: [-1.05, 0.9, 0], 3: [-1.35, -0.1, 0], 1: [-4.95, -0.3, 0], 2: [-2.35, -0.6, 0]}
        edges = VGroup(Line(top.get_center(), nodes[0], color=GREY_B), Line(top.get_center(), nodes[4], color=GREY_B),
                       Line(nodes[0], [xs[0], -1.35, 0], color=GREY_B), Line(nodes[0], [xs[1], -1.35, 0], color=BLUE),
                       Line(nodes[4], [xs[4], -1.35, 0], color=GREY_B), Line(nodes[4], nodes[3], color=EAR),
                       Line(nodes[3], [xs[3], -1.35, 0], color=GREY_B), Line(nodes[3], [xs[2], -1.35, 0], color=EAR))
        nums = VGroup(*[label(rf"{v}", font_size=24, color=EAR if v == max(hier) else TUNE).move_to([x, -2.15, 0]) for v, x in zip(hier, xs)])
        seqn = VGroup(*[label(rf"{v}", font_size=22, color=GREY_B).move_to([x, -2.65, 0]) for v, x in zip(seq, xs)])
        tags = VGroup(label(r"tree", font_size=20, color=TUNE).next_to(nums, LEFT, buff=0.35), label(r"chain", font_size=20, color=GREY_B).next_to(seqn, LEFT, buff=0.35))
        rows_ = VGroup(*[label(t_, font_size=24, color=c_) for t_, c_ in (
            (r"a chord's tension: \ its distance from the chord it elaborates", WHITE),
            (r"plus the tension that chord already carries", WHITE),
            (rf"Dm hangs from G7, \ which hangs from the final C: \ {hier[2]}", EAR),
            (r"the chain sees only neighbours; \ the tree sees the phrase", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.0))
        rows_.move_to(RIGHT * 3.7 + DOWN * 0.1)
        with self.voiceover(
            "Lerdahl's own model is subtler than a chain. <bookmark mark='a'/> It arranges the chords in a tree, each "
            "chord elaborating a more important one: here A minor prolongs the opening C, D minor prepares G seven, and "
            "G seven prepares the final C. A chord's tension is its distance from the chord it hangs from, "
            "<bookmark mark='b'/> plus the tension that chord already carries. <bookmark mark='c'/> So D minor, which "
            f"costs only {say(seq[2])} as a step from A minor, carries {say(hier[2])} in the tree: its own distance from "
            "G seven, and G seven's from the end. <bookmark mark='d'/> The chain hears only neighbours; the tree hears "
            "the phrase, tension rising toward the cadence and draining away at the close. Building such trees "
            "automatically is Part 22's subject."
        ) as vo:
            self.play(FadeIn(leaves), FadeIn(seqn), FadeIn(tags[1]), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(top), Create(edges), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(nums), FadeIn(tags[0]), FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()
