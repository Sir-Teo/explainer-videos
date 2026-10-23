from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (PART, PIX, POS, RAND, ROT, SUP, axes, curve, digit, digit_sheet, load, pct,
                                   seed_curves, tag, take_away)

ROT_NAMES = [r"0^\circ", r"90^\circ", r"180^\circ", r"270^\circ"]


def tiles(img, n=3, gap=2):
    """A 28 x 28 digit cut into n x n tiles (with ``gap`` pixels trimmed around each): a list of arrays."""
    s = 28 // n
    return [img[r * s + gap // 2:(r + 1) * s - gap // 2, c * s + gap // 2:(c + 1) * s - gap // 2]
            for r in range(n) for c in range(n)]


class Pretext(VoiceoverScene):
    def construct(self):
        self.card()
        self.zoo()
        self.replay()
        self.symmetric()
        self.verdict()
        self.bridge()

    def card(self):
        card = chapter_card(2, r"Invent a puzzle", r"Can a made-up task teach what a digit is?", lit=(), part=PART)
        with self.voiceover("Chapter two. Invent a puzzle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def zoo(self):
        v = load("views")
        d = np.asarray(v["orig"])[2].astype(float) / 255.0
        T = tiles(d)
        S_ = 0.42
        # context prediction: the centre tile and one neighbour; where does it go?
        ctx = Group(*[digit(t, S_, frame=True) for t in T]).arrange_in_grid(3, 3, buff=0.08)
        for i, m in enumerate(ctx):
            if i not in (4, 1):
                m.set_opacity(0.15)
        q = MathTex(r"?", font_size=30, color=ROT).move_to(ctx[1])
        p1 = Group(ctx, q)
        # jigsaw: the tiles shuffled
        perm = [5, 0, 7, 2, 8, 3, 1, 6, 4]
        jig = Group(*[digit(T[i], S_, frame=True) for i in perm]).arrange_in_grid(3, 3, buff=0.08)
        # inpainting: a hole in the middle
        hole = d.copy()
        hole[9:19, 9:19] = 0
        inp = Group(digit(hole, 1.35, frame=True), Square(1.35 * 10 / 28, color=ROT, stroke_width=2).move_to(ORIGIN))
        inp[1].move_to(inp[0].get_center())
        # colorization: a grey digit and a coloured one (schematic for photographs)
        col = Group(digit(d, 0.9, frame=True), MathTex(r"\to", font_size=30),
                    digit(d, 0.9, color=ROT, frame=True)).arrange(RIGHT, buff=0.1)
        # rotation
        rots = Group(*[digit(np.rot90(d, -k), 0.6, frame=True) for k in range(4)]).arrange_in_grid(2, 2, buff=0.08)
        pics = [p1, jig, col, inp, rots]
        names = [r"where does \\ this tile go?", r"unshuffle \\ the tiles", r"colour \\ the grey image",
                 r"fill in \\ the hole", r"which way \\ is up?"]
        who = [r"Doersch, Gupta \\ \& Efros (2015)", r"Noroozi \\ \& Favaro (2016)", r"Zhang, Isola \\ \& Efros (2016)",
               r"Pathak et al.\ \\ (2016)", r"Gidaris, Singh \& \\ Komodakis (2018)"]
        cards = Group()
        for p_, n_, w_ in zip(pics, names, who):
            if p_.height > 1.35:
                p_.height = 1.35
            g = Group(p_, label(n_, font_size=22, color=ROT), label(w_, font_size=17, color=GREY_B)).arrange(DOWN,
                                                                                                           buff=0.2)
            cards.add(g)
        cards.arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        head = label(r"Pretext tasks: \ puzzles whose answers come free", font_size=34).to_edge(UP, buff=0.4)
        shortcut = label(r"the catch: \ a network solves the puzzle, \ not your problem", font_size=26, color=GREY_A)
        shortcut.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The first idea was to invent a puzzle whose answer comes free with the data. <bookmark mark='a'/> Cut "
            "an image into tiles and ask where one tile sits relative to another. <bookmark mark='b'/> Shuffle the "
            "tiles and ask for the order. <bookmark mark='c'/> Remove the colour and ask for it back. <bookmark "
            "mark='d'/> Cut a hole and ask what was there. <bookmark mark='e'/> Or turn the image and ask which way "
            "is up. To answer, the reasoning went, the network has to know what things look like. <bookmark "
            "mark='f'/> The catch is that a network solves the puzzle you set, not the problem you meant."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate([None, "b", "c", "d", "e"]):
                if mk:
                    vo.wait_until(mk)
                elif k == 0:
                    vo.wait_until("a")
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(shortcut, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        p = load("pretext")
        runs, keys = p["runs"], sorted(p["runs"])
        P = np.asarray(p["rec_p"])  # (snap, 16, 4): rotation k of digit i at row k * 4 + i
        steps = np.asarray(p["rec_steps"])
        D = np.asarray(p["digits"]).astype(float) / 255.0
        n_s = len(steps)
        cell = 0.62
        grid = Group()
        for k in range(4):
            for i in range(4):
                grid.add(digit(np.rot90(D[i], -k), cell, frame=True))
        grid.arrange_in_grid(4, 4, buff=(0.75, 0.32)).move_to([-3.6, -0.25, 0])
        rl = VGroup(*[MathTex(ROT_NAMES[k], font_size=24, color=GREY_B).next_to(grid[4 * k], LEFT, buff=0.2)
                      for k in range(4)])
        tr = ValueTracker(0.0)
        cols = [ROT, GREY_C, GREY_C, GREY_C]

        def bars_for(j):
            k_true = j // 4

            def make():
                t = tr.get_value()
                a = int(np.clip(np.floor(t), 0, n_s - 1))
                f = t - a
                pr = P[a, j] if a + 1 >= n_s else (1 - f) * P[a, j] + f * P[a + 1, j]
                g = VGroup()
                base = grid[j].get_right() + RIGHT * 0.08 + DOWN * cell / 2
                for r in range(4):
                    h = max(0.01, cell * float(pr[r]))
                    g.add(Rectangle(width=0.1, height=h, stroke_width=0, fill_color=POS if r == k_true else GREY_C,
                                    fill_opacity=0.9).move_to(base + RIGHT * (0.06 + 0.13 * r) + UP * h / 2))
                return g
            return make

        bars = VGroup(*[always_redraw(bars_for(j)) for j in range(16)])
        ax = axes([0, steps[-1]], [0, 1], x_length=5.0, y_length=3.0, xlabel=r"training step",
                  ylabel=r"accuracy", xticks=[0, steps[-1]], yticks=[0, 0.5, 1], center=[3.6, -0.1, 0])
        acc = []
        for k in keys:
            r = runs[k]
            xs = [s for s, lg in zip(r["steps"], r["logs"]) if lg]
            ys = [lg["acc"] for lg in r["logs"] if lg]
            acc.append((xs, ys))
        rot_c = VGroup(*[curve(ax.ax, xs, ys, ROT, 3 if i == 0 else 1.8).set_stroke(opacity=1 if i == 0 else 0.5)
                         for i, (xs, ys) in enumerate(acc)])
        knn_c = seed_curves(ax.ax, runs, keys, "knn", POS)
        leg = VGroup(label(r"which way is up? \ (training batches)", font_size=20, color=ROT),
                     label(r"$k$-NN on digit labels", font_size=20, color=POS)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.1)
        leg.next_to(ax, UP, buff=0.1).align_to(ax, LEFT).shift(RIGHT * 0.3)
        cur = always_redraw(lambda: DashedLine(
            ax.ax.c2p(float(np.interp(tr.get_value(), np.arange(n_s), steps)), 0),
            ax.ax.c2p(float(np.interp(tr.get_value(), np.arange(n_s), steps)), 1), color=GREY_B, stroke_width=1.5))
        sl = always_redraw(lambda: label(rf"step ${steps[int(np.clip(round(tr.get_value()), 0, n_s - 1))]}$",
                                         font_size=22, color=GREY_A).next_to(grid, UP, buff=0.2))
        fin = [r["logs"][-1]["acc"] for r in (runs[k] for k in keys)]
        k0 = float(np.mean([runs[k]["knn"][0] for k in keys]))
        k1 = float(np.mean([runs[k]["knn"][-1] for k in keys]))
        tg = tag(r"computed: \ three seeds, \ the first replayed")
        with self.voiceover(
            "We trained the rotation puzzle. Each step, sixty-four digits are each turned four ways, and the "
            "network must say which turn it is looking at. <bookmark mark='a'/> Here are four test digits, each in "
            "its four turns, with the network's four probabilities beside them; green is the right answer. "
            "<bookmark mark='b'/> Within a few hundred steps it is right about "
            f"{pct(np.mean(fin), 0)} percent of the time. <bookmark mark='c'/> And the green curve is what we "
            "actually care about: whether the network's vectors put fives near fives. It never saw a label, yet "
            f"its nearest-neighbour accuracy on the digits goes from {pct(k0, 0)} to {pct(k1, 0)} percent on this "
            "quick test."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(rl), FadeIn(bars), FadeIn(sl), FadeIn(tg))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(leg), FadeIn(cur))
            vo.wait_until("b")
            self.play(tr.animate.set_value(n_s - 1), Create(rot_c), run_time=max(3.0, vo.until("c") - 0.2),
                      rate_func=linear)
            vo.wait_until("c")
            self.play(Create(knn_c), run_time=2.0)
        for m in (bars, cur, sl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def symmetric(self):
        p = load("pretext")
        runs, keys = p["runs"], sorted(p["runs"])
        per = np.mean([runs[k]["extra"]["rot_acc_by_digit"] for k in keys], 0)
        lo_, hi_ = np.min([runs[k]["extra"]["rot_acc_by_digit"] for k in keys], 0), \
            np.max([runs[k]["extra"]["rot_acc_by_digit"] for k in keys], 0)
        order = np.argsort(per)
        worst = [int(i) for i in order[:3]]
        W = 0.85
        bars = VGroup()
        base_y = -2.0
        H = 3.4
        vmin = max(0.0, float(np.floor((per.min() - 0.1) * 10) / 10))
        for c in range(10):
            x = -5.9 + c * 0.95
            h = H * (per[c] - vmin) / (1 - vmin)
            col = ROT if c in worst else GREY_B
            b = Rectangle(width=W * 0.7, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([x, base_y + h / 2, 0])
            wl = H * (lo_[c] - vmin) / (1 - vmin)
            wh = H * (hi_[c] - vmin) / (1 - vmin)
            wh_ = Line([x, base_y + wl, 0], [x, base_y + wh, 0], color=WHITE, stroke_width=1.5)
            v_ = MathTex(pct(per[c], 0), font_size=22, color=col).next_to(b, UP, buff=0.12 + max(0, wh - h))
            n_ = MathTex(str(c), font_size=30, color=GREY_A).next_to([x, base_y, 0], DOWN, buff=0.15)
            bars.add(VGroup(b, wh_, v_, n_))
        axis = Line([-6.4, base_y, 0], [3.2, base_y, 0], color=GREY_C, stroke_width=1.5)
        yl = label(rf"right turn found, \ \% \ (axis from ${pct(vmin, 0)}$)", font_size=20,
                   color=GREY_A).next_to(axis, UP, buff=3.7).align_to(axis, LEFT)
        v = load("views")
        ex = Group()
        for c in worst[:2]:
            d = np.asarray(v["orig"])[c].astype(float) / 255.0
            ex.add(Group(digit(d, 0.8, frame=True), MathTex(r"\circlearrowright\,180^\circ", font_size=24),
                         digit(np.rot90(d, 2), 0.8, frame=True)).arrange(RIGHT, buff=0.15))
        ex.arrange(DOWN, buff=0.3).move_to([5.3, 0.4, 0])
        names = ", ".join(str(c) for c in worst[:2]) + f" and {worst[2]}"
        sym = set(worst[:3]) & {0, 1, 8}
        why_ = ("These are the digits that look much the same turned half a turn, so the puzzle has no answer for "
                "them, and the network learns nothing from them about which way is up."
                if len(sym) >= 2 else
                "Some of these look much the same turned around, so for them the puzzle is partly unanswerable.")
        with self.voiceover(
            "The puzzle has blind spots, and we can measure them. This is how often the trained network finds the "
            "right turn, digit by digit, averaged over the three seeds. <bookmark mark='a'/> The worst are the "
            f"{names}. <bookmark mark='b'/> {why_} The task decides what the network attends to, digit by digit."
        ) as vo:
            self.play(Create(axis), FadeIn(yl), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("a")
            self.play(*[Indicate(bars[c][0], color=ROT) for c in worst])
            vo.wait_until("b")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        p = load("pretext")
        b = load("baselines")
        sup = load("supervised")["summary"]["cnn"]
        s = p["summary"]
        px = b["pixels"]
        rc = b["random_cnn"]
        rows = [(r"raw pixels", PIX, px["linear"], np.mean(px["few"])),
                (r"untrained", RAND, np.mean([r["linear"] for r in rc]), np.mean([np.mean(r["few"]) for r in rc])),
                (r"rotation puzzle", ROT, s["linear"][0], s["few"][0]),
                (r"supervised", SUP, sup["linear"][0], sup["few"][0])]
        hdr = VGroup(label(r"linear probe", font_size=24, color=GREY_A), label(r"10 labels per digit", font_size=24,
                                                                                  color=GREY_A))
        tab = VGroup()
        for i, (n, c, a, f) in enumerate(rows):
            tab.add(VGroup(label(n, font_size=28, color=c), MathTex(pct(a) + r"\%", font_size=34),
                           MathTex(pct(f) + r"\%", font_size=34)))
        xs = [-3.5, 0.6, 3.8]
        for i, r_ in enumerate(tab):
            for j, m in enumerate(r_):
                m.move_to([xs[j], 1.2 - 0.8 * i, 0])
        hdr[0].move_to([xs[1], 2.0, 0])
        hdr[1].move_to([xs[2], 2.0, 0])
        rot_lin, rot_few = s["linear"][0], s["few"][0]
        un_lin = rows[1][2]
        un_few = rows[1][3]
        beat = rot_few > un_few + 0.01
        line = (f"The rotation puzzle lifts the ten-label test from {pct(un_few, 0)} percent, for the untrained "
                f"network, to {pct(rot_few, 0)}; the supervised network, which saw every label, reaches "
                f"{pct(rows[3][3], 0)}." if beat else
                f"The rotation puzzle barely moves the ten-label test: {pct(rot_few, 0)} percent, against "
                f"{pct(un_few, 0)} for the untrained network.")
        aber = label(r"Doersch et al.\ (2015): \ the tile puzzle was solved \\ from the lens's colour fringes "
                     r"(chromatic aberration)", font_size=22, color=GREY_A).move_to([0, -2.1, 0])
        tk = take_away(r"a pretext task learns what its puzzle needs, \ which is only partly what we need")
        with self.voiceover(
            f"So how good is the representation? <bookmark mark='a'/> {line} <bookmark mark='b'/> Puzzles found "
            "shortcuts in real photographs too. The first tile puzzle, in 2015, was partly solved from chromatic "
            "aberration: the colour fringes a lens adds near the edge of a photo give away where a tile came from. "
            "The authors had to strip colour from the tiles. <bookmark mark='c'/> Pretext tasks taught the field "
            "that free labels work, and that the choice of puzzle decides what is learned."
        ) as vo:
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in tab], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(tab[2], color=ROT, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(aber))
            vo.wait_until("c")
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bridge(self):
        v = load("views")
        grid = np.asarray(v["grid"])[:8]
        full = np.asarray(v["full"])
        cols = ["#FF6B6B", "#FFA94D", "#FFD43B", "#A9E34B", "#3BC9DB", "#748FFC", "#B197FC", "#F783AC"]
        cells = Group()
        for i in range(8):
            d = digit(grid[i], 0.8, color=cols[i], frame=True)
            t = label(rf"class {i + 1}", font_size=18, color=cols[i]).next_to(d, DOWN, buff=0.1)
            cells.add(Group(d, t))
        cells.arrange(RIGHT, buff=0.3).move_to([0, 1.3, 0])
        ex = Group(*[digit(full[k, 3], 0.7, color=cols[0], frame=True) for k in range(5)]).arrange(RIGHT, buff=0.15)
        ex.move_to([-3.2, -1.0, 0])
        exl = label(r"its transformed copies: \\ the same class", font_size=20, color=cols[0]).next_to(ex, DOWN, buff=0.2)
        h1 = label(r"Exemplar CNN (Dosovitskiy et al., 2014): \\ thousands of images, \ each with its copies a class",
                   font_size=21, color=GREY_A).move_to([3.4, -0.6, 0])
        h2 = label(r"instance discrimination (Wu et al., 2018): \\ every image its own class, \ a bank of "
                   r"stored vectors \\ as the other classes", font_size=21, color=GREY_A).next_to(h1, DOWN, buff=0.35)
        with self.voiceover(
            "One puzzle turned out to be different from the rest, because it is not about any particular property "
            "of images. Make every image its own class. <bookmark mark='a'/> Its transformed copies count as the "
            "same class; every other image is a different one. Alexey Dosovitskiy and colleagues tried it in 2014, "
            "<bookmark mark='b'/> and in 2018 Zhirong Wu and colleagues scaled it to a million classes, one per "
            "ImageNet photo, by keeping a stored vector for every image and comparing against those. <bookmark "
            "mark='c'/> Telling one image from all the others is the contrastive idea, and the next chapter is its "
            "mathematics."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.1), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(ex), FadeIn(exl))
            self.play(FadeIn(h1))
            vo.wait_until("b")
            self.play(FadeIn(h2))
            vo.wait_until("c")
            self.play(Indicate(cells[0], color=cols[0]))
        self.wait(0.3)
        self.clear_scene()
